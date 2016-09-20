from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.DDM import *
from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.Deprecated.LinearMechanism import *
from PsyNeuLink.Functions.Process import process
from PsyNeuLink.Functions.Projections.ControlSignal import ControlSignal
from PsyNeuLink.Functions.System import System_Base
from PsyNeuLink.Functions.Utilities.Utility import Exponential, Linear
from PsyNeuLink.Globals.Keywords import *

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
Decision = DDM(
               # drift_rate=(2.0, CONTROL_SIGNAL),
               # drift_rate=(2.0, ControlSignal),
               # drift_rate=(2.0, ControlSignal()),
               # drift_rate=(2.0, ControlSignal(function=Linear)),
               drift_rate=(2.0, ControlSignal(function=Linear(slope=2, intercept=10),
                                              # allocation_samples=np.arange(.1, 1.01, .1))),
                                              allocation_samples=[0, .1, .5, 1.0])),
               # drift_rate=(2.0, ControlSignal(function=Exponential)),
               # drift_rate=(2.0, ControlSignal(function=Exponential(rate=2, scale=10))),
               # threshold=(5.0, CONTROL_SIGNAL),
               # threshold=(5.0, ControlSignal()),
               # threshold=(5.0, ControlSignal(function=Exponential)),
               # threshold=(5.0, ControlSignal(function=Exponential(slope=2, intercept=10))),
               threshold=(5.0, ControlSignal(function=Exponential(rate=2, scale=10))),
               # threshold=(5.0, ControlSignal(function=Exponential)),
               # threshold=(5.0, CONTROL_SIGNAL),
               analytic_solution=kwBogaczEtAl,
               prefs = DDM_prefs,
               name='Decision'
               )
#endregion


#region Processes
TaskExecutionProcess = process(default_input_value=[0],
                               configuration=[(Input, 0), IDENTITY_MATRIX, (Decision, 0)],
                               prefs = process_prefs,
                               name = 'TaskExecutionProcess')

RewardProcess = process(default_input_value=[0],
                        configuration=[(Reward, 1)],
                        prefs = process_prefs,
                        name = 'RewardProcess')
#endregion

#region System
mySystem = System_Base(processes=[TaskExecutionProcess, RewardProcess],
                       monitored_output_states=[Reward, ERROR_RATE, (RT_MEAN, -1, 1)],
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
