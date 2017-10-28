# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# *******************************************  InputState *****************************************************
#
"""

Overview
--------

An InputState receives the input to a Mechanism provided by the Projections to that Mechanism from others in a Process
or System.  If the InputState belongs to an `ORIGIN` Mechanism (see
`role of Mechanisms in Processes and Systems <Mechanism_Role_In_Processes_And_Systems>`), then it receives the input
specified when that Process or System is `run <Run>`.  The Projections received by an InputState are
listed in its `path_afferents <InputState.path_afferents>` attribute. Its
`function <InputState.function>` combines the values of these inputs, and the result is assigned to an item
corresponding to the InputState in the owner Mechanism's :keyword:`variable <Mechanism_Base.variable>` and
`input_values <Mechanism_Base.input_values>` attributes  (see `Mechanism InputStates <Mechanism_InputStates>`
for additional details about the role of InputStates in Mechanisms).


.. _InputState_Creation:

Creating an InputState
----------------------

An InputState can be created by calling its constructor, but in general this is not necessary as a Mechanism can
usually automatically create the InputState(s) it needs when it is created.  For example, if the Mechanism is
being created within the `pathway <Process.pathway` of a `Process`, its InputState will be created and  assigned
as the `receiver <MappingProjection.receiver>` of a `MappingProjection` from the  preceding `Mechanism <Mechanism>` in
the `pathway <Process.pathway>`.

.. _InputState_Deferred_Initialization:

An InputState must be owned by a `Mechanism <Mechanism>`.  When InputState is specified in the constructor for a
Mechanism (see `below <InputState_Specification>`), it is automatically assigned to that Mechanism as its owner. If
the InputState is created directly, its `owner <InputState.owner>` can specified in the **owner**  argument of its
constructor; otherwise, its initialization will be `deferred <State_Deferred_Initialization>` until it is assigned
to an owner using the owner's `add_states` method.

.. _InputState_Primary:

Primary InputState
~~~~~~~~~~~~~~~~~~~

Every Mechanism has at least one InputState, referred to as its *primary InputState*.  If InputStates are not
`explicitly specified <InputState_Specification>` for a Mechanism, a primary InputState is automatically created
and assigned to its `input_state <Mechanism_Base.input_state>` attribute (note the singular),
and also to the first entry of the Mechanism's `input_states <Mechanism_Base.inpput_states>` attribute
(note the plural).  The `value <InputState.value>` of the primary InputState is assigned as the first (and often
only) item of the Mechanism's `input_values <Mechanism_Base.input_values>` attribute, which is the first item of the
Mechanism's `variable <Mechanism_Base.variable>` attribute.

.. _InputState_Specification:

InputState Specification
~~~~~~~~~~~~~~~~~~~~~~~~

If one or more custom InputStates need to be specified for a `Mechanism <Mechanism>` when it is created, or the type
of Mechanism requires their specification, this can be done in the **input_states** argument of the Mechanism's
constructor, or in an *INPUT_STATES* entry of a parameter dictionary assigned to the constructor's **params**
argument.  The latter takes precedence over the former (that is, if an *INPUT_STATES* entry is included in the
parameter dictionary, any specified in the **input_states** argument are ignored).

.. note::
    Assigning InputStates to a Mechanism in its constructor **replaces** any that are automatically generated for that
    Mechanism (i.e., those that it creates for itself by default).  If any of those need to be retained, they must be
    explicitly specified in the list assigned to the **input_states** argument or the *INPUT_STATES* entry of
    the parameter dictionary in the **params** argument).  The number of InputStates specified must also be equal
    to the number of items in the Mechanism's <variable <Mechanism_Base.variable>` attribute.

InputStates can also be **added** to a Mechanism, using the Mechanism's `add_states` method.  However, this has
consequences for the Mechanism's `variable <Mechanism_Base.variable>` and possibly its relationship to the Mechanism's
`function <Mechanism_Base.function>` (these are discussed `below <InputStates_Mechanism_Variable_and_Function>`).
If the name of an InputState added to a Mechanism is the same as one that already exists, its name will be suffixed
with a numerical index (incremented for each InputState with that name), and the InputState will be added to the list
(that is, it will *not* replace ones that were already created).

Specifying an InputState can be done in a variety of ways, listed below, that include specification of its attributes
and/or the State(s) that project to it.  To create multiple InputStates, their specifications can be included in a
list, or in State specification dictionary as described below. Any of the following can be used to specify an
InputState:

## CONSOLIDATE DESCRIPTION OF VARIABLE ASSIGNMENT / COMPATIBILITY SPECIFICATION

    * existing **InputState object** or the name of one -- its `value <InputState.value>` must be compatible with
      the item of the owner Mechanism's `variable <Mechanism_Base.variable>` to which it will be assigned;  if it is
      specified in the **input_states** argument, this is item of the Mechanism's `variable <Mechanism_Base.variable>`
      corresponding to the place of the specification in the **input_states** list; otherwise it must correspond to the
      first item of the owner's `variable <Mechanism_Base.variable>`.
    ..
    * **InputState class**, keyword *INPUT_STATE*, or a string -- this creates a default InputState; if it is
      specified in an **input_states** argument, its `variable <InputState.variable>` is formatted using the item of
      the owner Mechanism's `variable <Mechanism_Base.variable>` corresponding to the place of the specification in the
      **input_states** list; otherwise the first item of the owner's `variable <Mechanism_Base.variable>` is used.
      If the InputState class name or *INPUT_STATE* keyword is used, a default name is assigned to the State;  if a
      string is specified, it is used as the name of the InputState (see :ref:`naming conventions <LINK>`).
    ..
    * **value** -- this creates a default InputState using the specified value as InputState's `variable
      <InputState.variable>`. This must be compatible with the item of the owner Mechanism's `variable
      <Mechanism_Base.variable>`, in the same manner as an existing InputState (see above).
    ..
    * **string** -- this creates a default `InputState` using the string as its name, and a `variable
      <InputState.variable>` formatted in the same manner as an InputState class, keyword or string specification
      (see above).  This can be used as a "placemarker" for an InputState that will be assigned its Projection(s) at
      a later time.

    .. _InputState_OutputState_Specification:

    * **OutputState** -- a reference to an existing `OutputState <OutputState>` of a Mechanism;  this creates an
      InputState with a `variable <InputState.variable>` that matches the format of the `value <OutputState.value>`
      of the specified OutputState, and a `MappingProjection` between them using an *IDENTITY_MATRIX*.

    * **Mechanism** -- the Mechanism's `primary OutputState <OutputState_Primary>` is used, and an `InputState` and
      `MappingProjection` are created as for an OutputState specification (see above).
    ..
    * **Projection object**.  This creates a default InputState and assigns it as the `Projection's
      <Projection>` `receiver <Projection.receiver>`;  the InputState's `variable <InputState.variable>` is
      formatted in the same manner an InputState class, keyword or string

using the first item of the owner Mechanism's
      `variable <Mechanism_Base.variable>` as the InputState's `variable <InputState.variable>`,

      The Projection's `value
      <Projection.value>` must be compatible with the InputState's `variable <InputState.variable>`.
    ..
    * **Projection subclass** -- this creates a default InputState using the first item of the owner Mechanism's
      `variable <Mechanism_Base.variable>` as the InputState's `variable <InputState.variable>`, and a `Projection
      <Projection>` of the specified type to the InputState using its `variable <InputState.variable>` as the template
      for the Projection's `value <Projection.value>`.  Since the Projection's `sender <Projection.sender>` is
      unspecified, its `initialization is deferred <Projection_Deferred_Initialization>`.  In some cases, initialization
      can happen automatically -- for example, when a `ControlProjection` is created for the parameter of a Mechanism
      that is included in a `System`, a `ControlSignal` is created as the Projection's `sender <Projection.sender>`
      that is added to the System's `controller System_Base.controller` (see `System_Control`).  However, for cases
      in which `deferred initialization <Component_Deferred_Init>` is not automatically completed, the Projection will
      not be operational until its `sender <Projection.sender>` has been specified and its initialization completed.

    .. _InputState_Specification_Dictionary:

    * A **State specification dictionary**.  This can be used to specify one or more InputStates, depending on
      the entries included.  In the simplest case, it is used to specify a single InputState using any of the entries
      that can be included in a `State specification dictionary <State_Specification>`, as well as well as the
      following two entries specific to an InputState:
      ..
      * *WEIGHT*:<number>
          the value must be an integer or float, and is assigned as the value of the InputState's `weight
          <InputState.weight>` attribute  (see `InputState_Weights_And_Exponents`);  this takes precedence over any
          specification in the **weight** argument of the InputState's constructor.
      ..
      * *EXPONENT*:<number>
          the value must be an integer or float, and is assigned as the value of the InputState's `exponent
          <InputState.exponent>` attribute  (see `InputState_Weights_And_Exponents`);  this takes precedence over any
          specification in the **exponent** argument of the InputState's constructor.

      .. _InputState_Projections_Specification:

      If a *PROJECTIONS* entry is included, it can include one or more `OutputStates <OutputState>` and/or
      `PathwayProjections <PathwayProjection>` the InputState should receive from them, as well as any
      `ModulatorySignals <ModulatorySignal>` and/or the the `ModulatoryProjections <ModulatoryProjection>` it should
      receive from those.

      Alternatively, an InputState specification dictionary can be used to specify multiple InputStates.  If it includes
      one or more keys that are strings not recognized as a keyword, then the keys are treated as the names of the
      InputStates to be created, and the value of each as its specification.

      Finally a dictionary can be used to specify a set of InputStates each of which receives a Projections from
      an OutputState, all of which belong to the same Mechanism;  this is a convenience format, that allows those
      OutputStates to be specified by their names.  This is done using the following pair of entries:

        * *MECHANISM*:<`Mechanism <Mechanism>`>
            this entry is used to specify the Mechanism to which the OutputStates belong. If it is appears in the
            dictionary, then all of the items specified in the OUTPUT_STATES entry (see below) are assumed to be
            from this Mechanism.  If the dictionary contains this entry but no *OUTPUT_STATES* entry, then the
            Mechanism's `primary OutputState <OutputState_Primary>` is used.
        ..
        * *OUTPUT_STATES*:<List[<str or any of the other forms of specifications for an OutputState>, ...]>
            this must be used with a *MECHANISM* entry, to list one or more of its OutputStates by their names;
            if a string appears in the list that is not the name of an OutputState of the Mechanism in the *MECHANISM*
            entry, it is treated as a string specification (i.e., for the creation of an InputState with that name,
            but that is not assigned any Projection).  The list can also contain, in the place of an OutputState's
            name, an InputState specification subdictionary;  this can be used to specify attributes of the InputState
            (e.g., its weight and/or exponent), in addition to the OutputState and/or MappingProjection from it to the
            InputState (specified in the *PROJECTIONS* entry of the subdictionary).

        If an InputState specification dictionary containing a *MECHANISM* and *OUTPUT_STATES* entry also contains
        other entries (e.g., *WEIGHTS* or *EXPONENTS* entries), their values are applied to all of the InputStates
        created for the OutputStates specified in the *OUTPUT_STATES* entry, except any that use a specification
        dictionary of their own containing the same entry.  For example, if a *WEIGHT* entry is included
        along with the *MECHANISM* and *OUTPUT_STATES* entries, then the specified weight is assigned to the
        `weight <InputState.weight>` attribute of the InputStates created for each of the OutputStates in the
        *OUTPUT_STATES* list, except any that are specified in the list using a specification subdictionary that
        includes its own *WEIGHT* entry;  in that case, the latter is assigned to the `weight <InputState.weight>`
        attribute created for (only) that OutputState, while the *WEIGHT* entry in the outer dictionary is used for
        all of the other InputStates.


    .. _InputState_Tuple_Specification:

COMMENT:
[CONVENIENCE FORMATS]:
    10/3/17 - CHANGE THIS SO THAT: 1) 2ND ITEM OF 2-ITEM TUPLE CAN BE ANY KIND OF PROJECTIONS (LIST??)
                                   2) ConnectionTuple CAN BE USED (MOVE EXAMPLES HERE FROM OBJECTIVE MECHANISM??

    * **a tuple specification** -- this can be used to compactly specify a monitored OutputState coupled with
      the MappingProjection (or its `matrix <MappingProjection.matrix>`) used to project to the corresponding
      InputState, and/or a `weight and exponent <ObjectiveMechanism_Weights_and_Exponents>` for that InputState;
      the latter can be used specify how the value of the OutputState is combined with others by the ObjectiveMechanism
      to determine its `outcome <ObjectiveMechanism_Function>` (see `example
      <ObjectiveMechanism_Tuple_Specification_Example>`).  It can take any of the forms of a `tuple specification
      <InputState_Tuple_Specification>` for an InputState.
COMMENT

    * **2-item tuple** -- the first item can be either a value (specifying the `variable <InputState.variable>` for
      the InputState, or a Mechanism or OutputState specification (see above) indicating the sender of a Projection
      to it; the second item must be a `Projection <Projection>` specification.  This creates an InputState and the
      specified Projection; it assigns the InputState as the Projection's `receiver <Projection.receiver>` and,
      if the first item specifies an OutputState, that is assigned as the Projection's `sender <Projection.sender>`.

    * **ConnectionTuple** -- this is an expanded version of the 2-item tuple that allows the specification of the
      `weight <InputState.weight>` and/or `exponent <InputState.exponent>` attributes of the InputState, as well as
      a Projection to it.  Each tuple must have the first three following items in the order listed, and can include
      the fourth:

        * **State specification** -- specifies either the `variable <InputState.variable>` of the InputState, or an
          OutputState that should project to it (which must be consistent with the Projection specified in the
          fourth item if that is included -- see below).
        |
        * **weight** -- must be an integer or a float; multiplies the `value <InputState.value>` of the InputState
          before it is combined with others by the Mechanism's `function <Mechanism.function>` (see
          `ObjectiveMechanism_Weights_and_Exponents` for examples).
        |
        * **exponent** -- must be an integer or float; exponentiates the `value <InputState.value>` of the InputState
          before it is combined with others by the ObjectiveMechanism's `function <ObjectiveMechanism.function>` (see
          `ObjectiveMechanism_Weights_and_Exponents` for examples).
        |
        * **Projection specification** (optional) -- this can be any `specification for a Projection
          <Projection_In_Context_Specification>`;  the `value <Projection.value>` of the Projection
          determines the format of the InputState's `variable <InputState.variable>`.

    .. note::
       In all cases, the resulting `value <InputState.value>` of the InputState must be compatible with (that is, have
       the same number and type of elements as) as the corresponding item of its owner Mechanism's
       `variable <Mechanism_Base.variable>` attribute (see `below <InputStates_Mechanism_Variable_and_Function>`).

COMMENT:
   CHECK THIS:
             reference_value IS THE ITEM OF variable CORRESPONDING TO THE InputState
COMMENT

The values of a Mechanism's InputStates are assigned as items in its `input_values <Mechanism_Base.input_values>`
attribute, in the order in which they are assigned in the constructor and/or added using the Mechanism's `add_states`
method, and in which they are listed in the Mechanism's `input_states <Mechanism_Base.input_states>` attribute.  Note
that a Mechanism's `input_value <Mechanism_Base.input_value>` attribute has the same information as the
Mechanism's `variable <Mechanism_Base.variable>`, but in a list rather than an ndarray.


.. _InputStates_Mechanism_Variable_and_Function:

COMMENT:
*************************************************************************************************************

FROM ObjectiveMechanism

.. _ObjectiveMechanism_InputStates:

InputStates
^^^^^^^^^^^

An ObjectiveMechanism creates one `InputState` for each item in its **input_states** argument. By default,
it uses the `value <OutputState.value>` of a monitored OutputState to determine the `variable
<InputState.variable>` of the corresponding InputState.  However, this can be modified (see
`ObjectiveMechanism_Monitored_Output_States_Examples` below), using any of the following:

* **default_variable** argument of the ObjectiveMechanism's constructor -- this is used to determine the format for
  the `variable <InputState.variable>` of each `InputState <InputState>` created for the corresponding `OutputState
  <OutputState>` in the **monitored_output_states* argument.  If this is used, the number of items in the outermost
  dimension (axis 0) of the  **variable** specification must match the number of items specified in the
  **monitored_output_states** argument.

* *VARIABLE* entry of a State specification dictionary in the **monitored_output_state** argument (see above) --
  note that the value of the entry specifies the `variable <InputState.variable>` attribute of the
  *InputState* created for the monitored OutputState, and does not affect to the monitored OutputState itself.

* *Projection* entry of a `tuple specification <InputState_Tuple_Specification>` -- the dimensions of the Projection's
  matrix (specifically, the number of its dimensions minus the number of dimensions of the `value <OutputState.value>`
  of the OutputState from which it projects) determines the size of the `variable <InputState.variable>` attribute of
  the InputState created.

.. note::
   The **monitored_output_states** argument of an ObjectiveMechanism serves the same purpose as the **input_states**
   argument for a standard `Mechanism`, and any specifications beyond those that identify the OutputStates are used
   to specify the attributes of the corresponding InputStates.

.. _MappingProjections:

MappingProjections
^^^^^^^^^^^^^^^^^^

A `MappingProjection` is created automatically from each OutputState specified in **monitored_output_states**
to the InputState of the ObjectiveMechanism created for it, using `AUTO_ASSIGN_MATRIX` as the `matrix
<MappingProjection.matrix>` parameter. However, if a specification in the **monitored_output_states** argument cannot be
resolved to an instantiated OutputState at the time the ObjectiveMechanism is created, no MappingProjection is
assigned, and this must be done by some other means; any specifications in the `monitored_output_states
<ObjectiveMechanism.monitored_output_states>` attribute that are not associated with an instantiated OutputState at
the time the ObjectiveMechanism is executed are ignored.

*************************************************************************************************************
COMMENT



InputStates and a Mechanism's `variable <Mechanism_Base.variable>` and `function <Mechanism_Base.function>` Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Mechanism must have one InputState for each item of its `variable <Mechanism_Base.variable>` (see
`Mechanism <Mechanism_Variable>`).  The value specified in the **variable** or **size** arguments of the
Mechanism's constructor determines the number of items in its `variable <Mechanism_Base>`, which ordinarily matches
the size (along axis 0) of the input expected by its `function <Mechanism_Base.function>`.  Therefore,
if any InputStates are specified in the constructor, the number of them must match the number of items in
`variable <Mechanism_Base.variable>`.  InputStates can be added to a Mechanism using its `add_states` method;  this
extends its `variable <Mechanism_Base.variable>` by a number of items equal to the number of InputStates
added, and each new item is assigned a value compatible with the `value <InputState.value>` of the corresponding
InputState added.

.. note::
    Adding InputStates to a Mechanism using its `add_states` method may introduce an incompatibility with the
    Mechanism's `function <Mechanism_Base.function>`, which takes the Mechanism's `variable <Mechanism_Base.variable>`
    as its input; such an incompatibility will generate an error.  It is the user's responsibility to ensure that the
    explicit assignment of InputStates to a Mechanism is coordinated with the assignment of its
    `function <Mechanism_Base.function>`, so that the total number of InputStates (listed in the Mechanism's
    `input_states <Mechanism_Base.input_states>` attribute matches the number of items expected for the input to the
    function specified in the Mechanism's `function <Mechanism_Base.function>` attribute  (i.e., its size along axis 0).


COMMENT:
However, if any InputStates are specified in its **input_states** argument or the *INPUT_STATES* entry of parameter
dictionary assigned to its **params** argument, then the number of InputStates specified determines the number of
items in the owner Mechanism's `variable <Mechanism_Base.variable>`, superseding any specification(s) in the
**variable** and/or **size** arguments of the constructor.  Each item of the `variable <Mechanism_Base.variable>` is
assigned a value compatible with the `value <InputState.value>` of the corresponding InputState). Similarly, if any
InputStates are added to a Mechanism using its `add_states` method, then its `variable <Mechanism_Base.variable>`
attribute is extended by a number of items equal to the number of InputStates added; and, again, each item is
assigned a value compatible with the `value <InputState.value>` of the corresponding InputState.

with one exception: If the Mechanism's `variable <Mechanism_Base.variable>` has more than one item, it may still be
assigned a single InputState;  in that case, the `value <InputState.value>` of that InputState must have the same
number of items as the Mechanisms's `variable <Mechanism_Base.variable>`.
COMMENT


.. _InputState_Projections:

Projections
~~~~~~~~~~~

XXX***??? AUGMENT PER ABOVE

When an InputState is created, it can be assigned one or more `Projections <Projection>`, using either the
**projections** argument of its constructor, or in an entry of a dictionary assigned to the **params** argument with
the key *PROJECTIONS*.  An InputState can be assigned either `MappingProjection(s) <MappingProjection>` or
`GatingProjection(s) <GatingProjection>`.  MappingProjections are assigned to its
`pathway_afferents <InputState.pathway_afferents>` attribute and GatingProjections to its
`mod_afferents <InputState.mod_afferents>` attribute.  See `State Projections <State_Projections>` for additional
details concerning the specification of Projections when creating a State.


.. _InputState_Structure:

Structure
---------

Every InputState is owned by a `Mechanism <Mechanism>`. It can receive one or more
`MappingProjections <MappingProjection>` from other Mechanisms, as well as from the Process or System to which its
owner belongs (if it is the `ORIGIN` Mechanism for that Process or System).  The MappingProjections received by an
InputState are listed in its `path_afferents <InputState.path_afferents>` attribute.  An InputState can also receive
one or more `GatingProjections <GatingProjection>` and that regulate its value (see the descriptions of Modulation
under `ModulatorySignals <ModulatorySignal_Modulation>` and `GatingSignals <GatingSignal_Modulation>` for additional
details). The GatingProjections received by an InputState are listed in its `mod_afferents <InputState.mod_afferents>`
attribute.

.. _InputState_Weights_And_Exponents:

Weights and Exponents
~~~~~~~~~~~~~~~~~~~~~

Every InputState has a `weight <InputState.weight>`  and an `exponent <InputState.exponent>` attribute.  These can be
used by the Mechanism to which it belongs when that combines the `value <InputState.value>`\\s of its States (e.g.,
an ObjectiveMechanism uses the weights and exponents assigned to its InputStates to determine how the values it monitors
are combined by its `function <ObjectiveMechanism>`).  The value of each must be an integer or float, and the default
is 1 for both.

Variable, Function and Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

***???  ADD DISCUSSION FROM OBJECTIVE MECHANISM OF RELATIONSHIP TO PROJECTION/OUTPUT STATE AND OVERRIDE

Like all PsyNeuLink components, an InputState also has the three following core attributes:

* `variable <InputState.variable>`:  this serves as a template for the `value <Projection.value>` of each Projection
  that the InputState receives: each must match both the number and type of elements of the InputState's
  `variable <InputState.variable>`.
..
* `function <InputState.function>`:  this aggregates the `value <Projection.value>` of all of the `Projections
  <Projection>` received by the InputState, and assigns the result to the InputState's `value <InputState.value>`
  attribute.  The default function is `LinearCombination` that performs an elementwise (Hadamard) sums the values.
  However, the parameters of the `function <InputState.function>` -- and thus the `value <InputState.value>` of the
  InputState -- can be modified by any `GatingProjections <GatingProjection>` received by the InputState (listed in its
  `mod_afferents <InputState.mod_afferents>` attribute.  A custom function can also be specified, so long as it
  generates a result that is compatible with the item of the Mechanism's `variable <Mechanism_Base.variable>` to
  which the InputState corresponds (see `above <InputStates_Mechanism_Variable_and_Function>`.
..
* `value <InputState.value>`:  this is the aggregated value of the `Projections <Projection>` received by the
  InputState and assigned to it by the InputState's `function <InputState.function>`, possibly modified by the
  influence of any `GatingProjections <GatingProjection>` received by the InputState. It must be compatible with the
  item of the owner Mechanism's `variable <Mechanism_Base.variable>` to which the InputState has been
  assigned.

.. _InputState_Execution:

Execution
---------

An InputState cannot be executed directly.  It is executed when the Mechanism to which it belongs is executed.
When this occurs, the InputState executes any `Projections <Projection>` it receives, calls its `function
<InputState.function>` to aggregate the values received from any `MappingProjections <MappingProjection>` it receives
(listed in its its `path_afferents  <InputState.path_afferents>` attribute) and modulate them in response to any
`GatingProjections <GatingProjection>` (listed in its `mod_afferents <InputState.mod_afferents>` attribute),
and then assigns the result to the InputState's `value <InputState.value>` attribute.
This, in turn, is assigned to the item of the Mechanism's  `variable <Mechanism_Base.variable>` and
`input_values <Mechanism_Base.input_values>` attributes  corresponding to that InputState (see `Mechanism
variable and input_values attributes <Mechanism_Variable>` for additional details).

.. _InputState_Class_Reference:

Class Reference
---------------

"""
import numbers
import warnings

import numpy as np
import typecheck as tc

from psyneulink.components.component import InitStatus
from psyneulink.components.functions.function import Linear, LinearCombination
from psyneulink.components.mechanisms.mechanism import Mechanism
from psyneulink.components.states.outputstate import OutputState
from psyneulink.components.states.state import StateError, State_Base, _instantiate_state_list, state_type_keywords
from psyneulink.globals.keywords import EXPONENT, FUNCTION, INPUT_STATE, INPUT_STATE_PARAMS, MAPPING_PROJECTION, \
    MECHANISM, OUTPUT_STATES, MATRIX, PROJECTIONS, PROJECTION_TYPE, SUM, VARIABLE, WEIGHT, REFERENCE_VALUE
from psyneulink.globals.preferences.componentpreferenceset import is_pref_set
from psyneulink.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.globals.utilities import append_type_to_name, iscompatible

__all__ = [
    'InputState', 'InputStateError', 'state_type_keywords',
]
state_type_keywords = state_type_keywords.update({INPUT_STATE})

# InputStatePreferenceSet = ComponentPreferenceSet(log_pref=logPrefTypeDefault,
#                                                          reportOutput_pref=reportOutputPrefTypeDefault,
#                                                          verbose_pref=verbosePrefTypeDefault,
#                                                          param_validation_pref=paramValidationTypeDefault,
#                                                          level=PreferenceLevel.TYPE,
#                                                          name='InputStateClassPreferenceSet')

# class InputStateLog(IntEnum):
#     NONE            = 0
#     TIME_STAMP      = 1 << 0
#     ALL = TIME_STAMP
#     DEFAULTS = NONE

# STATE_SPEC_INDEX = 0 <- DECLARED IN State
WEIGHT_INDEX = 1
EXPONENT_INDEX = 2

class InputStateError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


class InputState(State_Base):
    """
    InputState(                                \
    owner,                                     \
    reference_value=None,                      \
    function=LinearCombination(operation=SUM), \
    value=None,                                \
    projections=None,                          \
    weight=None,                               \
    exponent=None,                             \
    params=None,                               \
    name=None,                                 \
    prefs=None)

    Subclass of `State <State>` that calculates and represents the input to a `Mechanism <Mechanism>` from one or more
    `PathwayProjection <PathwayProjection>`.

    COMMENT:

        Description
        -----------
            The InputState class is a Component type in the State category of Function,
            Its FUNCTION executes the Projections that it receives and updates the InputState's value

        Class attributes
        ----------------
            + componentType (str) = INPUT_STATE
            + paramClassDefaults (dict)
                + FUNCTION (LinearCombination, Operation.SUM)
                + FUNCTION_PARAMS (dict)
                # + kwStateProjectionAggregationFunction (LinearCombination, Operation.SUM)
                # + kwStateProjectionAggregationMode (LinearCombination, Operation.SUM)

        Class methods
        -------------
            _instantiate_function: insures that function is ARITHMETIC)
            update_state: gets InputStateParams and passes to super (default: LinearCombination with Operation.SUM)

        StateRegistry
        -------------
            All INPUT_STATE are registered in StateRegistry, which maintains an entry for the subclass,
              a count for all instances of it, and a dictionary of those instances

    COMMENT


    Arguments
    ---------

    owner : Mechanism
        the Mechanism to which the InputState belongs;  it must be specified or determinable from the context in which
        the InputState is created.

    reference_value : number, list or np.ndarray
        the value of the item of the owner Mechanism's `variable <Mechanism_Base.variable>` attribute to which
        the InputState is assigned; used as the template for the InputState's `value <InputState.value>` attribute.

    variable : number, list or np.ndarray
        specifies the template for the InputState's `variable <InputState.variable>` attribute.

    function : Function or method : default LinearCombination(operation=SUM)
        specifies the function used to aggregate the `values <Projection.value>` of the `Projections <Projection>`
        received by the InputState, under the possible influence of `GatingProjections <GatingProjection>` received
        by the InputState.  It must produce a result that has the same format (number and type of elements) as the
        item of its owner Mechanism's `variable <Mechanism_Base.variable>` to which the InputState has been assigned.

    projections : list of Projection specifications
        species the `MappingProjection(s) <MappingProjection>` and/or `GatingProjection(s) <GatingProjection>` to be
        received by the InputState, and that will be listed in its `path_afferents <InputState.path_afferents>` and
        `mod_afferents <InputState.mod_afferents>` attributes, respectively (see `InputState_Projections` for additional
        details).

    weight : number : default 1
        specifies the value of the `weight <InputState.weight>` attribute of the InputState.

    exponent : number : default 1
        specifies the value of the `exponent <InputState.exponent>` attribute of the InputState.

    params : Optional[Dict[param keyword, param value]]
        a `parameter dictionary <ParameterState_Specification>` that can be used to specify the parameters for
        the InputState or its function, and/or a custom function and its parameters. Values specified for parameters in
        the dictionary override any assigned to those parameters in arguments of the constructor.

    name : str : default InputState-<index>
        a string used for the name of the InputState.
        If not is specified, a default is assigned by StateRegistry of the Mechanism to which the InputState belongs
        (see :doc:`Registry <LINK>` for conventions used in naming, including for default and duplicate names).

    prefs : Optional[PreferenceSet or specification dict : State.classPreferences]
        the `PreferenceSet` for the InputState.
        If it is not specified, a default is assigned using `classPreferences` defined in ``__init__.py``
        (see :doc:`PreferenceSet <LINK>` for details).


    Attributes
    ----------

    owner : Mechanism
        the Mechanism to which the InputState belongs.

    path_afferents : List[MappingProjection]
        a list of the `MappingProjections <MappingProjection>` received by the InputState
        (i.e., for which it is a `receiver <Projection.Projection.receiver>`).

    mod_afferents : List[GatingProjection]
        a list of the `GatingProjections <GatingProjection>` received by the InputState.

    variable : value, list or np.ndarray
        the template for the `value <Projection.Projection.value>` of each Projection that the InputState receives,
        each of which must match the format (number and types of elements) of the InputState's
        `variable <InputState.variable>`.

    size : int, list or np.ndarray of ints
        specifies variable as array(s) of zeros if **variable** is not passed as an argument;
        if **variable** is specified, it takes precedence over the specification of **size**.

    function : CombinationFunction : default LinearCombination(operation=SUM))
        performs an element-wise (Hadamard) aggregation of the `value <Projection.Projection.value>` of each Projection
        received by the InputState, under the possible influence of any `GatingProjections <GatingProjection>` received
        by the InputState.

    value : value or ndarray
        the output of the InputState's `function <InputState.function>`, which is the the aggregated value of the
        `PathwayProjections <PathwayProjection>` (e.g., `MappingProjections <MappingProjection>`) received by the
        InputState (and listed in its `path_afferents <InputState.path_afferents>` attribute), possibly `modulated
        <ModulatorySignal_Modulation>` by any `GatingProjections <GatingProjection>` it receives (listed in its
        `mod_afferents <InputState.mod_afferents>` attribute).  The result (whether a value or an ndarray) is
        assigned to an item of the owner Mechanism's `variable <Mechanism_Base.variable>`.

    weight : number
        see `InputState_Weights_And_Exponents` for description.

    exponent : number
        see `InputState_Weights_And_Exponents` for description.

    name : str : default <State subclass>-<index>
        the name of the InputState.
        Specified in the **name** argument of the constructor for the OutputState.  If not is specified, a default is
        assigned by the StateRegistry of the Mechanism to which the OutputState belongs
        (see :doc:`Registry <LINK>` for conventions used in naming, including for default and duplicate names).

        .. note::
            Unlike other PsyNeuLink components, State names are "scoped" within a Mechanism, meaning that States with
            the same name are permitted in different Mechanisms.  However, they are *not* permitted in the same
            Mechanism: States within a Mechanism with the same base name are appended an index in the order of their
            creation.

    prefs : PreferenceSet or specification dict : State.classPreferences
        the `PreferenceSet` for the InputState.
        Specified in the **prefs** argument of the constructor for the Projection;  if it is not specified, a default is
        assigned using `classPreferences` defined in ``__init__.py``
        (see :doc:`PreferenceSet <LINK>` for details).

    """

    #region CLASS ATTRIBUTES

    componentType = INPUT_STATE
    paramsType = INPUT_STATE_PARAMS

    classPreferenceLevel = PreferenceLevel.TYPE
    # Any preferences specified below will override those specified in TypeDefaultPreferences
    # Note: only need to specify setting;  level will be assigned to TYPE automatically
    # classPreferences = {
    #     kwPreferenceSetName: 'InputStateCustomClassPreferences',
    #     kp<pref>: <setting>...}

    # Note: the following enforce encoding as 1D np.ndarrays (one variable/value array per state)
    variableEncodingDim = 1
    valueEncodingDim = 1

    paramClassDefaults = State_Base.paramClassDefaults.copy()
    paramClassDefaults.update({PROJECTION_TYPE: MAPPING_PROJECTION,
                               MECHANISM: None,
                               OUTPUT_STATES: None
                               })

    #endregion

    @tc.typecheck
    def __init__(self,
                 owner=None,
                 reference_value=None,
                 variable=None,
                 size=None,
                 function=LinearCombination(operation=SUM),
                 projections=None,
                 weight=None,
                 exponent=None,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 context=None):

        # Assign args to params and functionParams dicts (kwConstants must == arg names)
        params = self._assign_args_to_param_dicts(function=function,
                                                  weight=weight,
                                                  exponent=exponent,
                                                  params=params)

        # If owner or reference_value has not been assigned, defer init to State._instantiate_projection()
        if owner is None or reference_value is None:
            # Store args for deferred initialization
            self.init_args = locals().copy()
            self.init_args['context'] = self
            self.init_args['name'] = name
            self.init_args['projections'] = projections

            # Flag for deferred initialization
            self.init_status = InitStatus.DEFERRED_INITIALIZATION
            return

        self.reference_value = reference_value

        # Validate sender (as variable) and params, and assign to variable and paramInstanceDefaults
        # Note: pass name of owner (to override assignment of componentName in super.__init__)
        super(InputState, self).__init__(owner,
                                         variable=variable,
                                         size=size,
                                         projections=projections,
                                         params=params,
                                         name=name,
                                         prefs=prefs,
                                         context=self)

    def _validate_params(self, request_set, target_set=None, context=None):
        """Validate weights and exponents

        This needs to be done here, since paramClassDefault declarations assign None as default
            (so that they can be ignored if not specified here or in the function)
        """

        super()._validate_params(request_set=request_set, target_set=target_set, context=context)

        if WEIGHT in target_set and target_set[WEIGHT] is not None:
            if not isinstance(target_set[WEIGHT], (int, float)):
                raise InputStateError("{} parameter of {} for {} ({}) must be an int or float".
                                      format(WEIGHT, self.name, self.owner.name, target_set[WEIGHT]))

        if EXPONENT in target_set and target_set[EXPONENT] is not None:
            if not isinstance(target_set[EXPONENT], (int, float)):
                raise InputStateError("{} parameter of {} for {} ({}) must be an int or float".
                                      format(EXPONENT, self.name, self.owner.name, target_set[EXPONENT]))


    def _instantiate_function(self, context=None):
        """Insure that function is LinearCombination and that output is compatible with owner.instance_defaults.variable

        Insures that function:
            - is LinearCombination (to aggregate Projection inputs)
            - generates an output (assigned to self.value) that is compatible with the component of
                owner.function's variable that corresponds to this InputState,
                since the latter will be called with the value of this InputState;

        Notes:
        * Relevant item of owner.function's variable should have been provided
            as reference_value arg in the call to InputState__init__()
        * Insures that self.value has been assigned (by call to super()._validate_function)
        * This method is called only if the parameterValidationPref is True

        :param context:
        :return:
        """

        super(InputState, self)._instantiate_function(context=context)

        # Insure that function is Function.LinearCombination
        if not isinstance(self.function.__self__, (LinearCombination, Linear)):
            raise StateError("{0} of {1} for {2} is {3}; it must be of LinearCombination or Linear type".
                                      format(FUNCTION,
                                             self.name,
                                             self.owner.name,
                                             self.function.__self__.componentName, ))

        # Insure that self.value is compatible with (relevant item of) self.reference_value
        if not iscompatible(self.value, self.reference_value):
            raise InputStateError("Value ({}) of {} {} for {} is not compatible with "
                                           "the variable ({}) of its function".
                                           format(self.value,
                                                  self.componentName,
                                                  self.name,
                                                  self.owner.name,
                                                  self.reference_value))
                                                  # self.owner.variable))

    def _instantiate_projections(self, projections, context=None):
        """Instantiate Projections specified in PROJECTIONS entry of params arg of State's constructor

        Call _instantiate_projections_to_state to assign:
            PathwayProjections to .pathway_afferents
            ModulatoryProjections to .mod_afferents
        """
        self._instantiate_projections_to_state(projections=projections, context=context)

    def _execute(self, function_params, context):
        """Call self.function with self._path_proj_values

        If there were no Transmissive Projections, ignore and return None
        """

        # If there were any Transmissive Projections:
        if self._path_proj_values:
            # Combine Projection values
            # TODO: stateful - this seems dangerous with statefulness, maybe safe when self.value is only passed or stateful
            combined_values = self.function(variable=self._path_proj_values,
                                            params=function_params,
                                            context=context)
            return combined_values

        # There were no Projections
        else:
            # mark combined_values as none, so that (after being assigned to self.value)
            #    it is ignored in execute method (i.e., not combined with base_value)
            return None

    def _get_primary_state(self, mechanism):
        return mechanism.input_state

# MODIFIED 9/30/17 NEW:
    @tc.typecheck
    def _parse_state_specific_params(self, owner, state_dict, state_specific_params):
        """Get weights, exponents and/or any connections specified in an InputState specification tuple

        Tuple specification can be:
            (state_spec, connections)
            (state_spec, weights, exponents, connections)

        Returns params dict with WEIGHT, EXPONENT and/or CONNECTIONS entries if any of these was specified.

        """
        # FIX: MAKE SURE IT IS OK TO USE DICT PASSED IN (as params) AND NOT INADVERTENTLY OVERWRITING STUFF HERE

        # FIX: ADD FACILITY TO SPECIFY WEIGHTS AND/OR EXPONENTS FOR INDIVIDUAL OutputState SPECS
        #      CHANGE EXPECTATION OF *PROJECTIONS* ENTRY TO BE A SET OF TUPLES WITH THE WEIGHT AND EXPONENT FOR IT
        #      THESE CAN BE USED BY THE InputState's LinearCombination Function
        #          (AKIN TO HOW THE MECHANISM'S FUNCTION COMBINES InputState VALUES)
        #      THIS WOULD ALLOW AN ADDITONAL HIERARCHICAL LEVEL FOR NESTING ALGEBRAIC COMBINATION OF INPUT VALUES
        #      TO A MECHANISM
        from psyneulink.components.projections.projection import Projection, _parse_connection_specs

        params_dict = {}

        if isinstance(state_specific_params, dict):
            # FIX: 10/3/17 - CHECK HERE THAT, IF MECHANISM ENTRY IS USED, A VARIABLE, WEIGHT AND/OR EXPONENT ENTRY
            # FIX:                       IS APPLIED TO ALL THE OutputStates SPECIFIED IN OUTPUT_STATES
            # FIX:                       UNLESS THEY THEMSELVES USE A State specification dict WITH ANY OF THOSE ENTRIES
            # FIX:           USE ObjectiveMechanism EXAMPLES
            return state_specific_params

        elif isinstance(state_specific_params, tuple):

            tuple_spec = state_specific_params
            # Note: 1s item is assumed to be a specification for the InputState itself, handled in _parse_state_spec()

            # # MODIFIED 10/25/17 OLD:
            # # Get connection (afferent Projection(s)) specification from tuple
            # PROJECTIONS_INDEX = len(tuple_spec)-1
            # try:
            #     projections_spec = tuple_spec[PROJECTIONS_INDEX]
            # except IndexError:
            #     projections_spec = None
            # MODIFIED 10/25/17 NEW:
            if len(tuple_spec) == 2:
                projections_spec = tuple_spec[1]
            elif len(tuple_spec) == 4:
                projections_spec = tuple_spec
            # MODIFIED 10/25/17 END

            if projections_spec is not None:
                try:
                    params_dict[PROJECTIONS] = _parse_connection_specs(self,
                                                                       owner=owner,
                                                                       connections=[projections_spec])
                    for projection_spec in params_dict[PROJECTIONS]:
                        # Insure that value of all of the Projections are consistent with the variable of the State
                        #    or, if that is not specified, do so based on the value of the Projection(s):
                        if state_dict[REFERENCE_VALUE] is None:
                            # FIX: 10/3/17 - PUTTING THIS HERE IS A HACK...
                            # FIX:           MOVE TO _parse_state_spec UNDER PROCESSING OF ConnectionTuple SPEC
                            # FIX:           USING _get_state_for_socket
                            from psyneulink.components.projections.projection import _parse_projection_spec
                            sender_dim = projection_spec.state.value.ndim
                            matrix = projection_spec.projection[MATRIX]
                            # Remove dimensionality of sender OutputState, and assume that is what receiver will receive
                            proj_val_shape = matrix.shape[sender_dim :]
                            state_dict[VARIABLE] = np.zeros(proj_val_shape)

                except InputStateError:
                    raise InputStateError("Tuple specification in {} specification dictionary "
                                          "for {} ({}) is not a recognized specification for one or more "
                                          "{}s, {}s, or {}s that project to it".
                                          format(InputState.__name__,
                                                 owner.name,
                                                 projections_spec,
                                                 Mechanism.__name__,
                                                 OutputState.__name__,
                                                 Projection.__name))

            # Tuple is (spec, weights, exponents<, afferent_source_spec>),
            #    for specification of weights and exponents,  + connection(s) (afferent projection(s)) to InputState
            if len(tuple_spec) in {3, 4}:

                weight = tuple_spec[WEIGHT_INDEX]
                exponent = tuple_spec[EXPONENT_INDEX]

                if weight is not None and not isinstance(weight, numbers.Number):
                    raise InputStateError("Specification of the weight ({}) in tuple of {} specification dictionary "
                                          "for {} must be a number".format(weight, InputState.__name__, owner.name))
                params_dict[WEIGHT] = weight

                if exponent is not None and not isinstance(exponent, numbers.Number):
                    raise InputStateError("Specification of the exponent ({}) in tuple of {} specification dictionary "
                                          "for {} must be a number".format(exponent, InputState.__name__, owner.name))
                params_dict[EXPONENT] = exponent

            else:
                raise StateError("Tuple provided as state_spec for {} of {} ({}) must have either 2, 3 or 4 items".
                                 format(InputState.__name__, owner.name, tuple_spec))

        elif state_specific_params is not None:
            raise InputStateError("PROGRAM ERROR: Expected tuple or dict for {}-specific params but, got: {}".
                                  format(self.__class__.__name__, state_specific_params))

        return params_dict
# MODIFIED 9/30/17 END

    @property
    def pathway_projections(self):
        return self.path_afferents

    @pathway_projections.setter
    def pathway_projections(self, assignment):
        self.path_afferents = assignment


# def _instantiate_input_states(owner, input_states=None, context=None):
def _instantiate_input_states(owner, input_states=None, context=None):
    """Call State._instantiate_state_list() to instantiate ContentAddressableList of InputState(s)

    Create ContentAddressableList of InputState(s) specified in paramsCurrent[INPUT_STATES]

    If input_states is not specified:
        - use owner.input_states as list of InputState specifications
        - if owner.input_states is empty, user owner.instance_defaults.variable to create a default InputState

    When completed:
        - self.input_states contains a ContentAddressableList of one or more input_states
        - self.input_state contains the `primary InputState <InputState_Primary>`:  first or only one in input_states
        - paramsCurrent[INPUT_STATES] contains the same ContentAddressableList (of one or more input_states)
        - each InputState corresponds to an item in the variable of the owner's function
        - the value of all of the input_states is stored in a list in input_value
        - if there is only one InputState, it is assigned the full value

    Note: State._instantiate_state_list()
              parses self.instance_defaults.variable (2D np.array, passed in reference_value)
              into individual 1D arrays, one for each input state

    (See State._instantiate_state_list() for additional details)

    Returns list of instantiated InputStates
    """

    # This allows method to be called by Mechanism.add_input_states() with set of user-specified input_states,
    #    while calls from init_methods continue to use owner.input_states (i.e., InputState specifications
    #    assigned in the **input_states** argument of the Mechanism's constructor)
    input_states = input_states or owner.input_states

    state_list = _instantiate_state_list(owner=owner,
                                         state_list=input_states,
                                         state_type=InputState,
                                         state_param_identifier=INPUT_STATE,
                                         reference_value=owner.instance_defaults.variable,
                                         reference_value_name=VARIABLE,
                                         context=context)

    # Call from Mechanism.add_states, so add to rather than assign input_states (i.e., don't replace)
    if context and 'COMMAND_LINE' in context:
        owner.input_states.extend(state_list)
    else:
        owner._input_states = state_list

    # Check that number of input_states and their variables are consistent with owner.instance_defaults.variable,
    #    and adjust the latter if not
    variable_item_is_OK = False
    for i, input_state in enumerate(owner.input_states):
        try:
            variable_item_is_OK = iscompatible(owner.instance_defaults.variable[i], input_state.value)
            if not variable_item_is_OK:
                break
        except IndexError:
            variable_item_is_OK = False
            break

    if not variable_item_is_OK:
        # NOTE: This block of code appears unused, and the 'for' loop appears to cause an error anyways. (7/11/17 CW)
        old_variable = owner.instance_defaults.variable
        new_variable = []
        for state in owner.input_states:
            new_variable.append(state.value)
        owner.instance_defaults.variable = np.array(new_variable)
        if owner.verbosePref:
            warnings.warn(
                "Variable for {} ({}) has been adjusted to match number and format of its input_states: ({})".format(
                    old_variable,
                    append_type_to_name(owner),
                    owner.instance_defaults.variable,
                )
            )

    return state_list
