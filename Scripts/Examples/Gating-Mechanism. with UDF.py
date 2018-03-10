import functools
import numpy as np
import psyneulink as pnl


def my_linear_fct(x,
                  m=1.0,
                  b=0.0,
                  params={pnl.ADDITIVE_PARAM:'b',
                          pnl.MULTIPLICATIVE_PARAM:'m'}):
    return m * x + b

def my_simple_linear_fct(x, m=1.0, b=0.0):
    return m * x + b

def my_exp_fct(x,
               r=1,
               b=0,
               params={pnl.ADDITIVE_PARAM:'b',
                       pnl.MULTIPLICATIVE_PARAM:'r'}):
    return x**r + b

def my_sinusoidal_fct(input,
                      phase=0,
                      amplitude=1,
                      params={pnl.ADDITIVE_PARAM:'phase',
                              pnl.MULTIPLICATIVE_PARAM:'amplitude'}):
    frequency = input[0]
    t = input[1]
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

Input_Layer = pnl.TransferMechanism(
    name='Input_Layer',
    default_variable=np.zeros((2,)),
    function=pnl.Logistic
)

Output_Layer = pnl.TransferMechanism(
        name='Output_Layer',
        default_variable=[0, 0, 0],
        function=pnl.Linear,
        # function=pnl.Logistic,
        # output_states={pnl.NAME: 'RESULTS USING UDF',
        #                pnl.VARIABLE: [(pnl.OWNER_VALUE,0), pnl.TIME_STEP],
        #                pnl.FUNCTION: my_sinusoidal_fct}
        output_states={pnl.NAME: 'RESULTS USING UDF',
                       pnl.VARIABLE: (pnl.OWNER_VALUE, 0),
                       # pnl.FUNCTION: my_linear_fct
                       # pnl.FUNCTION: my_exp_fct
                       pnl.FUNCTION:pnl.UserDefinedFunction(custom_function=my_simple_linear_fct,
                                                            params={pnl.ADDITIVE_PARAM:'b',
                                                                    pnl.MULTIPLICATIVE_PARAM:'m'}
                                                            )
                       # pnl.FUNCTION:pnl.Linear(slope=1, intercept=2)
        #                                 FUNCTION: UserDefinedFunction(custom_function=MSE_fct,
        #                                                               params={
                       }
)

Gating_Mechanism = pnl.GatingMechanism(
    # default_gating_policy=0.0,
    size=[1],
    gating_signals=[
        # Output_Layer
        Output_Layer.output_state,
    ]
)

p = pnl.Process(
    size=2,
    pathway=[
        Input_Layer,
        Output_Layer
    ],
    prefs={
        pnl.VERBOSE_PREF: False,
        pnl.REPORT_OUTPUT_PREF: False
    }
)

g = pnl.Process(
    default_variable=[1.0],
    pathway=[Gating_Mechanism]
)

stim_list = {
    Input_Layer: [[-1, 30], [-1, 30], [-1, 30], [-1, 30]],
    Gating_Mechanism: [[0], [0.5], [1.0], [2.0]]
}


def print_header(system):
    print("\n\n**** Time: ", system.scheduler_processing.clock.simple_time)


def show_target():
    print('Gated: ',
          Gating_Mechanism.gating_signals[0].efferents[0].receiver.owner.name,
          Gating_Mechanism.gating_signals[0].efferents[0].receiver.name)
    print('- Input_Layer.value:                  ', Input_Layer.value)
    print('- Output_Layer.value:                 ', Output_Layer.value)
    print('- Output_Layer.output_state.variable: ', Output_Layer.output_state.variable)
    print('- Output_Layer.output_state.value:    ', Output_Layer.output_state.value)

mySystem = pnl.System(processes=[p, g])

mySystem.reportOutputPref = False
# mySystem.show_graph(show_learning=True)

results = mySystem.run(
    num_trials=4,
    inputs=stim_list,
    call_before_trial=functools.partial(print_header, mySystem),
    call_after_trial=show_target,
)
