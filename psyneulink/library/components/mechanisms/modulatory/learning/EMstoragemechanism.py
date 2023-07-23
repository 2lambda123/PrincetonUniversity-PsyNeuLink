# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# *************************************  EMStorageMechanism **********************************************

"""

Contents
--------

  * `EMStorageMechanism_Overview`
    - `EMStorageMechanism_Memory`
    - `EMStorageMechanism_Entry`
    - `EMStorageMechanism_Fields`
  * `EMStorageMechanism_Creation`
  * `EMStorageMechanism_Structure`
  * `EMStorageMechanism_Execution`
  * `EMStorageMechanism_Class_Reference`


.. _EMStorageMechanism_Overview:

Overview
--------

An EMStorageMechanism is a subclass of `LearningMechanism`, modified for use in an `EMComposition` to store a new
entry in its `memory <EMComposition.memory>` attribute each time it executes.

.. _EMStorageMechanism_Memory:

# FIX: NEEDS EDITING:

* **Memory** -- the `memory <EMComposition.memory>` attribute of an `EMComposition` is a list of entries, each of
    which is a 2d np.array with a shape that corresponds to the `memory_matrix <EMStorageMechanism.memory_matrix>`
    attribute of the EMStorageMechanism that stores it.  Each entry is stored in the `memory <EMComposition.memory>`
    attribute of the EMComposition as a row or column of the `matrix <MappingProjection.matrix>` parameter of the
    `MappingProjections <MappingProjection>` to which the `LearningProjections <LearningProjection>` of the
    EMStorageMechanism project.  The `memory <EMComposition.memory>` attribute of the EMComposition is used by its
    `controller <EMComposition.controller>` to generate the `memory <EMMemoryMechanism.memory>` attribute of an
    `EMMemoryMechanism` that is used to retrieve entries from the `memory <EMComposition.memory>` attribute of the
    EMComposition.

.. _EMStorageMechanism_Entry:

* **Entry** -- an entry is a 2d np.array with a shape that corresponds to the `memory_matrix
    <EMStorageMechanism.memory_matrix>` attribute of the EMStorageMechanism that stores it.  Each entry is stored in the
    `memory <EMComposition.memory>` attribute of the EMComposition as a row or column of the `matrix
    <MappingProjection.matrix>` parameter of the `MappingProjections <MappingProjection>` to which the
    `LearningProjections <LearningProjection>` of the EMStorageMechanism project.  The `memory
    <EMComposition.memory>` attribute of the EMComposition is used by its `controller <EMComposition.controller>` to
    generate the `memory <EMMemoryMechanism.memory>` attribute of an `EMMemoryMechanism` that is used to retrieve
    entries from the `memory <EMComposition.memory>` attribute of the EMComposition.

.. _EMStorageMechanism_Fields:

* **Fields** -- an entry is composed of one or more fields, each of which is a 1d np.array with a length that
    corresponds to the number of `fields <EMStorageMechanism_Fields>` of the EMStorageMechanism that stores it.  Each
    field is stored in the `memory <EMComposition.memory>` attribute of the EMComposition as a row or column of the
    `matrix <MappingProjection.matrix>` parameter of the `MappingProjections <MappingProjection>` to which the
    `LearningProjections <LearningProjection>` of the EMStorageMechanism project.  The `memory
    <EMComposition.memory>` attribute of the EMComposition is used by its `controller <EMComposition.controller>` to
    generate the `memory <EMMemoryMechanism.memory>` attribute of an `EMMemoryMechanism` that is used to retrieve
    entries from the `memory <EMComposition.memory>` attribute of the EMComposition.

.. _EMStorageMechanism_Creation:

Creating an EMStorageMechanism
--------------------------------------------

An EMStorageMechanism can be created directly by calling its constructor, but most commonly it is created
automatically when an `EMComposition` is created, as its `learning_mechanism <EMComposition.learning_mechanism>`
used to store entries in its `memory <EMComposition.memory>` of the EMComposition. The `memory_matrix` must be
specified (as a template for the shape of the entries to be stored, and of the `matrix <MappingProjection.matrix>`
parameters to which they are assigned. It must also have at least one, and usually several `fields
<EMStorageMechanism.fields>` specifications that identify the `OutputPort`\\s of the `ProcessingMechanism`\\s from
which it receives its `fields <EMStorageMechanism_Fields>`, and a `field_types <EMStorageMechanism.field_types>`
specification that inidicates whether each `field is a key or a value field <EMStorageMechanism_Fields>`.

.. _EMStorageMechanism_Structure:

Structure
---------

An EMStorageMechanism is identical to a `LearningMechanism` in all respects except the following:

  * it has no `input_source <LearningMechanism.input_source>`, `output_source <LearningMechanism.output_source>`,
    or `error_source <LearningMechanism.error_source>` attributes;  instead, it has the `fields
    <EMStorageMechanism.fields>` and `field_types <EMStorageMechanism.field_types>` attributes described below.

  * its `fields <EMStorageMechanism.fields>` attribute has as many *FIELDS* `field <EMStorage_mechanism.fields>`
    as there are `fields <EMStorageMechanism_Fields>` of an entry in its `memory_matrix
    <EMStorageMechanism.memory_matrix>` attribute;  these are listed in its `fields <EMStorageMechanism.fields>`
    attribute and serve as the `InputPort`\\s for the EMStorageMechanism;  each receives a `MappingProjection` from
    the `OutputPort` of a `ProcessingMechanism`, the activity of which constitutes the corresponding `field
    <EMStorageMechanism_Fields>` of the `entry <EMStorageMechanism_Entry>` to be stored in its `memory_matrix
    <EMStorageMechanism.memory_matrix>` attribute.

  * it has a `field_types <EMStorageMechanism.field_types>` attribute that specifies whether each `field
    <EMStorageMechanism_Fields>` is a `key or a value field <EMStorageMechanism_Fields>`.

  * it has a `memory_matrix <EMStorageMechanism.memory_matrix>` attribute that represents the full memory that the
    EMStorageMechanism is used to update.

  * it has a several *LEARNING_SIGNAL* `OutputPorts <OutputPort>` that each send a `LearningProjection` to the `matrix
    <MappingProjection.matrix>` parameter of a 'MappingProjection` that constitutes a `field <EMStorageMechanism_Fields>`
    of the `memory_matrix <EMStorageMechanism.memory_matrix>` attribute.

  * its `function <EMStorageMechanism.function>` is an `EMStorage` `LearningFunction`, that takes as its `variable
    <Function_Base.variable>` a list or 1d np.array with a length of the corresponding  *ACTIVATION_INPUT* InputPort;
    and it returns a `learning_signal <LearningMechanism.learning_signal>` (a weight matrix assigned to one of the 
    Mechanism's *LEARNING_SIGNAL* OutputPorts), but no `error_signal <LearningMechanism.error_signal>`.

  * its `decay_rate <EMStorageMechanism.decay_rate>`, a float in the interval [0,1] that is used to decay
    `memory_matrix <EMStorageMechanism.memory_matrix>` before an `entry <EMStorageMechanism_Entry>` is stored.

  * its `storage_prob <EMStorageMechanism.storage_prob>`, a float in the interval [0,1] is used in place of a
    LearningMechanism's `storage_prob <LearningMechanism.storage_prob>` to determine the probability that the 
    Mechanism will store its `variable <EMStorageMechanism.variable>` in its `memory_matrix
    <EMStorageMechanism.memory_matrix>` attribute each time it executes.

.. _EMStorageMechanism_Execution:

Execution
---------

An EMStorageMechanism executes in the same manner as standard `LearningMechanism`, however instead of modulating
the `matrix <MappingProjection.matrix>` Parameter of a `MappingProjection`, it replaces a row or column in each of
the `matrix <MappingProjection.matrix>` Parameters of the `MappingProjections <MappingProjection>` to which its
`LearningProjections <LearningProjection>` project with an item of its `variable <EMStorageMechanism.variable>` that
represents the corresponding `field <EMStorageMechanism.fields>`.


.. _EMStorageMechanism_Class_Reference:

Class Reference
---------------

"""

import numpy as np
from beartype import beartype
from typing import Literal

from psyneulink._typing import Optional, Union, Callable

from psyneulink.core.components.component import parameter_keywords
from psyneulink.core.components.functions.nonstateful.learningfunctions import EMStorage
from psyneulink.core.components.mechanisms.mechanism import Mechanism
from psyneulink.core.components.mechanisms.processing.objectivemechanism import ObjectiveMechanism
from psyneulink.core.components.mechanisms.modulatory.learning.learningmechanism import \
    ACTIVATION_INPUT, LearningMechanism, LearningMechanismError, LearningTiming, LearningType
from psyneulink.core.components.projections.projection import Projection, projection_keywords
from psyneulink.core.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.core.components.ports.inputport import InputPort
from psyneulink.core.components.ports.parameterport import ParameterPort
from psyneulink.core.components.ports.outputport import OutputPort
from psyneulink.core.globals.context import ContextFlags
from psyneulink.core.globals.keywords import \
    ADDITIVE, EM_STORAGE_MECHANISM, LEARNING, LEARNING_PROJECTION, MULTIPLICATIVE, MODULATION, \
    NAME, OVERRIDE, OWNER_VALUE, PROJECTIONS, REFERENCE_VALUE, VARIABLE
from psyneulink.core.globals.parameters import Parameter, check_user_specified
from psyneulink.core.globals.preferences.basepreferenceset import ValidPrefSet
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.core.globals.utilities import is_numeric, ValidParamSpecType, all_within_range

__all__ = [
    'EMStorageMechanism', 'EMStorageMechanismError',
]

# Parameters:

parameter_keywords.update({LEARNING_PROJECTION, LEARNING})
projection_keywords.update({LEARNING_PROJECTION, LEARNING})

MEMORY_MATRIX = 'memory_matrix'
FIELDS = 'fields'
FIELD_TYPES = 'field_types'
LEARNING_SIGNALS = 'learning_signals'

class EMStorageMechanismError(LearningMechanismError):
    pass


class EMStorageMechanism(LearningMechanism):
    """
    EMStorageMechanism(                       \
        variable,                             \
        fields,                               \
        field_types,                          \
        memory_matrix,                        \
        function=EMStorage,                   \
        decay_rate=0.0,                       \
        storage_prob=1.0,                     \
        learning_signals,                     \
        modulation=OVERRIDE,                  \
        params=None,                          \
        name=None,                            \
        prefs=None)

    Implements a `LearningMechanism` that modifies the `matrix <MappingProjection.matrix>` parameters of
    `MappingProjections <MappingProjection>` that implement its `memory_matrix <EMStorageMechanism.memory_matrix>`. 

    Arguments
    ---------

    variable : List or 2d np.array : default None
        each item of the 2d array specifies the shape of the corresponding `field <EMStorageMechanism_Fields>` of
        an `entry <EMStorageMechanism_Entry>`, that must be compatible (in number and type) with the `value 
        <InputPort.value>` of the corresponding item of its `fields <EMStorageMechanism.fields>`
        attribute (see `variable <EMStorageMechanism.variable>` for additional details).

    fields : List[OutputPort, Mechanism, Projection, tuple[str, Mechanism, Projection] or dict] : default None
        specifies the `OutputPort`\\(s), the `value <OutputPort.value>`\\s of which are used as the
        corresponding `fields <EMStorageMechanism_Fields>` of the `memory_matrix <EMStorageMechanism.memory_matrix>`;
        used to construct the Mechanism's `InputPorts <InputPort>`; must be the same lenghtt as `variable
        <EMStorageMechanism.variable>`.

    field_types : List[int] : default None
        specifies whether each item of `variable <EMStorageMechanism.variable>` corresponds to a `key or value field
        <EMStorageMechanism_Fields>` (see `field_types <EMStorageMechanism.field_types>` for additional details);
        must contain only 1's (for keys) and 0's (for values), with the same number of these as there are items in
        the `variable <EMStorageMechanism.variable>` and `fields <EMStorageMechanism.fields>` arguments.

    memory_matrix : List or 2d np.array : default None
        specifies the shape of the `memory <EMStorageMechanism_Memory>` used to store an `entry
        <EMStorageMechanism_Entry>` (see `memory_matrix <EMStorageMechanism.memory_matrix>` for additional details).

    function : LearningFunction or function : default EMStorage
        specifies the function used to assign each item of the `variable <EMStorageMechanism.variable>` to the
        corresponding `field <EMStorageMechanism_Fields>` of the `memory_matrix <EMStorageMechanism.memory_matrix>`.
        It must take as its `variable <EMSorage.variable> argument a list or 1d array of numeric values
        (the "activity vector") and return a list, 2d np.array or np.matrix for the corresponding `field
        <EMStorageMechanism_Fields>` of the `memory_matrix <EMStorageMechanism.memory_matrix>` (see `function
        <EMStorageMechanism.function>` for additional details).

    learning_signals : List[ParameterPort, Projection, tuple[str, Projection] or dict] : default None
        specifies the `ParameterPort`\\(s) of the `MappingProjections <MappingProjection>` that implement the `memory
        <EMStorageMechanism_Memory>` in which the `entry <EMStorageMechanism_Entry>` is stored; there must the same
        number of these as `fields <EMStorageMechanism.fields>`, and they must be specified in the sqme order.

    decay_rate : float : default 0.0
        specifies the rate at which `entries <EMStorageMechanism_Entry>` in the `memory_matrix
        <EMStorageMechanism.memory_matrix>` decays (see `decay_rate <EMStorageMechanism.decay_rate>` for additional
        details).

    storage_prob : float : default None
        specifies the probability with which the current entry is stored in the EMSorageMechanism's `memory_matrix
        <EMStorageMechanism.memory_matrix>` (see `storage_prob <EMStorageMechanism.storage_prob>` for details).

    Attributes
    ----------

    # FIX: FINISH EDITING:

    variable : 2d np.array
        each item of the 2d array is used as a template for the shape of each the `fields
        <EMStorageMechanism_Fields>` that  comprise and `entry <EMStorageMechanism_Entry>` in the `memory_matrix
        <EMStorageMechanism.memory_matrix>`, and that must be compatible (in number and type) with the `value
        <OutputPort.value>` of the item specified the corresponding itme of its `fields <EMStorageMechanism.fields>`
        attribute. The values of the `variable <EMStorageMechanism.variable>` are assigned to the `memory_matrix
        <EMStorageMechanism.memory_matrix>` by the `function <EMStorageMechanism.function>`.

    fields : List[OutputPort, Mechanism, Projection, tuple[str, Mechanism, Projection] or dict] : default None
        the `OutputPort`\\(s) used to get the value for each `field <EMStorageMechanism_Fields>` of
        an `entry <EMStorageMechanism_Entry>` of the `memory_matrix <EMStorageMechanism.memory_matrix>` attribute.

    field_types : List[int or tuple[slice]]
        contains a list of indicators of whether each item of `variable <EMStorageMechanism.variable>`
        and the corresponding `fields <EMStorageMechanism.fields>` are key (1) or value (0) fields.
        (see `fields <EMStorageMechanism_Fields>` for additional details).

    learned_projections : List[MappingProjection]
        list of the `MappingProjections <MappingProjection>`, the `matrix <MappingProjection.matrix>` Parameters of
        which are modified by the EMStorageMechanism.

    function : LearningFunction or function : default EMStorage
        the function used to assign the value of each `field <EMStorageMechanism.fields>` to the corresponding entry
        in `memory_matrix <EMStorageMechanism.memory_matrix>`.  It must take as its `variable <EMSorage.variable>`
        argument a list or 1d array of numeric values (an `entry <EMStorage.entry`) and return a list, 2d np.array or
        np.matrix assigned to the corresponding `field <EMStorageMechanism_Fields>` of the `memory_matrix
        <EMStorageMechanism.memory_matrix>`.

    decay_rate : float : default 0.0
        determines the rate at which `entries <EMStorageMechanism_Entry>` in the `memory_matrix
        <EMStorageMechanism.memory_matrix>` decay;  the decay rate is applied to `memory_matrix
        <EMStorageMechanism.memory_matrix>` before it is updated with the new `entry <EMStorageMechanism_Entry>`.

    storage_prob : float
        specifies the probability with which the current entry is stored in the EMSorageMechanism's `memory_matrix
        <EMStorageMechanism.memory_matrix>`.

    learning_signals : List[LearningSignal]
        list of all of the `LearningSignals <LearningSignal>` for the EMStorageMechanism, each of which
        sends a `LearningProjection` to the `ParameterPort`\\(s) for the `MappingProjections
        <MappingProjection>` that implement the `memory <EMStorageMechanism_Memory>` in which the `entry
        <EMStorageMechanism_Entry>` is stored.  The `value <LearningSignal.value>` of each LearningSignal is
        used by its `LearningProjection` to modify the `matrix <MappingProjection.matrix>` parameter of the
        MappingProjection to which that projects.

    learning_projections : List[LearningProjection]
        list of all of the LearningProjections <LearningProjection>` from the EMStorageMechanism, listed
        in the order of the `LearningSignals <LearningSignal>` to which they belong (that is, in the order they are
        listed in the `learning_signals <EMStorageMechanism.learning_signals>` attribute).

    output_ports : ContentAddressableList[OutputPort]
        list of the EMStorageMechanism's `OutputPorts <OutputPort>`, beginning with its
        `learning_signals <EMStorageMechanism.learning_signals>`, and followed by any additional
        (user-specified) `OutputPorts <OutputPort>`.

    output_values : 2d np.array
        the first items are the `value <OutputPort.value>`\\(s) of the LearningMechanism's `learning_signal
        <EMStorageMechanism.learning_signal>`\\(s), followed by the `value <OutputPort.value>`(s)
        of any additional (user-specified) OutputPorts.

    """

    componentType = EM_STORAGE_MECHANISM
    className = componentType
    suffix = " " + className

    class Parameters(LearningMechanism.Parameters):
        """
            Attributes
            ----------

                decay_rate
                    see `decay_rate <EMStorageMechanism.decay_rate>`

                    :default value: 0.0
                    :type: ``float``


                fields
                    see `fields <EMStorageMechanism.fields>`

                    :default value: None
                    :type: ``list``

                field_types
                    see `field_types <EMStorageMechanism.field_types>`

                    :default value: None
                    :type: ``list``

                memory_matrix
                    see `memory_matrix <EMStorageMechanism.memory_matrix>`

                    :default value: None
                    :type: ``np.ndarray``

                function
                    see `function <EMStorageMechanism.function>`

                    :default value: `EMStorage`
                    :type: `Function`

                input_ports
                    see `fields <EMStorageMechanism.fields>`

                    :default value: None
                    :type: ``list``
                    :read only: True

                output_ports
                    see `learning_signals <EMStorageMechanism.learning_signals>`

                    :default value: None
                    :type: ``list``
                    :read only: True

                storage_prob
                    see `storage_prob <EMStorageMechanism.storage_prob>`

                    :default value: 1.0
                    :type: ``float``

        """
        # input_ports = Parameter([],
        #                         stateful=False,
        #                         loggable=False,
        #                         read_only=True,
        #                         structural=True,
        #                         parse_spec=True,
        #                         # constructor_argument='fields',
        #                         )
        fields = Parameter([],
                                stateful=False,
                                loggable=False,
                                read_only=True,
                                structural=True,
                                parse_spec=True,
                                )
        field_types = Parameter([],
                                    stateful=False,
                                    loggable=False,
                                    read_only=True,
                                    structural=True,
                                    parse_spec=True,
                                    dependiencies='fields')
        function = Parameter(EMStorage, stateful=False, loggable=False)
        storage_prob = Parameter(1.0, modulable=True)
        storage_prob = Parameter(1.0, modulable=True)
        decay_rate = Parameter(0.0, modulable=True)
        modulation = OVERRIDE
        output_ports = Parameter([],
                                 stateful=False,
                                 loggable=False,
                                 read_only=True,
                                 structural=True,
                                 # constructor_argument='learning_signals'
                                 )
        learning_signals = Parameter([],
                                     stateful=False,
                                     loggable=False,
                                     read_only=True,
                                     structural=True)
        learning_type = LearningType.UNSUPERVISED
        learning_timing = LearningTiming.LEARNING_PHASE

    # FIX: WRITE VALIDATION AND PARSE METHODS FOR THESE
    def _validate_field_types(self, field_types):
        if not len(field_types) or len(field_types) != len(self.fields):
            return f"must be specified with a number of items equal to " \
                   f"the number of fields specified {len(self.fields)}"
        if not all(item in {1,0} for item in field_types):
            return f"must be a list of 1s (for keys) and 0s (for values)."


    def _validate_storage_prob(self, storage_prob):
        storage_prob = float(storage_prob)
        if not all_within_range(storage_prob, 0, 1):
            return f"must be a float in the interval [0,1]."

    def _validate_decay_rate(self, decay_rate):
        decay_rate = float(decay_rate)
        if not all_within_range(decay_rate, 0, 1):
            return f"must be a float in the interval [0,1]."


    classPreferenceLevel = PreferenceLevel.TYPE

    @check_user_specified
    @beartype
    def __init__(self,
                 default_variable: Union[list, np.ndarray],
                 fields: Union[list, tuple, dict, OutputPort, Mechanism, Projection] = None,
                 field_types: list = None,
                 memory_matrix: Union[list, np.ndarray] = None,
                 function: Optional[Callable] = EMStorage,
                 learning_signals: Union[list, dict, ParameterPort, Projection, tuple] = None,
                 modulation: Optional[Literal[OVERRIDE, ADDITIVE, MULTIPLICATIVE]] = OVERRIDE,
                 decay_rate: Optional[float] = 0.0,
                 storage_prob: Optional[float] = 1.0,
                 params=None,
                 name=None,
                 prefs: Optional[ValidPrefSet] = None,
                 **kwargs
                 ):

        # # USE FOR IMPLEMENTATION OF deferred_init()
        # # Store args for deferred initialization
        # self._init_args = locals().copy()
        # self._init_args['context'] = self
        # self._init_args['name'] = name

        # # Flag for deferred initialization
        # self.initialization_status = ContextFlags.DEFERRED_INIT
        # self.initialization_status = ContextFlags.DEFERRED_INIT

        # self._storage_prob = storage_prob
        # self.num_key_fields = len([i for i in field_types if i==0])

        super().__init__(default_variable=default_variable,
                         fields=fields,
                         field_types=field_types,
                         memory_matrix=memory_matrix,
                         function=function,
                         modulation=modulation,
                         decay_rate=decay_rate,
                         storage_prob=storage_prob,
                         learning_signals=learning_signals,
                         params=params,
                         name=name,
                         prefs=prefs,
                         **kwargs
                         )

    def _validate_variable(self, variable, context=None):
        """Validate that variable has only one item: activation_input.
        """

        # Skip LearningMechanism._validate_variable in call to super(), as it requires variable to have 3 items
        variable = super(LearningMechanism, self)._validate_variable(variable, context)

        # Items in variable should be 1d and have numeric values
        if not (all(np.array(variable)[i].ndim == 1 for i in range(len(variable))) and is_numeric(variable)):
            raise EMStorageMechanismError(f"Variable for {self.name} ({variable}) must be "
                                          f"a list or 2d np.array containing 1d arrays with only numbers.")
        return variable

    def _validate_params(self, request_set, target_set=None, context=None):

        # Ensure that the shape of variable is equivalent to an entry in memory_matrix
        if MEMORY_MATRIX in request_set:
            memory_matrix = request_set[MEMORY_MATRIX]
            # Items in variable should have the same shape as memory_matrix
            if memory_matrix[0].shape != np.array(self.variable).shape:
                raise EMStorageMechanismError(f"The 'variable' arg for {self.name} ({variable}) must be "
                                              f"a list or 2d np.array containing entries that have the same shape "
                                              f"({memory_matrix.shape}) as an entry (row) in 'memory_matrix' arg.")

        # Ensure the number of fields is equal to the number of items in variable
        if FIELDS in request_set:
            fields = request_set[FIELDS]
            if len(fields) != len(self.variable):
                raise EMStorageMechanismError(f"The 'fields' arg for {self.name} ({fields}) must have the same "
                                              f"number of items as its variable arg ({len(self.variable)}).")

        # Ensure the number of field_types is equal to the number of fields
        if FIELD_TYPES in request_set:
            field_types = request_set[FIELD_TYPES]
            num_keys = len([i for i in field_types if i==0])
            if len(field_types) != len(fields):
                raise EMStorageMechanismError(f"The 'field_types' arg for {self.name} ({field_types}) must have "
                                              f"the same number of items as its 'fields' arg ({len(fields)}).")

        # Ensure the number of learning_signals is equal to the number of fields + number of keys
        if LEARNING_SIGNALS in request_set:
            learning_signals = request_set[LEARNING_SIGNALS]
            if len(learning_signals) != len(fields) + num_keys:
                raise EMStorageMechanismError(f"The 'learning_signals' arg for {self.name} ({learning_signals}) "
                                              f"must have the same number of items as its variable arg "
                                              f"({len(self.variable)}).")

        # Ensure shape of memory_matrix is equal to the shape of the aggregated matrices for learning_signals
        learning_signals = np.array([learning_signal.parameters.matrix._get(context)
                                           for learning_signal in learning_signals[num_keys:]])
        if (learning_signals.shape[0] != memory_matrix.shape[1]
                or learning_signals.shape[1] != memory_matrix.shape[0]
                or learning_signals.shape[2] != memory_matrix.shape[2]):
            raise EMStorageMechanismError(f"The shape ({learning_signals.shape}) of the matrices for the Projections "
                                          f"in the 'learning_signals' arg of {self.name} do not match the shape of the "
                                          f"'memory_matrix' arg {memory_matrix.shape}).")

    def _instantiate_input_ports(self, input_ports=None, reference_value=None, context=None):
        """Override LearningMechanism to instantiate an InputPort for each field"""
        input_ports = [{NAME: f"KEY_INPUT_{i}" if self.field_types[i] == 1 else f"VALUE_INPUT_{i}",
                        VARIABLE: self.variable[i],
                        PROJECTIONS: field}
                       for i, field in enumerate(self.fields)]
        return super()._instantiate_input_ports(input_ports=input_ports, context=context)

    def _instantiate_output_ports(self, output_ports=None, reference_value=None, context=None):
        # FIX: SHOULD HAVE SPECS FROM learning_signals ARG HERE
        learning_signal_dicts = []
        for i, learning_signal in enumerate(self.learning_signals):
            learning_signal_dicts.append({NAME: f"LEARNING_SIGNAL_{i}",
                                         VARIABLE: (OWNER_VALUE, i),
                                         REFERENCE_VALUE: self.value[i],
                                         MODULATION: self.modulation,
                                         PROJECTIONS: learning_signal.parameter_ports['matrix']})
        self.parameters.learning_signals._set(learning_signal_dicts, context)

        return super()._instantiate_output_ports(context=context)

    def _parse_function_variable(self, variable, context=None):
        # Function expects a single field (one item of Mechanism's variable) at a time
        if self.initialization_status == ContextFlags.INITIALIZING:
            # During initialization, Mechanism's variable is its default_variable,
            # which has all field's worth of input, so need get a single one here
            return variable[0]
        # During execution, _execute passes only a entry (item of variable) at a time,
        #    so can just pass that along here
        return variable

    def _execute(self,
                 variable=None,
                 context=None,
                 runtime_params=None):
        """Execute EMStorageMechanism. function and return learning_signals

        :return: List[2d np.array] self.learning_signal
        """

        num_key_fields = len([i for i in self.field_types if i==0])
        # Note: learing_signals have afferents to match_nodes then retrieval_nodes
        match_node_afferents = self.learning_signals[:num_key_fields]
        retrieval_node_afferents = self.learning_signals[num_key_fields:]

        value = []
        for i, learning_signal in enumerate(match_node_afferents):
            matrix = learning_signal.parameters.matrix._get(context)
            entry = learning_signal.sender.value
            value.append(super(LearningMechanism, self)._execute(variable=entry,
                                                                 memory_matrix=matrix,
                                                                 context=context,
                                                                 runtime_params=runtime_params))
        for i, learning_signal in enumerate(retrieval_node_afferents):
            matrix = learning_signal.parameters.matrix._get(context)
            entry = variable[i]
            # FIX: MAY NEED TO PASS AXIS HERE
            value.append(super(LearningMechanism, self)._execute(variable=entry,
                                                                 memory_matrix=matrix,
                                                                 context=context,
                                                                 runtime_params=runtime_params))

        self.parameters.value._set(value, context)

        return value

    def _update_output_ports(self, runtime_params=None, context=None):
        """Update the weights for the AutoAssociativeProjection for which this is the EMStorageMechanism

        Must do this here, so it occurs after LearningMechanism's OutputPort has been updated.
        This insures that weights are updated within the same trial in which they have been learned
        """

        super()._update_output_ports(runtime_params, context)
        if self.parameters.learning_enabled._get(context):
            learned_projection = self.activity_source.recurrent_projection
            old_exec_phase = context.execution_phase
            context.execution_phase = ContextFlags.LEARNING
            learned_projection.execute(context=context)
            context.execution_phase = old_exec_phase

    @property
    def activity_source(self):
        return self.input_port.path_afferents[0].sender.owner
