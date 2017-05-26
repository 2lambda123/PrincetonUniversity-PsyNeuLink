# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# **************************************  GatingMechanism ************************************************

"""
Overview
--------

A GatingMechanism is an `AdaptiveMechanism` that modulates the value of the inputState(s) and/or outputState(s) of 
one or more `ProcessingMechanisms`.   It's function takes a value 
COMMENT:
    ??FROM WHERE?
COMMENT
and uses that to calculate a `gating_policy`:  a list of `gating <LINK>` values, one for each of states that it 
gates.  Each of these values is assigned as the value of a `GatingSignal` (a subclass of `OutputState`) in the
GatingMechanism, and used by an associated `GatingProjection` to modulate the value of the state to which it projects.  
A GatingMechanism can regulate only the parameters of mechanisms in the `System` to which it belongs. 
COMMENT: TBI
The gating components of a system can be displayed using the system's 
`show_graph` method with its **show_gating** argument assigned as :keyword:``True`.  
COMMENT
The gating components of a system are executed after all `Proces singMechanisms <ProcessingMechanism>`, 
`LearningMechanisms <LearningMechanism>`, and  `ControlMechanisms <ControlMechanism>` in that system have been executed.


.. _GatingMechanism_Creation:

Creating A GatingMechanism
---------------------------

GatingMechanisms can be created using the standard Python method of calling the constructor for the desired type.
A GatingMechanism is also created automatically if `gating is specified <GatingMechanism_Specifying_Gating>` for an 
inputState or outputState, in which case a `GatingProjection` is also automatically created that projects 
from the GatingMechanism to the specified state. How a GatingMechanism creates its `GatingProjections 
<GatingProjection>` and determines their value depends on the `subclass <GatingMechanism>`.

.. _GatingMechanism_Specifying_Gating:

Specifying gating
~~~~~~~~~~~~~~~~~

GatingMechanisms are used to modulate the value of an `inputState <InputState>` or `outputState <OutputState>`.  
An inputState or outputState can be specified for gating by assigning it a `GatingProjection` in the 
**input_states** or **output_states** arguments of the constructor for the mechanism to which it belongs 
(see `Mechanism_States <LINK>`).  The inputStates and outputStates to be gated by a GatingMechanism can also be 
specified in the  **gating_signals**  argument of the constructor for a GatingMechanism.  The **gating_signals** 
argument must be a list, each item of which must refer to a state to be gated specified in any of the following ways:

  * *InputState* or *OutputState of the Mechanism to which the state belongs;
  |
  * *tuple*, with the *name* of the state as its 1st item. and the mechanism to which it belongs as the 2nd;  
    note that this is a convenience format, which is simpler to use than a specification dictionary (see below), 
    but precludes specification of any parameters <GatingSignal_Structure>` for the GatingSignal.
  |
  * *specification dictionary*, that must contain at least the following two entries:
    * *NAME* - a string that is the name of the state to be gated;
    * *MECHANISM*:Mechanism - the Mechanism to which the state belongs. 
    The dictionary can also contain entries for any other GatingSignal parameters to be specified
    (e.g., *MODULATION_OPERATION*:ModulationOperation to specify how the value of the state will be modulated;
    see `below <GatingSignal_Structure>` for a list of parameters).

A `GatingSignal` is created for each item listed in **gating_signals**, and all of the GatingSignals for a  
GatingMechanism are listed in its `gating_signals <GatingMechanism.gating_signals>` attribute.  Each GatingSignal is 
assigned a `GatingProjection` to the inputState or outputState of the mechanism specified, that is used to modulate 
the state's value. GatingSignals are a type of `OutputState`, and so they are also listed in the GatingMechanism's 
`output_states <GatingMechanism.outut_states>` attribute.

COMMENT:
  *** PUT IN InputState AND OutputState DOCUMENTATION

  Gating can be also be specified for an `InputState` or `OutputState` when it is created in any of the following ways:

    * in a 2-item tuple, in which the first item is a `state specification <LINK>`, 
      and the second item is a `gating specification <>`

    * keywords GATE (==GATE_PRIMARY) GATE_ALL, GATE_PRIMARY
        or an entry in the state specification dictionary with the key "GATING", and a value that is the
        keyword TRUE/FALSE, ON/OFF, GATE, a ModulationOpearation value, GatingProjection, or its constructor

.. _GatingMechanism_Execution:

Execution
---------

A GatingMechanism executes in the same way as a ProcessingMechanism, based on its place in the system's 
`graph <System.graph>`.  Because GatingProjections are likely to introduce cycles (loops) in the graph,
the effects of a GatingMechanism and its projections will generally not be applied in the first
`round of execution <LINK>` (see `initialization <LINK>` for a description of how to configure the initialization
of feedback loops in a System).  When executd, a GatingMechanism uses its input to determine the value of its
`GatingSignals <GatingSignal>` and their corresponding `GatingProjections <GatingProjection>`.  In the subsequent 
round of execution , each GatingProjection's value is used by the state to which it projects to modulate the 
`value <State.value>` of that state.

When a GatingMechanism executes, the value of each item in its `gating_policy` are assigned as the values of each of
the corresponding GatingSignals in its `gating_signals` attribute.  Those, in turn, as used by their associated
`GatingProjections` to modulate the value of the state to which they project.  This is done by assigning the
GatingSignal's value to a parameter of the state's function, as specified by the GatingSignal's `modulation_operation` 
parameter (see `GatingSignal_Execution` for details). 

.. note::
   A state that receives a `GatingProjection` does not update its value until its owner mechanism executes 
   (see `Lazy Evaluation <LINK>` for an explanation of "lazy" updating).  This means that even if a GatingMechanism 
   has executed, a state that it gates will not assume its new value until the state's owner has executed.

.. _GatingMechanism_Class_Reference:

Class Reference
---------------

"""

# IMPLEMENTATION NOTE: COPIED FROM DefaultProcessingMechanism;
#                      ADD IN GENERIC CONTROL STUFF FROM DefaultGatingMechanism

from collections import OrderedDict

from PsyNeuLink.Components.Mechanisms.Mechanism import Mechanism_Base
from PsyNeuLink.Components.Mechanisms.AdaptiveMechanisms.AdaptiveMechanism import AdaptiveMechanism_Base
from PsyNeuLink.Components.ShellClasses import *

GatingMechanismRegistry = {}


class GatingMechanismError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value


class GatingMechanism(AdaptiveMechanism_Base):
    """
    GatingMechanism_Base(     \
    default_input_value=None, \
    gating_signals=None       \
    function=Linear,          \
    params=None,              \
    name=None,                \
    prefs=None)

    Abstract class for GatingMechanism.

    .. note::
       GatingMechanisms should NEVER be instantiated by a direct call to the base class.
       They should be instantiated using the constructor for a :doc:`subclass <GatingMechanism>`.

    COMMENT:
        Description:
            # VERIFY:
            Protocol for instantiating unassigned GatingProjections (i.e., w/o a sender specified):
               If sender is not specified for a GatingProjection (e.g., in an inputState or OutputState tuple spec) 
                   it is flagged for deferred_init() in its __init__ method
               When the next GatingMechanism is instantiated, if its params[MAKE_DEFAULT_GATING_MECHANISM] == True, its
                   _take_over_as_default_gating_mechanism method is called in _instantiate_attributes_after_function;
                   it then iterates through all of the inputStates and outputStates of all of the mechanisms in its 
                   system, identifies ones without a sender specified, calls its deferred_init() method,
                   instantiates a GatingSignal for it, and assigns it as the GatingProjection's sender.

        Class attributes:
            + componentType (str): System Default Mechanism
            + paramClassDefaults (dict):
                + FUNCTION: Linear
                + FUNCTION_PARAMS:{SLOPE:1, INTERCEPT:0}
    COMMENT

    Arguments
    ---------

    default_gating_policy : value, list or np.ndarray : :py:data:`defaultGatingPolicy <LINK]>`
        the default value for each of the GatingMechanism's GatingSignals;
        its length must equal the number of items specified in the **gating_signals** arg.

    gating_signals : List[InputState or OutputState, tuple[str, Mechanism], or dict]
        specifies the inputStates and/or outputStates to be gated by the GatingMechanism;
        the number of items must equal the length of the **default_gating_policy** arg 
        (see `gating_signals <GatingMechanism.gating_signals>` for details).

    function : TransferFunction : default Linear(slope=1, intercept=0)
        specifies function used to combine values of monitored output states.
        
    params : Optional[Dict[param keyword, param value]]
        a `parameter dictionary <ParameterState_Specifying_Parameters>` that can be used to specify the parameters
        for the mechanism, parameters for its function, and/or a custom function and its parameters. Values
        specified for parameters in the dictionary override any assigned to those parameters in arguments of the
        constructor.

    name : str : default ControlMechanism-<index>
        a string used for the name of the mechanism.
        If not is specified, a default is assigned by `MechanismRegistry`
        (see :doc:`Registry <LINK>` for conventions used in naming, including for default and duplicate names).

    prefs : Optional[PreferenceSet or specification dict : Mechanism.classPreferences]
        the `PreferenceSet` for the mechanism.
        If it is not specified, a default is assigned using `classPreferences` defined in __init__.py
        (see :doc:`PreferenceSet <LINK>` for details).


    Attributes
    ----------

    gating_signals : List[GatingSignal]
        list of `GatingSignals <ControlSignals>` for the GatingMechanism, each of which sends a `GatingProjection`
        to the `inputState <InputState>` or `outputState <OutputState>` that it gates (same as GatingMechanism's 
        `output_states <Mechanism.output_states>` attribute).

    gating_projections : List[GatingProjection]
        list of `GatingProjections <GatingProjection>`, one for each `GatingSignal` in `gating_signals`.

    gating_policy : 2d np.array
        each items is the value assigned to the corresponding GatingSignal listed in `gating_signals`
        (same as the GatingMechanism's `value <Mechanism.value>` attribute).
        
    """

    componentType = "GatingMechanism"

    initMethod = INIT__EXECUTE__METHOD_ONLY

    classPreferenceLevel = PreferenceLevel.TYPE
    # Any preferences specified below will override those specified in TypeDefaultPreferences
    # Note: only need to specify setting;  level will be assigned to TYPE automatically
    # classPreferences = {
    #     kwPreferenceSetName: 'GatingMechanismClassPreferences',
    #     kp<pref>: <setting>...}

    # variableClassDefault = defaultControlAllocation
    # This must be a list, as there may be more than one (e.g., one per GATING_SIGNAL)
    variableClassDefault = defaultControlAllocation

    from PsyNeuLink.Components.Functions.Function import Linear
    paramClassDefaults = Mechanism_Base.paramClassDefaults.copy()
    paramClassDefaults.update({GATING_PROJECTIONS: None})

    @tc.typecheck
    def __init__(self,
                 default_gating_policy=None,
                 function = Linear(slope=1, intercept=0),
                 gating_signals:tc.optional(list) = None,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 context=None):

        # self.system = None

        # Assign args to params and functionParams dicts (kwConstants must == arg names)
        params = self._assign_args_to_param_dicts(gating_signals=gating_signals,
                                                  function=function,
                                                  params=params)

        super().__init__(variable=default_gating_policy,
                         params=params,
                         name=name,
                         prefs=prefs,
                         context=self)

    def _validate_params(self, request_set, target_set=None, context=None):
        """Validate GATING_SIGNALS

        Check that all items in GATING_SIGNALS are InputStates or OutputStates for Mechanisms in self.system
        """

        super(GatingMechanism, self)._validate_params(request_set=request_set,
                                                      target_set=target_set,
                                                      context=context)

        if GATING_SIGNALS in target_set and target_set[GATING_SIGNALS]:

            from PsyNeuLink.Components.Mechanisms.AdaptiveMechanisms.GatingMechanisms.GatingSignal import GatingSignal

            for spec in target_set[GATING_SIGNALS]:

                # Specification is for a GatingSignal
                if isinstance(spec, GatingSignal):
                    #  Check that any GatingProjections it has are to mechanisms in the controller's system
                    if not all(gating_proj.receiver.owner in self.system.mechanisms
                               for gating_proj in spec.efferents):
                        raise GatingMechanismError("The GatingSignal specified in the {} arg for {} ({}) "
                                                    "has one more more GatingProjections to a mechanism "
                                                    "that is not in {}".
                                                    format(GATING_SIGNALS, self.name, spec.name, self.system.name))
                    continue

                # Specification is for a tuple (str, Mechanism):
                elif isinstance(spec, tuple):
                    state_name = spec[0]
                    mech = spec[1]
                    # Check that 1st item is a str (presumably the name of mechanism attribute for the param)
                    if not isinstance(state_name, str):
                        raise GatingMechanismError("1st item of tuple in specification of {} for {} ({}) "
                                                    "must be a string".format(GATING_SIGNAL, owner.name, state_name))
                    # Check that 2nd item is a mechanism
                    if not isinstance(mech, Mechanism):
                        raise GatingMechanismError("2nd item of tuple in specification of {} for {} ({}) "
                                                    "must be a Mechanism".format(GATING_SIGNAL, owner.name, mech))

                # GatingSignal specification dictionary, must have the following entries:
                #    NAME:str - must be the name of an InputState or OutputState of MECHANISM
                #    MECHANISM:Mechanism - must be a Mechanism in self.system
                #    PARAMS:dict - entries must be valid GatingSignal parameters (e.g,. MODULATION_OPERATION)
                elif isinstance(spec, dict):
                    if not NAME in spec:
                        raise GatingMechanismError("Specification dict for {} of {} must have a NAME entry".
                                                    format(GATING_SIGNAL, self.name))
                    state_name = spec[NAME]
                    if not MECHANISM in spec:
                        raise GatingMechanismError("Specification dict for {} of {} must have a MECHANISM entry".
                                                    format(GATING_SIGNAL, self.name))
                    mech = spec[MECHANISM]
                    # Check that all of the other entries in the specification dictionary are valid GatingSignal params
                    for param in spec:
                        if param in {NAME, MECHANISM}:
                            continue
                        if not hasattr(mech, param):
                            raise GatingMechanismError("Entry in specification dictionary for {} arg of {} ({}) "
                                                       "is not a valid {} parameter".
                                                       format(GATING_SIGNAL, self.name, param,
                                                              GatingSignal.__class__.__name__))
                else:
                    # raise GatingMechanismError("PROGRAM ERROR: unrecognized GatingSignal specification for {} ({})".
                    #                             format(self.name, spec))
                    #
                    raise GatingMechanismError("Specification of {} for {} ({}) must be an InputState, OutputState, "
                                               "a tuple specifying a name for one and a mechanism to which it belongs ,"
                                               "a GatingSignal specification dictionary, or an existing GatingSignal".
                                                format(GATING_SIGNAL, self.name, spec))

                # Check that specified state is an InputState or OutputState of the Mechanism
                if state_name in mech.input_states:
                    state_type = INPUT_STATE
                elif state_name in mech.output_states:
                    state_type = OUTPUT_STATE
                else:
                    raise GatingMechanismError("{} (in specification of {}  {}) is not an "
                                               "InputState or OutputState of {}".
                                                format(state_name, GATING_SIGNAL, owner.name, mech))

                # Check that the Mechanism is in the controller's system
                if not mech in self.system.mechanisms:
                    raise GatingMechanismError("Specification in {} arg for {} ({} {} of {}) "
                                                "must be for a Mechanism in {}".
                                                format(GATING_SIGNALS,
                                                       self.name,
                                                       state_name,
                                                       state_type,
                                                       mech.name,
                                                       self.system.name))

    def _validate_projection(self, projection, context=None):
        """Insure that projection is to mechanism within the same system as self
        """

        if projection.value is DEFERRED_INITIALIZATION:
            receiver_mech = projection.init_args['receiver'].owner
        else:
            receiver_mech = projection.receiver.owner
        if not receiver_mech in self.system.mechanisms:
            raise GatingMechanismError("Attempt to assign GatingProjection {} to a mechanism ({}) that is not in {}".
                                              format(projection.name, receiver_mech.name, self.system.name))

    def _instantiate_attributes_after_function(self, context=None):
        """Take over as default GatingMechanism (if specified) and implement any specified GatingProjections

        """

        if MAKE_DEFAULT_GATING_MECHANISM in self.paramsCurrent:
            if self.paramsCurrent[MAKE_DEFAULT_GATING_MECHANISM]:
                self._take_over_as_default_controller(context=context)
            if not self.system.enable_controller:
                return

        # If GatingProjections were specified, implement them
        if GATING_PROJECTIONS in self.paramsCurrent:
            if self.paramsCurrent[GATING_PROJECTIONS]:
                for key, projection in self.paramsCurrent[GATING_PROJECTIONS].items():
                    self._instantiate_gating_projection(projection, context=self.name)

    def _take_over_as_default_controller(self, context=None):

        # Check the parameterStates of the system's mechanisms for any GatingProjections with deferred_init()
        for mech in self.system.mechanisms:
            for parameter_state in mech._parameter_states:
                for projection in parameter_state.afferents:
                    # If projection was deferred for init, initialize it now and instantiate for self
                    if projection.value is DEFERRED_INITIALIZATION and projection.init_args['sender'] is None:
                        # Get params specified with projection for its ControlSignal (cached in GATING_SIGNAL attrib)
                        params = projection.GATING_SIGNAL
                        self._instantiate_gating_projection(projection, params=params, context=context)

    def _instantiate_gating_projection(self, projection, params=None, context=None):
        """Add outputState (as ControlSignal) and assign as sender to requesting GatingProjection

        # Updates allocation_policy and GATING_SIGNAL_costs attributes to accommodate instantiated projection

        Notes:  
        * params are expected to be for (i.e., to be passed to) ControlSignal;
        * wait to instantiate deferred_init() projections until after ControlSignal is instantiated,
             so that correct outputState can be assigned as its sender;
        * index of outputState is incremented based on number of ControlSignals already instantiated;
        * assume that self.allocation_policy has already been extended 
            to include the particular (indexed) allocation to be used for the outputState being created here.


        Returns state: (OutputState)
        """

        self._validate_projection(projection)
        # get name of projection receiver (for use in naming the ControlSignal)
        if projection.value is DEFERRED_INITIALIZATION:
            receiver = projection.init_args['receiver']
        else:
            receiver = projection.receiver

        from PsyNeuLink.Components.Projections.ModulatoryProjections.GatingProjection import GatingProjection
        if not isinstance(projection, GatingProjection):
            raise GatingMechanismError("PROGRAM ERROR: Attempt to assign {0}, "
                                              "that is not a GatingProjection, to outputState of {1}".
                                              format(projection, self.name))

        #  Update self.value by evaluating function
        self._update_value(context=context)

        # Instantiate new outputState and assign as sender of GatingProjection
        try:
            output_state_index = len(self.output_states)
        except AttributeError:
            output_state_index = 0
        from PsyNeuLink.Components.Mechanisms.AdaptiveMechanisms.GatingMechanisms.ControlSignal import ControlSignal
        output_state_name = receiver.name + '_' + ControlSignal.__name__
        output_state_value = self.allocation_policy[output_state_index]
        from PsyNeuLink.Components.States.State import _instantiate_state
        from PsyNeuLink.Components.Mechanisms.AdaptiveMechanisms.GatingMechanisms.ControlSignal import ControlSignal
        state = _instantiate_state(owner=self,
                                            state_type=ControlSignal,
                                            state_name=output_state_name,
                                            state_spec=defaultControlAllocation,
                                            state_params=params,
                                            constraint_value=output_state_value,
                                            constraint_value_name='Default control allocation',
                                            # constraint_output_state_index=output_item_output_state_index,
                                            context=context)

        # Assign outputState as GatingProjection's sender
        if projection.value is DEFERRED_INITIALIZATION:
            projection.init_args['sender']=state
            if projection.init_args['name'] is None:
                projection.init_args['name'] = GATING_PROJECTION + ' for ' + receiver.owner.name + ' ' + receiver.name
            projection._deferred_init()
        else:
            projection.sender = state

        # Update self.outputState and self.outputStates
        try:
            self.output_states[state.name] = state
        except AttributeError:
            self.output_states = OrderedDict({output_state_name:state})

        # Add index assignment to outputState
        state.index = output_state_index

        # Add GatingProjection to list of outputState's outgoing projections
        # (note: if it was deferred, it just added itself, skip)
        if not projection in state.efferents:
            state.efferents.append(projection)

        # Add GatingProjection to GatingMechanism's list of GatingProjections
        try:
            self.gatingProjections.append(projection)
        except AttributeError:
            self.gatingProjections = [projection]

        # Update GATING_SIGNAL_costs to accommodate instantiated projection
        try:
            self.GATING_SIGNAL_costs = np.append(self.GATING_SIGNAL_costs, np.empty((1,1)),axis=0)
        except AttributeError:
            self.GATING_SIGNAL_costs = np.empty((1,1))

        return state

    def _execute(self,
                    variable=None,
                    runtime_params=None,
                    clock=CentralClock,
                    time_scale=TimeScale.TRIAL,
                    context=None):
        """Updates GatingProjections based on inputs

        Must be overriden by subclass
        """
        raise GatingMechanismError("{0} must implement execute() method".format(self.__class__.__name__))

    def show(self):

        print ("\n---------------------------------------------------------")

        print ("\n{0}".format(self.name))
        print("\n\tMonitoring the following mechanism outputStates:")
        for state_name, state in list(self.monitoring_mechanism.input_states.items()):
            for projection in state.afferents:
                monitored_state = projection.sender
                monitored_state_mech = projection.sender.owner
                monitored_state_index = self.monitored_output_states.index(monitored_state)

                # # MODIFIED 1/9/16 OLD:
                # exponent = \
                #     np.ndarray.item(self.paramsCurrent[OUTCOME_FUNCTION].__self__.exponents[
                #     monitored_state_index])
                # weight = \
                #     np.ndarray.item(self.paramsCurrent[OUTCOME_FUNCTION].__self__.weights[monitored_state_index])

                # MODIFIED 1/9/16 NEW:
                weight = self.monitor_for_control_weights_and_exponents[monitored_state_index][0]
                exponent = self.monitor_for_control_weights_and_exponents[monitored_state_index][1]
                # MODIFIED 1/9/16 END

                print ("\t\t{0}: {1} (exp: {2}; wt: {3})".
                       format(monitored_state_mech.name, monitored_state.name, weight, exponent))

        print ("\n\tControlling the following mechanism parameters:".format(self.name))
        # Sort for consistency of output:
        state_names_sorted = sorted(self.output_states.keys())
        for state_name in state_names_sorted:
            for projection in self.output_states[state_name].efferents:
                print ("\t\t{0}: {1}".format(projection.receiver.owner.name, projection.receiver.name))

        print ("\n---------------------------------------------------------")
