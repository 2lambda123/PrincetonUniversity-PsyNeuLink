import numpy as np
import pytest
from itertools import combinations, product

import psyneulink.core.components.functions.statefulfunctions.memoryfunctions as Functions
import psyneulink.core.llvm as pnlvm
from psyneulink import *

# **********************************************************************************************************************
# OMINBUS TEST *********************************************************************************************************
# **********************************************************************************************************************

#region

np.random.seed(0)
SIZE=10
test_var = np.random.rand(2, SIZE)
test_initializer = np.array([[test_var[0], test_var[1]]])
test_noise_arr = np.random.rand(SIZE)

RAND1 = np.random.random(1)
RAND2 = np.random.random()

test_data = [
# Default initializer does not work
#    (Functions.Buffer, test_var, {'rate':RAND1}, [[0.0],[0.0]]),
    (Functions.Buffer, test_var[0], {'history':512, 'rate':RAND1, 'initializer':[test_var[0]]}, [[0.03841128, 0.05005587, 0.04218721, 0.0381362 , 0.02965146, 0.04520592, 0.03062659, 0.0624149 , 0.06744644, 0.02683695],[0.14519169, 0.18920736, 0.15946443, 0.1441519 , 0.11208025, 0.17087491, 0.11576615, 0.23592355, 0.25494239, 0.10144161]]),
    (Functions.DictionaryMemory, test_var, {'rate':RAND1}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777], [
       0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694, 0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
    (Functions.DictionaryMemory, test_var, {'rate':RAND1, 'retrieval_prob':0.5},
     [[ 0. for i in range(SIZE) ],[ 0. for i in range(SIZE) ]]),
    (Functions.DictionaryMemory, test_var, {'rate':RAND1, 'storage_prob':0.1},
     [[ 0. for i in range(SIZE) ],[ 0. for i in range(SIZE) ]]),
    (Functions.DictionaryMemory, test_var, {'rate':RAND1, 'retrieval_prob':0.9, 'storage_prob':0.9}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777], [
       0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694, 0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
    (Functions.DictionaryMemory, test_var, {'initializer':test_initializer, 'rate':RAND1}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777], [
       0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694, 0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
# Disable noise tests for now as they trigger failure in DictionaryMemory lookup
#    (Functions.DictionaryMemory, test_var, {'rate':RAND1, 'noise':RAND2}, [[
#       0.79172504, 0.52889492, 0.56804456, 0.92559664, 0.07103606, 0.0871293 , 0.0202184 , 0.83261985, 0.77815675, 0.87001215 ],[
#       1.3230471933615413, 1.4894230558066361, 1.3769970655058605, 1.3191168724311135, 1.1978884887731214, 1.4201278025008728, 1.2118209006969092, 1.6660066902162964, 1.737896449935246, 1.1576752082599944
#]]),
#    (Functions.DictionaryMemory, test_var, {'rate':RAND1, 'noise':[RAND2], 'retrieval_prob':0.5},
#       [[ 0. for i in range(SIZE) ],[ 0. for i in range(SIZE) ]]),
#    (Functions.DictionaryMemory, test_var, {'rate':RAND1, 'noise':RAND2, 'storage_prob':0.5},
#       [[ 0. for i in range(SIZE) ],[ 0. for i in range(SIZE) ]]),
#    (Functions.DictionaryMemory, test_var, {'initializer':test_initializer, 'rate':RAND1, 'noise':RAND2}, [[
#       0.79172504, 0.52889492, 0.56804456, 0.92559664, 0.07103606, 0.0871293 , 0.0202184 , 0.83261985, 0.77815675, 0.87001215 ],[
#       1.3230471933615413, 1.4894230558066361, 1.3769970655058605, 1.3191168724311135, 1.1978884887731214, 1.4201278025008728, 1.2118209006969092, 1.6660066902162964, 1.737896449935246, 1.1576752082599944
#]]),
    (Functions.DictionaryMemory, test_var, {'rate':RAND1}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777], [
       0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694, 0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
    (Functions.ContentAddressableMemory, test_var, {'rate':RAND1, 'retrieval_prob':0.5},
     [[ 0. for i in range(SIZE) ],[ 0. for i in range(SIZE) ]]),
    (Functions.ContentAddressableMemory, test_var, {'rate':RAND1, 'storage_prob':0.1},
     [[ 0. for i in range(SIZE) ],[ 0. for i in range(SIZE) ]]),
    (Functions.ContentAddressableMemory, test_var, {'rate':RAND1, 'retrieval_prob':0.9, 'storage_prob':0.9}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777], [
       0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694, 0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
    (Functions.ContentAddressableMemory, test_var, {'initializer':test_initializer, 'rate':RAND1}, [[
       0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777], [
       0.7917250380826646, 0.5288949197529045, 0.5680445610939323, 0.925596638292661, 0.07103605819788694, 0.08712929970154071, 0.02021839744032572, 0.832619845547938, 0.7781567509498505, 0.8700121482468192 ]]),
]

# use list, naming function produces ugly names
names = [
    "Buffer",
#    "Buffer Initializer",
    "DictionaryMemory",
    "DictionaryMemory Random Retrieval",
    "DictionaryMemory Random Storage",
    "DictionaryMemory Random Retrieval-Storage",
    "DictionaryMemory Initializer",
#    "DictionaryMemory Noise",
#    "DictionaryMemory Noise Random Retrieval",
#    "DictionaryMemory Noise Random Storage",
#    "DictionaryMemory Initializer Noise",
    "ContentAddressableMemory",
    "ContentAddressableMemory Random Retrieval",
    "ContentAddressableMemory Random Storage",
    "ContentAddressableMemory Random Retrieval-Storage",
    "ContentAddressableMemory Initializer",
]

@pytest.mark.function
@pytest.mark.memory_function
@pytest.mark.benchmark
@pytest.mark.parametrize("func, variable, params, expected", test_data, ids=names)
def test_basic(func, variable, params, expected, benchmark, func_mode):
    if func is Functions.Buffer and func_mode != 'Python':
        pytest.skip("Not implemented")
    if func is Functions.ContentAddressableMemory and func_mode != 'Python':
        pytest.skip("Not implemented")

    f = func(default_variable=variable, **params)
    benchmark.group = func.componentName
    if func_mode == 'Python':
        EX = f.function
    elif func_mode == 'LLVM':
        e = pnlvm.execution.FuncExecution(f)
        EX = e.execute
    elif func_mode == 'PTX':
        e = pnlvm.execution.FuncExecution(f)
        EX = e.cuda_execute
    EX(variable)
    res = EX(variable)
    assert np.allclose(res[0], expected[0])
    assert np.allclose(res[1], expected[1])
    if benchmark.enabled:
        benchmark(f, variable)

#endregion

# **********************************************************************************************************************
# TEST Dictionary Memory ***********************************************************************************************
# **********************************************************************************************************************

#region

class TestDictionaryMemory:
    # Test of DictionaryMemory without LLVM:
    def test_DictionaryMemory_with_initializer_and_key_size_same_as_val_size(self):

        stimuli = {'A': [[1,2,3],[4,5,6]],
                   'B': [[8,9,10],[11,12,13]],
                   'C': [[1,2,3],[11,12,13]],
                   'D': [[1,2,3],[21,22,23]],
                   'E': [[9,8,4],[11,12,13]],
                   'F': [[10,10,30],[40,50,60]],
                   }

        em = EpisodicMemoryMechanism(
                content_size=3,
                assoc_size=3,
                function = DictionaryMemory(
                        seed=2,
                        initializer=np.array([stimuli['F'], stimuli['F']], dtype=object),
                        duplicate_keys=True,
                        equidistant_keys_select=RANDOM)
        )

        retrieved_keys=[]
        for key in sorted(stimuli.keys()):
            retrieved = [i for i in em.execute(stimuli[key])]
            retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
            retrieved_keys.append(retrieved_key)
        assert retrieved_keys == [['F'], ['A'], ['A'], ['C'], ['B'], ['F']]

        # Run again to test re-initialization and random retrieval
        em.function.reset(np.array([stimuli['A'], stimuli['F']]))
        retrieved_keys=[]
        for key in sorted(stimuli.keys()):
            retrieved = [i for i in em.execute(stimuli[key])]
            retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
            retrieved_keys.append(retrieved_key)
        assert retrieved_keys == [['A'], ['A'], ['A'], ['A'], ['B'], ['F']]

        stim = 'C'
        em.function.equidistant_keys_select = OLDEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['A']

        em.function.equidistant_keys_select = NEWEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        em.function.duplicate_keys = False
        stim = 'A'

        text = r'More than one item matched key \(\[1 2 3\]\) in memory for DictionaryMemory'
        with pytest.warns(UserWarning, match=text):
            retrieved = em.execute(stimuli[stim])

        retrieved_key = [k for k,v in stimuli.items() if v==list(retrieved)] or [None]
        assert retrieved_key == [None]
        assert retrieved[0] == [0, 0, 0]
        assert retrieved[1] == [0, 0, 0]

    def test_DictionaryMemory_with_initializer_and_key_size_diff_from_val_size(self):

        stimuli = {'A': [[1,2,3],[4,5,6,7]],
                   'B': [[8,9,10],[11,12,13,14]],
                   'C': [[1,2,3],[11,12,13,14]],
                   'D': [[1,2,3],[21,22,23,24]],
                   'E': [[9,8,4],[11,12,13,14]],
                   'F': [[10,10,30],[40,50,60,70]],
                   }

        em = EpisodicMemoryMechanism(
                content_size=3,
                assoc_size=4,
                function = DictionaryMemory(
                        initializer=np.array([stimuli['F'], stimuli['F']], dtype=object),
                        duplicate_keys=True,
                        equidistant_keys_select=RANDOM)
        )

        retrieved_keys=[]
        for key in sorted(stimuli.keys()):
            print(key)
            retrieved = [i for i in em.execute(stimuli[key])]
            retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
            retrieved_keys.append(retrieved_key)
        assert retrieved_keys == [['F'], ['A'], ['A'], ['A'], ['B'], ['F']]

        stim = 'C'
        em.function.equidistant_keys_select = OLDEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['A']

        em.function.equidistant_keys_select = NEWEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        em.function.duplicate_keys = False
        stim = 'A'

        text = r'More than one item matched key \(\[1 2 3\]\) in memory for DictionaryMemory'
        with pytest.warns(UserWarning, match=text):
            retrieved = em.execute(stimuli[stim])

        retrieved_key = [k for k,v in stimuli.items() if v==list(retrieved)] or [None]
        assert retrieved_key == [None]
        assert retrieved[0] == [0, 0, 0]
        assert retrieved[1] == [0, 0, 0, 0]

    # def test_DictionaryMemory_without_initializer_in_composition():
    #
    #     content = TransferMechanism(size=5)
    #     assoc = TransferMechanism(size=3)
    #     content_out = TransferMechanism(size=5)
    #     assoc_out = TransferMechanism(size=3)
    #
    #     # Episodic Memory, Decision and Control
    #     em = EpisodicMemoryMechanism(name='EM',
    #                                  content_size=5, assoc_size=3)
    #     comp = Composition()
    #     comp.add_nodes([content, assoc, content_out, assoc_out, em])
    #     comp.add_projection(MappingProjection(), content, em.input_ports[KEY_INPUT])
    #     comp.add_projection(MappingProjection(), assoc, em.input_ports[VALUE_INPUT])
    #     comp.add_projection(MappingProjection(), em.output_ports[KEY_OUTPUT], content_out)
    #     comp.add_projection(MappingProjection(), em.output_ports[VALUE_OUTPUT], assoc_out)
    #
    #     comp.run(inputs={content:[1,2,3,4,5],
    #                      assoc:[6,7,8]})

    def test_DictionaryMemory_without_initializer_and_key_size_same_as_val_size(self):

        stimuli = {'A': [[1,2,3],[4,5,6]],
                   'B': [[8,9,10],[11,12,13]],
                   'C': [[1,2,3],[11,12,13]],
                   'D': [[1,2,3],[21,22,23]],
                   'E': [[9,8,4],[11,12,13]],
                   'F': [[10,10,30],[40,50,60]],
                   }

        em = EpisodicMemoryMechanism(
                content_size=3,
                assoc_size=3,
                function = DictionaryMemory(
                        duplicate_keys=True,
                        equidistant_keys_select=RANDOM)
        )

        retrieved_keys=[]
        for key in sorted(stimuli.keys()):
            retrieved = [i for i in em.execute(stimuli[key])]
            retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
            retrieved_keys.append(retrieved_key)
        assert retrieved_keys == [[None], ['A'], ['A'], ['C'], ['B'], ['D']]

        stim = 'C'
        em.function.equidistant_keys_select = OLDEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['A']

        em.function.equidistant_keys_select = NEWEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        em.function.duplicate_keys = False
        stim = 'A'

        text = r'More than one item matched key \(\[1 2 3\]\) in memory for DictionaryMemory'
        with pytest.warns(UserWarning, match=text):
            retrieved = em.execute(stimuli[stim])

        retrieved_key = [k for k,v in stimuli.items() if v==list(retrieved)] or [None]
        assert retrieved_key == [None]
        assert retrieved[0] == [0, 0, 0]
        assert retrieved[1] == [0, 0, 0]

    def test_DictionaryMemory_without_initializer_and_key_size_diff_from_val_size(self):

        stimuli = {'A': [[1,2,3],[4,5,6,7]],
                   'B': [[8,9,10],[11,12,13,14]],
                   'C': [[1,2,3],[11,12,13,14]],
                   'D': [[1,2,3],[21,22,23,24]],
                   'E': [[9,8,4],[11,12,13,14]],
                   'F': [[10,10,30],[40,50,60,70]],
                   }

        em = EpisodicMemoryMechanism(
                content_size=3,
                assoc_size=4,
                function = DictionaryMemory(
                        duplicate_keys=True,
                        equidistant_keys_select=RANDOM)
        )

        retrieved_keys=[]
        for key in sorted(stimuli.keys()):
            retrieved = [i for i in em.execute(stimuli[key])]
            retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
            retrieved_keys.append(retrieved_key)
        assert retrieved_keys == [[None], ['A'], ['A'], ['C'], ['B'], ['D']]

        stim = 'C'
        em.function.equidistant_keys_select = OLDEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['A']

        em.function.equidistant_keys_select = NEWEST
        retrieved = [i for i in em.function.get_memory(stimuli[stim][0])]
        retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
        assert retrieved_key == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        em.function.duplicate_keys = False
        stim = 'A'

        text = r'More than one item matched key \(\[1 2 3\]\) in memory for DictionaryMemory'
        with pytest.warns(UserWarning, match=text):
            retrieved = em.execute(stimuli[stim])

        retrieved_key = [k for k,v in stimuli.items() if v==list(retrieved)] or [None]
        assert retrieved_key == [None]
        assert retrieved[0] == [0, 0, 0]
        assert retrieved[1] == [0, 0, 0, 0]

    def test_DictionaryMemory_without_assoc(self):

        stimuli = {'A': [[1,2,3]],
                   'B': [[8,9,10]],
                   'C': [[1,2,3]],
                   'D': [[1,2,3]],
                   'E': [[9,8,4]],
                   'F': [[10,10,30]],
                   }

        em = EpisodicMemoryMechanism(
                name='EPISODIC MEMORY MECH',
                content_size=3,
                function = DictionaryMemory(
                        # initializer=np.array([stimuli['F'], stimuli['F']], dtype=object),
                        duplicate_keys=True,
                        equidistant_keys_select=RANDOM,
                        retrieval_prob = 1.0
                )
        )

        for key in sorted(stimuli.keys()):
            print(f'\nCurrent memory: \n{em.memory}\n')
            retrieved = [i for i in em.execute(stimuli[key])]
            retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
            print(f'\nExecuted with stimulus {key}: {stimuli[key]};'
                  f'\nRetrieved memory {retrieved_key[0]}: \n\t{retrieved}')

        retrieved_keys=[]
        for key in sorted(stimuli.keys()):
            retrieved = [i for i in em.execute(stimuli[key])]
            retrieved_key = [k for k,v in stimuli.items() if v == retrieved] or [None]
            retrieved_keys.append(retrieved_key)

        assert retrieved_keys == [['A', 'C', 'D'], ['B'], ['A', 'C', 'D'], ['A', 'C', 'D'], ['E'], ['F']]

    def test_DictionaryMemory_with_duplicate_entry_in_initializer_warning(self):

        regexp = r'Attempt to initialize memory of DictionaryMemory with an entry \([[1 2 3]'
        with pytest.warns(UserWarning, match=regexp):
            em = EpisodicMemoryMechanism(
                    name='EPISODIC MEMORY MECH',
                    content_size=3,
                    assoc_size=3,
                    function = DictionaryMemory(
                            initializer=np.array([[[1,2,3], [4,5,6]],
                                                  [[1,2,3], [7,8,9]]]),
                            duplicate_keys=False,
                            equidistant_keys_select=RANDOM,
                            retrieval_prob = 1.0
                    )
            )
        assert np.allclose(em.memory, np.array([[[1, 2, 3], [4, 5, 6]]]))

    def test_DictionaryMemory_add_and_delete_from_memory(self):

        em = DictionaryMemory(
                initializer=[[[1,2,3], [4,5,6]],
                             [[7,8,9], [10,11,12]]],
                duplicate_keys=True,
                equidistant_keys_select=RANDOM,
                retrieval_prob = 1.0,
                storage_prob = 1.0
        )
        em.add_to_memory([[[10,20,30],[40,50,60]],
                         [[11,21,31],[41,51,61]]])

        expected_memory = [[[ 1,  2,  3],[ 4,  5,  6]],
                           [[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]]]
        assert np.allclose(em.memory, expected_memory)

        em.delete_from_memory([[[1,2,3],[4,5,6]]])
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]]]
        assert np.allclose(em.memory, expected_memory)

        # Test adding and deleting a single memory
        em.add_to_memory([[1,2,3],[100,101,102]])
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]],
                           [[ 1,  2,  3],[100,101,102]]]
        assert np.allclose(em.memory, expected_memory)

        em.delete_from_memory([[1,2,3],[100,101,102]])
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]]]
        assert np.allclose(em.memory, expected_memory)

        # Test adding memory with different size value
        em.add_to_memory([[1,2,3],[100,101,102,103]])
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]],
                           [[ 1,  2,  3],[100,101,102,103]]]
        for m,e in zip(em.memory,expected_memory):
            for i,j in zip(m,e):
                assert np.allclose(i,j)

        # Test adding memory with different size value as np.array
        em.add_to_memory(np.array([[1,2,3],[200,201,202,203]], dtype=object))
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]],
                           [[ 1,  2,  3],[100,101,102,103]],
                           [[ 1,  2,  3],[200,201,202,203]]]
        for m,e in zip(em.memory,expected_memory):
            for i,j in zip(m,e):
                assert np.allclose(i,j)

        # Test error for illegal key:
        with pytest.raises(FunctionError) as error_text:
            em.add_to_memory(np.array([[1,2],[200,201,202,203]], dtype=object))
        assert "Length of 'key'" in str(error_text.value) and "must be same as others in the dict" in str(error_text.value)

    def test_DictionaryMemory_overwrite_mode(self):

        em = DictionaryMemory(
                initializer=[[[1,2,3], [4,5,6]],
                             [[7,8,9], [10,11,12]]],
                duplicate_keys=True,
                equidistant_keys_select=RANDOM,
                retrieval_prob = 1.0,
                storage_prob = 1.0
        )

        em.duplicate_keys = OVERWRITE

        # Add new memory
        retreived = em.execute([[7,8,10], [100,110,120]])
        assert np.allclose(list(retreived), [[7,8,9],[10,11,12]])
        expected_memory = [[[ 1,  2,  3],[4, 5, 6]],
                           [[7,8,9], [10,11,12]],
                           [[7,8,10], [100,110,120]]]
        assert np.allclose(em.memory, expected_memory)

        # Overwrite old memory
        retreived = em.execute([[7,8,9], [100,110,120]])
        assert np.allclose(list(retreived), [[7,8,9],[10,11,12]])
        expected_memory = [[[ 1,  2,  3],[4, 5, 6]],
                           [[7,8,9], [100,110,120]],
                           [[7,8,10], [100,110,120]]]
        assert np.allclose(em.memory, expected_memory)

        # Allow entry of memory with duplicate key
        em.duplicate_keys = True
        retreived = em.execute([[7,8,9], [200,210,220]])
        assert np.allclose(list(retreived), [[7,8,9],[100,110,120]])
        expected_memory = [[[ 1,  2,  3],[4, 5, 6]],
                           [[7,8,9], [100,110,120]],
                           [[7,8,10], [100,110,120]],
                           [[7,8,9], [200,210,220]]]
        assert np.allclose(em.memory, expected_memory)

        # Attempt to overwrite with two matches should generate error
        em.duplicate_keys = OVERWRITE
        with pytest.raises(FunctionError) as error_text:
            em.execute([[7,8,9], [200,210,220]])
        assert ('Attempt to store item' in str(error_text.value)
                and 'with \'duplicate_keys\'=\'OVERWRITE\'' in str(error_text.value))

    def test_DictionaryMemory_max_entries(self):

        em = DictionaryMemory(
                initializer=[[[1,2,3], [4,5,6]],
                             [[7,8,9], [10,11,12]],
                             [[1,2,3], [100,101,102]]],
                duplicate_keys=True,
                equidistant_keys_select=RANDOM,
                retrieval_prob = 1.0,
                storage_prob = 1.0,
                max_entries = 4
        )
        em.add_to_memory([[[10,20,30],[40,50,60]],
                        [[11,21,31],[41,51,61]],
                        [[12,22,32],[42,52,62]]])
        expected_memory = [[[1,2,3], [100,101,102]],
                           [[10,20,30],[40,50,60]],
                           [[11,21,31],[41,51,61]],
                           [[12,22,32],[42,52,62]]]
        assert np.allclose(em.memory, expected_memory)

    @pytest.mark.parametrize(
        'param_name',
        [
            'distance_function',
            'selection_function',
        ]
    )
    def test_DictionaryMemory_unique_functions(self, param_name):
        a = DictionaryMemory()
        b = DictionaryMemory()

        assert (
            getattr(a.parameters, param_name).get()
            is not getattr(b.parameters, param_name).get()
        )

        assert (
            getattr(a.defaults, param_name)
            is not getattr(b.defaults, param_name)
        )
#endregion

# **********************************************************************************************************************
# TEST ContentAddressableMemory ****************************************************************************************
# **********************************************************************************************************************

def retrieve_label(retrieved, stimuli):
    return [k for k,v in stimuli.items()
            if all(np.alltrue(a)
                   for a in np.equal(retrieved,v, dtype=object))] or [None]

#region
class TestContentAddressableMemory:


    def test_ContentAddressableMemory_distances(self):

        stimuli = np.array([[[1,2,3],[4,5,6]],
                            [[7,8,9],[10,11,12]],
                            [[13,14,15],[16,17,18]]])

        c = ContentAddressableMemory(
            initializer=stimuli,
            storage_prob=0,
            distance_function=Distance(metric=COSINE)
        )
        pairs = list(combinations(range(0,3),2))
        # Distances between all stimuli
        distances = [Distance(metric=COSINE)([stimuli[i],stimuli[j]]) for i, j in pairs]
        c_distances = []
        # for i,j in pairs:

        retrieved = c(stimuli[0])
        np.all(retrieved==stimuli[0])
        assert np.allclose(c.distances_to_entries, [0, distances[0], distances[1]])

        retrieved = c(stimuli[1])
        np.all(retrieved==stimuli[1])
        assert np.allclose(c.distances_to_entries, [distances[0], 0, distances[2]])

        retrieved = c(stimuli[2])
        np.all(retrieved==stimuli[2])
        assert np.allclose(c.distances_to_entries, [distances[1], distances[2], 0])

        # Test distances based only on field 0

        field_weights = np.array([[1],[0]])
        c.distance_field_weights = field_weights
        distances = []
        for k in range(2):
            distances.append([Distance(metric=COSINE)([stimuli[i][k], stimuli[j][k]]) * field_weights[k]
                              for i, j in pairs])
        distances = np.array(distances)
        distances = np.squeeze((distances[0] + distances[1]) / 2)

        retrieved = c(stimuli[0])
        np.all(retrieved==stimuli[0])
        assert np.allclose(c.distances_to_entries, [0, distances[0], distances[1]])

        retrieved = c(stimuli[1])
        np.all(retrieved==stimuli[1])
        assert np.allclose(c.distances_to_entries, [distances[0], 0, distances[2]])

        retrieved = c(stimuli[2])
        np.all(retrieved==stimuli[2])
        assert np.allclose(c.distances_to_entries, [distances[1], distances[2], 0])

        assert True


    # Test of ContentAddressableMemory without LLVM:
    def test_ContentAddressableMemory_with_initializer_and_equal_field_sizes(self):

        stimuli = {'A': [[1,2,3],[4,5,6]],
                   'B': [[8,9,10],[11,12,13]],
                   'C': [[1,2,3],[11,12,13]],
                   'D': [[1,2,3],[21,22,23]],
                   'E': [[9,8,4],[11,12,13]],
                   'F': [[10,10,30],[40,50,60]],
                   }

        c = ContentAddressableMemory(
            seed=2,
            initializer=np.array([stimuli['F'], stimuli['F']], dtype=object),
            distance_function=Distance(metric=COSINE),
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM
        )

        retrieved_labels=[]
        sorted_labels = sorted(stimuli.keys())
        for label in sorted_labels:
            retrieved = [i for i in c(stimuli[label])]
            # Get label of retrieved item
            retrieved_label = retrieve_label(retrieved, stimuli)
            # Get distances of retrieved entry to all other entries and assert it has the minimum distance
            distances = [Distance(metric=COSINE)([retrieved,stimuli[k]]) for k in sorted_labels]
            min_idx = distances.index(min(distances))
            assert retrieved_label == [sorted_labels[min_idx]]
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [['F'], ['A'], ['F'], ['C'], ['B'], ['F']]

        # Run again to test re-initialization and random retrieval
        c.reset(np.array([stimuli['A'], stimuli['F']]))
        retrieved_labels=[]
        for label in sorted(stimuli.keys()):
            retrieved = [i for i in c(stimuli[label])]
            retrieved_label = retrieve_label(retrieved, stimuli)
            # Get distances of retrieved entry to all other entries and assert it has the minimum distance
            distances = [Distance(metric=COSINE)([retrieved,stimuli[k]]) for k in sorted_labels]
            min_idx = distances.index(min(distances))
            assert retrieved_label == [sorted_labels[min_idx]]
            retrieved_labels.append(retrieved_label)
            Distance()([retrieved,stimuli['A']])
        assert retrieved_labels == [['A'], ['A'], ['F'], ['C'], ['B'], ['F']]

        # Test  restricting retrieval to only 1st field (which has duplicate values) and selecting for OLDEST
        c.distance_field_weights = [1,0]
        stim = 'C' # Has same 1st field as A (older) and D (newer)

        c.equidistant_entries_select = OLDEST  # Should return A
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = [k for k,v in stimuli.items()
                         if np.all([v[i] == retrieved[i] for i in range(len(v))])] or [None]
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST  # Should return D
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups and now disallowing them, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'
        text = "More than one entry matched cue"
        with pytest.warns(UserWarning, match=text):
            retrieved = c(stimuli[stim])
        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == [None]
        expected = np.array([[0,0,0],[0,0,0]])
        assert np.all(expected==retrieved)

    def test_ContentAddressableMemory_with_initializer_and_diff_field_sizes(self):

        stimuli = {'A': [[1.,2.,3.],[4.,5.,6.,7.]],
                   'B': [[8.,9.,10.],[11.,12.,13.,14.]],
                   'C': [[1.,2.,3.],[11.,12.,13.,14.]],
                   'D': [[1.,2.,3.],[21.,22.,23.,24.]],
                   'E': [[9.,8.,4.],[11.,12.,13.,14.]],
                   'F': [[10.,10.,30.],[40.,50.,60.,70.]],
                   }

        c = ContentAddressableMemory(
            initializer=np.array([stimuli['F'], stimuli['F']], dtype=object),
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM)

        # Run again to test re-initialization and random retrieval
        c.reset(np.array([stimuli['A'], stimuli['F']]))
        retrieved_labels=[]
        for key in sorted(stimuli.keys()):
            retrieved = c(stimuli[key])
            retrieved_label = retrieve_label(retrieved, stimuli)
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [['A'], ['A'], ['F'], ['C'], ['B'], ['F']]

        c.distance_field_weights = [1,0]
        stim = 'C'
        c.equidistant_entries_select = OLDEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label(retrieved, stimuli)
        retrieved_labels.append(retrieved_label)
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'

        text = r'More than one entry matched cue'
        with pytest.warns(UserWarning, match=text):
            retrieved = c(stimuli[stim])

        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == [None]
        expected = np.array([np.array([0,0,0]),np.array([0,0,0,0])])
        assert all(np.alltrue(x) for x in np.equal(expected,retrieved, dtype=object))

    def test_ContentAddressableMemory_without_initializer_and_equal_field_sizes(self):

        stimuli = {'A': [[1,2,3],[4,5,6]],
                   'B': [[8,9,10],[11,12,13]],
                   'C': [[1,2,3],[11,12,13]],
                   'D': [[1,2,3],[21,22,23]],
                   'E': [[9,8,4],[11,12,13]],
                   'F': [[10,10,30],[40,50,60]],
                   }

        c = ContentAddressableMemory(
            distance_function=Distance(metric=COSINE),
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM
        )

        retrieved_labels=[]
        sorted_labels = sorted(stimuli.keys())
        for label in sorted_labels:
            retrieved = [i for i in c(stimuli[label])]
            retrieved_label = retrieve_label(retrieved, stimuli)
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [[None], ['A'], ['A'], ['C'], ['B'], ['A']]

        stim = 'C'
        c.distance_field_weights = [1,0]
        c.equidistant_entries_select = OLDEST
        retrieved = [i for i in c.get_memory(stimuli[stim])]
        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST
        retrieved = [i for i in c.get_memory(stimuli[stim])]
        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'

        text = "More than one entry matched cue"
        with pytest.warns(UserWarning, match=text):
            retrieved = c.execute(stimuli[stim])

        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == [None]
        expected = np.array([np.array([0,0,0]),np.array([0,0,0])])
        assert all(np.alltrue(x) for x in np.equal(expected,retrieved, dtype=object))

    def test_ContentAddressableMemory_without_initializer_and_diff_field_sizes(self):

        stimuli = {'A': [[1,2,3],[4,5,6,7]],
                   'B': [[8,9,10],[11,12,13,14]],
                   'C': [[1,2,3],[11,12,13,14]],
                   'D': [[1,2,3],[21,22,23,24]],
                   'E': [[9,8,4],[11,12,13,14]],
                   'F': [[10,10,30],[40,50,60,70]],
                   }

        c = ContentAddressableMemory(
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM,
            distance_field_weights=[1,0]
        )

        retrieved_labels=[]
        for key in sorted(stimuli.keys()):
            retrieved = c(stimuli[key])
            retrieved_label = retrieve_label(retrieved, stimuli)
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [[None], ['A'], ['A'], ['C'], ['B'], ['D']]

        stim = 'C'
        c.equidistant_entries_select = OLDEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'

        text = "More than one entry matched cue"
        with pytest.warns(UserWarning, match=text):
            retrieved = c(stimuli[stim])

        retrieved_label = retrieve_label(retrieved, stimuli)
        assert retrieved_label == [None]
        expected = np.array([np.array([0,0,0]),np.array([0,0,0,0])])
        assert all(np.alltrue(x) for x in np.equal(expected,retrieved, dtype=object))

    def test_ContentAddressableMemory_with_duplicate_entry_in_initializer_warning(self):

        regexp = r'Attempt to initialize memory of ContentAddressableMemory with an entry \([[1 2 3]'
        with pytest.warns(UserWarning, match=regexp):
            c = ContentAddressableMemory(
                initializer=np.array([[[1,2,3], [4,5,6]],
                                      [[1,2,3], [7,8,9]]]),
                duplicate_entries_allowed=False,
                distance_field_weights=[1,0],
                equidistant_entries_select=RANDOM,
                retrieval_prob = 1.0
            )
        assert np.allclose(c.memory, np.array([[[1, 2, 3], [4, 5, 6]]]))

    def test_ContentAddressableMemory_add_and_delete_from_memory(self):

        c = ContentAddressableMemory(
            initializer=[[[1,2,3], [4,5,6]],
                         [[7,8,9], [10,11,12]]],
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM,
            retrieval_prob = 1.0,
            storage_prob = 1.0
        )
        c.add_to_memory([[[10,20,30],[40,50,60]],
                         [[11,21,31],[41,51,61]]])

        expected_memory = [[[ 1,  2,  3],[ 4,  5,  6]],
                           [[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]]]
        assert np.allclose(c.memory, expected_memory)

        c.delete_from_memory([[[1,2,3],[4,5,6]]])
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]]]
        assert np.allclose(c.memory, expected_memory)

        # Test adding and deleting a single memory
        c.add_to_memory([[1,2,3],[100,101,102]])
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]],
                           [[ 1,  2,  3],[100,101,102]]]
        assert np.allclose(c.memory, expected_memory)

        c.delete_from_memory([[1,2,3],[100,101,102]])
        expected_memory = [[[ 7,  8,  9],[10, 11, 12]],
                           [[10, 20, 30],[40, 50, 60]],
                           [[11, 21, 31],[41, 51, 61]]]
        assert np.allclose(c.memory, expected_memory)

        # Test adding memory with different size value
        with pytest.raises(FunctionError) as error_text:
            c.add_to_memory([[1,2,3],[100,101,102,103]])
        assert "Field 1 of entry ([array([1, 2, 3]) array([100, 101, 102, 103])]) has incorrect shape ((4,)) " \
               "for memory of 'ContentAddressableMemory Function-0';  should be: (3,)." in str(error_text.value)

        # Test adding memory in first field of np.ndarray with wrong size:
        with pytest.raises(FunctionError) as error_text:
            c.add_to_memory(np.array([[1,2],[200,201,202,203]], dtype=object))
        assert "Field 0 of entry ([array([1, 2]) array([200, 201, 202, 203])]) has incorrect shape ((2,)) " \
               "for memory of 'ContentAddressableMemory Function-0';  should be: (3,)." in str(error_text.value)

        # Test adding memory in second field of np.ndarray with wrong size:
        with pytest.raises(FunctionError) as error_text:
            c.add_to_memory(np.array([[1,2,3],[200,201,202,203]], dtype=object))
        assert "Field 1 of entry ([array([1, 2, 3]) array([200, 201, 202, 203])]) has incorrect shape ((4,)) " \
               "for memory of 'ContentAddressableMemory Function-0';  should be: (3,)." in str(error_text.value)

    def test_ContentAddressableMemory_overwrite_mode(self):

        c = ContentAddressableMemory(
                initializer=[[[1,2,3], [4,5,6]],
                             [[7,8,9], [10,11,12]]],
                distance_field_weights=[1,0],
                duplicate_entries_allowed=OVERWRITE,
                equidistant_entries_select=RANDOM,
                retrieval_prob = 1.0,
                storage_prob = 1.0
        )

        # Add new memory
        retreived = c([[10,11,12], [100,110,120]])
        assert np.allclose(list(retreived), [[7,8,9], [10,11,12]])
        expected_memory = [[[1,2,3], [4,5,6]],
                           [[7,8,9], [10,11,12]],
                           [[10,11,12], [100,110,120]]]
        assert np.allclose(c.memory, expected_memory)

        # Overwrite old memory
        retreived = c([[7,8,9], [200,201,202]])
        assert np.allclose(list(retreived), [[7,8,9], [10,11,12]])
        expected_memory = [[[1,2,3], [4,5,6]],
                           [[7,8,9], [200,201,202]],
                           [[10,11,12], [100,110,120]]]
        assert np.allclose(c.memory, expected_memory)

        # Allow entry duplicate of memory with
        c.duplicate_entries_allowed = True
        retreived = c([[7,8,9], [300,310,320]])
        assert np.allclose(list(retreived), [[7,8,9],[200,201,202]])
        expected_memory = [[[1,2,3],[4,5,6]],
                           [[7,8,9], [200,201,202]],
                           [[10,11,12], [100,110,120]],
                           [[7,8,9], [300,310,320]]]
        assert np.allclose(c.memory, expected_memory)

        # Attempt to overwrite with two matches should generate error
        c.duplicate_entries_allowed = OVERWRITE
        with pytest.raises(FunctionError) as error_text:
            c.execute([[7,8,9], [100,110,120]])
        assert ('Attempt to store item' in str(error_text.value)
                and 'with \'duplicate_entries_allowed\'=\'OVERWRITE\'' in str(error_text.value))
        with pytest.raises(FunctionError) as error_text:
            c.execute([[7,8,9], [300,310,320]])
        assert ('Attempt to store item' in str(error_text.value)
                and 'with \'duplicate_entries_allowed\'=\'OVERWRITE\'' in str(error_text.value))

    def test_ContentAddressableMemory_max_entries(self):

        c = ContentAddressableMemory(
                initializer=[[[1,2,3], [4,5,6]],
                             [[7,8,9], [10,11,12]],
                             [[1,2,3], [100,101,102]]],
                duplicate_entries_allowed=True,
                equidistant_entries_select=RANDOM,
                retrieval_prob = 1.0,
                storage_prob = 1.0,
                max_entries = 4
        )
        c.add_to_memory([[[10,20,30],[40,50,60]],
                        [[11,21,31],[41,51,61]],
                        [[12,22,32],[42,52,62]]])
        expected_memory = [[[1,2,3], [100,101,102]],
                           [[10,20,30],[40,50,60]],
                           [[11,21,31],[41,51,61]],
                           [[12,22,32],[42,52,62]]]
        assert np.allclose(c.memory, expected_memory)

    def test_ContentAddressableMemory_errors(self):

        # Test constructor

        with pytest.raises(ParameterError) as error_text:
            clear_registry(FunctionRegistry)
            c = ContentAddressableMemory(retrieval_prob=32)
        assert 'Value (32) assigned to parameter \'retrieval_prob\' of (ContentAddressableMemory ' \
               'ContentAddressableMemory Function-0).parameters is not valid: ' \
               'retrieval_prob must be a float in the interval [0,1].' in str(error_text.value)

        with pytest.raises(ParameterError) as error_text:
            clear_registry(FunctionRegistry)
            c = ContentAddressableMemory(storage_prob=-1)
        assert 'Value (-1) assigned to parameter \'storage_prob\' of (ContentAddressableMemory ' \
               'ContentAddressableMemory Function-0).parameters is not valid: ' \
               'storage_prob must be a float in the interval [0,1].' in str(error_text.value)

        with pytest.raises(ParameterError) as error_text:
            clear_registry(FunctionRegistry)
            c = ContentAddressableMemory(equidistant_entries_select='HELLO')
        assert "parameters is not valid: 'equidistant_entries_select' must be random or oldest or newest."\
               in str(error_text.value)

        with pytest.raises(ParameterError) as error_text:
            clear_registry(FunctionRegistry)
            c = ContentAddressableMemory(duplicate_entries_allowed='HELLO')
        assert "parameters is not valid: 'duplicate_entries_allowed' must be a bool or 'OVERWRITE'."\
               in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            clear_registry(FunctionRegistry)
            c = ContentAddressableMemory(distance_function=LinearCombination)
        assert "Value returned by 'distance_function' (LinearCombination) specified for ContentAddressableMemory " \
               "must return a scalar if 'distance_field_weights' is not specified or is homogenous " \
               "(i.e., all elements are the same." in str(error_text.value)

        clear_registry(FunctionRegistry)
        c = ContentAddressableMemory()
        c([[1,2,3],[4,5,6]])

        # Test parameter and value assignments

        with pytest.raises(ParameterError) as error_text:
            clear_registry(FunctionRegistry)
            c.parameters.retrieval_prob = 2
        assert "Value (2) assigned to parameter 'retrieval_prob' of (ContentAddressableMemory " \
               "ContentAddressableMemory Function-0).parameters is not valid: retrieval_prob " \
               "must be a float in the interval [0,1]." in str(error_text.value)

        with pytest.raises(ParameterError) as error_text:
            clear_registry(FunctionRegistry)
            c = ContentAddressableMemory(retrieval_prob=32)
        assert "Value (32) assigned to parameter 'retrieval_prob' of (ContentAddressableMemory " \
               "ContentAddressableMemory Function-0).parameters is not valid: retrieval_prob must " \
               "be a float in the interval [0,1]." in str(error_text.value)

        with pytest.raises(ParameterError) as error_text:
            clear_registry(FunctionRegistry)
            c = ContentAddressableMemory(storage_prob=-1)
        assert "Value (-1) assigned to parameter 'storage_prob' of (ContentAddressableMemory " \
               "ContentAddressableMemory Function-0).parameters is not valid: storage_prob must " \
               "be a float in the interval [0,1]." in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            c([[[1,2,3],[4,5,6]]])
        assert 'Attempt to store and/or retrieve an entry in ContentAddressableMemory ([[[1 2 3]\n  [4 5 6]]]) that ' \
               'has more than 2 dimensions (3);  try flattening innermost ones.' in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            c([[1,2,3],[4,5],[6,7]])
        assert ('Attempt to store and/or retrieve entry in ContentAddressableMemory' in str(error_text.value)
                and 'that has an incorrect number of fields' in str(error_text.value))

        with pytest.raises(FunctionError) as error_text:
            c([[1,2,3],[4,5,6,7]])
        assert "Field 1 of entry ([array([1, 2, 3]) array([4, 5, 6, 7])]) has incorrect shape ((4,)) for memory of " \
               "'ContentAddressableMemory Function-0';  should be: (3,)." in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            # c = ContentAddressableMemory()
            # c = ContentAddressableMemory(equidistant_entries_select='HELLO')
            c.duplicate_entries_allowed = True
            c([[1,2,3],[4,5,6]])
            # c.equidistant_entries_select = 'HELLO'
            # c([[1., 2., 3.],  [4.,5.,6.]])
            c.duplicate_entries_allowed = OVERWRITE
            c([[1,2,3],[4,5,6]])
        assert "Attempt to store item ([[1. 2. 3.]\n [4. 5. 6.]]) in ContentAddressableMemory Function-0 with " \
               "'duplicate_entries_allowed'='OVERWRITE' when there is more than one matching entry in its memory; " \
               "'duplicate_entries_allowed' may have previously been set to 'True'" in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            clear_registry(FunctionRegistry)
            c.add_to_memory([[[1,2,3],[4,5,6]],
                             [[8,9,10],[11,12,13,14]]])
        assert "Field 1 of entry ([list([8, 9, 10]) list([11, 12, 13, 14])]) has incorrect shape ((4,)) " \
               "for memory of 'ContentAddressableMemory Function-0';  should be: (3,)." in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            clear_registry(FunctionRegistry)
            c.add_to_memory([1,2,3])
        assert 'Attempt to store and/or retrieve entry in ContentAddressableMemory ([1 2 3]) ' \
               'that has an incorrect number of fields (3; should be 2).' in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            clear_registry(FunctionRegistry)
            c.add_to_memory([[[1]]])
        assert 'Attempt to store and/or retrieve entry in ContentAddressableMemory ([[1]]) ' \
               'that has an incorrect number of fields (1; should be 2).' in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            clear_registry(FunctionRegistry)
            c.add_to_memory(1)
        assert "The 'memories' arg for add_to_memory method of must be a list or array containing 1d or 2d arrays " \
               "(was scalar)." in str(error_text.value)

        with pytest.raises(FunctionError) as error_text:
            clear_registry(FunctionRegistry)
            c.add_to_memory([[[[1,2]]]])
        assert "The 'memories' arg for add_to_memory method of must be a list or array containing 1d or 2d arrays " \
               "(was 4d)." in str(error_text.value)

    @pytest.mark.parametrize(
        'param_name',
        [
            'distance_function',
            'selection_function',
        ]
    )
    def test_ContentAddressableMemory_unique_functions(self, param_name):
        a = ContentAddressableMemory()
        b = ContentAddressableMemory()

        assert (
            getattr(a.parameters, param_name).get()
            is not getattr(b.parameters, param_name).get()
        )

        assert (
            getattr(a.defaults, param_name)
            is not getattr(b.defaults, param_name)
        )

    #

        # (
        #     "ContentAddressableMemory Initializer Ndimensional Fields",
        #     # FIX:
        #     # OTHER DATA
        #     [[[1],[[2],[3,4]],[4]],[[1],[[2],[3,4]],[4]]]
        #     [[[1,2,3],[4]],[[1],[[2],[3,4]],[4]]]
        # ),
        # FIX: THESE SHOULD BE IN MemoryFunctions TEST for ContentAddressableMemory
        # (
        #     "ContentAddressableMemory Random Retrieval",
        #     # FIX:
        #     # OTHER DATA
        # ),
        # (
        #     "ContentAddressableMemory Random Storage",
        #     # FIX:
        #     # OTHER DATA
        # ),
        # (
        #     "ContentAddressableMemory Random Retrieval-Storage",
        #     # FIX:
        #     # OTHER DATA
        # ),
        # (
        #     "ContentAddressableMemory Weighted Retrieval",
        #     # FIX:
        #     # OTHER DATA
        # ),
        # (
        #     "ContentAddressableMemory Duplicates Retrieval",
        #     # FIX:
        #     # OTHER DATA
        # ),


        # # Initializer with >2d regular array
        # with pytest.raises(FunctionError) as error_text:
        #     f = ContentAddressableMemory(initializer=[[[[1,0],[1,0],[1,0]], [[1,0],[1,0],[1,0]], [[1,0],[1,0],[1,0]]],
        #                                               [[[0,1],[0,1],[0,1]], [[0,1],[0,0],[1,0]], [[0,1],[0,1],[0,1]]]])
        #     em = EpisodicMemoryMechanism(size = [1,1,1], function=f)
        #     em.execute([[[0,1],[0,1],[0,1]], [[0,1],[0,0],[1,0]], [[0,1],[0,1],[0,1]]])
        # assert 'Attempt to store and/or retrieve an entry in ContentAddressableMemory that has more than 2 dimensions (' \
        #        '3);  try flattening innermost ones.' in str(error_text.value)
        #
        # # Initializer with >2d ragged array
        # with pytest.raises(FunctionError) as error_text:
        #     f = ContentAddressableMemory(initializer=[ [[1,2,3], [4]], [[1,2,3], [[1],[4]]] ])
        #     em = EpisodicMemoryMechanism(size = [1,1,1], function=f)
        #     em.execute([[[0,1],[0,1],[0,1]], [[0,1],[0,0],[1,0]], [[0,1],[0,1],[0,1]]])
        # assert 'Attempt to store and/or retrieve an entry in ContentAddressableMemory that has more than 2 dimensions (' \
        #        '3);  try flattening innermost ones.' in str(error_text.value)

        # [ [[1,2,3], [4]], [[1,2,3], [[1],[4]]] ]

#endregion
