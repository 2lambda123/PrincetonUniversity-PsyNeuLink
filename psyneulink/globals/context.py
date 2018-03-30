# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
#
# ********************************************  System Defaults ********************************************************

from uuid import UUID
from enum import IntEnum
from collections import namedtuple

import typecheck as tc
import warnings


from psyneulink.globals.keywords import FLAGS, INITIALIZING, VALIDATE, EXECUTING, CONTROL, LEARNING
# from psyneulink.composition import Composition


__all__ = [
    'Context',
    'ContextFlags',
    '_get_context'
]

STATUS = 'status'

time = namedtuple('time', 'run trial pass_ time_step')

class ContextError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value


class ContextFlags(IntEnum):
    """Used to identify the status of a `Component` when its value or one of its attributes is being accessed.
    Also used to specify the context in which a value of the Component or its attribute is `logged <Log_Conditions>`.
    """

    # INITIALIZATION = 1<<1  # 2
    # """Set during execution of the Component's constructor."""
    # VALIDATION =     1<<2  # 4
    # """Set during validation of the value of a Component or its attribute."""
    # EXECUTION =      1<<3  # 8
    # """Set during any execution of the Component."""
    # PROCESSING =     1<<4  # 16
    # """Set during the `processing phase <System_Execution_Processing>` of execution of a Composition."""
    # LEARNING =       1<<5  # 32
    # """Set during the `learning phase <System_Execution_Learning>` of execution of a Composition."""
    # CONTROL =        1<<6  # 64
    # """Set during the `control phase System_Execution_Control>` of execution of a Composition."""
    # TRIAL =          1<<7  # 128
    # """Set at the end of a `TRIAL`."""
    # RUN =            1<<8  # 256
    # """Set at the end of a `RUN`."""
    # SIMULATION =     1<<9  # 512
    # # Set during simulation by Composition.controller
    # COMMAND_LINE =   1<<10 # 1024
    # # Component accessed by user
    # CONSTRUCTOR =    1<<11 # 2048

    # initialization_status flags
    UNINITIALIZED = 0
    """Not Initialized."""
    DEFERRED_INIT = 1<<1  # 2
    """Set if flagged for deferred initialization."""
    INITIALIZING =  1<<2  # 4
    """Set during initialization of the Component."""
    VALIDATING =    1<<3  # 8
    """Set during validation of the value of a Component or its attribute."""
    INITIALIZED =   1<<4  # 16
    """Set after completion of initialization of the Component."""
    REINITIALIZED =   1<<4  # 16
    """Set on stateful Components when they are re-initialized."""

    INITIALIZATION_MASK = UNINITIALIZED | DEFERRED_INIT | INITIALIZING | VALIDATING | INITIALIZED | REINITIALIZED

    # execution_phase flags
    PROCESSING =    1<<5  # 32
    """Set during the `processing phase <System_Execution_Processing>` of execution of a Composition."""
    LEARNING =      1<<6 # 64
    """Set during the `learning phase <System_Execution_Learning>` of execution of a Composition."""
    CONTROL =       1<<7 # 128
    """Set during the `control phase System_Execution_Control>` of execution of a Composition."""
    SIMULATION =    1<<8  # 256
    """Set during simulation by Composition.controller"""
    EXECUTION_PHASE_MASK = PROCESSING | LEARNING | CONTROL | SIMULATION
    EXECUTING = EXECUTION_PHASE_MASK
    IDLE = ~EXECUTION_PHASE_MASK

    # source (source-of-call) flags
    CONSTRUCTOR =   1<<9  # 512
    """Call to method from Component's constructor."""
    COMMAND_LINE =  1<<10 # 1024
    """Direct call to method by user (either interactively from the command line, or in a script)."""
    COMPONENT =     1<<11 # 2048
    """Call to method by the Component."""
    COMPOSITION =   1<<12 # 4096
    """Call to method by a/the Composition to which the Component belongs."""
    SOURCE_MASK = CONSTRUCTOR | COMMAND_LINE | COMPONENT | COMPOSITION

    ALL_FLAGS = INITIALIZATION_MASK | EXECUTION_PHASE_MASK | SOURCE_MASK

    @classmethod
    def _get_context_string(cls, condition, string=None):
        """Return string with the names of all flags that are set in **condition**, prepended by **string**"""
        if string:
            string += ": "
        else:
            string = ""
        flagged_items = []
        # If OFF or ALL_FLAGS, just return that
        if condition == ContextFlags.ALL_FLAGS:
            return ContextFlags.ALL_FLAGS.name
        if condition == ContextFlags.UNINITIALIZED:
            return ContextFlags.UNINITIALIZED.name
        # Otherwise, append each flag's name to the string
        for c in list(cls.__members__):
            # Skip ALL_FLAGS (handled above)
            if c is ContextFlags.ALL_FLAGS.name:
                continue
            if ContextFlags[c] & condition:
               flagged_items.append(c)
        string += ", ".join(flagged_items)
        return string

INITIALIZATION_STATUS_FLAGS = {ContextFlags.UNINITIALIZED,
                               ContextFlags.DEFERRED_INIT,
                               ContextFlags.INITIALIZING,
                               ContextFlags.VALIDATING,
                               ContextFlags.INITIALIZED,
                               ContextFlags.REINITIALIZED}

EXECUTION_PHASE_FLAGS = {ContextFlags.PROCESSING,
                         ContextFlags.LEARNING,
                         ContextFlags.CONTROL,
                         ContextFlags.SIMULATION}

SOURCE_FLAGS = {ContextFlags.CONSTRUCTOR,
                ContextFlags.COMMAND_LINE,
                ContextFlags.COMPONENT,
                ContextFlags.COMPOSITION}

# For backward compatibility
class ContextStatus(IntEnum):
    """Used to identify the status of a `Component` when its value or one of its attributes is being accessed.
    Also used to specify the context in which a value of the Component or its attribute is `logged <Log_Conditions>`.
    """
    OFF = 0
    # """No recording."""
    INITIALIZATION = ContextFlags.INITIALIZING
    """Set during execution of the Component's constructor."""
    VALIDATION =  ContextFlags.VALIDATING
    """Set during validation of the value of a Component or its attribute."""
    EXECUTION =  ContextFlags.EXECUTING
    """Set during any execution of the Component."""
    PROCESSING = ContextFlags.PROCESSING
    """Set during the `processing phase <System_Execution_Processing>` of execution of a Composition."""
    LEARNING = ContextFlags.LEARNING
    """Set during the `learning phase <System_Execution_Learning>` of execution of a Composition."""
    CONTROL = ContextFlags.LEARNING
    """Set during the `control phase System_Execution_Control>` of execution of a Composition."""
    SIMULATION = ContextFlags.SIMULATION
    # Set during simulation by Composition.controller
    COMMAND_LINE = ContextFlags.COMMAND_LINE
    # Component accessed by user
    CONSTRUCTOR = ContextFlags.CONSTRUCTOR
    # Component being constructor (used in call to super.__init__)
    ALL_ASSIGNMENTS = \
        INITIALIZATION | VALIDATION | EXECUTION | PROCESSING | LEARNING | CONTROL
    """Specifies all contexts."""


class Context():
    __name__ = 'Context'
    def __init__(self,
                 owner,
                 composition=None,
                 flags=None,
                 initialization_status=ContextFlags.UNINITIALIZED,
                 execution_phase=None,
                 source=ContextFlags.COMPONENT,
                 execution_id:UUID=None,
                 string:str='', time=None):

        self.owner = owner
        self.composition = composition
        self.initialization_status = initialization_status
        self.execution_phase = execution_phase
        self.source = source
        if flags:
            if (initialization_status != (ContextFlags.UNINITIALIZED) and
                    not (flags & ContextFlags.INITIALIZATION_MASK & initialization_status)):
                raise ContextError("Conflict in assignment to flags ({}) and status ({}) arguments of Context for {}".
                                   format(ContextFlags._get_context_string(flags & ContextFlags.INITIALIZATION_MASK),
                                          ContextFlags._get_context_string(initialization_status),
                                          self.owner.name))
            if (execution_phase and not (flags & ContextFlags.EXECUTION_PHASE_MASK & execution_phase)):
                raise ContextError("Conflict in assignment to flags ({}) and execution_phase ({}) arguments "
                                   "of Context for {}".
                                   format(ContextFlags._get_context_string(flags & ContextFlags.EXECUTION_PHASE_MASK),
                                          ContextFlags._get_context_string(execution_phase), self.owner.name))
            if (source != ContextFlags.COMPONENT) and not (flags & ContextFlags.SOURCE_MASK & source):
                raise ContextError("Conflict in assignment to flags ({}) and source ({}) arguments of Context for {}".
                                   format(ContextFlags._get_context_string(flags & ContextFlags.SOURCE_MASK),
                                          ContextFlags._get_context_string(source),
                                          self.owner.name))
        self.execution_id = execution_id
        self.execution_time = None
        self.string = string

    @property
    def composition(self):
        try:
            return self._composition
        except AttributeError:
            self._composition = None

    @composition.setter
    def composition(self, composition):
        # from psyneulink.composition import Composition
        # if isinstance(composition, Composition):
        if composition is None or composition.__class__.__name__ in {'Composition', 'System'}:
            self._composition = composition
        else:
            raise ContextError("Assignment to context.composition for {} ({}) "
                               "must be a Composition (or \'None\').".format(self.owner.name, composition))

    @property
    def flags(self):
        try:
            return self._flags
        except:
            self._flags = ContextFlags.UNINITIALIZED |ContextFlags.COMPONENT
            return self._flags

    @flags.setter
    def flags(self, flags):
        if isinstance(flags, (ContextFlags, int)):
            self._flags = flags
        else:
            raise ContextError("\'{}\'{} argument in call to {} must be a {} or an int".
                               format(FLAGS, flags, self.__name__, ContextFlags.__name__))

    @property
    def initialization_status(self):
        return self.flags & ContextFlags.INITIALIZATION_MASK

    @initialization_status.setter
    def initialization_status(self, flag):
        """Check that a flag is one and only one status flag """
        flag &= ContextFlags.INITIALIZATION_MASK
        if flag in INITIALIZATION_STATUS_FLAGS:
            self.flags |= flag
        elif not flag:
            raise ContextError("Attempt to assign a flag ({}) to {}.context.flags "
                               "that is not an initialization status flag".
                               format(ContextFlags._get_context_string(flag), self.owner.name))
        else:
            raise ContextError("Attempt to assign more than one flag ({}) to {}.context.initialization_status".
                               format(ContextFlags._get_context_string(flag), self.owner.name))

    @property
    def execution_phase(self):
        return self.flags & ContextFlags.EXECUTION_PHASE_MASK

    @execution_phase.setter
    def execution_phase(self, flag):
        """Check that a flag is one and only one execution_phase flag """
        if flag in EXECUTION_PHASE_FLAGS:
            self.flags |= flag
        elif flag is None or flag is ContextFlags.IDLE:
            self.flags &= ContextFlags.IDLE
        elif not flag & ContextFlags.EXECUTION_PHASE_MASK:
            raise ContextError("Attempt to assign a flag ({}) to {}.context.execution_phase "
                               "that is not an execution phase flag".
                               format(ContextFlags._get_context_string(flag), self.owner.name))
        else:
            raise ContextError("Attempt to assign more than one flag ({}) to {}.context.execution_phase".
                               format(ContextFlags._get_context_string(flag), self.owner.name))

    @property
    def source(self):
        return self.flags & ContextFlags.SOURCE_MASK

    @source.setter
    def source(self, flag):
        """Check that a flag is one and only one source flag """
        if flag in SOURCE_FLAGS:
            self.flags |= flag
        elif not flag & ContextFlags.SOURCE_MASK:
            raise ContextError("Attempt to assign a flag ({}) to {}.context.source that is not a source flag".
                               format(ContextFlags._get_context_string(flag), self.owner.name))
        else:
            raise ContextError("Attempt to assign more than one flag ({}) to {}.context.source".
                               format(ContextFlags._get_context_string(flag), self.owner.name))

    @property
    def execution_time(self):
        try:
            return self._execution_time
        except:
            return None

    @execution_time.setter
    def execution_time(self, time):
        self._execution_time = time

    def update_execution_time(self):
        if self.execution & ContextFlags.EXECUTING:
            self.execution_time = _get_time(self.owner, self.context.flags)
        else:
            raise ContextError("PROGRAM ERROR: attempt to call update_execution_time for {} "
                               "when 'EXECUTING' was not in its context".format(self.owner.name))


@tc.typecheck
def _get_context(context:tc.any(ContextFlags, str)):
    """Set flags based on a string of ContextFlags keywords
    If context is already a ContextFlags mask, return that
    Otherwise, return mask with flags set corresponding to keywords in context
    """
    # FIX: 3/23/18 UPDATE WITH NEW FLAGS
    if isinstance(context, ContextFlags):
        return context
    context_flag = ContextFlags.UNINITIALIZED
    if INITIALIZING in context:
        context_flag |= ContextFlags.INITIALIZING
    if VALIDATE in context:
        context_flag |= ContextFlags.VALIDATING
    if EXECUTING in context:
        context_flag |= ContextFlags.EXECUTING
    if CONTROL in context:
        context_flag |= ContextFlags.CONTROL
    if LEARNING in context:
        context_flag |= ContextFlags.LEARNING
    # if context == ContextFlags.TRIAL.name: # cxt-test
    #     context_flag |= ContextFlags.TRIAL
    # if context == ContextFlags.RUN.name:
    #     context_flag |= ContextFlags.RUN
    if context == ContextFlags.COMMAND_LINE.name:
        context_flag |= ContextFlags.COMMAND_LINE
    return context_flag

def _get_time(component, context_flags):

    """Get time from Scheduler of System in which Component is being executed.

    Returns tuple with (run, trial, time_step) if being executed during Processing or Learning
    Otherwise, returns (None, None, None)

    """

    from psyneulink.globals.context import time
    from psyneulink.components.mechanisms.mechanism import Mechanism
    from psyneulink.components.states.state import State
    from psyneulink.components.projections.projection import Projection

    no_time = time(None, None, None, None)

    # Get mechanism to which Component being logged belongs
    if isinstance(component, Mechanism):
        ref_mech = component
    elif isinstance(component, State):
        if isinstance(component.owner, Mechanism):
            ref_mech = component.owner
        elif isinstance(component.owner, Projection):
            ref_mech = component.owner.receiver.owner
        else:
            raise ContextError("Logging currently does not support {} (only {}s, {}s, and {}s).".
                           format(component.__class__.__name__,
                                  Mechanism.__name__, State.__name__, Projection.__name__))
    elif isinstance(component, Projection):
        ref_mech = component.receiver.owner
    else:
        raise ContextError("Logging currently does not support {} (only {}s, {}s, and {}s).".
                       format(component.__class__.__name__,
                              Mechanism.__name__, State.__name__, Projection.__name__))

    # FIX: Modify to use component.owner.context.composition once that is implemented
    # Get System in which it is being (or was last) executed (if any):

    # If called from COMMAND_LINE, get context for last time value was assigned:
    if context_flags & ContextFlags.COMMAND_LINE:
    # if context_flags & (ContextFlags.COMMAND_LINE | ContextFlags.RUN | ContextFlags.TRIAL):
        context_flags = component.prev_context.flags
        execution_context = component.prev_context.string
    else:
        execution_context = component.context.string

    system = ref_mech.context.composition

    if system:
        # FIX: Add ContextFlags.VALIDATE?
        if context_flags == ContextFlags.PROCESSING:
            t = system.scheduler_processing.clock.time
            t = time(t.run, t.trial, t.pass_, t.time_step)
        elif context_flags == ContextFlags.CONTROL:
            t = system.scheduler_processing.clock.time
            t = time(t.run, t.trial, t.pass_, t.time_step)
        elif context_flags == ContextFlags.LEARNING:
            t = system.scheduler_learning.clock.time
            t = time(t.run, t.trial, t.pass_, t.time_step)
        else:
            t = None

    else:
        if component.verbosePref:
            offender = "\'{}\'".format(component.name)
            if ref_mech is not component:
                offender += " [{} of {}]".format(component.__class__.__name__, ref_mech.name)
            warnings.warn("Attempt to log {} which is not in a System (logging is currently supported only "
                          "when running Components within a System".format(offender))
        t = None

    return t or no_time
