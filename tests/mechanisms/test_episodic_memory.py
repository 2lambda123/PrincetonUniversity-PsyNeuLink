import numpy as np
import pytest

import psyneulink.core.llvm as pnlvm
from psyneulink.core.components.functions.function import FunctionError
from psyneulink.core.components.functions.statefulfunctions.memoryfunctions import DictionaryMemory, \
    ContentAddressableMemory
from psyneulink.library.components.mechanisms.processing.integrator.episodicmemorymechanism import \
    EpisodicMemoryMechanism

np.random.seed(0)

# TEST WITH DictionaryMemory ****************************************************************************************

CONTENT_SIZE=10
ASSOC_SIZE=10
test_var = np.random.rand(2, CONTENT_SIZE)
test_initializer = {tuple(test_var[0]): test_var[1]}

test_data = [
    (test_var, DictionaryMemory, {'default_variable':test_var}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047,
        0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777],
        [0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694,
         0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
    (test_var, DictionaryMemory, {'default_variable':test_var, 'retrieval_prob':0.5},
     [[ 0. for i in range(CONTENT_SIZE) ],[ 0. for i in range(ASSOC_SIZE) ]]),
    (test_var, DictionaryMemory, {'default_variable':test_var, 'storage_prob':0.1},
     [[ 0. for i in range(CONTENT_SIZE) ],[ 0. for i in range(ASSOC_SIZE) ]]),
    (test_var, DictionaryMemory, {'default_variable':test_var, 'retrieval_prob':0.9, 'storage_prob':0.9}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047,
        0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777],
        [0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694,
         0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
]

# use list, naming function produces ugly names
names = [
    "DictionaryMemory",
    "DictionaryMemory Random Retrieval",
    "DictionaryMemory Random Storage",
    "DictionaryMemory Random Retrieval-Storage",
]

@pytest.mark.function
@pytest.mark.memory_function
@pytest.mark.benchmark
@pytest.mark.parametrize('variable, func, params, expected', test_data, ids=names)
def test_with_dictionary_memory(variable, func, params, expected, benchmark, mech_mode):
    f = func(seed=0, **params)
    m = EpisodicMemoryMechanism(content_size=len(variable[0]), assoc_size=len(variable[1]), function=f)
    if mech_mode == 'Python':
        def EX(variable):
            m.execute(variable)
            return m.output_values
    elif mech_mode == 'LLVM':
        EX = pnlvm.execution.MechExecution(m).execute
    elif mech_mode == 'PTX':
        EX = pnlvm.execution.MechExecution(m).cuda_execute

    EX(variable)
    res = EX(variable)
    assert np.allclose(res[0], expected[0])
    assert np.allclose(res[1], expected[1])
    if benchmark.enabled:
        benchmark(EX, variable)

# TEST WITH ContentAddressableMemory ***********************************************************************************
# Note:  ContentAddressableMemory has not yet been compiled for use with LLVM or PTX, so those are dummy tests for now

test_data = [
    (
        # name
        "ContentAddressableMemory Func Default Variable Mech Size Init",
        # func
        ContentAddressableMemory,
        # func_params
        {'default_variable': [[0],[0,0],[0,0,0]]},
        # mech_params
        {'size':[1,2,3]},
        # test_var
        [[10.],[20., 30.],[40., 50., 60.]],
        # expected input_port names
        ['FIELD_0_INPUT', 'FIELD_1_INPUT', 'FIELD_2_INPUT'],
        # expected output_port names
        ['RETREIVED_FIELD_0', 'RETREIVED_FIELD_1', 'RETREIVED_FIELD_2'],
        # expected output
        [[10.],[20., 30.],[40., 50., 60.]]
    ),
    (
        "ContentAddressableMemory Func Default Variable Mech Default Var Init",
        ContentAddressableMemory,
        {'default_variable': [[0],[0,0],[0,0,0]]},
        {'default_variable': [[0],[0,0],[0,0,0]]},
        [[10.],[20., 30.],[40., 50., 60.]],
        ['FIELD_0_INPUT', 'FIELD_1_INPUT', 'FIELD_2_INPUT'],
        ['RETREIVED_FIELD_0', 'RETREIVED_FIELD_1', 'RETREIVED_FIELD_2'],
        [[10.],[20., 30.],[40., 50., 60.]]
    ),
    (
        "ContentAddressableMemory Func Initializer (ragged) Mech Size Init",
        ContentAddressableMemory,
        {'initializer':np.array([[np.array([1]), np.array([2, 3]), np.array([4, 5, 6])],
                                 [list([10]), list([20, 30]), list([40, 50, 60])],
                                 [np.array([11]), np.array([22, 33]), np.array([44, 55, 66])]])},
        {'size':[1,2,3]},
        [[10.],[20., 30.],[40., 50., 60.]],
        ['FIELD_0_INPUT', 'FIELD_1_INPUT', 'FIELD_2_INPUT'],
        ['RETREIVED_FIELD_0', 'RETREIVED_FIELD_1', 'RETREIVED_FIELD_2'],
        [[10.],[20., 30.],[40., 50., 60.]]
    ),
    (
        "ContentAddressableMemory Func Initializer (ragged) Mech Default Variable Init",
        ContentAddressableMemory,
        {'initializer':np.array([[np.array([1]), np.array([2, 3]), np.array([4, 5, 6])],
                                 [[10], [20, 30], [40, 50, 60]],
                                 [np.array([11]), np.array([22, 33]), np.array([44, 55, 66])]])},
        {'default_variable': [[0],[0,0],[0,0,0]], 'input_ports':['hello','world','goodbye']},
        [[10.],[20., 30.],[40., 50., 60.]],
        ['hello', 'world', 'goodbye'],
        ['RETREIVED_hello', 'RETREIVED_world', 'RETREIVED_goodbye'],
        [[10.],[20., 30.],[40., 50., 60.]]
    ),
    (
        "ContentAddressableMemory Func Initializer (regular 2d) Mech Size Init",
        ContentAddressableMemory,
        {'initializer':np.array([[np.array([1,2]), np.array([3,4]), np.array([5, 6])],
                                 [[10,20], [30,40], [50,60]],
                                 [np.array([11,12]), np.array([22, 23]), np.array([34, 35])]])},
        {'size':[2,2,2]},
        [[10,20], [30,40], [50, 60]],
        ['FIELD_0_INPUT', 'FIELD_1_INPUT', 'FIELD_2_INPUT'],
        ['RETREIVED_FIELD_0', 'RETREIVED_FIELD_1', 'RETREIVED_FIELD_2'],
        [[10,20], [30,40], [50, 60]],
    ),
    (
        "ContentAddressableMemory Func Initializer (regular 2d) Mech Default Variable Init",
        ContentAddressableMemory,
        {'initializer':np.array([[np.array([1,2]), np.array([3,4]), np.array([5, 6])],
                                 [[10,20], [30,40], [50,60]],
                                 [np.array([11,12]), np.array([22, 23]), np.array([34, 35])]])},
        {'default_variable':[[0,0],[0,0],[0,0]]},
        [[10,20], [30,40], [50, 60]],
        ['FIELD_0_INPUT', 'FIELD_1_INPUT', 'FIELD_2_INPUT'],
        ['RETREIVED_FIELD_0', 'RETREIVED_FIELD_1', 'RETREIVED_FIELD_2'],
        [[10,20], [30,40], [50, 60]],
    )
]

# Allows names to be with each test_data set
names = [test_data[i][0] for i in range(len(test_data))]

@pytest.mark.parametrize('name, func, func_params, mech_params, test_var,'
                         'input_port_names, output_port_names, expected_output', test_data, ids=names)
def test_with_contentaddressablememory(name, func, func_params, mech_params, test_var,
                                       input_port_names, output_port_names, expected_output, mech_mode):
    f = func(seed=0, **func_params)
    EpisodicMemoryMechanism(function=f, **mech_params)
    em = EpisodicMemoryMechanism(**mech_params)
    assert em.input_ports.names == input_port_names
    assert em.output_ports.names == output_port_names

    if mech_mode == 'Python':
        def EX(variable):
            em.execute(variable)
            return em.output_values
    elif mech_mode == 'LLVM':
        def EX(variable):
            # DUMMY UNTIL LLVM IMPLEMENTED
            return variable
    elif mech_mode == 'PTX':
        def EX(variable):
            # DUMMY UNTIL PTX IMPLEMENTED
            return variable

    EX(test_var)
    actual_output = EX(test_var)
    for i,j in zip(actual_output,expected_output):
        np.testing.assert_allclose(i, j, atol=1e-08)

def test_failures_with_contentaddressable_memory():

    # Initializer with >2d regular array
    with pytest.raises(FunctionError) as error_text:
        f = ContentAddressableMemory(initializer=[[[[1],[0],[1]], [[1],[0],[0]], [[0],[1],[1]]],
                                                  [[[0],[1],[0]], [[0],[1],[1]], [[1],[1],[0]]]])
        em = EpisodicMemoryMechanism(size = [1,1,1], function=f)
        em.execute([[[0],[1],[0]], [[0],[1],[1]], [[1],[1],[0]]])
    assert 'Attempt to store and/or retrieve an entry in ContentAddressableMemory that has more than 2 dimensions (' \
           '3);  try flattening innermost ones.' in str(error_text.value)
