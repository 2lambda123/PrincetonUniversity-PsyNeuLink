import functools
import numpy as np
import psyneulink as pnl

input_layer = pnl.TransferMechanism(
    size=2,
    name='Input Layer'
)

def decision_variable_to_one_hot(x):
    if x > 0:
        return [1,0]
    else:
        return [0,1]

action_selection = pnl.DDM(
    function=pnl.BogaczEtAl(
        # drift_rate=pnl.CONTROL,
        # threshold=pnl.CONTROL,
        # starting_point=pnl.CONTROL,
        # noise=pnl.CONTROL,
        #
        drift_rate=pnl.ControlSignal,
        threshold=pnl.ControlSignal,
        starting_point=pnl.ControlSignal,
        noise=pnl.ControlSignal

        # drift_rate=pnl.ControlSignal(),
        # threshold=pnl.ControlSignal(),
        # starting_point=pnl.ControlSignal(),
        # noise=pnl.ControlSignal()
    ),
    output_states=[{pnl.NAME: 'ACTION VECTOR',
                    pnl.INDEX: 0,
                    pnl.CALCULATE: decision_variable_to_one_hot}],
    name='DDM'
)

p = pnl.Process(
    default_variable=[0, 0],
    pathway=[input_layer, action_selection],
    learning=pnl.LearningProjection(learning_function=pnl.Reinforcement(learning_rate=0.05)),
    target=0
)

print('reward prediction weights: \n', action_selection.input_state.path_afferents[0].matrix)
print('target_mechanism weights: \n', action_selection.output_state.efferents[0].matrix)

actions = ['left', 'right']
reward_values = [10, 10]
first_reward = 0

# Must initialize reward (won't be used, but needed for declaration of lambda function)
action_selection.output_state.value = [0, 1]
# Get reward value for selected action)


def reward():
    return [reward_values[int(np.nonzero(action_selection.output_state.value)[0])]]


def print_header(system):
    print("\n\n**** Time: ", system.scheduler_processing.clock.simple_time)


def show_weights():
    print('Reward prediction weights: \n', action_selection.input_state.path_afferents[0].matrix)
    print(
        '\nAction selected:  {}; predicted reward: {}'.format(
            np.nonzero(action_selection.output_state.value)[0][0],
            action_selection.output_state.value[np.nonzero(action_selection.output_state.value)][0]
        )
    )

input_list = {input_layer: [[1, 1]]}

s = pnl.System(
        processes=[p],
        targets=[0],
        controller=pnl.EVCControlMechanism
)

# s.show_graph(show_learning=pnl.ALL, show_dimensions=True)

s.run(
    num_trials=10,
    inputs=input_list,
    targets=reward,
    call_before_trial=functools.partial(print_header, s),
    call_after_trial=show_weights
)
