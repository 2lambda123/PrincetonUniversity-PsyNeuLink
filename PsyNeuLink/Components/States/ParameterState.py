# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# **************************************  ParameterState ******************************************************

"""

Overview
--------

A parameterState belongs to either a `mechanism <Mechanism>` or a `MappingProjection`, and is used to represent and
possibly modify the value of a parameter of its owner or it owner's function.  It can receive one or more
`ControlProjections <ControlProjection>` and/or `LearningProjections <LearningProjection>` that modify that
parameter.   The projections received by a parameterState are listed in its
`receivesFromProjections <ParameterState.receivesFromProjections>` attribute.
Its `function <ParameterState.function>` combines the values of these inputs, and uses the result to modify the value
of the parameter for which it is responsible.


.. _ParameterState_Creation:

Creating a ParameterState
-------------------------

A parameterState can be created by calling its constructor, but in general this is not necessary or advisable as
parameterStates are created automatically when the mechanism or projection to which they belong is created.  The
`owner <ParamaterState.owner>` of a parameterState must be a `mechanism <Mechanism>` or `MappingProjection`.  If the
`owner <ParamaterState.owner>` is not explicitly specified, and can't be determined by context, the parameterState
will be assigned to the :ref:`DefaultProcessingMechanism`.  One parameterState is created for each configurable
parameter of its owner, as well as for each parameter that has been speciied for that object's :keyword:`function`.
Each parameterState is created using the specification of the parameter for which it is responsible, as described below.

.. _ParameterState_Specifying_Parameters:

Specifying Parameters
~~~~~~~~~~~~~~~~~~~~~

Parameters can be specified in one of several places:

    * In an **argument for the parameter** in the constructor for the `mechanism <Mechanism>` or
      `function <Mechanism.Mechanism_Base.function>` to which the parameter belongs
      (see :ref:`Component_Specifying_Functions_and_Parameters` for additional details).
    ..
    * In a **parameter dictionary** used to specify the `params` argument in the constructor for the object to which
      the parameter belongs. The entry for each parameter must use the keyword for the parameter as its key,
      and the parameter's specification as its value (see `examples <ParameterState_Specification_Examples>` below).
      Parameters for an object's :keyword:`function` must be specified in an entry with the key
      :keyword:`FUNCTION_PARAMS`, the value of which is a parameter dictionary containing an entry for each of the
      function's parameters to be specified.  When a value is assigned to a parameter in a parameter dictionary,
      it overrides any value assigned to the argument for the parameter in the object's constructor.
    ..
    * In the `assign_params` method for the object.
    COMMENT:
        * When the object is executed, in the `runtime_params` argument of a call to object's
          `execute <Mechanism.Mechanism_Base.execute>`
          IGNORE:
              or `run <Mechanism.Mechanism_Base.run>` methods
          IGNORE
          method
          (only for a mechanism), or in a tuple with the mechanism where it is specified as part of the
          `pathway` for a process to which it belongs
          (see :ref:`Runtime Specification <ParameterState_Runtime_Parameters:>` below).
    COMMENT

The value specified for the parameter (either explicitly or by default) is assigned as the parameterState's
`baseValue <ParameterState.baseValue>`, and any projections assigned to it are added to its
`receiveFromProjections <ParameterState.receivesFromProjections>` attribute. When the parameterState's owner is
executed, the parameterState's `baseValue <ParameterState.baseValue>` is combined with the value of the projections
it receives to determine the value of the parameter for which the parameterState is responsible
(see `ParameterState_Execution` for details).

The specification of a parameter can take any of the following forms:

    * A **value**.  This must be a valid value for the parameter.  it creates a default parameterState,
      assigns the parameter's default value as the parameterState's `baseValue <ParameterState.baseValue>`,
      and assigns the parameter's name as the name of the parameterState.
    ..
    * A reference to an existing **parameterState** object.
      COMMENT:
      It's name must be the name of a parameter of the
      owner's ``function``, and its
      COMMENT
      Its value must be a valid one for the parameter.

      .. note::
          This capability is provided for generality and potential
          future use, but its current use is not advised.
    ..
    * A `projection specification <Projection_In_Context_Specification>`.  This creates a default parameterState,
      assigns the parameter's default value as the parameterState's `baseValue <ParameterState.baseValue>`,
      and assigns the parameter's name as the name of the parameterState.  It also creates and/or assigns the
      specified projection, and assigns the parameterState as the projection's
      `receiver <Projection.Projection.receiver>`.  The projection must be a `ControlProjection` or
      `LearningProjection`, and its value must be a valid one for the parameter.
    ..
    * A `ParamValueProjection` or 2-item (value, projection specification) **tuple**.  This creates a default
      parameterState, uses the value (1st) item of the tuple as parameterState's
      `baseValue <ParameterState.baseValue>`, and assigns the parameter's name as the name of the parameterState.
      The projection (2nd) item of the tuple is used to create and/or assign the specified projection, that is assigned
      the parameterState as its `receiver <Projection.Projection.receiver>`.  The projection must be a
      `ControlProjection` or `LearningProjection`, and its value must be a valid one for the parameter.

      .. note::
          Currently, the :keyword:`function` of an object, although it can be specified a parameter value,
          cannot be assigned
          COMMENT:
          a ControlProjection, LearningProjection, or a runtime specification.
          COMMENT
          a ControlProjection or a LearningProjection. This may change in the future.

The **default value** assigned to a parameterState is the default value of the argument for the parameter in the
constructor for the parameter's owner.  If the value of a parameter is specified as `None`, `NotImplemented`,
or any other non-numeric value that is not one of those listed above, then no parameter state is created and the
parameter cannot be modified by a `ControlProjection`
COMMENT:
    , LearningProjection, or :ref:`runtime specification <ParameterState_Runtime_Parameters>`.
COMMENT
or `LearningProjection`.

COMMENT:
    - No parameterState is created for parameters that are:
       assigned a non-numeric value (including None, NotImplemented, False or True)
          unless it is:
              a tuple (could be one specifying ControlProjection, LearningProjection or ModulationOperation)
              a dict with an entry with the key FUNCTION_PARAMS and a value that is a dict (otherwise exclude)
       a function
           IMPLEMENTATION NOTE: FUNCTION_RUNTIME_PARAM_NOT_SUPPORTED
           (this is because paramInstanceDefaults[FUNCTION] could be a class rather than an bound method;
           i.e., not yet instantiated;  could be rectified by assignment in _instantiate_function)

    - self.variable must be compatible with self.value (enforced in _validate_variable)
        note: although it may receive multiple projections, the output of each must conform to self.variable,
              as they will be combined to produce a single value that must be compatible with self.variable
COMMENT


.. _ParameterState_Specification_Examples:

**Examples**

In the following example, a mechanism is created with a function that has four parameters,
each of which is specified using a different format::

    my_mechanism = SomeMechanism(function=SomeFunction(param_a=1.0,
                                                       param_b=(0.5, ControlProjection),
                                                       param_c=(36, ControlProjection(function=Logistic),
                                                       param_d=ControlProjection)))

The first parameter of the mechanism's function (``param_a``) is assigned a value directly; the second (``param_b``) is
assigned a value and a ControlProjection; the third (``param_c``) is assigned a value and a
`ControlProjection with a specified function  <ControlProjection_Structure>`; and the fourth (``param_d``) is
assigned just a `ControlProjection` (the default value for the parameter will be used).

In the following example, a `MappingProjection` is created, and its
`matrix <MappingProjection.MappingProjection.matrix>` parameter is assigned a random weight matrix (using a
`matrix keyword <Matrix_Keywords>`) and `LearningProjection`::

    my_mapping_projection = MappingProjection(sender=my_input_mechanism,
                                              receiver=my_output_mechanism,
                                              matrix=(RANDOM_CONNECTIVITY_MATRIX, LearningProjection))

.. note::
   the `matrix <MappingProjection.MappingProjection.matrix>` parameter belongs to the MappingProjection's
   `function <MappingProjection.MappingProjection.function>`;  however, since it has only one standard function,
   its arguments are available in the constructor for the projection (see
   `Component_Specifying_Functions_and_Parameters` for a more detailed explanation).

COMMENT:
    ADD EXAMPLE USING A PARAMS DICT, INCLUDING FUNCTION_PARAMS, AND assign_params
COMMENT

.. _ParameterState_Structure:

Structure
---------

Every parameterState is owned by a `mechanism <Mechanism>` or `MappingProjection`. It can receive one or more
`ControlProjections <ControlProjection>` or `LearningProjections <LearningProjection>`.  However, the format (the
number and type of its elements) of each must match the value of the parameter for which the parameterState is
responsible.  When the parameterState is updated (i.e., the owner is executed) the values of its projections are
combined (using the  parameterState's `function <ParameterState.function>`) and the result is used to modify the
parameter for which the parameterState is responsible (see `Execution <ParameterState_Execution>` below).  The
projections received by a parameterState are listed in its `receiveFromProjections
<ParameterState.receivesFromProjections>` attribute. Like all PsyNeuLink components, it has the three following core
attributes:

* `variable <ParameterState.variable>`:  this serves as a template for the `value <Projection.Projection.value>` of
  each projection that the parameterState receives.  It must match the format (the number and type of elements) of the
  parameter for which the parameterState is responsible. Any projections the parameterState receives must, it turn,
  match the format of :keyword:`variable`.

* `function <ParameterState.function>`:  this performs an elementwise (Hadamard) aggregation  of the values of the
  projections received by the parameterState.  The default function is `LinearCombination` that multiplies the
  values. A custom function can be specified (e.g., to perform a Hadamard sum, or to handle non-numeric values in
  some way), so long as it generates a result that is compatible with the `value <ParameterState.value>` of the
  parameterState.

* `value <ParameterState.value>`:  this is the value assigned to the parameter for which the parameterState is
  responsible.  It is the `baseValue <ParameterState.baseValue>` of the parameterState, modified by
  aggregated value of the projections received by the parameterState returned by the
  `function <ParameterState.function>.

In addition, a parameterState has two other attributes that are used to determine the value it assigns to the
parameter for which it is responsible (as shown in the `figure <ParameterState_Figure>` below):

.. ParameterState_BaseValue:

* `baseValue <ParameterState.baseValue>`:  this is the default value of the parameter for which the
  parameterState is responsible.  It is combined with the result of the parameterState's
  `function <ParameterState.function>` to determine the value of the parameter for which the parameterState is
  responsible.

.. ParameterState_Parameter_Modulation_Operation:

* `parameterModulationOperation <ParameterState.parameterModulationOperation>`: this determines how the
  result of the parameterState's `function <ParameterState.function>` (the aggregated values of the projections it
  receives) is combined with its `baseValue <ParameterState.baseValue>` to generate the value of the parameter
  for which it is responsible.  This must be a value of `ModulationOperation`.  It can be specified in either
  the :keyword:`parameter_modulation_operation` argument of the parameterState's constructor,
  COMMENT:
  of the constructor, or in a :keyword:`PARAMETER_MODULATION_OPERATION` entry of a params dictionary in either the
  constructor or a :keyword:`PARAMETER_STATE_PARAMS` dictionary in a
  :ref:`runtime specification <ParameterState_Runtime_Parameters>`.
  COMMENT
  or in its :keyword:`params` argument, in a :keyword:`PARAMETER_MODULATION_OPERATION` entry of a
  `parameter dictionary <ParameterState_Specifying_Parameters>`. The default is `ModulationOperation.PRODUCT`,
  which multiples the parameterState's `baseValue <ParameterState.baseValue>` by the aggregated value of the
  result of the parameterState's `function <ParameterState.function>` to determine the value of the parameter.

The value of a parameter of a mechanism or projection is accessible as an attribute with the corresponding name
(e.g., myMechanism.<param_name>.  The value of a parameter of a :keyword:`function` is accessible from the
`function_params` attribute of the mechanism or projection to which the function belongs;  this is a dictionary with
entries for each of the function's parameters. Each of the function's parameters can be referenced using a key that is
the name of the parameter (e.g., ``myMech.function_object.<param_name>``).  Parameter attributes of mechanisms,
projections, and their functions accessed in these ways are read-only.  To re-assign the value of a parameter,
use the `assign_params` method of the mechanism or projection to which the parameter of function belongs.

.. _ParameterState_Figure:

The figure below shows how the specifications for a parameter are combined by its parameterState to determine the
parameter's value.

    **How a ParameterState Determines the Value of a Parameter**

    .. figure:: _static/ParameterState_fig.jpg
       :alt: ParameterState
       :scale: 75 %

       ..

       +--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
       | Component    | Impact of ParameterState on Parameter Value                                                                                                                  |
       +==============+==============================================================================================================================================================+
       | A (brown)    | `baseValue <ParameterState.baseValue>` (default value of the parameter)                                                                                      |
       +--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
       | B (blue)     | parameterState's `function <ParameterState.function>` combines `value <Projection.Projection.value>` of projections                                          |
       +--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
       | C (green)    | parameterState's `parameterModulationOperation <ParameterState.parameterModulationOperation>` combines projections and `baseValue <ParameterState.baseValue>`|
       +--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+

       In example, the values for the parameters (shown in brown) -- ``param_x`` for the mechanism, and ``param_y``
       for its ``function`` -- specify the :py:data:`baseValue <ParameterState.baseValue>` of the paramterState for
       each parameter (labeled "A" in the figure).  These are the values that will be used for
       those parameters absent any other influences. However, ``param_y`` is assigned a ControlProjection, so its value
       will also be determined by the value of the ControlProjection to its parameterState;  that will be combined
       with its `baseValue <ParameterState.baseValue>` using the
       `parameterModulationOperation <ParameterState.parameterModulationOperation>`
       specified for the mechanism (``ModulationOperation.SUM``, shown in green, and labeled "C" in the figure). If
       there had been more than one ControlProjection specified, their values would have been combined using the
       parameterState's `function <ParameterState.function>` (lableled "B" in the figure), before combining the result
       with the
       baseValue.


.. _ParameterState_Execution:

Execution
---------

A parameterState cannot be executed directly.  It is executed when the mechanism to which it belongs is executed.
When this occurs, the parameterState executes any `ControlProjections` and/or `LearningProjections` it receives, and
calls its `function <ParameterState.function>` to aggregate their values.  It then combines the result with the
parameterState's `baseValue <ParameterState.baseValue>` using its
`parameterModulationOperation <ParameterState.parameterModulationOperation>` attribute,
COMMENT:
combines the result with any :ref:`runtime specification <ParameterState_Runtime_Parameters>` for the parameter using
the :any:`ModulationOperation` specified for runtime parameters, and finally
COMMENT
and then assigns the result as the `value <ParameterState.value>` of the parameterState.  This is used as the value of
the parameter for which the parameterState is responsible.

COMMENT:
    .. _ParameterState_Runtime_Parameters:

    Runtime Specification of Parameters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. note::
       This is an advanced feature, that is generally not required for most applications.

    In general, it should not be necessary to modify parameters programmatically each time a process or system is
    executed or run; ordinarily, this should be done using :doc:`control projections <ControlProjection>` and/or
    :doc:`learning projections <LearningProjection>`.  However, if necessary, it is possible to modify parameters
    "on-the-fly" in two ways:  by specifying runtime parameters for a mechanism as part of a tuple where it is
    specified in the :py:data:`pathway <Process.Process_Base.pathway>` of a process, or in the
    :py:meth:`execute <Mechanism.Mechanism_Base.execute>`
    IGNORE_START
        or :py:meth:`run <Mechanism.Mechanism_Base.run>` methods
    IGNORE_END
    method
    for a mechanism, process or system (see :ref:`Mechanism_Runtime_Parameters`).

    IGNORE_START
        IS THE MECHANISM TUPLE SPECIFICATION ONE TIME OR EACH TIME? <- BUG IN merge_dictionary()
        IS THE RUN AND EXECUTE SPECIFICATION ONE TRIAL OR ALL TRIALS IN THAT RUN?
    IGNORE_END

    .. note::
       At this time, runtime specification can be used only  for the parameters of a mechanism or of its ``function``.
       Since the function itself is not currently assigned a parameterState, it cannot be modified at runtime;  nor is
       there currently a method for runtime specification for the parameters of a MappingProjection.  These may be
       supported in the future.

    IGNORE_START

        RUNTIME:  runtime param assignment is one-time by default;
                   but can use runtimeParamsStickyAssignmentPref for persistent assignment
                   or use assign_param

       XXXXX MAKE SURE ROLE OF ParamModulationOperation FOR runtime params IS EXPLAINED THERE (OR EXPLAIN HERE)
       XXXX DOCUMENT THAT MOD OP CAN BE SPECIFIED IN A TUPLE WITH PARAM VALUE (INSTEAD OF PROJECTION) AS PER FIGURE?
    IGNORE_END

.. _ParameterState_Runtime_Figure:

The figure below shows how these factors are combined by the parameterState to determine a parameter value,
including runtime specifications:

    **How a ParameterState Determines the Value of a Parameter**

    .. figure:: _static/ParameterState_fig.jpg
       :alt: ParameterState
       :scale: 75 %

       ..

       +--------------+--------------------------------------------------------------------+
       | Component    | Impact of ParameterState on Parameter Value (including at runtime) |
       +==============+====================================================================+
       | A (brown)    | ``baseValue`` (default value of parameter``)                       |
       +--------------+--------------------------------------------------------------------+
       | B (blue)     | parameterState's ``function`` combines ``value`` of  projections   |
       +--------------+--------------------------------------------------------------------+
       | C (green)    | runtime parameter influences projection-modulated ``baseValue``    |
       +--------------+--------------------------------------------------------------------+
       | D (violet)   | runtime specification of parameter value                           |
       +--------------+--------------------------------------------------------------------+
       | E (red)      | combined projection values modulate ``baseValue``                  |
       +--------------+--------------------------------------------------------------------+

       In the first line, the values for ``param_x`` and ``param_z`` labeled "A" (and shown in brown)
       specify the :py:data:`baseValue <ParameterState.baseValue>` of the paramterStates for each parameter;
       these are the values that will be used for those parameters absent any other influences.  The values labelled
       IGNORE_START
         Constructor parameter specification:
             1st example: the values for ``param_x`` and ``param_z`` labeled "A" (and shown in brown)
                          specify the ``baseValue`` of the paramterStates for each parameter;  these are the values
                          that will be used for those parameters absent any other influences.
                          param_x is given a controlSignal;  any values specified by the control siginal are combined
                          using the parameterState's ``function`` (E) and then combined with its baseValue (A) using the
                          parameterState's ``parameterModulationOpeartion`` (D);  finally, those will be combined
                          with any runtime specification (see 2nd and 3rd examples)
                          using the runtime parameterModulationOperation (C)
         Runtime parameter specification:
             2nd example:  param_x is given a runtime value (violet) but no runtime ModulationOperation;
                           param_y is given a runtime value (violet) and also a runtime ModulationOperation (red);
                           the parameterState's parameterModulationOperation is set to MULTIPLY (green).
             3rd example:  param_x is given a runtime value (violet) and also a runtime ModulationOperation (red);
                           param_y is given a runtime value (violet) but no runtime ModulationOperation;
                           the parameterState's parameterModulationOperation is set to SUM (green)
         NOTE: CAPS FOR PARAM SPECIFICATION IN DICTS -> KEYWORDS


          AUGMENT FIGURE TO SHOW PARAM SPECIFICATIONS FOR BOTH THE OBJECT AND ITS FUNCTION
        IGNORE_END

COMMENT

.. _ParameterState_Class_Reference:

Class Reference
---------------

"""

from PsyNeuLink.Components.States.State import *
from PsyNeuLink.Components.States.State import _instantiate_state
from PsyNeuLink.Components.Functions.Function import *

class ParameterStateError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


class ParameterState(State_Base):
    """
    ParameterState(                                              \
    owner,                                                       \
    reference_value=None                                         \
    value=None,                                                  \
    function=LinearCombination(operation=PRODUCT),               \
    parameter_modulation_operation=ModulationOperation.MULTIPLY, \
    params=None,                                                 \
    name=None,                                                   \
    prefs=None)

    Implements a subclass of `State` that represents and possibly modifies the value of a parameter for a mechanism,
    projection, or function.

    COMMENT:

        Description
        -----------
            The ParameterState class is a componentType in the State category of Function,
            Its FUNCTION executes the projections that it receives and updates the ParameterState's value

        Class attributes
        ----------------
            + componentType (str) = kwMechanisParameterState
            + classPreferences
            + classPreferenceLevel (PreferenceLevel.Type)
            + paramClassDefaults (dict)
                + FUNCTION (LinearCombination)
                + FUNCTION_PARAMS  (Operation.PRODUCT)
                + PROJECTION_TYPE (CONTROL_PROJECTION)
                + PARAMETER_MODULATION_OPERATION   (ModulationOperation.MULTIPLY)
            + paramNames (dict)

        Class methods
        -------------
            _instantiate_function: insures that function is ARITHMETIC) (default: Operation.PRODUCT)
            update_state: updates self.value from projections, baseValue and runtime in PARAMETER_STATE_PARAMS

        StateRegistry
        -------------
            All ParameterStates are registered in StateRegistry, which maintains an entry for the subclass,
              a count for all instances of it, and a dictionary of those instances

    COMMENT


    Arguments
    ---------

    owner : Mechanism or Projection
        the `mechanism <Mechanism>` or `projection <Projection>` to which to which the parameterState belongs; it must
        be specified or determinable from the context in which the parameterState is created. The owner of a
        parameterState for the parameter of a :keyword:`function` should be specified as the mechanism or projection
        to which the function belongs.

    reference_value : number, list or np.ndarray
        specifies the default value of the parameter for which the parameterState is responsible.

    value : number, list or np.ndarray
        specifies the template for the parametersState's `variable <ParameterState.variable>` (since a parameterState's
        `variable <ParameterState.variable>` and `value <ParameterState.value>` attributes must have the same format
        (number and type of elements).

    function : Function or method : default LinearCombination(operation=SUM)
        specifies the function used to aggregate the values of the projections received by the parameterState.
        It must produce a result that has the same format (number and type of elements) as its input.

    parameter_modulation_operation : ModulationOperation : default ModulationOperation.MULTIPLY
        specifies the operation by which the values of the projections received by the parameterState are used
        to modify its `baseValue <ParameterState.baseValue>` before assigning it as the value of the parameter for
        which the parameterState is responsible.

    params : Optional[Dict[param keyword, param value]]
        a `parameter dictionary <ParameterState_Specifying_Parameters>` that can be used to specify the parameters for
        the parameterState or its function, and/or a custom function and its parameters.  Values specified for
        parameters in the dictionary override any assigned to those parameters in arguments of the constructor.

    name : str : default InputState-<index>
        a string used for the name of the inputState.
        If not is specified, a default is assigned by StateRegistry of the mechanism to which the inputState belongs
        (see :doc:`Registry <LINK>` for conventions used in naming, including for default and duplicate names).

    prefs : Optional[PreferenceSet or specification dict : State.classPreferences]
        the `PreferenceSet` for the inputState.
        If it is not specified, a default is assigned using `classPreferences` defined in __init__.py
        (see :doc:`PreferenceSet <LINK>` for details).


    Attributes
    ----------

    owner : Mechanism
        the mechanism to which the parameterState belongs.

    receivesFromProjections : Optional[List[Projection]]
        a list of the projections received by the parameterState (i.e., for which it is a
        `receiver <Projection.Projection.receiver>`); generally these are `ControlProjection(s) <ControlProjection>`
        and/or `LearningProjection(s) <LearningProjection>`.

    variable : number, list or np.ndarray
        the template for the `value <Projection.Projection.value>` of each projection that the parameterState receives,
        each of which must match the format (number and types of elements) of the parameterState's :keyword:`variable`.

    function : CombinationFunction : default LinearCombination(operation=PRODUCT))
        performs an element-wise (Hadamard) aggregation  of the `value <Projecction.Projection.value>` of each
        projection received by the parameterState.

    baseValue : number, list or np.ndarray
        the default value for the parameterState.  It is combined with the aggregated value of any projections it
        receives using its `parameterModulationOperation <ParameterState.parameterModulationOperation>`
        and then assigned to `value <ParameterState.value>`.

    parameterModulationOperation : ModulationOperation : default ModulationOperation.PRODUCT
        the arithmetic operation used to combine the aggregated value of any projections is receives
        (the result of the parameterState's `function <ParameterState.function>`) with its
        `baseValue <ParameterState.baseValue>`, the result of which is assigned to `value <ParameterState.value>`.

    value : number, list or np.ndarray
        the aggregated value of the projections received by the ParameterState, combined with the
        `baseValue <ParameterState.baseValue>` using its
        `parameterModulationOperation <ParameterState.parameterModulationOperation>`
        COMMENT:
        as well as any runtime specification
        COMMENT
        .  This is the value assigned to the parameter for which the parameterState is responsible.

    name : str : default <State subclass>-<index>
        the name of the inputState.
        Specified in the `name` argument of the constructor for the outputState.  If not is specified, a default is
        assigned by the StateRegistry of the mechanism to which the outputState belongs
        (see :doc:`Registry <LINK>` for conventions used in naming, including for default and duplicate names).

        .. note::
            Unlike other PsyNeuLink components, states names are "scoped" within a mechanism, meaning that states with
            the same name are permitted in different mechanisms.  However, they are *not* permitted in the same
            mechanism: states within a mechanism with the same base name are appended an index in the order of their
            creation.

    prefs : PreferenceSet or specification dict : State.classPreferences
        the `PreferenceSet` for the inputState.
        Specified in the `prefs` argument of the constructor for the projection;  if it is not specified, a default is
        assigned using `classPreferences` defined in __init__.py
        (see :doc:`PreferenceSet <LINK>` for details).

    """

    #region CLASS ATTRIBUTES

    componentType = PARAMETER_STATE
    paramsType = PARAMETER_STATE_PARAMS

    classPreferenceLevel = PreferenceLevel.TYPE
    # Any preferences specified below will override those specified in TypeDefaultPreferences
    # Note: only need to specify setting;  level will be assigned to TYPE automatically
    # classPreferences = {
    #     kwPreferenceSetName: 'ParameterStateCustomClassPreferences',
    #     kp<pref>: <setting>...}


    paramClassDefaults = State_Base.paramClassDefaults.copy()
    paramClassDefaults.update({PROJECTION_TYPE: CONTROL_PROJECTION})
    #endregion

    tc.typecheck
    def __init__(self,
                 owner,
                 reference_value=None,
                 variable=None,
                 function=LinearCombination(operation=PRODUCT),
                 parameter_modulation_operation=ModulationOperation.MULTIPLY,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 context=None):

        # Assign args to params and functionParams dicts (kwConstants must == arg names)
        params = self._assign_args_to_param_dicts(function=function,
                                                 parameter_modulation_operation=parameter_modulation_operation,
                                                 params=params)

        self.reference_value = reference_value

        # Validate sender (as variable) and params, and assign to variable and paramsInstanceDefaults
        # Note: pass name of mechanism (to override assignment of componentName in super.__init__)
        super(ParameterState, self).__init__(owner,
                                             variable=variable,
                                             params=params,
                                             name=name,
                                             prefs=prefs,
                                             context=self)

        self.parameterModulationOperation = self.paramsCurrent[PARAMETER_MODULATION_OPERATION]

    def _validate_params(self, request_set, target_set=None, context=None):
        """Insure that parameterState (as identified by its name) is for a valid parameter for owner

        Parameter can be either owner's, or owner's function_object
        """

        # # MODIFIED 11/29/16 OLD:
        # if not self.name in self.owner.function_params.keys():
        # MODIFIED 11/29/16 NEW:
        if not self.name in self.owner.user_params.keys() and not self.name in self.owner.function_params.keys():
        # MODIFIED 11/29/16 END
            raise ParameterStateError("Name of requested parameterState ({}) does not refer to a valid parameter "
                                      "of the function ({}) of its owner ({})".
                                      format(self.name,
                                             # self.owner.function_object.__class__.__name__,
                                             self.owner.function_object.componentName,
                                             self.owner.name))

        super()._validate_params(request_set=request_set, target_set=target_set, context=context)

    def _instantiate_function(self, context=None):
        """Insure function is LinearCombination and that its output is compatible with param with which it is associated

        Notes:
        * Relevant param should have been provided as reference_value arg in the call to InputState__init__()
        * Insures that self.value has been assigned (by call to super()._validate_function)
        * This method is called only if the parameterValidationPref is True

        :param context:
        :return:
        """

        # If parameterState is for a matrix of a MappingProjection,
        #     its parameter_modulation_operation should be SUM (rather than PRODUCT)
        #         so that weight changes (e.g., from a learningSignals) are added rather than multiplied
        if self.name == MATRIX:
            # IMPLEMENT / TEST: 10/20/16 THIS SHOULD BE ABLE TO REPLACE SPECIFICATION IN LEARNING PROJECTION
            self.params[PARAMETER_MODULATION_OPERATION] = ModulationOperation.ADD

        super()._instantiate_function(context=context)

        # Insure that function is LinearCombination
        if not isinstance(self.function.__self__, (LinearCombination)):
            raise StateError("Function {0} for {1} of {2} must be of LinearCombination type".
                                 format(self.function.__self__.componentName, FUNCTION, self.name))

        # # Insure that output of function (self.value) is compatible with relevant parameter's reference_value
        if not iscompatible(self.value, self.reference_value):
            raise ParameterStateError("Value ({0}) of {1} parameterState for {2} mechanism is not compatible with "
                                           "the variable ({3}) of its function".
                                           format(self.value,
                                                  self.name,
                                                  self.owner.name,
                                                  # self.owner.variable))
                                                  self.reference_value))


    def update(self, params=None, time_scale=TimeScale.TRIAL, context=None):
        """Parse params for parameterState params and XXX ***

# DOCUMENTATION:  MORE HERE:
        - get ParameterStateParams
        - pass params to super, which aggregates inputs from projections
        - combine input from projections (processed in super) with baseValue using paramModulationOperation
        - combine result with value specified at runtime in PARAMETER_STATE_PARAMS
        - assign result to self.value

        :param params:
        :param time_scale:
        :param context:
        :return:
        """

        super().update(params=params,
                       time_scale=time_scale,
                       context=context)

        #region COMBINE PROJECTIONS INPUT WITH BASE PARAM VALUE
        try:
            # Check whether ModulationOperation for projections has been specified at runtime
            # Note: this is distinct from ModulationOperation for runtime parameter (handled below)
            self.parameterModulationOperation = self.stateParams[PARAMETER_MODULATION_OPERATION]
        except (KeyError, TypeError):
            # If not, try to get from params (possibly passed from projection to ParameterState)
            try:
                self.parameterModulationOperation = params[PARAMETER_MODULATION_OPERATION]
            except (KeyError, TypeError):
                pass
            # If not, ignore (leave self.parameterModulationOperation assigned to previous value)
            pass

        # If self.value has not been set, assign to baseValue
        if self.value is None:
            if not context:
                context = kwAssign + ' Base Value'
            else:
                context = context + kwAssign + ' Base Value'
            self.value = self.baseValue

        # Otherwise, combine param's value with baseValue using modulatonOperation
        else:
            if not context:
                context = kwAssign + ' Modulated Value'
            else:
                context = context + kwAssign + ' Modulated Value'
            self.value = self.parameterModulationOperation(self.baseValue, self.value)
        #endregion

        # FIX: STRIP VALUES OUT OF ARRAY OR LIST OF THAT IS WHAT PARAMETER REQUIRES (USE TYPE-MATCH?)
        # FIX: DEHACK TEST FOR MATRIX
        # FIX: MOVE TO PROPERTY
        # MODIFIED 2/21/17 NEW: FOR EVC BUT BREAKS LEARNING
        # If this parameterState is for a parameter of its owner's function, then assign the value there as well
        if self.name in self.owner.function_params and not 'matrix' in self.name:
        #     setattr(self.owner.function.__self__, self.name, self.value)
            param_type = type(getattr(self.owner.function.__self__, self.name))
            setattr(self.owner.function.__self__, self.name, type_match(self.value, param_type))

        #region APPLY RUNTIME PARAM VALUES
        # If there are not any runtime params, or runtimeParamModulationPref is disabled, return
        if (not self.stateParams or self.prefs.runtimeParamModulationPref is ModulationOperation.DISABLED):
            return

        # Assign class-level pref as default operation
        default_operation = self.prefs.runtimeParamModulationPref

        # If there is a runtime param specified, could be a (parameter value, ModulationOperation) tuple
        try:
            value, operation = self.stateParams[self.name]

        except KeyError:
            # No runtime param for this param state
            return

        except TypeError:
            # If single ("exposed") value, use default_operation (class-level runtimeParamModulationPref)
            self.value = default_operation(self.stateParams[self.name], self.value)
        else:
            # If tuple, use param-specific ModulationOperation as operation
            self.value = operation(value, self.value)

        # MODIFIED 2/21/17 NEW: FOR EVC, BUT BREAKS LEARNING
        # If this parameterState is for a parameter of its owner's function, then assign the value there as well
        if self.name in self.owner.function_params and not 'matrix' in self.name:
        # if self.name in self.owner.function_params:
        #     setattr(self.owner.function.__self__, self.name, self.value)
            param_type = type(getattr(self.owner.function.__self__, self.name))
            setattr(self.owner.function.__self__, self.name, type_match(self.value, param_type))

        #endregion

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, assignment):
        self._value = assignment
        # # MODIFIED 2/21/17 NEW:
        # # If this parameterState is for a parameter of its owner's function, then assign the value there as well
        # if self.name in self.owner.function_params:
        #     setattr(self.owner.function.__self__, self.name, self.value)


def _instantiate_parameter_states(owner, context=None):
    """Call _instantiate_parameter_state for all params in user_params to instantiate ParameterStates for them

    If owner.params[PARAMETER_STATE] is None or False:
        - no parameterStates will be instantiated.
    Otherwise, instantiate parameterState for each allowable param in owner.user_params

    """

    # TBI / IMPLEMENT: use specs to implement paramterStates below

    owner.parameterStates = {}
    #
    # Check that parameterStates for owner have not been explicitly suppressed (by assigning to None)
    try:
        no_parameter_states = not owner.params[PARAMETER_STATES]
        # PARAMETER_STATES for owner was suppressed (set to False or None), so do not instantiate any parameterStates
        if no_parameter_states:
            return
    except KeyError:
        # PARAMETER_STATES not specified at all, so OK to continue and construct them
        pass

    try:
        owner.user_params
    except AttributeError:
        return

    # Instantiate parameterState for each param in user_params (including all params in function_params dict),
    #     using its value as the state_spec
    for param_name, param_value in owner.user_params.items():
        _instantiate_parameter_state(owner, param_name, param_value, context=context)


def _instantiate_parameter_state(owner, param_name, param_value, context):
    """Call _instantiate_state for allowable params, to instantiate a ParameterState for it

    Include ones in owner.user_params[FUNCTION_PARAMS] (nested iteration through that dict)
    Exclude if it is a:
        parameterState that already exists (e.g., in case of call from Component.assign_params)
        non-numeric value (including None, NotImplemented, False or True)
            unless it is:
                a tuple (could be on specifying ControlProjection, LearningProjection or ModulationOperation)
                a dict with the name FUNCTION_PARAMS (otherwise exclude)
        function or method
            IMPLEMENTATION NOTE: FUNCTION_RUNTIME_PARAM_NOT_SUPPORTED
            (this is because paramInstanceDefaults[FUNCTION] could be a class rather than an bound method;
            i.e., not yet instantiated;  could be rectified by assignment in _instantiate_function)
    """


    # EXCLUSIONS:

    # # Skip if parameterState already exists (e.g., in case of call from Component.assign_params)
    # if param_name in owner.parameterStates:
    #     return

    from PsyNeuLink.Components.Projections.Projection import Projection
    # Allow numerics but omit booleans (which are treated by is_numeric as numerical)
    if is_numeric(param_value) and not isinstance(param_value, bool):
        pass
    # Only allow a FUNCTION_PARAMS dict
    elif isinstance(param_value, dict) and param_name is FUNCTION_PARAMS:
        pass
    # Allow ControlProjection, LearningProjection
    elif isinstance(param_value, Projection):
        from PsyNeuLink.Components.Projections.ControlProjection import ControlProjection
        from PsyNeuLink.Components.Projections.LearningProjection import LearningProjection
        if isinstance(param_value, (ControlProjection, LearningProjection)):
            pass
        else:
            return
    # Allow Projection class
    elif inspect.isclass(param_value) and issubclass(param_value, Projection):
        from PsyNeuLink.Components.Projections.ControlProjection import ControlProjection
        from PsyNeuLink.Components.Projections.LearningProjection import LearningProjection
        if issubclass(param_value, (ControlProjection, LearningProjection)):
            pass
        else:
            return
    # Allow tuples (could be spec that includes a projection or ModulationOperation)
    elif isinstance(param_value, tuple):
        pass
    # Allow if it is a keyword for a parameter
    elif isinstance(param_value, str) and param_value in parameter_keywords:
        pass
    # elif param_value is NotImplemented:
    #     return
    # Exclude function (see docstring above)
    elif param_name is FUNCTION:
        return
    # Exclude all others
    else:
        return

    if param_name is FUNCTION_PARAMS:
        for function_param_name, function_param_value in param_value.items():
            # Assignment of ParameterState for Component objects, function or method are not currently supported
            if isinstance(function_param_value, (function_type, method_type, Component)):
                continue
            state = _instantiate_state(owner=owner,
                                      state_type=ParameterState,
                                      state_name=function_param_name,
                                      state_spec=function_param_value,
                                      state_params=None,
                                      constraint_value=function_param_value,
                                      constraint_value_name=function_param_name,
                                      context=context)
            if state:
                owner.parameterStates[function_param_name] = state
            continue

    else:
        state = _instantiate_state(owner=owner,
                                  state_type=ParameterState,
                                  state_name=param_name,
                                  state_spec=param_value,
                                  state_params=None,
                                  constraint_value=param_value,
                                  constraint_value_name=param_name,
                                  context=context)
        if state:
            owner.parameterStates[param_name] = state

