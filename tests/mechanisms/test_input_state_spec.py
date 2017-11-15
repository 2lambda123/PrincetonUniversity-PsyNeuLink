import numpy as np
import pytest

from psyneulink.components.mechanisms.mechanism import MechanismError
from psyneulink.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.components.projections.projection import ProjectionError
from psyneulink.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.components.states.state import StateError
from psyneulink.components.states.inputstate import InputState
from psyneulink.globals.keywords import INPUT_STATES, MECHANISM, NAME, OUTPUT_STATES, PROJECTIONS, VARIABLE

mismatches_default_variable_error_text = 'not compatible with the specified default variable'
mismatches_size_error_text = 'not compatible with the default variable determined from size parameter'


class TestInputStateSpec:
    # ------------------------------------------------------------------------------------------------

    # InputState SPECIFICATIONS

    # ------------------------------------------------------------------------------------------------
    # TEST 1
    # Match of default_variable and specification of multiple InputStates by value and string

    def test_match_with_default_variable(self):

        T = TransferMechanism(
            default_variable=[[0, 0], [0]],
            input_states=[[32, 24], 'HELLO']
        )
        assert T.instance_defaults.variable.shape == np.array([[0, 0], [0]]).shape
        assert len(T.input_states) == 2
        assert T.input_states[1].name == 'HELLO'
        # # PROBLEM WITH input FOR RUN:
        # my_mech_2.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 2
    # Mismatch between InputState variable specification and corresponding item of owner Mechanism's variable

    def test_mismatch_with_default_variable_error(self):

        with pytest.raises(MechanismError) as error_text:
            TransferMechanism(
                default_variable=[[0], [0]],
                input_states=[[32, 24], 'HELLO']
            )
        assert mismatches_default_variable_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 3
    # Override of input_states (mis)specification by INPUT_STATES entry in params specification dict

    def test_override_by_dict_spec(self):

        T = TransferMechanism(
            default_variable=[[0, 0], [0]],
            input_states=[[32], 'HELLO'],
            params={INPUT_STATES: [[32, 24], 'HELLO']}
        )
        assert T.instance_defaults.variable.shape == np.array([[0, 0], [0]]).shape
        assert len(T.input_states) == 2
        assert T.input_states[1].name == 'HELLO'
        # # PROBLEM WITH input FOR RUN:
        # my_mech_2.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 4
    # Specification using input_states without default_variable

    def test_transfer_mech_input_states_no_default_variable(self):

        # PROBLEM: SHOULD GENERATE TWO INPUT_STATES (
        #                ONE WITH [[32],[24]] AND OTHER WITH [[0]] AS VARIABLE INSTANCE DEFAULT
        #                INSTEAD, SEEM TO IGNORE InputState SPECIFICATIONS AND JUST USE DEFAULT_VARIABLE
        #                NOTE:  WORKS FOR ObjectiveMechanism, BUT NOT TransferMechanism
        T = TransferMechanism(input_states=[[32, 24], 'HELLO'])
        assert T.instance_defaults.variable.shape == np.array([[0, 0], [0]]).shape
        assert len(T.input_states) == 2
        assert T.input_states[1].name == 'HELLO'

    # ------------------------------------------------------------------------------------------------
    # TEST 5
    # Specification using INPUT_STATES entry in params specification dict without default_variable

    def test_transfer_mech_input_states_specification_dict_no_default_variable(self):

        # PROBLEM: SHOULD GENERATE TWO INPUT_STATES (
        #                ONE WITH [[32],[24]] AND OTHER WITH [[0]] AS VARIABLE INSTANCE DEFAULT
        #                INSTEAD, SEEM TO IGNORE InputState SPECIFICATIONS AND JUST USE DEFAULT_VARIABLE
        #                NOTE:  WORKS FOR ObjectiveMechanism, BUT NOT TransferMechanism
        T = TransferMechanism(params={INPUT_STATES: [[32, 24], 'HELLO']})
        assert T.instance_defaults.variable.shape == np.array([[0, 0], [0]]).shape
        assert len(T.input_states) == 2
        assert T.input_states[1].name == 'HELLO'

    # ------------------------------------------------------------------------------------------------
    # TEST 6
    # Mechanism specification

    def test_mech_spec_list(self):
        R1 = TransferMechanism(output_states=['FIRST', 'SECOND'])
        T = TransferMechanism(
            default_variable=[[0]],
            input_states=[R1]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0]]))
        assert len(T.input_states) == 1
        assert T.input_state.path_afferents[0].sender == R1.output_state
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 7
    # Mechanism specification outside of a list

    def test_mech_spec_standalone(self):
        R1 = TransferMechanism(output_states=['FIRST', 'SECOND'])
        # Mechanism outside of list specification
        T = TransferMechanism(
            default_variable=[[0]],
            input_states=R1
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0]]))
        assert len(T.input_states) == 1
        assert T.input_state.path_afferents[0].sender == R1.output_state
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 8
    # OutputState specification

    def test_output_state_spec_list_two_items(self):
        R1 = TransferMechanism(output_states=['FIRST', 'SECOND'])
        T = TransferMechanism(
            default_variable=[[0], [0]],
            input_states=[
                R1.output_states['FIRST'],
                R1.output_states['SECOND']
            ]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0], [0]]))
        assert len(T.input_states) == 2
        assert T.input_states.names[0] == 'InputState-0'
        assert T.input_states.names[1] == 'InputState-1'
        for input_state in T.input_states:
            for projection in input_state.path_afferents:
                assert projection.sender.owner is R1
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 9
    # OutputState specification outside of a list

    def test_output_state_spec_standalone(self):
        R1 = TransferMechanism(output_states=['FIRST', 'SECOND'])
        T = TransferMechanism(
            default_variable=[0],
            input_states=R1.output_states['FIRST']
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0]]))
        assert len(T.input_states) == 1
        assert T.input_states.names[0] == 'InputState-0'
        T.input_state.path_afferents[0].sender == R1.output_state
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 10
    # OutputStates in PROJECTIONS entries of a specification dictiontary, using with names (and one outside of a list)

    def test_specification_dict(self):
        R1 = TransferMechanism(output_states=['FIRST', 'SECOND'])
        T = TransferMechanism(
            default_variable=[[0], [0]],
            input_states=[
                {
                    NAME: 'FROM DECISION',
                    PROJECTIONS: [R1.output_states['FIRST']]
                },
                {
                    NAME: 'FROM RESPONSE_TIME',
                    PROJECTIONS: R1.output_states['SECOND']
                }
            ])
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0], [0]]))
        assert len(T.input_states) == 2
        assert T.input_states.names[0] == 'FROM DECISION'
        assert T.input_states.names[1] == 'FROM RESPONSE_TIME'
        for input_state in T.input_states:
            for projection in input_state.path_afferents:
                assert projection.sender.owner is R1
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 11
    # default_variable override of value of OutputState specification

    def test_default_variable_override_mech_list(self):

        R2 = TransferMechanism(size=3)

        # default_variable override of OutputState.value
        T = TransferMechanism(
            default_variable=[[0, 0]],
            input_states=[R2]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1
        assert len(T.input_state.path_afferents[0].sender.instance_defaults.variable) == 3
        assert len(T.input_state.instance_defaults.variable) == 2
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 12
    # 2-item tuple specification with default_variable override of OutputState.value

    def test_2_item_tuple_spec(self):
        R2 = TransferMechanism(size=3)
        T = TransferMechanism(size=2, input_states=[(R2, np.zeros((3, 2)))])
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1
        assert len(T.input_state.path_afferents[0].sender.instance_defaults.variable) == 3
        assert len(T.input_state.instance_defaults.variable) == 2
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 13
    # ConnectionTuple Specification

    def test_connection_tuple_spec(self):
        R2 = TransferMechanism(size=3)
        T = TransferMechanism(size=2, input_states=[(R2, None, None, np.zeros((3, 2)))])
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1
        assert len(T.input_state.path_afferents[0].sender.instance_defaults.variable) == 3
        assert len(T.input_state.instance_defaults.variable) == 2
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 14
    # Standalone Projection specification

    def test_projection_list(self):
        R2 = TransferMechanism(size=3)
        P = MappingProjection(sender=R2)
        T = TransferMechanism(
            size=2,
            input_states=[P]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1
        assert len(T.input_state.path_afferents[0].sender.instance_defaults.variable) == 3
        assert len(T.input_state.instance_defaults.variable) == 2
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 15
    # Projection specification in Tuple

    def test_projection_in_tuple(self):
        R2 = TransferMechanism(size=3)
        P = MappingProjection(sender=R2)
        T = TransferMechanism(
            size=2,
            input_states=[(R2, None, None, P)]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1
        assert len(T.input_state.path_afferents[0].sender.instance_defaults.variable) == 3
        assert len(T.input_state.instance_defaults.variable) == 2
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 16
    # PROJECTIONS specification in InputState specification dictionary

    def test_projection_in_specification_dict(self):
        R1 = TransferMechanism(output_states=['FIRST', 'SECOND'])
        T = TransferMechanism(
            input_states=[{
                NAME: 'My InputState with Two Projections',
                PROJECTIONS: [
                    R1.output_states['FIRST'],
                    R1.output_states['SECOND']
                ]
            }]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0]]))
        assert len(T.input_states) == 1
        assert T.input_state.name == 'My InputState with Two Projections'
        for input_state in T.input_states:
            for projection in input_state.path_afferents:
                assert projection.sender.owner is R1
        T.execute()

    # ------------------------------------------------------------------------------------------------
    # TEST 17
    # MECHANISMS/OUTPUT_STATES entries in params specification dict

    def test_output_state_in_specification_dict(self):
        R1 = TransferMechanism(output_states=['FIRST', 'SECOND'])
        T = TransferMechanism(
            input_states=[{
                MECHANISM: R1,
                OUTPUT_STATES: ['FIRST', 'SECOND']
            }]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0]]))
        assert len(T.input_states) == 1
        for input_state in T.input_states:
            for projection in input_state.path_afferents:
                assert projection.sender.owner is R1

    # ------------------------------------------------------------------------------------------------
    # TEST 18
    # String specification with variable specification

    def test_dict_with_variable(self):
        T = TransferMechanism(input_states=[{NAME: 'FIRST', VARIABLE: [0, 0]}])
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 19
    # String specification with variable specification conflicts with default_variable

    def test_dict_with_variable_matches_default(self):
        T = TransferMechanism(
            default_variable=[0, 0],
            input_states=[{NAME: 'FIRST', VARIABLE: [0, 0]}]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 20

    def test_dict_with_variable_matches_default_2(self):
        T = TransferMechanism(
            default_variable=[[0, 0]],
            input_states=[{NAME: 'FIRST', VARIABLE: [0, 0]}]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 21

    def test_dict_with_variable_matches_default_multiple_input_states(self):
        T = TransferMechanism(
            default_variable=[[0, 0], [0]],
            input_states=[
                {NAME: 'FIRST', VARIABLE: [0, 0]},
                {NAME: 'SECOND', VARIABLE: [0]}
            ]
        )
        assert T.instance_defaults.variable.shape == np.array([[0, 0], [0]]).shape
        assert len(T.input_states) == 2

    # ------------------------------------------------------------------------------------------------
    # TEST 22

    def test_dict_with_variable_mismatches_default(self):
        with pytest.raises(MechanismError) as error_text:
            TransferMechanism(
                default_variable=[0],
                input_states=[{NAME: 'FIRST', VARIABLE: [0, 0]}]
            )
        assert mismatches_default_variable_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 23

    def test_dict_with_variable_mismatches_default_multiple_input_states(self):
        with pytest.raises(MechanismError) as error_text:
            TransferMechanism(
                default_variable=[[0], [0]],
                input_states=[
                    {NAME: 'FIRST', VARIABLE: [0, 0]},
                    {NAME: 'SECOND', VARIABLE: [0]}
                ]
            )
        assert mismatches_default_variable_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 24

    def test_dict_with_variable_matches_size(self):
        T = TransferMechanism(
            size=2,
            input_states=[{NAME: 'FIRST', VARIABLE: [0, 0]}]
        )
        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 25

    def test_dict_with_variable_mismatches_size(self):
        with pytest.raises(MechanismError) as error_text:
            TransferMechanism(
                size=1,
                input_states=[{NAME: 'FIRST', VARIABLE: [0, 0]}]
            )
        assert mismatches_size_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 26

    def test_params_override(self):
        T = TransferMechanism(
            input_states=[[0], [0]],
            params={INPUT_STATES: [[0, 0], [0]]}
        )
        assert T.instance_defaults.variable.shape == np.array([[0, 0], [0]]).shape
        assert len(T.input_states) == 2

    # ------------------------------------------------------------------------------------------------
    # TEST 27

    def test_add_input_state_belonging_to_another_mech_error(self):
        with pytest.raises(StateError) as error_text:
            m = TransferMechanism(default_variable=[0, 0, 0])
            i = InputState(owner=m, variable=[0, 0, 0])
            TransferMechanism(input_states=[i])
        assert 'that belongs to another Mechanism' in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 28

    def test_inputstate_class(self):
        T = TransferMechanism(input_states=[InputState])

        np.testing.assert_array_equal(T.instance_defaults.variable, [InputState.ClassDefaults.variable])
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 29

    def test_inputstate_class_with_variable(self):
        T = TransferMechanism(default_variable=[0, 0], input_states=[InputState])

        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 30

    def test_InputState_mismatches_default(self):
        with pytest.raises(MechanismError) as error_text:
            i = InputState(reference_value=[0, 0, 0])
            TransferMechanism(default_variable=[0, 0], input_states=[i])
        assert mismatches_default_variable_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 31

    def test_projection_with_matrix_and_sender(self):
        m = TransferMechanism(size=2)
        p = MappingProjection(sender=m, matrix=[[0, 0, 0], [0, 0, 0]])
        T = TransferMechanism(input_states=[p])

        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 32

    def test_projection_with_matrix_and_sender_mismatches_default(self):
        with pytest.raises(MechanismError) as error_text:
            m = TransferMechanism(size=2)
            p = MappingProjection(sender=m, matrix=[[0, 0, 0], [0, 0, 0]])
            TransferMechanism(default_variable=[0, 0], input_states=[p])
        assert mismatches_default_variable_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 33

    def test_projection_with_sender_and_default(self):
        t = TransferMechanism(size=3)
        p = MappingProjection(sender=t)
        T = TransferMechanism(default_variable=[0, 0], input_states=[p])

        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 34

    def test_projection_no_args_projection_spec(self):
        p = MappingProjection()
        T = TransferMechanism(input_states=[p])

        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 35

    def test_projection_no_args_projection_spec_with_default(self):
        p = MappingProjection()
        T = TransferMechanism(default_variable=[0, 0], input_states=[p])

        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 36

    def test_projection_no_args_dict_spec(self):
        p = MappingProjection()
        T = TransferMechanism(input_states=[{VARIABLE: [0, 0, 0], PROJECTIONS:[p]}])

        np.testing.assert_array_equal(T.instance_defaults.variable, np.array([[0, 0, 0]]))
        assert len(T.input_states) == 1

    # ------------------------------------------------------------------------------------------------
    # TEST 37

    def test_projection_no_args_dict_spec_mismatch_with_default(self):
        with pytest.raises(MechanismError) as error_text:
            p = MappingProjection()
            TransferMechanism(default_variable=[0, 0], input_states=[{VARIABLE: [0, 0, 0], PROJECTIONS: [p]}])
        assert mismatches_default_variable_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 38

    def test_outputstate_(self):
        with pytest.raises(MechanismError) as error_text:
            p = MappingProjection()
            TransferMechanism(default_variable=[0, 0], input_states=[{VARIABLE: [0, 0, 0], PROJECTIONS: [p]}])
        assert mismatches_default_variable_error_text in str(error_text.value)

    # ------------------------------------------------------------------------------------------------
    # TEST 26

    def test_add_input_state_with_projection_in_mech_constructor(self):
        T1 = TransferMechanism()
        I = InputState(projections=[T1])
        T2 = TransferMechanism(input_states=[I])
        assert T2.input_states[0].path_afferents[0].sender.owner is T1

    # ------------------------------------------------------------------------------------------------
    # TEST 27

    def test_add_input_state_with_projection_using_add_states(self):
        T1 = TransferMechanism()
        I = InputState(projections=[T1])
        T2 = TransferMechanism()
        T2.add_states([I])
        assert T2.input_states[1].path_afferents[0].sender.owner is T1

    # ------------------------------------------------------------------------------------------------
    # TEST 28

    def test_add_input_state_with_projection_by_assigning_owner(self):
        T1 = TransferMechanism()
        T2 = TransferMechanism()
        InputState(owner=T2, projections=[T1])
        assert T2.input_states[1].path_afferents[0].sender.owner is T1

    # ------------------------------------------------------------------------------------------------
    # TEST 29

    def test_add_input_state_with_projection_by_assigning_owner_error(self):
        with pytest.raises(StateError) as error_text:
            S1 = TransferMechanism()
            S2 = TransferMechanism()
            TransferMechanism(name='T',
                              input_states=[{'MY INPUT 1':[S1],
                                             'MY INPUT 2':[S2]}])

    # ------------------------------------------------------------------------------------------------
    # TEST 30

    def test_use_set_to_specify_projections_for_input_state_error(self):
        with pytest.raises(ProjectionError) as error_text:
            T1 = TransferMechanism()
            T2 = TransferMechanism()
            TransferMechanism(input_states=[{'MY STATE':{T1, T2}}])
        assert ('Connection specification for InputState of' in str(error_text.value)
                and 'is a set' in str(error_text.value)
                and 'it should be a list' in str(error_text.value))

    # ------------------------------------------------------------------------------------------------
    # TEST 31

    def test_multiple_states_specified_using_STATE_NAME_format_error(self):
        with pytest.raises(StateError) as error_text:
            # Don't bother to specify anything as the value for each entry in the dict, since doesn't get there
            TransferMechanism(input_states=[{'MY STATE A':{},
                                             'MY STATE B':{}}])
        assert ('There is more than one entry of the InputState specification dictionary' in str(error_text.value)
                and'that is not a keyword; there should be only one (used to name the State, with a list of '
                   'Projection specifications' in str(error_text.value))

    # ------------------------------------------------------------------------------------------------
    # TEST 32

    def test_default_name_and_projections_listing_for_input_state_in_constructor(self):
        T1 = TransferMechanism()
        my_input_state = InputState(projections=[T1])
        T2 = TransferMechanism(input_states=[my_input_state])
        assert T2.input_states[0].name == 'InputState-0'
        assert T2.input_states[0].projections[0].sender.name == 'RESULT'