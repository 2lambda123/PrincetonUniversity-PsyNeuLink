from Functions.System import System_Base
from Functions.Process import Process_Base
from Functions.Mechanisms.DDM import *
from Functions.Mechanisms.LinearMechanism import *
from Functions.Mechanisms.AdaptiveIntegrator import *
from Functions.Mechanisms.EVCMechanism import *
from Globals.Keywords import *
from Functions.Utility import UtilityRegistry
from Functions.MechanismStates.MechanismState import MechanismStateRegistry
import random as rnd


#region Preferences
DDM_prefs = FunctionPreferenceSet(
                prefs = {
                    kpVerbosePref: PreferenceEntry(False,PreferenceLevel.INSTANCE),
                    kpReportOutputPref: PreferenceEntry(True,PreferenceLevel.INSTANCE)})

process_prefs = FunctionPreferenceSet(reportOutput_pref=PreferenceEntry(False,PreferenceLevel.INSTANCE),
                                      verbose_pref=PreferenceEntry(True,PreferenceLevel.INSTANCE))
#endregion

#region Mechanisms
Input = LinearMechanism(name='Input')
Reward = LinearMechanism(name='Reward')
Decision = DDM(params={kwExecuteMethodParams:{kwDDM_DriftRate:(1.0, kwControlSignal),
                                              #   kwDDM_Threshold:(10.0, kwControlSignal)
                                              },
                          kwDDM_AnalyticSolution:kwDDM_BogaczEtAl},
                  prefs = DDM_prefs,
                  name='Decision'
                  )
#endregion

#region Processes
TaskExecutionProcess = Process_Base(default_input_value=[0],
                                    params={kwConfiguration:[(Input, 0),
                                                             kwIdentityMatrix,
                                                             (Decision, 0)]},
                                    prefs = process_prefs,
                                    name = 'TaskExecutionProcess')

RewardProcess = Process_Base(default_input_value=[0],
                             params={kwConfiguration:[(Reward, 1)]},
                             prefs = process_prefs,
                             name = 'RewardProcess')
#endregion

#region System
mySystem = System_Base(params={kwProcesses:[TaskExecutionProcess, RewardProcess]},
                       name='EVC Test System')
#endregion

#region Inspect
mySystem.inspect()
mySystem.controller.inspect()
#endregion

outputStateLabels = mySystem.terminalMechanisms.outputStateLabels
#region Run
# adding comment

numTrials = 10
for i in range(0, numTrials):
    stimulus = rnd.random()*3 - 2

    # Present stimulus:
    CentralClock.time_step = 0
    mySystem.execute([[stimulus],[0]])
    print ('\n{0}\n{1}'.format(mySystem.terminalMechanisms.outputStateLabels,
                               mySystem.terminalMechanisms.outputStateValues))

    # Present feedback:
    CentralClock.time_step = 1
    mySystem.execute([[0],[1]])
    print ('\n{0}\n{1}'.format(mySystem.terminalMechanisms.outputStateLabels,
                               mySystem.terminalMechanisms.outputStateValues))

# # Run EVC:
# CentralClock.time_step = 2
# mySystem.execute([[0],[0],[0]])

#endregion