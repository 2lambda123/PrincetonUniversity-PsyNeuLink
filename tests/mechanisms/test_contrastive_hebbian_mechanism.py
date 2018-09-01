import psyneulink as pnl
import numpy as np
import pytest

class TestContrastiveHebbian:

    def test_scheduled_contrastive_hebbian(self):
        o = pnl.TransferMechanism()
        m = pnl.ContrastiveHebbianMechanism(
                input_size=2,
                hidden_size=0,
                target_size=2,
                separated=False,
                mode=pnl.SIMPLE_HEBBIAN,
                integrator_mode=True,
                enable_learning=False,
                matrix=[[0,-1],[-1, 0]],
            # auto=0,
            # hetero=-1,
        )
        s = pnl.sys(m, o)
        ms = pnl.Scheduler(system=s)
        ms.add_condition(o, pnl.WhenFinished(m))
        s.scheduler_processing = ms
        # m.reinitialize_when=pnl.Never()
        print('matrix:\n', m.afferents[1].matrix)
        results = s.run(inputs=[2, 2], num_trials=4)
        print(results)
        np.testing.assert_allclose(results, [[np.array([2.])], [np.array([2.])], [np.array([2.])], [np.array([2.])]])


    def test_using_Hebbian_learning_of_orthognal_inputs_without_integrator_mode(self):
        '''Same as tests/mechanisms/test_recurrent_transfer_mechanism/test_learning_of_orthognal_inputs

        Tests that ContrastiveHebbianMechanism behaves like RecurrentTransferMechanism with Hebbian LearningFunction
        (allowing for epsilon differences due CONVERGENCE CRITERION.
        '''
        size=4
        R = pnl.ContrastiveHebbianMechanism(
                input_size=4,
                hidden_size=0,
                target_size=4,
                mode=pnl.SIMPLE_HEBBIAN,
                enable_learning=True,
                function=pnl.Linear,
                learning_function=pnl.Hebbian,
                minus_phase_termination_criterion=.01,
                plus_phase_termination_criterion=.01,
                # auto=0,
                hetero=np.full((size,size),0.0)
        )
        P=pnl.Process(pathway=[R])
        S=pnl.System(processes=[P])

        inputs_dict = {R:[1,0,1,0]}
        S.run(num_trials=4,
              inputs=inputs_dict)
        assert R.current_execution_time.pass_ == 5
        np.testing.assert_allclose(R.output_states[pnl.ACTIVITY_DIFFERENCE_OUTPUT].value,
                                   [1.20074767, 0.0, 1.20074767, 0.0])
        np.testing.assert_allclose(R.plus_phase_activity, [1.20074767, 0.0, 1.20074767, 0.0])
        np.testing.assert_allclose(R.minus_phase_activity, [0.0, 0.0, 0.0, 0.0])
        np.testing.assert_allclose(R.output_states[pnl.CURRENT_ACTIVITY_OUTPUT].value, [1.20074767, 0.0, 1.20074767, 0.0])
        np.testing.assert_allclose(
            R.recurrent_projection.mod_matrix,
            [
                [0.0,         0.0,         0.2399363,  0.0 ],
                [0.0,         0.0,         0.0,       0.0  ],
                [0.2399363,    0.0,         0.0,       0.0 ],
                [0.0,         0.0,         0.0,       0.0  ]
            ]
        )

        # Reset state so learning of new pattern is "uncontaminated" by activity from previous one
        R.output_state.value = [0,0,0,0]
        inputs_dict = {R:[0,1,0,1]}
        S.run(num_trials=4,
              inputs=inputs_dict)
        np.testing.assert_allclose(
            R.recurrent_projection.mod_matrix,
            [
                [0.0,        0.0,        0.2399363,   0.0      ],
                [0.0,        0.0,        0.0,        0.2399363 ],
                [0.2399363,   0.0,        0.0,        0.0      ],
                [0.0,        0.2399363,   0.0,        0.0      ]
            ]
        )
        np.testing.assert_allclose(R.output_states[pnl.ACTIVITY_DIFFERENCE_OUTPUT].value, [0.0, 1.20074767, 0.0, 1.20074767])
        np.testing.assert_allclose(R.output_states[pnl.ACTIVITY_DIFFERENCE_OUTPUT].value,
                                   [ 0.0, 1.20074767, 0.0, 1.20074767])
        np.testing.assert_allclose(R.plus_phase_activity, [0.0, 1.20074767, 0.0, 1.20074767])
        np.testing.assert_allclose(R.minus_phase_activity, [0.0, 0.0, 0.0, 0.0])

    def test_using_Hebbian_learning_of_orthognal_inputs_with_integrator_mode(self):
        '''Same as tests/mechanisms/test_recurrent_transfer_mechanism/test_learning_of_orthognal_inputs

        Tests that ContrastiveHebbianMechanism behaves like RecurrentTransferMechanism with Hebbian LearningFunction
        (allowing for epsilon differences due to INTEGRATION and convergence criterion).
        '''
        size=4
        R = pnl.ContrastiveHebbianMechanism(
                input_size=4,
                hidden_size=0,
                target_size=4,
                separated=False,
                mode=pnl.SIMPLE_HEBBIAN,
                enable_learning=True,
                function=pnl.Linear,
                integrator_mode=True,
                integration_rate=0.2,
                learning_function=pnl.Hebbian,
                minus_phase_termination_criterion=.01,
                plus_phase_termination_criterion=.01,
                # auto=0,
                hetero=np.full((size,size),0.0)
        )
        P=pnl.Process(pathway=[R])
        S=pnl.System(processes=[P])

        inputs_dict = {R:[1,0,1,0]}
        S.run(num_trials=4,
              inputs=inputs_dict)
        assert R.current_execution_time.pass_ == 18
        np.testing.assert_allclose(R.output_states[pnl.ACTIVITY_DIFFERENCE_OUTPUT].value,
                                   [1.14142296, 0.0, 1.14142296, 0.0])
        np.testing.assert_allclose(R.plus_phase_activity, [1.14142296, 0.0, 1.14142296, 0.0])
        np.testing.assert_allclose(R.minus_phase_activity, [0.0, 0.0, 0.0, 0.0])
        np.testing.assert_allclose(R.output_states[pnl.CURRENT_ACTIVITY_OUTPUT].value,
                                   [1.1414229612568625, 0.0, 1.1414229612568625, 0.0])
        np.testing.assert_allclose(
            R.recurrent_projection.mod_matrix,
            [
                [0.0,         0.0,         0.22035998,  0.0        ],
                [0.0,         0.0,         0.0,         0.0        ],
                [0.22035998,  0.0,         0.0,         0.0        ],
                [0.0,         0.0,         0.0,         0.0        ]
            ]
        )
        # Reset state so learning of new pattern is "uncontaminated" by activity from previous one
        R.output_state.value = [0,0,0,0]
        inputs_dict = {R:[0,1,0,1]}
        S.run(num_trials=4,
              inputs=inputs_dict)
        np.testing.assert_allclose(
            R.recurrent_projection.mod_matrix,
            [
                [0.0,        0.0,        0.22035998, 0.0       ],
                [0.0,        0.0,        0.0,        0.22035998],
                [0.22035998, 0.0,        0.0,        0.        ],
                [0.0,        0.22035998, 0.0,        0.        ]
            ]
        )
        np.testing.assert_allclose(R.output_states[pnl.CURRENT_ACTIVITY_OUTPUT].value,
                                   [0.0, 1.1414229612568625, 0.0, 1.1414229612568625])
        np.testing.assert_allclose(R.output_states[pnl.ACTIVITY_DIFFERENCE_OUTPUT].value,
                                   [ 0.0, 1.14142296, 0.0, 1.14142296])
        np.testing.assert_allclose(R.plus_phase_activity, [0.0, 1.14142296, 0.0, 1.14142296])
        np.testing.assert_allclose(R.minus_phase_activity, [0.0, 0.0, 0.0, 0.0])


    def test_additional_output_states(self):
        CHL1 = pnl.ContrastiveHebbianMechanism(
                input_size=2, hidden_size=0, target_size=2,
                additional_output_states=[pnl.PLUS_PHASE_OUTPUT, pnl.MINUS_PHASE_OUTPUT])
        assert len(CHL1.output_states)==5
        assert pnl.PLUS_PHASE_OUTPUT in CHL1.output_states.names

        CHL2 = pnl.ContrastiveHebbianMechanism(
                input_size=2, hidden_size=0, target_size=2,
                additional_output_states=[pnl.PLUS_PHASE_OUTPUT, pnl.MINUS_PHASE_OUTPUT],
                separated=False)
        assert len(CHL2.output_states)==5
        assert pnl.PLUS_PHASE_OUTPUT in CHL2.output_states.names


    def test_configure_learning(self):

        o = pnl.TransferMechanism()
        m = pnl.ContrastiveHebbianMechanism(
                input_size=2, hidden_size=0, target_size=2,
                mode=pnl.SIMPLE_HEBBIAN,
                separated=False,
                matrix=[[0,-.5],[-.5,0]]
        )

        with pytest.warns(UserWarning) as record:
            m.learning_enabled = True

        correct_message_found = False
        for warning in record:
            if ("Learning cannot be enabled" in str(warning.message) and
                    "because it has no LearningMechanism" in str(warning.message)):
                correct_message_found = True
                break
        assert correct_message_found

        m.configure_learning()
        m.reinitialize_when=pnl.Never()
        s = pnl.sys(m,o)

        ms = pnl.Scheduler(system=s)
        ms.add_condition(o, pnl.WhenFinished(m))
        s.scheduler_processing=ms
        results = s.run(inputs=[2,2], num_trials=4)

        np.testing.assert_allclose(results, [[[2.671875]],
                                             [[2.84093837]],
                                             [[3.0510183]],
                                             [[3.35234623]]])