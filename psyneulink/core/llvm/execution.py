# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# ********************************************* Binary Execution Wrappers **************************************************************

from psyneulink.core.globals.context import Context
from psyneulink.core.globals.utilities import NodeRole

import copy
import ctypes
from collections import defaultdict
import numpy as np
from inspect import isgenerator
from psyneulink.core import llvm as pnlvm
from . import helpers, jit_engine
from .debug import debug_env

__all__ = ['CompExecution', 'FuncExecution', 'MechExecution']


def _convert_ctype_to_python(x):
    if isinstance(x, ctypes.Structure):
        return [_convert_ctype_to_python(getattr(x, field_name)) for field_name, _ in x._fields_]
    if isinstance(x, ctypes.Array):
        return [_convert_ctype_to_python(num) for num in x]
    if isinstance(x, ctypes.c_double):
        return x.value
    if isinstance(x, (float, int)):
        return x

    assert False, "Don't know how to convert: {}".format(x)


def _tupleize(x):
    try:
        return tuple(_tupleize(y) for y in x)
    except TypeError:
        return x if x is not None else tuple()


class CUDAExecution:
    def __init__(self, buffers=['param_struct', 'state_struct', 'out']):
        for b in buffers:
            setattr(self, "_buffer_cuda_" + b, None)
        self._uploaded_bytes = 0
        self._downloaded_bytes = 0
        self.__debug_env = debug_env

    def __del__(self):
        if "cuda_data" in self.__debug_env:
            try:
                name = self._bin_func.name
            except AttributeError:
                name = self._composition.name

            print("{} CUDA uploaded: {}".format(name, self._uploaded_bytes))
            print("{} CUDA downloaded: {}".format(name, self._downloaded_bytes))

    @property
    def _bin_func_multirun(self):
        # CUDA uses the same function for single and multi run
        return self._bin_func

    def _get_ctype_bytes(self, data):
        # Return dummy buffer. CUDA does not handle 0 size well.
        if ctypes.sizeof(data) == 0:
            return bytearray(b'aaaa')
        return bytearray(data)

    def upload_ctype(self, data):
        self._uploaded_bytes += ctypes.sizeof(data)
        return jit_engine.pycuda.driver.to_device(self._get_ctype_bytes(data))

    def download_ctype(self, source, ty):
        self._downloaded_bytes += ctypes.sizeof(ty)
        out_buf = bytearray(ctypes.sizeof(ty))
        jit_engine.pycuda.driver.memcpy_dtoh(out_buf, source)
        return ty.from_buffer(out_buf)

    def __get_cuda_buffer(self, struct_name):
        private_attr_name = "_buffer_cuda" + struct_name
        private_attr = getattr(self, private_attr_name)
        if private_attr is None:
            # Set private attribute to a new buffer
            private_attr = self.upload_ctype(getattr(self, struct_name))
            setattr(self, private_attr_name, private_attr)

        return private_attr

    @property
    def _cuda_param_struct(self):
        return self.__get_cuda_buffer("_param_struct")

    @property
    def _cuda_state_struct(self):
        return self.__get_cuda_buffer("_state_struct")

    @property
    def _cuda_data_struct(self):
        return self.__get_cuda_buffer("_data_struct")

    @property
    def _cuda_conditions(self):
        return self.__get_cuda_buffer("_conditions")

    @property
    def _cuda_out(self):
        if self._buffer_cuda_out is None:
            size = ctypes.sizeof(self._vo_ty)
            self._buffer_cuda_out = jit_engine.pycuda.driver.mem_alloc(size)
        return self._buffer_cuda_out

    def cuda_execute(self, variable):
        # Create input parameter
        new_var = np.asfarray(variable)
        data_in = jit_engine.pycuda.driver.In(new_var)
        self._uploaded_bytes += new_var.nbytes

        self._bin_func.cuda_call(self._cuda_param_struct,
                                 self._cuda_state_struct,
                                 data_in, self._cuda_out,
                                 threads=len(self._execution_contexts))

        # Copy the result from the device
        ct_res = self.download_ctype(self._cuda_out, self._vo_ty)
        return _convert_ctype_to_python(ct_res)


class FuncExecution(CUDAExecution):

    def __init__(self, component, execution_ids=[None]):
        super().__init__()
        self._bin_func = pnlvm.LLVMBinaryFunction.from_obj(component)
        self._execution_contexts = [
            Context(execution_id=eid) for eid in execution_ids
        ]
        self._component = component

        par_struct_ty, ctx_struct_ty, vi_ty, vo_ty = self._bin_func.byref_arg_types

        if len(execution_ids) > 1:
            self._bin_multirun = self._bin_func.get_multi_run()
            self._ct_len = ctypes.c_int(len(execution_ids))
            vo_ty = vo_ty * len(execution_ids)
            vi_ty = vi_ty * len(execution_ids)

            self.__param_struct = None
            self.__state_struct = None

        self._vo_ty = vo_ty
        self._ct_vo = vo_ty()
        self._vi_ty = vi_ty

    def _get_compilation_param(self, name, initializer, arg, context):
        param = getattr(self._component._compilation_data, name)
        struct = param._get(context)
        if struct is None:
            initializer = getattr(self._component, initializer)(context)
            struct_ty = self._bin_func.byref_arg_types[arg]
            struct = struct_ty(*initializer)
            param._set(struct, context=context)

        return struct

    def _get_multirun_struct(self, arg, init):
        struct_ty = self._bin_multirun.byref_arg_types[arg] * len(self._execution_contexts)
        initializer = (getattr(self._component, init)(ex_id) for ex_id in self._execution_contexts)
        return struct_ty(*initializer)

    @property
    def _param_struct(self):
        if len(self._execution_contexts) > 1:
            if self.__param_struct is None:
                self.__param_struct = self._get_multirun_struct(0, '_get_param_initializer')
            return self.__param_struct

        return self._get_compilation_param('parameter_struct', '_get_param_initializer', 0, self._execution_contexts[0])

    @property
    def _state_struct(self):
        if len(self._execution_contexts) > 1:
            if self.__state_struct is None:
                self.__state_struct = self._get_multirun_struct(1, '_get_state_initializer')
            return self.__state_struct

        return self._get_compilation_param('state_struct', '_get_state_initializer', 1, self._execution_contexts[0])

    def execute(self, variable):
        new_variable = np.asfarray(variable)

        if len(self._execution_contexts) > 1:
            # wrap_call casts the arguments so we only need contiguous data
            # layout
            ct_vi = np.ctypeslib.as_ctypes(new_variable)
            self._bin_multirun.wrap_call(self._param_struct,
                                         self._state_struct,
                                         ct_vi, self._ct_vo, self._ct_len)
        else:
            ct_vi = new_variable.ctypes.data_as(ctypes.POINTER(self._vi_ty))
            self._bin_func(ctypes.byref(self._param_struct),
                           ctypes.byref(self._state_struct),
                           ct_vi, ctypes.byref(self._ct_vo))

        return _convert_ctype_to_python(self._ct_vo)


class MechExecution(FuncExecution):

    def execute(self, variable):
        # Convert to 3d. We always assume that:
        #   a) the input is vector of input ports
        #   b) input ports take vector of projection outputs
        #   c) projection output is a vector (even 1 element vector)
        new_var = [np.atleast_2d(x) for x in np.atleast_1d(variable)]
        return super().execute(new_var)


class CompExecution(CUDAExecution):

    def __init__(self, composition, execution_ids=[None], additional_tags=frozenset()):
        super().__init__(buffers=['state_struct', 'param_struct', 'data_struct', 'conditions'])
        self._composition = composition
        self._execution_contexts = [
            Context(execution_id=eid) for eid in execution_ids
        ]
        self.__bin_exec_func = None
        self.__bin_exec_multi_func = None
        self.__bin_func = None
        self.__bin_run_func = None
        self.__bin_run_multi_func = None
        self.__debug_env = debug_env
        self.__frozen_vals = None
        self.__additional_tags = frozenset(additional_tags)

        # TODO: Consolidate these
        if len(execution_ids) > 1:
            self.__state_struct = None
            self.__param_struct = None
            self.__data_struct = None
            self.__conds = None
            self._ct_len = ctypes.c_int(len(execution_ids))

    @property
    def _bin_func(self):
        if self.__bin_func is not None:
            assert len(self._execution_contexts) == 1
            return self.__bin_func
        if self.__bin_exec_func is not None:
            return self.__bin_exec_func
        if self.__bin_run_func is not None:
            return self.__bin_run_func

        assert False, "Binary function not set for execution!"

    @property
    def _bin_func_multirun(self):
        if self.__bin_exec_multi_func is not None:
            return self.__bin_exec_multi_func
        if self.__bin_run_multi_func is not None:
            return self.__bin_run_multi_func

        return super()._bin_func_multirun

    def _set_bin_node(self, node):
        assert node in self._composition._all_nodes
        wrapper = self._composition._get_node_wrapper(node)
        tags = frozenset(self.__additional_tags.union({"node_wrapper"}))
        self.__bin_func = pnlvm.LLVMBinaryFunction.from_obj(wrapper, tags=tags)

    @property
    def _conditions(self):
        if len(self._execution_contexts) > 1:
            if self.__conds is None:
                cond_type = self._bin_func_multirun.byref_arg_types[4] * len(self._execution_contexts)
                gen = helpers.ConditionGenerator(None, self._composition)
                cond_initializer = (gen.get_condition_initializer() for _ in self._execution_contexts)
                self.__conds = cond_type(*cond_initializer)
            return self.__conds

        conds = self._composition._compilation_data.scheduler_conditions._get(self._execution_contexts[0])
        if conds is None:
            cond_type = self._bin_func.byref_arg_types[4]
            gen = helpers.ConditionGenerator(None, self._composition)
            cond_initializer = gen.get_condition_initializer()
            conds = cond_type(*cond_initializer)
            self._composition._compilation_data.scheduler_conditions._set(conds, context=self._execution_contexts[0])
        return conds

    def _get_compilation_param(self, name, initializer, arg, context):
        param = getattr(self._composition._compilation_data, name)
        struct = param._get(context)
        if struct is None:
            initializer = getattr(self._composition, initializer)(context)
            struct_ty = self._bin_func.byref_arg_types[arg]
            struct = struct_ty(*initializer)
            param._set(struct, context=context)

        return struct

    def _get_multirun_struct(self, arg, init):
        struct_ty = self._bin_func_multirun.byref_arg_types[arg] * len(self._execution_contexts)
        initializer = (getattr(self._composition, init)(ex) for ex in self._execution_contexts)
        return struct_ty(*initializer)

    @property
    def _param_struct(self):
        if len(self._execution_contexts) > 1:
            if self.__param_struct is None:
                self.__param_struct = self._get_multirun_struct(1, '_get_param_initializer')
            return self.__param_struct

        return self._get_compilation_param('parameter_struct', '_get_param_initializer', 1, self._execution_contexts[0])

    @property
    def _state_struct(self):
        if len(self._execution_contexts) > 1:
            if self.__state_struct is None:
                self.__state_struct = self._get_multirun_struct(0, '_get_state_initializer')
            return self.__state_struct

        return self._get_compilation_param('state_struct', '_get_state_initializer', 0, self._execution_contexts[0])

    @property
    def _data_struct(self):
        # Run wrapper changed argument order
        arg = 2 if self._bin_func is self.__bin_run_func else 3

        if len(self._execution_contexts) > 1:
            if self.__data_struct is None:
                self.__data_struct = self._get_multirun_struct(arg, '_get_data_initializer')
            return self.__data_struct

        return self._get_compilation_param('data_struct', '_get_data_initializer', arg, self._execution_contexts[0])

    @_data_struct.setter
    def _data_struct(self, data_struct):
        if len(self._execution_contexts) > 1:
            self.__data_struct = data_struct
        else:
            self._composition._compilation_data.data_struct._set(data_struct, context=self._execution_contexts[0])

    def _extract_node_struct(self, node, data):
        # context structure consists of a list of node contexts,
        #   followed by a list of projection contexts; get the first one
        # parameter structure consists of a list of node parameters,
        #   followed by a list of projection parameters; get the first one
        # output structure consists of a list of node outputs,
        #   followed by a list of nested data structures; get the first one
        field = data._fields_[0][0]
        res_struct = getattr(data, field)
        index = self._composition._get_node_index(node)
        field = res_struct._fields_[index][0]
        res_struct = getattr(res_struct, field)
        return _convert_ctype_to_python(res_struct)

    def extract_node_struct(self, node, struct):
        if len(self._execution_contexts) > 1:
            return [self._extract_node_struct(node, struct[i]) for i, _ in enumerate(self._execution_contexts)]
        else:
            return self._extract_node_struct(node, struct)

    def extract_frozen_node_output(self, node):
        return self.extract_node_struct(node, self.__frozen_vals)

    def extract_node_output(self, node):
        return self.extract_node_struct(node, self._data_struct)

    def extract_node_state(self, node):
        return self.extract_node_struct(node, self._state_struct)

    def extract_node_params(self, node):
        return self.extract_node_struct(node, self._param_struct)

    def insert_node_output(self, node, data):
        my_field_name = self._data_struct._fields_[0][0]
        my_res_struct = getattr(self._data_struct, my_field_name)
        index = self._composition._get_node_index(node)
        node_field_name = my_res_struct._fields_[index][0]
        setattr(my_res_struct, node_field_name, _tupleize(data))

    def _get_input_struct(self, inputs):
        origins = self._composition.get_nodes_by_role(NodeRole.INPUT)
        # Either node or composition execute.
        # All execute functions expect inputs to be 3rd param.
        c_input = self._bin_func.byref_arg_types[2]

        # Read provided input data and separate each InputPort
        if len(self._execution_contexts) > 1:
            assert len(self._execution_contexts) == len(inputs)
            c_input = c_input * len(self._execution_contexts)
            input_data = (([x] for m in origins for x in inp[m]) for inp in inputs)
        else:
            input_data = ([x] for m in origins for x in inputs[m])

        return c_input(*_tupleize(input_data))

    def freeze_values(self):
        self.__frozen_vals = copy.deepcopy(self._data_struct)

    def execute_node(self, node, inputs=None, context=None):
        # We need to reconstruct the inputs here if they were not provided.
        # This happens during node execution of nested compositions.
        if inputs is None and node is self._composition.input_CIM:
            # This assumes origin mechanisms are in the same order as
            # CIM input ports
            origins = (n for n in self._composition.get_nodes_by_role(NodeRole.INPUT) for iport in n.input_ports)
            input_data = ([proj.parameters.value._get(context) for proj in port.all_afferents] for port in node.input_ports)
            inputs = defaultdict(list)
            for n, d in zip(origins, input_data):
                inputs[n].append(d[0])

        # Set bin node to make sure self._*struct works as expected
        self._set_bin_node(node)
        if inputs is not None:
            inputs = self._get_input_struct(inputs)

        assert inputs is not None or node is not self._composition.input_CIM

        # Freeze output values if this is the first time we need them
        if node is not self._composition.input_CIM and self.__frozen_vals is None:
            self.freeze_values()

        self._bin_func(self._state_struct, self._param_struct,
                       inputs, self.__frozen_vals, self._data_struct)

        if "comp_node_debug" in self.__debug_env:
            print("RAN: {}. CTX: {}".format(node, self.extract_node_state(node)))
            print("RAN: {}. Params: {}".format(node, self.extract_node_params(node)))
            print("RAN: {}. Results: {}".format(node, self.extract_node_output(node)))

    @property
    def _bin_exec_func(self):
        if self.__bin_exec_func is None:
            tags=frozenset(self.__additional_tags)
            self.__bin_exec_func = pnlvm.LLVMBinaryFunction.from_obj(
                self._composition, tags=tags)

        return self.__bin_exec_func

    @property
    def _bin_exec_multi_func(self):
        if self.__bin_exec_multi_func is None:
            self.__bin_exec_multi_func = self._bin_exec_func.get_multi_run()

        return self.__bin_exec_multi_func

    def execute(self, inputs):
        # NOTE: Make sure that input struct generation is inlined.
        # We need the binary function to be setup for it to work correctly.
        if len(self._execution_contexts) > 1:
            self._bin_exec_multi_func.wrap_call(self._state_struct,
                                                self._param_struct,
                                                self._get_input_struct(inputs),
                                                self._data_struct,
                                                self._conditions, self._ct_len)
        else:
            self._bin_exec_func(self._state_struct, self._param_struct,
                                self._get_input_struct(inputs),
                                self._data_struct, self._conditions)

    def cuda_execute(self, inputs):
        # NOTE: Make sure that input struct generation is inlined.
        # We need the binary function to be setup for it to work correctly.
        self._bin_exec_func.cuda_call(self._cuda_state_struct,
                                      self._cuda_param_struct,
                                      self.upload_ctype(self._get_input_struct(inputs)),
                                      self._cuda_data_struct,
                                      self._cuda_conditions,
                                      threads=len(self._execution_contexts))

        # Copy the data struct from the device
        self._data_struct = self.download_ctype(self._cuda_data_struct, type(self._data_struct))

    # Methods used to accelerate "Run"

    def _get_run_input_struct(self, inputs, num_input_sets):
        origins = self._composition.get_nodes_by_role(NodeRole.INPUT)
        input_type = self._bin_run_func.byref_arg_types[3]
        c_input = (input_type * num_input_sets) * len(self._execution_contexts)
        if len(self._execution_contexts) == 1:
            inputs = [inputs]

        assert len(inputs) == len(self._execution_contexts)
        # Extract input for each trial and execution id
        run_inputs = ((([iv] for m in origins for iv in inp[m][i]) for i in range(num_input_sets)) for inp in inputs)
        return c_input(*_tupleize(run_inputs))

    @property
    def _bin_run_func(self):
        if self.__bin_run_func is None:
            run_tags = frozenset({"run"}.union(self.__additional_tags))
            self.__bin_run_func = pnlvm.LLVMBinaryFunction.from_obj(
                self._composition, tags=run_tags)

        return self.__bin_run_func

    @property
    def _bin_run_multi_func(self):
        if self.__bin_run_multi_func is None:
            self.__bin_run_multi_func = self._bin_run_func.get_multi_run()

        return self.__bin_run_multi_func

    def run(self, inputs, runs=0, num_input_sets=0, learning=False):
        if isgenerator(inputs):
            list_inputs = list(inputs)
            inputs = {k:[list(v)] for (k,v) in list_inputs[0].items()}
            for i, inp in enumerate(list_inputs):
                if i == 0:
                    continue
                for k,v in inp.items():
                    inputs[k].append(v)
            num_input_sets = len(next(iter(inputs.values())))
            runs = num_input_sets
        inputs = self._get_run_input_struct(inputs, num_input_sets)

        ct_vo = self._bin_run_func.byref_arg_types[4] * runs
        if len(self._execution_contexts) > 1:
            ct_vo = ct_vo * len(self._execution_contexts)
        outputs = ct_vo()
        runs_count = ctypes.c_int(runs)
        input_count = ctypes.c_int(num_input_sets)
        if len(self._execution_contexts) > 1:
            self._bin_run_multi_func.wrap_call(self._state_struct, self._param_struct,
                                               self._data_struct, inputs, outputs,
                                               runs_count, input_count, self._ct_len)
        else:
            self._bin_run_func.wrap_call(self._state_struct, self._param_struct,
                                         self._data_struct, inputs, outputs,
                                         runs_count, input_count)
        return _convert_ctype_to_python(outputs)

    def cuda_run(self, inputs, runs, num_input_sets):
        # Create input buffer
        inputs = self._get_run_input_struct(inputs, num_input_sets)
        data_in = self.upload_ctype(inputs)

        # Create output buffer
        output_type = (self._bin_run_func.byref_arg_types[4] * runs)
        if len(self._execution_contexts) > 1:
            output_type = output_type * len(self._execution_contexts)
        output_size = ctypes.sizeof(output_type)
        data_out = jit_engine.pycuda.driver.mem_alloc(output_size)

        runs_count = jit_engine.pycuda.driver.In(np.int32(runs))
        input_count = jit_engine.pycuda.driver.In(np.int32(num_input_sets))
        self._uploaded_bytes += 8   # runs_count + input_count

        self._bin_run_func.cuda_call(self._cuda_state_struct,
                                     self._cuda_param_struct,
                                     self._cuda_data_struct,
                                     data_in, data_out, runs_count, input_count,
                                     threads=len(self._execution_contexts))

        # Copy the data struct from the device
        ct_out = self.download_ctype(data_out, output_type)
        return _convert_ctype_to_python(ct_out)
