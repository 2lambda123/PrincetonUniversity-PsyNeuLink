import logging
import timeit as timeit
import os
import numpy as np

import pytest

import psyneulink as pnl

from psyneulink.core.components.functions.nonstateful.transferfunctions import Logistic
from psyneulink.core.components.functions.nonstateful.learningfunctions import BackPropagation
from psyneulink.core.compositions.composition import Composition
from psyneulink.core.globals import Context
from psyneulink.core.globals.keywords import TRAINING_SET, Loss, CONTROL
from psyneulink.core.components.mechanisms.mechanism import Mechanism
from psyneulink.core.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.core.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.library.compositions.emcomposition import EMComposition, EMCompositionError
from psyneulink.core.compositions.report import ReportOutput

module_seed = 0
np.random.seed(0)

logger = logging.getLogger(__name__)


# All tests are set to run. If you need to skip certain tests,
# see http://doc.pytest.org/en/latest/skipping.html

# Unit tests for functions of EMComposition class that are new (not in Composition)
# or override functions in Composition

def _single_learn_results(composition, *args, **kwargs):
    composition.learn(*args, **kwargs)
    return composition.learning_results

@pytest.mark.pytorch
@pytest.mark.acconstructor
class TestACConstructor:

    def test_two_calls_no_args(self):
        comp = EMComposition()
        comp_2 = EMComposition()
        assert isinstance(comp, EMComposition)
        assert isinstance(comp_2, EMComposition)

    def test_pytorch_representation(self):
        comp = EMComposition()
        assert comp.pytorch_representation is None

    def test_report_prefs(self):
        comp = EMComposition()
        assert comp.input_CIM.reportOutputPref == ReportOutput.OFF
        assert comp.output_CIM.reportOutputPref == ReportOutput.OFF

# memory_template - NUMBER OF ENTRIES AND FORMAT:
# 1) single entry
#    √ memory_template is tuple - 0
#    √ memory_template is list with zeros and same lengths - 1, 2.x
#    √ memory_template is list with zeros and different lengths - 3,4,6,7,11
#    √ memory_template is list with non-zeros and same lengths - 9
#    √ memory_template is np.ndarray with zeros and different lengths - 9.1, 10
#    - memory_template is np.ndarray with zeros and same lengths - FIX
#    - memory_template is np.ndarray with zeros and different lengths FIX
# 2) multiple entries
#    √ memory_template is partial entries with zeros and different lengths
#    √ memory_template is partial entries with non-zeros and different lengths - 13,14,15,16
#    - memory_template is full entries with zeros and different lengths
#    - memory_template is full entries with non-zeros and different lengths - 17

# memory_fill
# √ single value - 10-17
# √ tuple of values (random) 0.2

# field_weights
# √ single value - 5.x
# √ multiple values all same - 6,7,12-14
# √ multiple values different - 8-11, 15-17

# TODO:
# field names

# normalize_memory - True/False

# Execution:
# retrieval:
# 1) concatenation - True/False
# 2) normalization - True/False
# 3) field_weights - same / different
# softmax_gain - None/float/function
# memory_decay - True/False
# storage_probability - None, float
# learn_weights - True/False

    # FIX: ADD WARNING TESTS
    # FIX: ADD ERROR TESTS
    test_data = [
        # ------------------ SPECS ---------------------------------------------   ------- EXPECTED -------------------
        #   memory_template       memory_fill   field_wts cncat_ky nmlze sm_gain   repeat  #fields #keys #vals  concat
        (0,    (2,3),                  None,      None,    None,    None,  None,    False,    2,     1,   1,    False,),
        (0.1,  (2,3),                   .1,       None,    None,    None,  None,    False,    2,     1,   1,    False,),
        (0.2,  (2,3),                 (0,.1),     None,    None,    None,  None,    False,    2,     1,   1,    False,),
        (1,    [[0,0],[0,0]],          None,      None,    None,    None,  None,    False,    2,     1,   1,    False,),
        (1.1,  [[0,0],[0,0]],          None,      [1,1],   None,    None,  None,    False,    2,     2,   0,    True,),
        (2,    [[0,0],[0,0],[0,0]],    None,      None,    None,    None,  None,    False,    3,     2,   1,    True,),
        (2.1,  [[0,0],[0,0],[0,0]],    None,      None,    None,    None,   1.5,    False,    3,     2,   1,    True,),
        (2.2,  [[0,0],[0,0],[0,0]],    None,      None,    None,    None, CONTROL,  False,    3,     2,   1,    True,),
        (3,    [[0,0,0],[0,0]],        None,      None,    None,    None,  None,    False,    2,     1,   1,    False,),
        (4,    [[0,0,0],[0],[0,0]],    None,      None,    None,    None,  None,    False,    3,     2,   1,    True,),
        (5,    [[0,0],[0,0],[0,0]],    None,       1,      None,    None,  None,    False,    3,     3,   0,    True,),
        (5.1,  [[0,0],[0,0],[0,0]],    None,       1,      None,    None,   0.1,    False,    3,     3,   0,    True,),
        (5.2,  [[0,0],[0,0],[0,0]],    None,       1,      None,    None, CONTROL,  False,    3,     3,   0,    True,),
        (6,    [[0,0,0],[0],[0,0]],    None,    [1,1,1],   None,    None,  None,    False,    3,     3,   0,    True,),
        (7,    [[0,0,0],[0],[0,0]],    None,    [1,1,1],   False,   None,  None,    False,    3,     3,   0,    False,),
        (7.1,  [[0,0,0],[0],[0,0]],    None,    [1,1,1],   True ,   False, None,    False,    3,     3,   0,    False,),
        (8,    [[0,0],[0,0],[0,0]],    None,    [1,2,0],   None,    None,  None,    False,    3,     2,   1,    False,),
        (8.1,  [[0,0],[0,0],[0,0]],    None,    [1,2,0],   True,    None,  None,    False,    3,     2,   1,    False,),
        (9,    [[0,1],[0,0],[0,0]],    None,    [1,2,0],   None,    None,  None,    [0,1],    3,     2,   1,    False,),
        (9.1,  [[0,1],[0,0,0],[0,0]],  None,    [1,2,0],   None,    None,  None,    [0,1],    3,     2,   1,    False,),
        (10,   [[0,1],[0,0,0],[0,0]],    .1,    [1,2,0],   None,    None,  None,    [0,1],    3,     2,   1,    False,),
        (11,   [[0,0],[0,0,0],[0,0]],    .1,    [1,2,0],   None,    None,  None,    False,    3,     2,   1,    False,),
        (12,   [[[0,0],[0,0],[0,0]],   # two entries specified, fields all same length, both entries have all 0's
                [[0,0],[0,0],[0,0]]],    .1,    [1,1,1],   None,    None,  None,      2,      3,     3,   0,    True,),
        (12.1, [[[0,0],[0,0,0],[0,0]], # two entries specified, fields have different lenghts, entries all have 0's
                [[0,0],[0,0,0],[0,0]]],  .1,    [1,1,0],   None,    None,  None,      2,      3,     2,   1,    True,),
        (12.2,  [[[0,0],[0,0,0],[0,0]], # two entries specified, first has 0's
                [[0,2],[0,0,0],[0,0]]],  .1,    [1,1,0],   None,    None,  None,      2,      3,     2,   1,    True,),
        (12.3, [[[0,1],[0,0,0],[0,0]], # two entries specified, fields have same weights
                [[0,2],[0,0,0],[0,0]]],  .1,    [1,1,0],   None,    None,  None,      2,      3,     2,   1,    True,),
        (13,   [[[0,1],[0,0,0],[0,0]], # two entries specified, fields have same weights, but conccatenate_keys is False
                [[0,2],[0,0,0],[0,0]]],  .1,    [1,1,0],   False,   None,  None,      2,      3,     2,   1,    False),
        (14,   [[[0,1],[0,0,0],[0,0]], # two entries specified, all fields are keys
                [[0,2],[0,0,0],[0,0]]],  .1,    [1,1,1],   None,    None,  None,      2,      3,     3,   0,    True),
        (15,   [[[0,1],[0,0,0],[0,0]], # two entries specified; fields have different weights, constant memory_fill
                [[0,2],[0,0,0],[0,0]]],  .1,    [1,2,0],   None,    None,  None,      2,      3,     2,   1,    False),
        (15.1, [[[0,1],[0,0,0],[0,0]], # two entries specified; fields have different weights, random memory_fill
                [[0,2],[0,0,0],[0,0]]], (0,.1), [1,2,0],   None,    None,  None,      2,      3,     2,   1,    False),
        (16,   [[[0,1],[0,0,0],[0,0]], # three enrtries specified
                [[0,2],[0,0,0],[0,0]],
                [[0,3],[0,0,0],[0,0]]],  .1,     [1,2,0],   None,    None,  None,     3,      3,     2,   1,    False),
        (17,   [[[0,1],[0,0,0],[0,0]], # all four enrtries allowed by memory_capacity specified
                [[0,2],[0,0,0],[0,0]],
                [[0,3],[0,0,0],[0,0]],
                [[0,4],[0,0,0],[0,0]]],  .1,     [1,2,0],   None,    None,  None,      4,      3,     2,   1,    False),
    ]
    args_names = "test_num, memory_template, memory_fill, field_weights, concatenate_keys, normalize_memories, " \
                 "softmax_gain, repeat, num_fields, num_keys, num_values, concatenate_node"
    @pytest.mark.parametrize(args_names,
                             test_data,
                             ids=[x[0] for x in test_data]
                             )
    @pytest.mark.benchmark
    def test_structure(self,
                       test_num,
                       memory_template,
                       memory_fill,
                       field_weights,
                       concatenate_keys,
                       normalize_memories,
                       softmax_gain,
                       repeat,
                       num_fields,
                       num_keys,
                       num_values,
                       concatenate_node,
                       benchmark):
        """Note: weight matrices used for memory are validated by using em.memory, since its getter uses thos matrices
        """
        memory_capacity = 4
        params = {'memory_template': memory_template,
                  'memory_capacity': memory_capacity,
                  }
        # Add explicit argument specifications (to avoid forcing to None in constructor)
        if memory_fill is not None:
            params.update({'memory_fill': memory_fill})
        if field_weights is not None:
            params.update({'field_weights': field_weights})
        if concatenate_keys is not None:
            params.update({'concatenate_keys': concatenate_keys})
        if normalize_memories is not None:
            params.update({'normalize_memories': normalize_memories})
        if softmax_gain is not None:
            params.update({'softmax_gain': softmax_gain})

        em = EMComposition(**params)

        # Validate basic structure
        assert len(em.memory) == memory_capacity
        assert len(em.memory[0]) == num_fields
        assert len(em.field_weights) == num_fields
        assert len(em.field_weights) == num_keys + num_values

        # Validate memory_template
        # If tuple spec, ensure that all fields have the same length
        if isinstance(memory_template, tuple):
            assert all(len(em.memory[j][i]) == memory_template[1]
                       for i in range(num_fields) for j in range(memory_capacity))
        # If list or array spec, ensure that all fields have the same length as those in the specified memory_template
        else:
            # memory_template has all zeros, so all fields should be empty
            if not repeat:
                assert all(len(em.memory[j][i]) == len(memory_template[i])
                       for i in range(num_fields) for j in range(memory_capacity))
            # memory_template is a single specified entry:
            elif repeat and isinstance(repeat, list):
                assert all(len(em.memory[k][j]) == len(memory_template[j])
                           for j in range(num_fields) for k in range(memory_capacity))
            # memory_template is multiple entries, so need outer dimension on em.memory for test
            else:
                # ensure all specified entries have correct number of fields
                assert all(len(em.memory[k][j]) == len(memory_template[k][j])
                       for j in range(num_fields) for k in range(repeat))
                # ensure all repeated entries have correct number of fields
                assert all(len(em.memory[k][j]) == len(memory_template[0][j])
                       for j in range(num_fields) for k in range(repeat,memory_capacity))

        # Validate node structure
        assert len(em.key_input_nodes) == num_keys
        assert len(em.value_input_nodes) == num_values
        assert isinstance(em.concatenate_keys_node, Mechanism) == concatenate_node
        if em.concatenate_keys:
            assert em.retrieval_gating_nodes == []
            assert bool(softmax_gain in {None, CONTROL}) == bool(len(em.softmax_control_nodes))
        else:
            assert len(em.retrieval_gating_nodes) == num_keys
            if softmax_gain in {None, CONTROL}:
                assert len(em.softmax_control_nodes) == num_keys
            else:
                assert em.softmax_control_nodes == []
        assert len(em.retrieval_nodes) == num_fields

        def test_memory_fill(start, memory_fill):
            memory_fill = memory_fill or 0
            for k in range(start, memory_capacity):
                for j in range(num_fields):
                    for i in range(len(em.memory[k][j])):
                        elem = em.memory[k][j][i]
                        # Random fill
                        if isinstance(memory_fill, tuple):
                            assert isinstance(elem, float) and (elem >= memory_fill[0] and elem <= memory_fill[1])
                        # Constant fill
                        else:
                            assert elem == memory_fill

        # Validate specified entries and memory_memory_fill
        # If memory_template is all zeros, ensure that all fields are filled with zeros or memory_fill
        if not repeat:
            test_memory_fill(start=0, memory_fill=memory_fill)

        if isinstance(repeat,list):  # Single entry specification and repeat = item repeated for all entries
            for j in range(num_fields):
                for i in range(len(em.memory[0][j])):
                    np.testing.assert_allclose(em.memory[0][j][i], em.memory[-1][j][i])
            np.testing.assert_allclose(em.memory[-1][0], np.array(repeat,dtype=object).astype(float))
        elif repeat and repeat < memory_capacity:  # Multi-entry specification and repeat = number entries; remainder
            test_memory_fill(start=repeat, memory_fill=memory_fill)


class TestExecution:

    # TEST:
    # 0: 3 entries that fill memory; no decay, one key, high softmax gain, no storage, inputs has only key (no value)
    # 1: 3 entries that fill memory; no decay, one key, high softmax gain, no storage, inputs has key & value
    # 2:   same as 1 but different value (that should be ignored)
    # 3:   same as 2 but has extra entry filled with random values (which changes retrieval)
    # 4:   same as 3 but uses both fields as keys (no values)
    # 5:   same as 4 but no concatentation of keys
    # 6:   same as 5, but different field_weights
    # 7:  EFFECTS OF VALUE ON STORAGE AND FUTURE RETRIEVAL

    test_data = [
        # ---------------------------------------- SPECS -----------------------------------  ----- EXPECTED ---------
        #   memory_template         mem    mem  mem  fld   concat  nlz  sm   str    inputs        expected_retrieval
        #                           fill   cap decay wts    keys       gain  prob
        # ----------------------------------------------------------------------------------  ------------------------
        # (0, [[[1,2,3],[4,5,6]],
        #      [[1,2,5],[4,5,8]],
        #      [[1,2,10],[4,5,10]]],  None,   3,  0, [1,0],  None, None,  100,  0, [[[1, 2, 3]]], [[1., 2., 3.16585899],
        #                                                                                          [4., 5., 6.16540637]]),
        # (1, [[[1,2,3],[4,5,6]],
        #      [[1,2,5],[4,5,8]],
        #      [[1,2,10],[4,5,10]]],  None,   3,  0, [1,0],  None, None,  100,  0, [[[1, 2, 3]],
        #                                                                           [[4, 5, 6]]], [[1., 2., 3.16585899],
        #                                                                                          [4., 5., 6.16540637]]),
        # (2, [[[1,2,3],[4,5,6]],
        #      [[1,2,5],[4,5,8]],
        #      [[1,2,10],[4,5,10]]],  None,   3,  0, [1,0],  None, None,  100,  0, [[[1, 2, 3]],
        #                                                                           [[4, 5, 8]]], [[1., 2., 3.16585899],
        #                                                                                          [4., 5., 6.16540637]]),
        # (3, [[[1,2,3],[4,5,6]],
        #      [[1,2,5],[4,5,8]],
        #      [[1,2,10],[4,5,10]]], (0,.01), 4,  0, [1,0],  None, None,  100,  0, [[[1, 2, 3]],
        #                                                                            [[4, 5, 8]]], [[0.99998628,
        #                                                                                            1.99997247,
        #                                                                                            3.1658154 ],
        #                                                                                           [3.99994492,
        #                                                                                            4.99993115,
        #                                                                                            6.16532141]]),
        (4, [[[1,2,3],[4,5,6]],
             [[1,2,5],[4,5,8]],
             [[1,2,10],[4,5,10]]], (0,.01), 4,  0, [1,1],  None, None,  100,  0, [[[1, 2, 4]],
                                                                                   [[4, 5, 8]]], [[0.99999932,
                                                                                                   1.99999864,
                                                                                                   4.34651032],
                                                                                                  [3.99999727,
                                                                                                   4.99999659,
                                                                                                   7.33742455]]),
        (5, [[[1,2,3],[4,5,6]],
             [[1,2,5],[4,5,8]],
             [[1,2,10],[4,5,10]]], (0,.01), 4,  0, [1,1],  False, None,  100,  0, [[[1, 2, 3]],
                                                                                   [[4, 5, 6]]], [[0.99998628,
                                                                                                   1.99997247,
                                                                                                   3.1658154 ],
                                                                                                  [3.99994492,
                                                                                                   4.99993115,
                                                                                                   6.16532141]]),
    ]

    args_names = "test_num, memory_template, memory_fill, memory_capacity, memory_decay, field_weights, " \
                 "concatenate_keys, normalize_memories, softmax_gain, storage_prob, inputs, expected_retrieval"
    @pytest.mark.parametrize(args_names,
                             test_data,
                             ids=[x[0] for x in test_data]
                             )
    @pytest.mark.benchmark
    def test_simple_retrieval_without_storage_or_decay(self,
                                                       test_num,
                                                       memory_template,
                                                       memory_fill,
                                                       memory_capacity,
                                                       memory_decay,
                                                       field_weights,
                                                       concatenate_keys,
                                                       normalize_memories,
                                                       softmax_gain,
                                                       storage_prob,
                                                       inputs,
                                                       expected_retrieval):

        em = EMComposition(memory_template=memory_template,
                           memory_capacity=memory_capacity,
                           memory_fill=memory_fill,
                           field_weights=field_weights,
                           memory_decay=memory_decay,
                           softmax_gain=softmax_gain,
                           storage_prob=storage_prob,
                           # seed=module_seed,
                           )

        input_nodes = em.key_input_nodes + em.value_input_nodes
        inputs = {input_nodes[i]:inputs[i] for i in range(len(inputs))}

        if len(np.array(em.memory_template)) == len(np.array(memory_template)):
            np.testing.assert_equal(np.array(em.memory_template), np.array(memory_template))
        retrieved = em.run(inputs=inputs)
        np.testing.assert_allclose(retrieved, expected_retrieval)

        # # Test with 0 as field weight
        # em.field_weights=[1,0]
        # retrieved = c([[1, 2, 3], [4, 5, 10]])
        # np.testing.assert_equal(retrieved, [[1, 2, 3], [4, 5, 6]])
        #
        # em.distance_field_weights=[0,1]
        # retrieved = c([[1, 2, 3], [4, 5, 10]])
        # np.testing.assert_equal(retrieved, [[1, 2, 10], [4, 5, 10]])
        #
        # # Test with None as field weight
        # em.distance_field_weights=[None,1]
        # retrieved = c([[1, 2, 3], [4, 5, 10]])
        # np.testing.assert_equal(retrieved, [[1, 2, 10], [4, 5, 10]])
        #
        # em.distance_field_weights=[1, None]
        # retrieved = c([[1, 2, 3], [4, 5, 10]])
        # np.testing.assert_equal(retrieved, [[1, 2, 3], [4, 5, 6]])
        #
        # # Test with [] as field weight
        # em.distance_field_weights=[[],1]
        # retrieved = c([[1, 2, 3], [4, 5, 10]])
        # np.testing.assert_equal(retrieved, [[1, 2, 10], [4, 5, 10]])
        #
        # em.distance_field_weights=[1, []]
        # retrieved = c([[1, 2, 3], [4, 5, 10]])
        # np.testing.assert_equal(retrieved, [[1, 2, 3], [4, 5, 6]])

    @pytest.mark.skip(reason="test not yet fully implemented")
    def test_parametric_distances(self):

        stimuli = np.array([[[1,2,3],[4,5,6]],
                            [[7,8,9],[10,11,12]],
                            [[13,14,15],[16,17,18]]])

        c = EMComposition(
            initializer=stimuli,
            storage_prob=0,
            distance_function=Distance(metric=COSINE),
            seed=module_seed,
        )

        pairs = list(combinations(range(0,3),2))
        # Distances between all stimuli
        distances = [Distance(metric=COSINE)([stimuli[i],stimuli[j]]) for i, j in pairs]
        c_distances = []
        # for i,j in pairs:

        # Test distances with evenly weighted fields
        retrieved = c(stimuli[0])
        np.testing.assert_equal(retrieved, stimuli[0])
        np.testing.assert_allclose(c.distances_to_entries, [0, distances[0], distances[1]], rtol=1e-5, atol=1e-8)

        retrieved = c(stimuli[1])
        np.testing.assert_equal(retrieved, stimuli[1])
        np.testing.assert_allclose(c.distances_to_entries, [distances[0], 0, distances[2]], rtol=1e-5, atol=1e-8)

        retrieved = c(stimuli[2])
        np.testing.assert_equal(retrieved, stimuli[2])
        np.testing.assert_allclose(c.distances_to_entries, [distances[1], distances[2], 0], rtol=1e-5, atol=1e-8)

        # Test distances using distance_field_weights
        field_weights = [np.array([[1],[0]]), np.array([[0],[1]])]
        for fw in field_weights:
            c.distance_field_weights = fw
            distances = []
            for k in range(2):
                if fw[k]:
                    distances.append([Distance(metric=COSINE)([stimuli[i][k], stimuli[j][k]]) * fw[k]
                                      for i, j in pairs])
            distances = np.array(distances)
            distances = np.squeeze(np.sum(distances, axis=0) / len([f for f in fw if f]))

            retrieved = c(stimuli[0])
            np.testing.assert_equal(retrieved, stimuli[0])
            np.testing.assert_allclose(c.distances_to_entries, [0, distances[0], distances[1]], rtol=1e-5, atol=1e-8)

            retrieved = c(stimuli[1])
            np.testing.assert_equal(retrieved, stimuli[1])
            np.testing.assert_allclose(c.distances_to_entries, [distances[0], 0, distances[2]], rtol=1e-5, atol=1e-8)

            retrieved = c(stimuli[2])
            np.testing.assert_equal(retrieved, stimuli[2])
            np.testing.assert_allclose(c.distances_to_entries, [distances[1], distances[2], 0], rtol=1e-5, atol=1e-8)

        # Test distances_by_fields
        c.distance_field_weights=[1,1]
        stim = [[8,9,10],[11,12,13]]
        retrieved = c(stim)
        np.testing.assert_equal(retrieved, [[7, 8, 9], [10, 11, 12]])
        distances_by_field = [Distance(metric=COSINE)([retrieved[i], stim[i]]) for i in range(2)]
        np.testing.assert_equal(c.distances_by_field, distances_by_field)

    # Test of EMComposition without LLVM:
    @pytest.mark.skip(reason="test not yet fully implemented")
    def test_with_initializer_and_equal_field_sizes(self):

        stimuli = {'A': [[1,2,3],[4,5,6]],
                   'B': [[8,9,10],[11,12,13]],
                   'C': [[1,2,3],[11,12,13]],
                   'D': [[1,2,3],[21,22,23]],
                   'E': [[9,8,4],[11,12,13]],
                   'F': [[10,10,30],[40,50,60]],
                   }

        c = EMComposition(
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
            retrieved_label = retrieve_label_helper(retrieved, stimuli)
            # Get distances of retrieved entry to all other entries and assert it has the minimum distance
            distances = [Distance(metric=COSINE)([retrieved,stimuli[k]]) for k in sorted_labels]
            min_idx = distances.index(min(distances))
            assert retrieved_label == [sorted_labels[min_idx]]
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [['F'], ['A'], ['F'], ['C'], ['B'], ['F']]

        # Run again to test re-initialization and random retrieval
        c.reset(np.array([stimuli['A'], stimuli['F']], dtype=object))
        retrieved_labels=[]
        for label in sorted(stimuli.keys()):
            retrieved = [i for i in c(stimuli[label])]
            retrieved_label = retrieve_label_helper(retrieved, stimuli)
            # Get distances of retrieved entry to all other entries and assert it has the minimum distance
            distances = [Distance(metric=COSINE)([retrieved,stimuli[k]]) for k in sorted_labels]
            min_idx = distances.index(min(distances))
            assert retrieved_label == [sorted_labels[min_idx]]
            retrieved_labels.append(retrieved_label)
            Distance(metric=COSINE)([retrieved,stimuli['A']])
        assert retrieved_labels == [['A'], ['A'], ['F'], ['C'], ['B'], ['F']]

        # Test  restricting retrieval to only 1st field (which has duplicate values) and selecting for OLDEST
        c.distance_field_weights = [1,0]
        stim = 'C' # Has same 1st field as A (older) and D (newer)

        c.equidistant_entries_select = OLDEST  # Should return A
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = [k for k, v in stimuli.items()
                           if np.all([vi == retrieved[i] for i, vi in enumerate(v)])] or [None]
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST  # Should return D
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups and now disallowing them, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'
        text = "More than one entry matched cue"
        with pytest.warns(UserWarning, match=text):
            retrieved = c(stimuli[stim])
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == [None]
        np.testing.assert_equal(retrieved, [[0, 0, 0], [0, 0, 0]])

    @pytest.mark.skip(reason="test not yet fully implemented")
    def test_with_initializer_and_diff_field_sizes(self):

        stimuli = {'A': np.array([[1.,2.,3.],[4.,5.,6.,7.]], dtype=object),
                   'B': np.array([[8.,9.,10.],[11.,12.,13.,14.]], dtype=object),
                   'C': np.array([[1.,2.,3.],[11.,12.,13.,14.]], dtype=object),
                   'D': np.array([[1.,2.,3.],[21.,22.,23.,24.]], dtype=object),
                   'E': np.array([[9.,8.,4.],[11.,12.,13.,14.]], dtype=object),
                   'F': np.array([[10.,10.,30.],[40.,50.,60.,70.]], dtype=object),
                   }

        c = EMComposition(
            initializer=np.array([stimuli['F'], stimuli['F']], dtype=object),
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM,
            seed=module_seed,
        )

        # Run again to test re-initialization and random retrieval
        c.reset(np.array([stimuli['A'], stimuli['F']], dtype=object))
        retrieved_labels=[]
        for key in sorted(stimuli.keys()):
            retrieved = c(stimuli[key])
            retrieved_label = retrieve_label_helper(retrieved, stimuli)
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [['A'], ['A'], ['F'], ['C'], ['B'], ['F']]

        c.distance_field_weights = [1,0]
        stim = 'C'
        c.equidistant_entries_select = OLDEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        retrieved_labels.append(retrieved_label)
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'

        text = r'More than one entry matched cue'
        with pytest.warns(UserWarning, match=text):
            retrieved = c(stimuli[stim])

        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == [None]

        expected = convert_all_elements_to_np_array([[0, 0, 0], [0, 0, 0, 0]])

        # There's no np.testing function that handles the rugged arrays correctly
        assert len(retrieved) == len(expected)
        for m, e in zip(retrieved, expected):
            assert len(m) == len(e)
            for x, y in zip(m, e):
                np.testing.assert_array_equal(x, y)

    @pytest.mark.skip(reason="test not yet fully implemented")
    def test_without_initializer_and_equal_field_sizes(self):

        stimuli = {'A': [[1,2,3],[4,5,6]],
                   'B': [[8,9,10],[11,12,13]],
                   'C': [[1,2,3],[11,12,13]],
                   'D': [[1,2,3],[21,22,23]],
                   'E': [[9,8,4],[11,12,13]],
                   'F': [[10,10,30],[40,50,60]],
                   }

        c = EMComposition(
            distance_function=Distance(metric=COSINE),
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM,
            seed=module_seed,
        )

        retrieved_labels=[]
        sorted_labels = sorted(stimuli.keys())
        for label in sorted_labels:
            retrieved = [i for i in c(stimuli[label])]
            retrieved_label = retrieve_label_helper(retrieved, stimuli)
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [[None], ['A'], ['A'], ['C'], ['B'], ['A']]

        stim = 'C'
        c.distance_field_weights = [1,0]
        c.equidistant_entries_select = OLDEST
        retrieved = [i for i in c.get_memory(stimuli[stim])]
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST
        retrieved = [i for i in c.get_memory(stimuli[stim])]
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'

        text = "More than one entry matched cue"
        with pytest.warns(UserWarning, match=text):
            retrieved = c.execute(stimuli[stim])

        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == [None]
        expected = np.array([np.array([0,0,0]),np.array([0,0,0])])
        assert all(np.alltrue(x) for x in np.equal(expected,retrieved, dtype=object))

    @pytest.mark.skip(reason="test not yet fully implemented")
    def test_without_initializer_and_diff_field_sizes(self):

        stimuli = {'A': np.array([[1,2,3],[4,5,6,7]], dtype=object),
                   'B': np.array([[8,9,10],[11,12,13,14]], dtype=object),
                   'C': np.array([[1,2,3],[11,12,13,14]], dtype=object),
                   'D': np.array([[1,2,3],[21,22,23,24]], dtype=object),
                   'E': np.array([[9,8,4],[11,12,13,14]], dtype=object),
                   'F': np.array([[10,10,30],[40,50,60,70]], dtype=object),
                   }

        c = EMComposition(
            duplicate_entries_allowed=True,
            equidistant_entries_select=RANDOM,
            distance_field_weights=[1,0],
            seed=module_seed,
        )

        retrieved_labels=[]
        for key in sorted(stimuli.keys()):
            retrieved = c(stimuli[key])
            retrieved_label = retrieve_label_helper(retrieved, stimuli)
            retrieved_labels.append(retrieved_label)
        assert retrieved_labels == [[None], ['A'], ['A'], ['C'], ['B'], ['D']]

        stim = 'C'
        c.equidistant_entries_select = OLDEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == ['A']

        c.equidistant_entries_select = NEWEST
        retrieved = c.get_memory(stimuli[stim])
        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == ['D']

        # Test that after allowing dups, warning is issued and memory with zeros is returned
        c.duplicate_entries_allowed = False
        stim = 'A'

        text = "More than one entry matched cue"
        with pytest.warns(UserWarning, match=text):
            retrieved = c(stimuli[stim])

        retrieved_label = retrieve_label_helper(retrieved, stimuli)
        assert retrieved_label == [None]

        expected = convert_all_elements_to_np_array([[0, 0, 0], [0, 0, 0, 0]])

        # There's no np.testing function that handles the rugged arrays correctly
        assert len(retrieved) == len(expected)
        for m, e in zip(retrieved, expected):
            assert len(m) == len(e)
            for x, y in zip(m, e):
                np.testing.assert_array_equal(x, y)










# *****************************************************************************************************************
# *************************************  FROM AutodiffComposition  ************************************************
# *****************************************************************************************************************

@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
@pytest.mark.composition
def test_autodiff_forward(autodiff_mode):
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass


@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
@pytest.mark.accorrectness
@pytest.mark.composition
class TestTrainingCorrectness:
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass


@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
@pytest.mark.acidenticalness
class TestTrainingIdenticalness():
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass


@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
@pytest.mark.acmisc
@pytest.mark.composition
class TestMiscTrainingFunctionality:
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass

@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
@pytest.mark.actime
class TestTrainingTime:
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass


@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
def test_autodiff_saveload(tmp_path):
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass


@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
@pytest.mark.aclogging
class TestACLogging:
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass


@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
@pytest.mark.acnested
@pytest.mark.composition
class TestNested:
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass


@pytest.mark.skip(reason="no pytorch representation of EMComposition yet")
@pytest.mark.pytorch
class TestBatching:
    """FIX: SHOULD IMPLEMENT CORRESPONDING TESTS FROM AutodiffComposition"""
    pass
