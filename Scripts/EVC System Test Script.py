from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.DDM import *
from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.Deprecated.LinearMechanism import *
from PsyNeuLink.Functions.Process import Process_Base
from PsyNeuLink.Functions.System import System_Base
from PsyNeuLink.Globals.Keywords import *
from PsyNeuLink.Functions.Projections.ControlSignal import ControlSignal

if MPI_IMPLEMENTATION:
    import time
    from mpi4py import MPI
    Comm = MPI.COMM_WORLD
    Comm.Barrier()
    startTime = time.time()
    Comm.Barrier()

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
Decision = DDM(params={kwFunctionParams:{kwDDM_DriftRate:(1.0, kwControlSignal),
                                              # kwDDM_Threshold:(10.0, ControlSignal)
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
mySystem = System_Base(params={kwProcesses:[TaskExecutionProcess, RewardProcess],
                               kwMonitoredOutputStates:[Reward, kwDDM_Error_Rate,(kwDDM_RT_Mean, -1, 1)]},
                       name='Test System')
#endregion

#region Inspect
mySystem.inspect()
mySystem.controller.inspect()
#endregion

#region Run

for i in range(2):
    # Present stimulus:
    CentralClock.trial = i
    CentralClock.time_step = 0
    mySystem.execute([[0.5],[0]])
    print ('\nTRIAL: {}; Time Step: {}\n{}\n{}'.format(CentralClock.trial, CentralClock.time_step,
                                                     mySystem.terminalMechanisms.outputStateNames,
                                                     mySystem.terminalMechanisms.outputStateValues))

    # Present feedback:
    CentralClock.time_step = 1
    mySystem.execute([[0],[1]])
    print ('\nTRIAL: {}; Time Step: {}\n{}\n{}'.format(CentralClock.trial, CentralClock.time_step,
                                                     mySystem.terminalMechanisms.outputStateNames,
                                                     mySystem.terminalMechanisms.outputStateValues))

#endregion

if MPI_IMPLEMENTATION:
    Comm.Barrier()
    endTime = time.time()
    Comm.Barrier()

    print("\nRuntime: ", endTime-startTime)

print('DONE')
