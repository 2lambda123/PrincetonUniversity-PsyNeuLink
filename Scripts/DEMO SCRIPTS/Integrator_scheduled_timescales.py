from psyneulink.components.functions.function import Integrator, Linear
from psyneulink.components.mechanisms.processing import integratormechanism
from psyneulink.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.components.system import *
from psyneulink.scheduling.condition import AfterNCalls, Any, AtPass, EveryNCalls
from psyneulink.scheduling.scheduler import Scheduler

logger = logging.getLogger(__name__)

process_prefs = {
    REPORT_OUTPUT_PREF: False,
    VERBOSE_PREF: False
}

A = TransferMechanism(
    name='A',
    default_variable = [0],
    function=Linear(slope=2.0),
    prefs={REPORT_OUTPUT_PREF: PreferenceEntry(False,PreferenceLevel.INSTANCE)}
)

B = integratormechanism(
    name='B',
    default_variable = [0],
    function=Integrator(
        rate=.5,
        integration_type=SIMPLE
    ),
    prefs={REPORT_OUTPUT_PREF: PreferenceEntry(False,PreferenceLevel.INSTANCE)}
)

C = integratormechanism(
    name='C',
    default_variable = [0],
    function=Integrator(
        rate=.5,
        integration_type=SIMPLE
    ),
    prefs={REPORT_OUTPUT_PREF: PreferenceEntry(False,PreferenceLevel.INSTANCE)}
)

D = TransferMechanism(
    name='D',
    default_variable = [0],
    function=Linear(slope=1.0),
    prefs={REPORT_OUTPUT_PREF: PreferenceEntry(False,PreferenceLevel.INSTANCE)}
)

p = process(
    default_variable = [0],
    pathway = [A, B, D],
    name = 'p'
)

q = process(
    default_variable = [0],
    pathway = [A, C, D],
    name = 'q',
    prefs=process_prefs
)

s = system(
    processes=[p, q],
    name = 's'
)

stim_list = {A: [[1]]}

s.scheduler_processing = Scheduler(system=s)
s.scheduler_processing.add_condition(A, Any(AtPass(0), EveryNCalls(D, 1)))
# B has default condition of Always - run at every chance
s.scheduler_processing.add_condition(C, EveryNCalls(B, 5))
s.scheduler_processing.add_condition(D, EveryNCalls(C, 1))

term_conds = {TimeScale.TRIAL: AfterNCalls(D, 1)}

s.show_graph()
results = s.run(
    inputs=stim_list,
    termination_processing=term_conds
)
logger.info('Executed in order: {0}'.format(s.scheduler_processing.execution_list))
logger.info('System result: {0}'.format(results))
