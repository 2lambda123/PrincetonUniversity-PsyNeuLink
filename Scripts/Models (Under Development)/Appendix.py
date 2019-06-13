# The following script contains the full computational model in this study
# which includes the Control Module, Decision Module, and Meta-Controller

import numpy as np
import psyneulink as pnl
import csv
from random import randint
import sys

if len(sys.argv) < 2:
    print("Error: Need File Name")

fileName = '1.csv'


# Function that allows this script to be run on cluster cumputers with .csv inputs
def readFile(fileName):

    fileContent = []
    # reading csv file
    with open(fileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            fileContent.append(row)

        # cast each string into an int
        for i in range(0, len(fileContent)):
            for j in range(0, len(fileContent[0])):
                fileContent[i][j] = int(fileContent[i][j])

    return fileContent


# Function to extract the Task Train inputs from a .csv file
def getTaskTrain(dataFile):

    tasks = []
    trials = len(dataFile)

    for i in range(0, trials):
        task = [0, 0]
        if dataFile[i][0] == 1:
            task = [1, 0]
        elif dataFile[i][0] == 2:
            task = [0, 1]

        tasks.append(task)

    return tasks


# Function that creates a Stimulus train
def getStimulusTrain():

    a = [-1, 1]
    b = [1, -1]
    stimulus = []

    for i in range(0, 260):
        x = randint(0, 1)
        if x == 0:
            stimulus.append(a)
        elif x == 1:
            stimulus.append(b)
    return stimulus

# Function that akes an existing set of tasks and stimuli inputs, and inserts cues
def insertCues(tasks, stimuli):

    trials = len(tasks)
    newTasks = []
    newStimuli = []
    for i in range(0, trials):
        newTasks.append(tasks[i])
        newTasks.append(tasks[i])

        newStimuli.append([0, 0])
        newStimuli.append(stimuli[i])

    return newTasks, newStimuli

# Helper function to computing the accuracy from log outputs of the model
def extractValues(outputLog):
    decisionVariable = []
    probabilityUpper = []
    probabilityLower = []
    responseTime = []

    DECISION_VARIABLE = outputLog[1][1][4]
    PROBABILITY_LOWER_THRESHOLD = outputLog[1][1][5]
    PROBABILITY_UPPER_THRESHOLD = outputLog[1][1][6]
    RESPONSE_TIME = outputLog[1][1][7]

    for j in range(1, len(PROBABILITY_LOWER_THRESHOLD)):
        decision = DECISION_VARIABLE[j]
        trialUpper = PROBABILITY_UPPER_THRESHOLD[j]
        trialLower = PROBABILITY_LOWER_THRESHOLD[j]
        reaction = RESPONSE_TIME[j]

        decisionVariable.append(decision[0])
        probabilityUpper.append(trialUpper[0])
        probabilityLower.append(trialLower[0])
        responseTime.append(reaction[0])

    return probabilityUpper, probabilityLower

# User defined function to compute the accuracy for output
def computeAccuracy(variable):
    taskInputs = variable[0]
    stimulusInputs = variable[1]
    upperThreshold = variable[2]
    lowerThreshold = variable[3]

    accuracy = []

    for i in range(0, len(taskInputs)):

        colorTrial = (taskInputs[i][0] > 0)
        motionTrial = (taskInputs[i][1] > 0)

        # during color trials

        if colorTrial:
            # if the correct answer is the upper threshold
            if stimulusInputs[i][0] > 0:
                accuracy.append(upperThreshold[i])
                # print('Color Trial: 1')

            # if the correct answer is the lower threshold
            elif stimulusInputs[i][0] < 0:
                accuracy.append(lowerThreshold[i])
                # print('Color Trial: -1')

        if motionTrial:
            # if the correct answer is the upper threshold
            if stimulusInputs[i][1] > 0:
                accuracy.append(upperThreshold[i])
                # print('Motion Trial: 1')

            # if the correct answer is the lower threshold
            elif stimulusInputs[i][1] < 0:
                accuracy.append(lowerThreshold[i])
                # print('Motion Trial: -1')

    return accuracy


# BEGIN: PSYNEULINK IMPLEMENTATION OF THE STABILITY FLEXIBILITY MODEL

# PARAMETERS
integrationConstant = 0.8       # Time Constant
DRIFT = 0.25                    # Drift Rate
STARTING_POINT = 0.0            # Starting Point
THRESHOLD = 0.05                # Threshold
NOISE = 0.1                     # Noise
T0 = 0.2                        # T0
congruentWeight = 0.2           # Weight of Congruent elemtns

# Task Layer: [Task 1, Task 2] {0, 1} Mutually Exclusive
# Origin Node
taskLayer = pnl.TransferMechanism(default_variable=[[0.0, 0.0]],
                                  size=2,
                                  function=pnl.Linear(slope=1, intercept=0),
                                  output_states=[pnl.RESULT],
                                  name='Task Input [I1, I2]')

# Stimulus Layer: [S1, S2]
# Origin Node
stimulusInfo = pnl.TransferMechanism(default_variable=[[0.0, 0.0]],
                                     size=2,
                                     function=pnl.Linear(slope=1, intercept=0),
                                     output_states=[pnl.RESULT],
                                     name="Stimulus Input [S1, S2]")

congruenceWeighting = pnl.TransferMechanism(default_variable=[[0.0, 0.0]],
                                            size=2,
                                            function=pnl.Linear(slope=congruentWeight,
                                                                intercept=0),
                                            name='Congruence * Automatic Component')

# Activation Layer: [act1, act2]
# Recurrent: Self Excitation, Mutual Inhibition
# Controlled: Gain Parameter
activation = pnl.RecurrentTransferMechanism(default_variable=[[0.0, 0.0]],
                                            function=pnl.Logistic(gain=1.0),
                                            matrix=[[1.0, -1.0],
                                                    [-1.0, 1.0]],
                                            integrator_mode=True,
                                            integrator_function=
                                            pnl.AdaptiveIntegrator
                                            (rate=integrationConstant),
                                            initial_value=np.array([[0.0, 0.0]]),
                                            output_states=[pnl.RESULT],
                                            name='Task Activations [Act 1, Act 2]')

# Dot product of Activation and Stimulus Information
nonAutomaticComponent = pnl.TransferMechanism(default_variable=[[0.0, 0.0]],
                                              size=2,
                                              function=pnl.Linear(slope=1,
                                                                  intercept=0),
                                              input_states=
                                              pnl.InputState(combine=pnl.PRODUCT),
                                              output_states=[pnl.RESULT],
                                              name='Non-Automatic Component '
                                                   '[S1*Activity1, S2*Activity2]')

# Summation of nonAutomatic and Automatic Components
ddmCombination = pnl.TransferMechanism(size=1,
                                       function=pnl.Linear(slope=1, intercept=0),
                                       input_states=pnl.InputState(combine=pnl.SUM),
                                       output_states=[pnl.RESULT],
                                       name="Drift = Wa(S1 + S2) + "
                                            "(S1*Activity1 + S2*Activity2)")

decisionMaker = pnl.DDM(function=pnl.DriftDiffusionAnalytical(drift_rate=DRIFT,
                                                              starting_point=
                                                              STARTING_POINT,
                                                              threshold=THRESHOLD,
                                                              noise=NOISE,
                                                              t0=T0),
                        output_states=[pnl.DECISION_VARIABLE, pnl.RESPONSE_TIME,
                                       pnl.PROBABILITY_UPPER_THRESHOLD,
                                       pnl.PROBABILITY_LOWER_THRESHOLD],
                        name='DDM')

# Log all relevant parameters
taskLayer.set_log_conditions([pnl.RESULT])
stimulusInfo.set_log_conditions([pnl.RESULT])
activation.set_log_conditions([pnl.RESULT, "mod_gain"])
nonAutomaticComponent.set_log_conditions([pnl.RESULT])
ddmCombination.set_log_conditions([pnl.RESULT])
decisionMaker.set_log_conditions([pnl.PROBABILITY_UPPER_THRESHOLD,
                                  pnl.PROBABILITY_LOWER_THRESHOLD,
                                  pnl.DECISION_VARIABLE,
                                  pnl.RESPONSE_TIME])

# CREATE: Stability Flexibility Composition

stabilityFlexibility = pnl.Composition()

# Node Creation
stabilityFlexibility.add_node(taskLayer)
stabilityFlexibility.add_node(activation)
stabilityFlexibility.add_node(congruenceWeighting)
stabilityFlexibility.add_node(nonAutomaticComponent)
stabilityFlexibility.add_node(stimulusInfo)
stabilityFlexibility.add_node(ddmCombination)
stabilityFlexibility.add_node(decisionMaker)

# Projection Creation
stabilityFlexibility.add_projection(sender=taskLayer,
                                    receiver=activation)
stabilityFlexibility.add_projection(sender=activation,
                                    receiver=nonAutomaticComponent)
stabilityFlexibility.add_projection(sender=stimulusInfo,
                                    receiver=nonAutomaticComponent)
stabilityFlexibility.add_projection(sender=stimulusInfo,
                                    receiver=congruenceWeighting)
stabilityFlexibility.add_projection(sender=congruenceWeighting,
                                    receiver=ddmCombination)
stabilityFlexibility.add_projection(sender=nonAutomaticComponent,
                                    receiver=ddmCombination)
stabilityFlexibility.add_projection(sender=ddmCombination,
                                    receiver=decisionMaker)

# Beginning of Controller

# Grid Search Range
searchRange = pnl.SampleSpec(start=0.5, stop=5.0, num=10)

# Modulate the GAIN parameter from activation layer
# Initalize cost function as 0
signal = pnl.ControlSignal(projections=[(pnl.GAIN, activation)],
                           function=pnl.Linear,
                           variable=1.0,
                           intensity_cost_function=pnl.Linear(slope=0.0),
                           allocation_samples=searchRange)

# Use the computeAccuracy function to obtain selection values
# Pass in 4 arguments: Task Inputs, Stimulus Inputs, Prob. Upper, Prob. Lower
objectiveMechanism = pnl.ObjectiveMechanism(monitor=[taskLayer, stimulusInfo,
                                            (pnl.PROBABILITY_UPPER_THRESHOLD,
                                             decisionMaker),
                                            (pnl.PROBABILITY_LOWER_THRESHOLD,
                                            decisionMaker)],
                                            function=pnl.AccuracyIntegrator,
                                            name="Controller Objective Mechanism")
objectiveMechanism.set_log_conditions(items=pnl.VALUE)

#  Sets trial history for simulations over specified signal search parameters
metaController = \
    pnl.OptimizationControlMechanism(agent_rep=stabilityFlexibility,
                                     features=[taskLayer.input_state,
                                               stimulusInfo.input_state],
                                     feature_function=pnl.Buffer(history=10),
                                     name="Controller",
                                     objective_mechanism=objectiveMechanism,
                                     function=pnl.GridSearch(),
                                    control_signals=[signal])

# enables the meta-controller and retains old simulation data
stabilityFlexibility.add_controller(metaController)
stabilityFlexibility.enable_controller = True
activation.parameters.value.retain_old_simulation_data = True

# Runs a set of simulations to determine the first gain parameter specified
stabilityFlexibility.controller_mode = pnl.BEFORE

for i in range(1, len(stabilityFlexibility.controller.input_states)):
    stabilityFlexibility.controller.input_states[i].function.reinitialize()

# END OF COMPOSITION CONSTRUCTION


# TESTING

# Processes a .csv file to obtain the task input sequence
# Create a stimulus input sequence to match
dataFile = readFile(fileName)
taskTrain = getTaskTrain(dataFile)
stimulusTrain = getStimulusTrain()

# Inserts cue trials (Simulation 4)
taskTrain, stimulusTrain = insertCues(taskTrain, stimulusTrain)

# Inputs the task and stimulus and runs the model
inputs = {taskLayer: taskTrain, stimulusInfo: stimulusTrain}
stabilityFlexibility.run(inputs)

# DOCUMENTATION AND OUTPUT COMMANDS

print("File Name:", fileName)
condition = dataFile[0][14]
print("Condition:", condition)

# Print Contents of Logs
activation.log.print_entries()
decisionMaker.log.print_entries()
objectiveMechanism.log.print_entries()
decisions = decisionMaker.log.nparray()

# Prints Accuracies and Gains as lists

runs = len(taskTrain)
upper = []
lower = []
accuracy = []
upper, lower = extractValues(decisions)
variable = [taskTrain, stimulusTrain, upper, lower]
accuracy = computeAccuracy(variable)
print(accuracy)

activations = activation.log.nparray()
gains = []
for i in range(0, runs):
    optimalGain = activations[1][1][5][i + 1][0]
    gains.append(optimalGain)
print(gains)



