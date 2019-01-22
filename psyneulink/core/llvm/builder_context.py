# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# ********************************************* LLVM bindings **************************************************************

import atexit
import ctypes
import inspect
import numpy as np
import os, re

from psyneulink.core.scheduling.time import TimeScale

from .debug import debug_env
from .helpers import ConditionGenerator
from llvmlite import ir

__all__ = ['LLVMBuilderContext', '_modules', '_find_llvm_function', '_convert_llvm_ir_to_ctype']

_modules = set()
_all_modules = set()

@atexit.register
def module_count():
    if "mod_count" in debug_env:
        print("Total LLVM modules: ", len(_all_modules))

# TODO: Should this be selectable?
_int32_ty = ir.IntType(32)
_float_ty = ir.DoubleType()

class LLVMBuilderContext:
    module = None
    nest_level = 0
    uniq_counter = 0
    _llvm_generation = 0

    def __init__(self):
        self.int32_ty = _int32_ty
        self.float_ty = _float_ty

    def __enter__(self):
        if LLVMBuilderContext.nest_level == 0:
            assert LLVMBuilderContext.module is None
            LLVMBuilderContext.module = ir.Module(name="PsyNeuLinkModule-" + str(LLVMBuilderContext._llvm_generation))
        LLVMBuilderContext.nest_level += 1
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        LLVMBuilderContext.nest_level -= 1
        if LLVMBuilderContext.nest_level == 0:
            assert LLVMBuilderContext.module is not None
            _modules.add(LLVMBuilderContext.module)
            _all_modules.add(LLVMBuilderContext.module)
            LLVMBuilderContext.module = None

        LLVMBuilderContext._llvm_generation += 1

    def get_unique_name(self, name):
        LLVMBuilderContext.uniq_counter += 1
        name = re.sub(r"[- ()\[\]]", "_", name)
        return name + '_' + str(LLVMBuilderContext.uniq_counter)

    def get_builtin(self, name, args, function_type = None):
        if name in ('pow', 'log', 'exp'):
            return self.get_llvm_function("__pnl_builtin_" + name)
        return self.module.declare_intrinsic("llvm." + name, args, function_type)

    def get_llvm_function(self, name):
        if hasattr(name, '_llvm_symbol_name'):
            name = name._llvm_symbol_name

        f = _find_llvm_function(name, _all_modules | {LLVMBuilderContext.module})
        # Add declaration to the current module
        if f.name not in LLVMBuilderContext.module.globals:
            decl_f = ir.Function(LLVMBuilderContext.module, f.type.pointee, f.name)
            assert decl_f.is_declaration
            return decl_f
        return f

    @staticmethod
    def _get_full_func_name(func, component):
        name = func.name
        try:
            while component is not None:
                name = str(component) + ":" + name
                component = component.owner
        except AttributeError:
            pass

        return name

    @staticmethod
    def get_debug_location(func, component):
        if 'debug_info' not in debug_env:
            return
        mod = func.module
        path = inspect.getfile(component.__class__) if component is not None else "<builtin>"
        d_version = mod.add_metadata([ir.IntType(32)(2), "Dwarf Version", ir.IntType(32)(4)])
        di_version = mod.add_metadata([ir.IntType(32)(2), "Debug Info Version", ir.IntType(32)(3)])
        flags = mod.add_named_metadata("llvm.module.flags")
        if len(flags.operands) == 0:
            flags.add(d_version)
            flags.add(di_version)
        cu = mod.add_named_metadata("llvm.dbg.cu")
        di_file = mod.add_debug_info("DIFile", {
            "filename": os.path.basename(path),
            "directory": os.path.dirname(path),
        })
        di_func_type = mod.add_debug_info("DISubroutineType", {
            # None as `null`
            "types":           mod.add_metadata([None]),
            })
        di_compileunit = mod.add_debug_info("DICompileUnit", {
            "language":        ir.DIToken("DW_LANG_Python"),
            "file":            di_file,
            "producer":        "PsyNeuLink",
            "runtimeVersion":  0,
            "isOptimized":     False,
        }, is_distinct=True)
        cu.add(di_compileunit)
        di_func = mod.add_debug_info("DISubprogram", {
            "name":            LLVMBuilderContext._get_full_func_name(func, component),
            "file":            di_file,
            "line":            0,
            "type":            di_func_type,
            "isLocal":         False,
            "unit":            di_compileunit,
}, is_distinct=True)
        di_loc = mod.add_debug_info("DILocation", {
            "line":            0,
            "column":          0,
            "scope":           di_func,
        })
        return di_loc

    def get_input_struct_type(self, component):
        if hasattr(component, '_get_input_struct_type'):
            return component._get_input_struct_type(self)

        # KDM 12/28/18: <_instance_defaults_note> left _instance_defaults in place so that this code could use it.
        # Ideally this would be simply .defaults. After going through the special handler above, component becomes a
        # super() object, which seems to return the .defaults attr of the class associated with the super() object,
        # whereas _instance_defaults retuns the .defaults attr of the instance associated. I don't know whether
        # is a design or a convenience measure for workarounds, so I left this in place.
        default_var = component._instance_defaults.variable
        return self.convert_python_struct_to_llvm_ir(default_var)

    def get_output_struct_type(self, component):
        if hasattr(component, '_get_output_struct_type'):
            return component._get_output_struct_type(self)

        default_val = component._instance_defaults.value
        return self.convert_python_struct_to_llvm_ir(default_val)

    def get_param_struct_type(self, component):
        if hasattr(component, '_get_param_struct_type'):
            return component._get_param_struct_type(self)

        params = component._get_param_values()
        return self.convert_python_struct_to_llvm_ir(params)

    def get_context_struct_type(self, component):
        if hasattr(component, '_get_context_struct_type'):
            return component._get_context_struct_type(self)

        try:
            stateful = tuple((getattr(component, sa) for sa in component.stateful_attributes))
            return self.convert_python_struct_to_llvm_ir(stateful)
        except AttributeError:
            return ir.LiteralStructType([])

    def get_data_struct_type(self, component):
        if hasattr(component, '_get_data_struct_type'):
            return component._get_data_struct_type(self)

        return ir.LiteralStructType([])

    def get_param_ptr(self, component, builder, params_ptr, param_name):
        idx = self.int32_ty(component._get_param_ids().index(param_name))
        ptr = builder.gep(params_ptr, [self.int32_ty(0), idx])
        return ptr, builder

    def unwrap_2d_array(self, builder, element):
        if isinstance(element.type.pointee, ir.ArrayType) and isinstance(element.type.pointee.element, ir.ArrayType):
            assert(element.type.pointee.count == 1)
            return builder.gep(element, [self.int32_ty(0), self.int32_ty(0)])
        return element

    def gen_composition_exec(self, composition):
        func_name = None
        llvm_func = None

        # Create condition generator
        cond_gen = ConditionGenerator(self, composition)

        func_name = self.get_unique_name('exec_wrap_' + composition.name)
        func_ty = ir.FunctionType(ir.VoidType(), (
            self.get_context_struct_type(composition).as_pointer(),
            self.get_param_struct_type(composition).as_pointer(),
            self.get_input_struct_type(composition).as_pointer(),
            self.get_data_struct_type(composition).as_pointer(),
            cond_gen.get_condition_struct_type().as_pointer()))
        llvm_func = ir.Function(self.module, func_ty, name=func_name)
        llvm_func.attributes.add('argmemonly')
        context, params, comp_in, data, cond = llvm_func.args
        for a in llvm_func.args:
            a.attributes.add('nonnull')
            a.attributes.add('noalias')

        # Create entry block
        entry_block = llvm_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(entry_block)
        builder.debug_metadata = self.get_debug_location(llvm_func, composition)

        if 'const_params' in debug_env:
            const_params = params.type.pointee(composition._get_param_initializer(None))
            builder.store(const_params, params)

        # Call input CIM
        input_cim_name = composition._get_node_wrapper(composition.input_CIM);
        input_cim_f = self.get_llvm_function(input_cim_name)
        builder.call(input_cim_f, [context, params, comp_in, data, data])

        # Allocate run set structure
        run_set_type = ir.ArrayType(ir.IntType(1), len(composition.c_nodes))
        run_set_ptr = builder.alloca(run_set_type, name="run_set")

        # Allocate temporary output storage
        output_storage = builder.alloca(data.type.pointee, name="output_storage")

        iter_ptr = builder.alloca(self.int32_ty, name="iter_counter")
        builder.store(self.int32_ty(0), iter_ptr)

        loop_condition = builder.append_basic_block(name="scheduling_loop_condition")
        builder.branch(loop_condition)

        # Generate a while not 'end condition' loop
        builder.position_at_end(loop_condition)
        run_cond = cond_gen.generate_sched_condition(builder,
                        composition.termination_processing[TimeScale.TRIAL],
                        cond, None)
        run_cond = builder.not_(run_cond, name="not_run_cond")

        loop_body = builder.append_basic_block(name="scheduling_loop_body")
        exit_block = builder.append_basic_block(name="exit")
        builder.cbranch(run_cond, loop_body, exit_block)


        # Generate loop body
        builder.position_at_end(loop_body)

        zero = self.int32_ty(0)
        any_cond = ir.IntType(1)(0)

        # Calculate execution set before running the mechanisms
        for idx, mech in enumerate(composition.c_nodes):
            run_set_mech_ptr = builder.gep(run_set_ptr,
                                           [zero, self.int32_ty(idx)],
                                           name="run_cond_ptr_" + mech.name)
            mech_cond = cond_gen.generate_sched_condition(builder,
                            composition._get_processing_condition_set(mech),
                            cond, mech)
            ran = cond_gen.generate_ran_this_pass(builder, cond, mech)
            mech_cond = builder.and_(mech_cond, builder.not_(ran),
                                     name="run_cond_" + mech.name)
            any_cond = builder.or_(any_cond, mech_cond, name="any_ran_cond")
            builder.store(mech_cond, run_set_mech_ptr)

        for idx, mech in enumerate(composition.c_nodes):
            run_set_mech_ptr = builder.gep(run_set_ptr, [zero, self.int32_ty(idx)])
            mech_cond = builder.load(run_set_mech_ptr, name="mech_" + mech.name + "_should_run")
            with builder.if_then(mech_cond):
                mech_name = composition._get_node_wrapper(mech);
                mech_f = self.get_llvm_function(mech_name)
                # Wrappers do proper indexing of all strctures
                if len(mech_f.args) == 5: # Mechanism wrappers have 5 inputs
                    builder.call(mech_f, [context, params, comp_in, data, output_storage])
                else:
                    builder.call(mech_f, [context, params, comp_in, data, output_storage, cond])

                cond_gen.generate_update_after_run(builder, cond, mech)

        # Writeback results
        for idx, mech in enumerate(composition.c_nodes):
            run_set_mech_ptr = builder.gep(run_set_ptr, [zero, self.int32_ty(idx)])
            mech_cond = builder.load(run_set_mech_ptr, name="mech_" + mech.name + "_ran")
            with builder.if_then(mech_cond):
                out_ptr = builder.gep(output_storage, [zero, zero, self.int32_ty(idx)], name="result_ptr_" + mech.name)
                data_ptr = builder.gep(data, [zero, zero, self.int32_ty(idx)],
                                       name="data_result_" + mech.name)
                builder.store(builder.load(out_ptr), data_ptr)

        # Update step counter
        with builder.if_then(any_cond):
            cond_gen.bump_ts(builder, cond)

        # Increment number of iterations
        iters = builder.load(iter_ptr, name="iterw")
        iters = builder.add(iters, self.int32_ty(1), name="iterw_inc")
        builder.store(iters, iter_ptr)

        max_iters = len(composition.scheduler_processing.consideration_queue)
        completed_pass = builder.icmp_unsigned("==", iters,
                                               self.int32_ty(max_iters),
                                               name="completed_pass")
        # Increment pass and reset time step
        with builder.if_then(completed_pass):
            builder.store(zero, iter_ptr)
            # Bumping automatically zeros lower elements
            cond_gen.bump_ts(builder, cond, (0, 1, 0))

        builder.branch(loop_condition)

        builder.position_at_end(exit_block)
        # Call output CIM
        output_cim_name = composition._get_node_wrapper(composition.output_CIM);
        output_cim_f = self.get_llvm_function(output_cim_name)
        builder.call(output_cim_f, [context, params, comp_in, data, data])

        # Bump run counter
        cond_gen.bump_ts(builder, cond, (1, 0, 0))

        builder.ret_void()

        return func_name

    def gen_composition_run(self, composition):
        func_name = self.get_unique_name('run_wrap_' + composition.name)
        func_ty = ir.FunctionType(ir.VoidType(), (
            self.get_context_struct_type(composition).as_pointer(),
            self.get_param_struct_type(composition).as_pointer(),
            self.get_data_struct_type(composition).as_pointer(),
            self.get_input_struct_type(composition).as_pointer(),
            self.get_output_struct_type(composition).as_pointer(),
            self.int32_ty.as_pointer(),
            self.int32_ty.as_pointer()))
        llvm_func = ir.Function(self.module, func_ty, name=func_name)
        llvm_func.attributes.add('argmemonly')
        context, params, data, data_in, data_out, runs_ptr, inputs_ptr = llvm_func.args
        for a in llvm_func.args:
            a.attributes.add('nonnull')
            a.attributes.add('noalias')

        # Create entry block
        entry_block = llvm_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(entry_block)
        builder.debug_metadata = self.get_debug_location(llvm_func, composition)

        # Allocate and initialize condition structure
        cond_gen = ConditionGenerator(self, composition)
        cond_type = cond_gen.get_condition_struct_type()
        cond = builder.alloca(cond_type)
        cond_init = cond_type(cond_gen.get_condition_initializer())
        builder.store(cond_init, cond)

        iter_ptr = builder.alloca(self.int32_ty, name="iter_counter")
        builder.store(self.int32_ty(0), iter_ptr)

        loop_condition = builder.append_basic_block(name="run_loop_condition")
        builder.branch(loop_condition)

        # Generate a "while < count" loop
        builder.position_at_end(loop_condition)
        count = builder.load(iter_ptr)
        runs = builder.load(runs_ptr)
        run_cond = builder.icmp_unsigned('<', count, runs)

        loop_body = builder.append_basic_block(name="run_loop_body")
        exit_block = builder.append_basic_block(name="exit")
        builder.cbranch(run_cond, loop_body, exit_block)

        # Generate loop body
        builder.position_at_end(loop_body)

        # Current iteration
        iters = builder.load(iter_ptr);

        # Get the right input stimulus
        input_idx = builder.urem(iters, builder.load(inputs_ptr))
        data_in_ptr = builder.gep(data_in, [input_idx])

        # Call execution
        exec_f_name = composition._get_execution_wrapper()
        exec_f = self.get_llvm_function(exec_f_name)
        builder.call(exec_f, [context, params, data_in_ptr, data, cond])

        # Extract output_CIM result
        idx = composition._get_node_index(composition.output_CIM)
        result_ptr = builder.gep(data, [self.int32_ty(0), self.int32_ty(0), self.int32_ty(idx)])
        output_ptr = builder.gep(data_out, [iters])
        result = builder.load(result_ptr)
        builder.store(result, output_ptr)

        # Increment counter
        iters = builder.add(iters, self.int32_ty(1))
        builder.store(iters, iter_ptr)
        builder.branch(loop_condition)

        builder.position_at_end(exit_block)

        # Store the number of executed iterations
        builder.store(builder.load(iter_ptr), runs_ptr)

        builder.ret_void()

        return func_name

    def convert_python_struct_to_llvm_ir(self, t):
        if type(t) is list:
            assert all(type(x) == type(t[0]) for x in t)
            elem_t = self.convert_python_struct_to_llvm_ir(t[0])
            return ir.ArrayType(elem_t, len(t))
        elif type(t) is tuple:
            elems_t = (self.convert_python_struct_to_llvm_ir(x) for x in t)
            return ir.LiteralStructType(elems_t)
        elif isinstance(t, (int, float)):
            return self.float_ty
        elif isinstance(t, np.ndarray):
            return self.convert_python_struct_to_llvm_ir(t.tolist())
        elif t is None:
            return ir.LiteralStructType([])

        print(type(t))
        assert False

def _find_llvm_function(name, mods = _all_modules):
    f = None
    for m in mods:
        if name in m.globals:
            f = m.get_global(name)

    if not isinstance(f, ir.Function):
        raise ValueError("No such function: {}".format(name))
    return f

def _gen_cuda_kernel_wrapper_module(function):
    module = ir.Module(name="wrapper_"  + function.name)

    decl_f = ir.Function(module, function.type.pointee, function.name)
    assert decl_f.is_declaration
    kernel_func = ir.Function(module, function.type.pointee, function.name + "_cuda_kernel")
    block = kernel_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Calculate global id of a thread in x dimension
    intrin_ty = ir.FunctionType(ir.IntType(32), [])
    tid_x_f = ir.Function(module, intrin_ty, "llvm.nvvm.read.ptx.sreg.tid.x")
    ntid_x_f = ir.Function(module, intrin_ty, "llvm.nvvm.read.ptx.sreg.ntid.x")
    ctaid_x_f = ir.Function(module, intrin_ty, "llvm.nvvm.read.ptx.sreg.ctaid.x")
    global_id = builder.mul(builder.call(ctaid_x_f, []), builder.call(ntid_x_f, []))
    global_id = builder.add(global_id, builder.call(tid_x_f, []))

    # Runs need special handling. data_in and data_out are one dimensional,
    # but hold entries for all parallel invocations.
    is_comp_run = len(kernel_func.args) == 7
    if is_comp_run:
        runs_count = kernel_func.args[5]
        input_count = kernel_func.args[6]

    # Index all pointer arguments
    indexed_args = []
    for i, arg in enumerate(kernel_func.args):
        # Don't adjust #inputs and #trials
        if isinstance(arg.type, ir.PointerType):
            offset = global_id
            # #runs and #trials needs to be the same
            if is_comp_run and i >= 5:
                offset = ir.IntType(32)(0)
            # data arrays need spcial hadling
            elif is_comp_run and i == 4: # data_out
                offset = builder.mul(global_id, builder.load(runs_count))
            elif is_comp_run and i == 3: # data_in
                offset = builder.mul(global_id, builder.load(input_count))

            arg = builder.gep(arg, [offset])

        indexed_args.append(arg)
    builder.call(decl_f, indexed_args)
    builder.ret_void()

    # Add kernel mark metadata
    module.add_named_metadata("nvvm.annotations", [kernel_func, "kernel", ir.IntType(32)(1)])

    return module

_field_count = 0
_struct_count = 0

def _convert_llvm_ir_to_ctype(t):
    if type(t) is ir.VoidType:
        return None
    elif type(t) is ir.PointerType:
        # FIXME: Can this handle void*? Do we care?
        pointee = _convert_llvm_ir_to_ctype(t.pointee)
        return ctypes.POINTER(pointee)
    elif type(t) is ir.IntType:
        # FIXME: We should consider bitwidth here
        return ctypes.c_int
    elif type(t) is ir.DoubleType:
        return ctypes.c_double
    elif type(t) is ir.FloatType:
        return ctypes.c_float
    elif type(t) is ir.ArrayType:
        element_type = _convert_llvm_ir_to_ctype(t.element)
        return element_type * len(t)
    elif type(t) is ir.LiteralStructType:
        field_list = []
        for e in t.elements:
            # llvmlite modules get _unique string only works for symbol names
            global _field_count
            uniq_name = "field_" + str(_field_count)
            _field_count += 1

            field_list.append((uniq_name, _convert_llvm_ir_to_ctype(e)))

        global _struct_count
        uniq_name = "struct_" + str(_struct_count)
        _struct_count += 1

        def __init__(self, *args, **kwargs):
            ctypes.Structure.__init__(self, *args, **kwargs)

        new_type = type(uniq_name, (ctypes.Structure,), {"__init__": __init__})
        new_type.__name__ = uniq_name
        new_type._fields_ = field_list
        assert len(new_type._fields_) == len(t.elements)
        return new_type

    print(t)
    assert(False)
