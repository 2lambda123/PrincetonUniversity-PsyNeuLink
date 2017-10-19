from psyneulink.components.functions.function import Logistic
from psyneulink.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.components.system import *

# specification of task environment
NFeatures = 2
NOutputDimensions = 2
NInputDimensions = 4

# number of units for each layer
NInputUnits = NInputDimensions * NFeatures
NOutputUnits = NOutputDimensions * NFeatures
NHiddenUnits = NOutputDimensions * NInputDimensions * NFeatures
NTaskUnits = NInputDimensions * NOutputDimensions


# MECHANISMS

Stimulus_Layer = TransferMechanism(name='Stimulus Layer',
                       function=Linear(),
                       default_variable = np.zeros((NInputUnits,)))

Task_Layer = TransferMechanism(name='Task Layer',
                       function=Linear(),
                       default_variable = np.zeros((NTaskUnits,)))

Hidden_Layer = TransferMechanism(name='Hidden Layer',
                          function=Logistic(),
                          default_variable = np.zeros((NHiddenUnits,)))

Output_Layer = TransferMechanism(name='Output Layer',
                        function=Logistic(),
                        default_variable = np.zeros((NOutputUnits,)))


# WEIGHT MATRICES

Stimulus_Hidden_Weights_Matrix = np.random.uniform(0, 0.1, (NInputUnits, NHiddenUnits))
Hidden_Output_Weights_Matrix = np.random.uniform(0, 0.1, (NHiddenUnits, NOutputUnits))
Task_Hidden_Weights_Matrix = np.random.uniform(0, 0.1, (NTaskUnits, NHiddenUnits))
Task_Output_Weights_Matrix = np.random.uniform(0, 0.1, (NTaskUnits, NOutputUnits))

# MAPPING PROJECTIONS

Stimulus_Hidden_Weights = MappingProjection(name='Stimulus-Hidden Weights',
                        sender=Stimulus_Layer,
                        receiver=Hidden_Layer,
                        matrix=Stimulus_Hidden_Weights_Matrix)

Hidden_Output_Weights = MappingProjection(name='Hidden-Output Weights',
                        sender=Hidden_Layer,
                        receiver=Output_Layer,
                        matrix=Hidden_Output_Weights_Matrix)

Task_Hidden_Weights = MappingProjection(name='Task-Hidden Weights',
                        sender=Task_Layer,
                        receiver=Hidden_Layer,
                        matrix=Task_Hidden_Weights_Matrix)

Task_Output_Weights = MappingProjection(name='Task-Output Weights',
                        sender=Task_Layer,
                        receiver=Output_Layer,
                        matrix=Task_Output_Weights_Matrix)


# PROCESSES

process_prefs = ComponentPreferenceSet(reportOutput_pref=PreferenceEntry(True,PreferenceLevel.INSTANCE),
                                      verbose_pref=PreferenceEntry(True,PreferenceLevel.INSTANCE))

StimulusResponseProcess = process(
    pathway=[Stimulus_Layer, Stimulus_Hidden_Weights, Hidden_Layer, Hidden_Output_Weights, Output_Layer],
    prefs = process_prefs,
    learning=LEARNING,
    target = [1, 0, 0, 0,],
    name = 'Stimulus Response Process')

TaskHiddenProcess = process(
    pathway=[Task_Layer, Task_Hidden_Weights, Hidden_Layer],
    prefs = process_prefs,
    learning=LEARNING,
    name = 'Task Hidden Process')

# TaskHiddenProcess = process(
#     pathway=[Task_Layer, Task_Hidden_Weights, Hidden_Layer, Hidden_Output_Weights, Output_Layer],
#     prefs = process_prefs,
#     learning=LEARNING,
#     target = [1, 0, 0, 0,],
#     name = 'Task Hidden Process')

TaskOutputProcess = process(
    pathway=[Task_Layer, Task_Output_Weights, Output_Layer],
    prefs = process_prefs,
    learning=LEARNING,
    target = [1, 0, 0, 0,],
    name = 'Task Output Process')

# SYSTEM

system_prefs = {REPORT_OUTPUT_PREF: True,
                VERBOSE_PREF: False}


stim_list_dict = {Stimulus_Layer:[1, 0, 1, 0, 1, 0, 1, 0],
                  Task_Layer:[1, 0, 0, 0, 0, 0, 0, 0]}

target_list_dict = {Output_Layer:[1, 0, 0, 0,]}

multitaskingModel = system(processes=[StimulusResponseProcess, TaskHiddenProcess, TaskOutputProcess],
                           name='Multitasking Model',
                           prefs=system_prefs)

#
# multitaskingModel.run(num_trials=1,
#             inputs=stim_list_dict,
#             targets=target_list_dict)


# BUGS
# 1) enforcing to specify target at the process level ddoes seem redundant in this case
# 2) specifying weights with random_weight_matrix = lambda sender, receiver : random_matrix(sender, receiver, .2, -.1) doesn't work anymore
# 3) how to specify learning rate?
