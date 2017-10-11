from psyneulink.components.functions.function import Integrator, Linear
from psyneulink.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.components.system import *
from psyneulink.globals.keywords import DIFFUSION
from psyneulink.library.mechanisms.processing.integrator.ddm import DDM
from psyneulink.scheduling.condition import AfterNCalls, Any, AtPass, WhenFinished
from psyneulink.scheduling.scheduler import Scheduler
from psyneulink.scheduling.timescale import TimeScale

logger = logging.getLogger(__name__)

o = TransferMechanism(
    name='origin',
    default_variable = [0],
    function=Linear(slope=.5),
    prefs={REPORT_OUTPUT_PREF: PreferenceEntry(True,PreferenceLevel.INSTANCE)}
)

ddm = DDM(
    function=Integrator(
        integration_type = DIFFUSION,
        noise=0.5
    ),
    name='ddm',
    time_scale=TimeScale.TIME_STEP,
    thresh=10
)

term = TransferMechanism(
    name='terminal',
    default_variable = [0],
    function=Linear(slope=2.0),
    prefs={REPORT_OUTPUT_PREF: PreferenceEntry(True,PreferenceLevel.INSTANCE)}
)

p = Process(
    default_variable = [0],
    pathway = [o, ddm, term],
    name = 'p',
)

# origin → DDM → terminal
s = system(
    processes=[p],
    name='s',
)

stim_list = {o: [[1]]}

s.scheduler_processing = Scheduler(system=s)
s.scheduler_processing.add_condition(o, AtPass(0))
# ddm has default condition of Always - run at every chance
s.scheduler_processing.add_condition(term, Any(WhenFinished(ddm), AfterNCalls(ddm, 10)))

term_conds = {TimeScale.TRIAL: AfterNCalls(term, 1)}

s.show_graph()
results = s.run(
    inputs=stim_list,
    termination_processing=term_conds
)
logger.info('System result: {0}'.format(results))
