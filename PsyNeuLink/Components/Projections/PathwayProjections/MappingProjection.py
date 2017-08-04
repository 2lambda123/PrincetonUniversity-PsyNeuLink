# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# **********************************************  MappingProjection ****************************************************

"""
.. _Mapping_Overview:

Overview
--------

A MappingProjection transmits the `value <OutputState.value>` of an `OutputState` of one `ProcessingMechanism` (its
`sender <MappingProjection.sender>`) to the `InputState` of another (its `receiver <MappingProjection.receiver>`).
The default `function <MappingProjection.function>` for a MappingProjection is  `LinearMatrix`, which uses the
MappingProjection's `matrix <MappingProjection.matrix>` attribute to transform the value received from its `sender
<MappingProjection.sender>` and provide the result to its `receiver <MappingProjection.receiver>`.

.. _Mapping_Creation:

Creating a MappingProjection
-----------------------------

A MappingProjection can be created in any of the ways that can be used to create a `Projection <Projection_Creation>`).
MappingProjections are also generated automatically in the following circumstances, using a value for its `matrix
<MappingProjection.matrix>` parameter appropriate to the circumstance:

  * by a `Process`, when two adjacent `Mechanisms <Mechanism>` in its `pathway <Process.pathway>` do not already have a
    Projection assigned between them (`AUTO_ASSIGN_MATRIX` is used as the `matrix <MappingProjection.matrix>`
    specification, which determines the appropriate matrix by context);
  ..
  * by an `ObjectiveMechanism`, from each `OutputState` listed in its `monitored_values
    <ObjectiveMechanism.monitored_values>` attribute to the corresponding `InputState` of the ObjectiveMechanism
    (`AUTO_ASSIGN_MATRIX` is used as the `matrix <MappingProjection.matrix>` specification, which determines the
    appropriate matrix by context);
  ..
  * by a `LearningMechanism`, between it and the other components required to implement learning
    (see `LearningMechanism_Learning_Configurations` for details);
  ..
  * by a `ControlMechanism <ControlMechanism>`, from the `ObjectiveMechanism` that `it creates
    <ControlMechanism_Monitored_Values>` to its `primary InputState <InputState_Primary>`, and from the OutputStates
    listed in the ControlMechanism's `monitored_output_states <ControlMechanism_Base.monitored_output_states>`
    attribute) to the ObjectiveMechanism (as described above; an `IDENTITY_MATRIX` is used for all of these).

.. _Mapping_Matrix_Specification:

Matrix Parameter
~~~~~~~~~~~~~~~~

When a MappingProjection is created explicitly, the **matrix** argument of its constructor can be used to specify
its `matrix <MappingProjection.matrix>` parameter.  This is used by the MappingProjection's `function
<MappingProjection.function>` to transform the input from its `sender <MappingProjection.sender>` into the `value
<MappingProjection.value>` provided to its `receiver <MappingProjection.receiver>`. It can be specified in any of the
following ways:

  * **List, array or matrix**  -- if it is a list, each item must be a list or 1d np.array of numbers;  otherwise,
    it must be a 2d np.array or np.matrix.  In each case, the outer dimension (outer list items, array axis 0,
    or matrix rows) corresponds to the elements of the `sender <MappingProjection.sender>`, and the inner dimension
    (inner list items, array axis 1, or matrix columns) corresponds to the weighting of the contribution that a
    given `sender <MappingProjection.sender>` makes to the `receiver <MappingProjection.receiver>` (the number of which
    must match the length of the receiver's `variable <InputState.variable>`).

  .. _Matrix_Keywords:

  * **Matrix keyword** -- used to specify a standard type of matrix without having to specify its individual
    values, or to allow the type of matrix to be determined by context;  any of the `matrix keywords
    <Keywords.MatrixKeywords>` can be used.

  ..
  * **Random matrix function** (`random_matrix <Utilities.random_matrix>`) -- a convenience function
    that provides more flexibility than `RANDOM_CONNECTIVITY_MATRIX`.  It generates a random matrix sized for a
    **sender** and **receiver**, with random numbers drawn from a uniform distribution within a specified **range** and
    with a specified **offset**.

  .. _MappingProjection_Tuple_Specification:

  * **Tuple** -- used to specify the `matrix <MappingProjection.matrix>` along with a specification for learning;
    The tuple must have two items: the first can be any of the specifications described above; the second must be
    a specification for `LearningProjection`, using either the keywords *LEARNING_PROJECTION* or *LEARNING*, or a
    reference to the class (in which case a default LearningProjection is created), or an existing LearningProjection.

.. _MappingProjection_Deferred_Initialization:

Deferred Initialization
~~~~~~~~~~~~~~~~~~~~~~~

When a MappingProjection is created, its full initialization is `deferred <Component_Deferred_Init>` until its
`sender <MappingProjection.sender>` and `receiver <MappingProjection.receiver>` have been fully specified.  This
allows a MappingProjection to be created before its `sender <MappingProjection.sender>` and/or `receiver
<MappingProjection.receiver>` have been created (e.g., before them in a script), by calling its constructor without
specifying its **sender** or **receiver** arguments. However, for the MappingProjection to be operational,
initialization must be completed by calling its `deferred_init` method.  This is not necessary if the MappingProjection
is specified in the `pathway <Process_Base.pathway>` of `Process`, or anywhere else that its `sender
<MappingProjection.sender>` and receiver <MappingProjection.receiver>` can be determined by context.

.. _Mapping_Structure:

Structure
---------

COMMENT:
    .. _MappingProjection_Sender:
    .. _MappingProjection_Receiver:
    XXXX NEED TO ADD DESCRIPTION OF SENDER AND RECEIVER -- SPECIFIED AS MECHANISM OR STATE.

COMMENT

COMMENT:
    XXXX NEED TO ADD SOMETHING ABOUT HOW A LearningProjection CAN BE SPECIFIED HERE:
            IN THE pathway FOR A process;  BUT ALSO IN ITS CONSTRUCTOR??
            SEE BELOW:  If there is a params[FUNCTION_PARAMS][MATRIX][1]
    SPECIFIED IN TUPLE ASSIGNED TO MATRIX PARAM (MATRIX ENTRY OF PARAMS DICT)

COMMENT

In addition to its `function <MappingProjection.function>`, MappingProjections use the following two parameters:

.. _Mapping_Matrix:

* `matrix <MappingProjection.matrix>`

  Used by the MappingProjection's `function <MappingProjection.function>` to carry out a matrix transformation of its
  input, that is then provided to its `receiver <MappingProjection.receiver>`.  It can be specified using a number of
  different formats, as described `above <Mapping_Matrix_Specification>`.

.. _Mapping_Execution:

Execution
---------

A MappingProjection uses its `function <MappingProjection.function>` and `matrix <MappingProjection.matrix>`
parameter to transform its `sender <MappingProjection.sender>` into a form suitable for the `variable
<InputState.variable>` of its `receiver <MappingProjection.receiver>`.  When executed, it updates its *MATRIX*
`ParameterState`, that in turn updates its `matrix <MappingProjection.matrix>` parameter based on any
`LearningProjection(s)` it receives (listed in the ParameterState's `mod_afferents <ParameterState.mod_afferents>`
attribute).  This brings into effect any changes that occurred due to `learning <LearningMechanism_Execution>` in the
previous `TRIAL` of execution of the `System <System_Base_Execution>` or `Process <Process_Base_Execution>` to which
the  MappingProjection belongs.  Because of :ref:`Lazy Evaluation <LINK>`, those changes take effect only after the
current `TRIAL` of execution; as a consequence, inspecting `matrix <MappingProjection.matrix>` or its ParameterState do
not show the effects of learning until the MappingProjection has been executed.

.. _Mapping_Class_Reference:


Class Reference
---------------

"""
import inspect
import typecheck as tc

import numpy as np

from PsyNeuLink.Components.Component import InitStatus, parameter_keywords
from PsyNeuLink.Components.Functions.Function import AccumulatorIntegrator, LinearMatrix, get_matrix
from PsyNeuLink.Components.Projections.PathwayProjections.PathwayProjection import PathwayProjection_Base
from PsyNeuLink.Components.Projections.Projection import ProjectionError, Projection_Base, projection_keywords
from PsyNeuLink.Components.ShellClasses import Projection
from PsyNeuLink.Globals.Keywords import AUTO_ASSIGN_MATRIX, CHANGED, CONTROL_PROJECTION, DEFAULT_MATRIX, \
    DEFERRED_INITIALIZATION, FULL_CONNECTIVITY_MATRIX, FUNCTION, FUNCTION_PARAMS, HOLLOW_MATRIX, IDENTITY_MATRIX, \
    LEARNING, LEARNING_PROJECTION, MAPPING_PROJECTION, MATRIX, OUTPUT_STATE, PROJECTION_SENDER, PROJECTION_SENDER_VALUE
from PsyNeuLink.Globals.Preferences.ComponentPreferenceSet import is_pref_set
from PsyNeuLink.Globals.Preferences.PreferenceSet import PreferenceEntry, PreferenceLevel
from PsyNeuLink.Scheduling.TimeScale import CentralClock

parameter_keywords.update({MAPPING_PROJECTION})
projection_keywords.update({MAPPING_PROJECTION})


class MappingError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value


class MappingProjection(PathwayProjection_Base):
    """
    MappingProjection(                                      \
        sender=None,                                        \
        receiver=None,                                      \
        matrix=DEFAULT_MATRIX,                              \
        params=None,                                        \
        name=None,                                          \
        prefs=None)

    Implements a Projection that transmits the output of one mechanism to the input of another.


    COMMENT:
        Description:
            The MappingProjection class is a type in the Projection category of Component.
            It implements a Projection that takes the value of an OutputState of one mechanism, transforms it as
            necessary, and provides it to the inputState of another ProcessingMechanism.
            It's function conveys (and possibly transforms) the OutputState.value of a sender
                to the InputState.value of a receiver.

            IMPLEMENTATION NOTE:
                AUGMENT SO THAT SENDER CAN BE A Mechanism WITH MULTIPLE OUTPUT STATES, IN WHICH CASE:
                    RECEIVER MUST EITHER BE A MECHANISM WITH SAME NUMBER OF INPUT STATES AS SENDER HAS OUTPUTSTATES
                        (FOR WHICH SENDER OUTPUTSTATE IS MAPPED TO THE CORRESPONDING RECEIVER INPUT STATE
                            USING THE SAME MAPPING_PROJECTION MATRIX, OR AN ARRAY OF THEM)
                    OR BOTH MUST BE 1D ARRAYS (I.E., SINGLE VECTOR)
                    SHOULD BE CHECKED IN OVERRIDE OF _validate_variable
                        THEN HANDLED IN _instantiate_sender and _instantiate_receiver

        Class attributes:
            + className = MAPPING_PROJECTION
            + componentType = PROJECTION
            + paramClassDefaults (dict)
                paramClassDefaults.update({
                                   FUNCTION:LinearMatrix,
                                   FUNCTION_PARAMS: {
                                       # LinearMatrix.kwReceiver: receiver.value,
                                       LinearMatrix.MATRIX: LinearMatrix.DEFAULT_MATRIX},
                                   PROJECTION_SENDER: INPUT_STATE, # Assigned to class ref in __init__ module
                                   PROJECTION_SENDER_VALUE: [1],
                                   })
            + classPreference (PreferenceSet): MappingPreferenceSet, instantiated in __init__()
            + classPreferenceLevel (PreferenceLevel): PreferenceLevel.TYPE

        Class methods:
            function (executes function specified in params[FUNCTION]
    COMMENT

    Arguments
    ---------

    sender : Optional[OutputState or Mechanism]
        specifies the source of the Projection's input. If a mechanism is specified, its
        `primary OutputState <OutputState_Primary>` will be used. If it is not specified, it will be assigned in
        the context in which the Projection is used.

    receiver: Optional[InputState or Mechanism]
        specifies the destination of the Projection's output.  If a mechanism is specified, its
        `primary InputState <InputState_Primary>` will be used. If it is not specified, it will be assigned in
        the context in which the Projection is used.

    matrix : list, np.ndarray, np.matrix, function or keyword : default DEFAULT_MATRIX
        the matrix used by `function <MappingProjection.function>` (default: `LinearCombination`) to transform the
        value of the `sender <MappingProjection.sender>`.

    params : Optional[Dict[param keyword, param value]]
        a `parameter dictionary <ParameterState_Specification>` that can be used to specify the parameters for
        the Projection, its function, and/or a custom function and its parameters. By default, it contains an entry for
        the Projection's default assignment (`LinearCombination`).  Values specified for parameters in the dictionary
        override any assigned to those parameters in arguments of the constructor.

    name : str : default MappingProjection-<index>
        a string used for the name of the MappingProjection.
        If not is specified, a default is assigned by `ProjectionRegistry`
        (see `Registry <LINK>` for conventions used in naming, including for default and duplicate names).

    prefs : Optional[PreferenceSet or specification dict : Projection.classPreferences]
        the `PreferenceSet` for the MappingProjection.
        If it is not specified, a default is assigned using `classPreferences` defined in __init__.py
        (see `PreferenceSet <LINK>` for details).

    Attributes
    ----------

    componentType : MAPPING_PROJECTION

    sender : OutputState
        identifies the source of the Projection's input.

    receiver: InputState
        identifies the destination of the Projection.

    learning_mechanism : LearningMechanism
        source of error signal for that determine changes to the `matrix <MappingProjection.matrix>` when
        `learning <LearningProjection>` is used.

    matrix : 2d np.array
        matrix used by `function <MappingProjection.function>` to transform input from the
        `sender <MappingProjection.sender>` to the value provided to the `receiver <MappingProjection.receiver>`.

    has_learning_projection : bool : False
        identifies whether the MappingProjection's `MATRIX` `ParameterState <ParameterState>` has been assigned a
        `LearningProjection`.

    value : ndarray
        Output of MappingProjection, transmitted to `variable <InputState.variable>` of `receiver
        <MappingProjection.receiver>`.

    name : str : default MappingProjection-<index>
        the name of the MappingProjection.
        Specified in the **name** argument of the constructor for the Projection;
        if not is specified, a default is assigned by ProjectionRegistry
        (see :doc:`Registry <LINK>` for conventions used in naming, including for default and duplicate names).

    prefs : PreferenceSet or specification dict : Projection.classPreferences
        the `PreferenceSet` for Projection.
        Specified in the **prefs** argument of the constructor for the Projection;
        if it is not specified, a default is assigned using `classPreferences` defined in __init__.py
        (see :doc:`PreferenceSet <LINK>` for details).

    """

    componentType = MAPPING_PROJECTION
    className = componentType
    suffix = " " + className

    classPreferenceLevel = PreferenceLevel.TYPE

    paramClassDefaults = Projection_Base.paramClassDefaults.copy()
    paramClassDefaults.update({FUNCTION: LinearMatrix,
                               PROJECTION_SENDER: OUTPUT_STATE, # Assigned to class ref in __init__.py module
                               PROJECTION_SENDER_VALUE: [1],
                               })
    @tc.typecheck
    def __init__(self,
                 sender=None,
                 receiver=None,
                 matrix=DEFAULT_MATRIX,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 context=None):

        # if matrix is DEFAULT_MATRIX:
        #     initializer = get_matrix(matrix)
        #     initial_rate = initializer * 0.0
        #     matrix={VALUE:DEFAULT_MATRIX,
        #             FUNCTION:ConstantIntegrator(owner=self._parameter_states[MATRIX],
        #                                         initializer=get_matrix(DEFAULT_MATRIX),
        #                                         rate=initial_rate)}

        # Assign args to params and functionParams dicts (kwConstants must == arg names)
        # Assign matrix to function_params for use as matrix param of MappingProjection.function
        # (7/12/17 CW) this is a PATCH to allow the user to set matrix as an np.matrix... I still don't know why
        # it wasn't working.
        if isinstance(matrix, (np.matrix, list)):
            matrix = np.array(matrix)

        params = self._assign_args_to_param_dicts(
                function_params={MATRIX: matrix},
                params=params)

        self.learning_mechanism = None
        self.has_learning_projection = False

        # If sender or receiver has not been assigned, defer init to State.instantiate_projection_to_state()
        if sender is None or receiver is None:
            self.init_status = InitStatus.DEFERRED_INITIALIZATION

        # Validate sender (as variable) and params, and assign to variable and paramsInstanceDefaults
        super(MappingProjection, self).__init__(sender=sender,
                                                receiver=receiver,
                                                params=params,
                                                name=name,
                                                prefs=prefs,
                                                context=self)

    # def _instantiate_sender(self, context=None):
            # # IMPLEMENT: HANDLE MULTIPLE SENDER -> RECEIVER MAPPINGS, EACH WITH ITS OWN MATRIX:
            # #            - kwMATRIX NEEDS TO BE A 3D np.array, EACH 3D ITEM OF WHICH IS A 2D WEIGHT MATRIX
            # #            - MAKE SURE len(self.sender.value) == len(self.receiver.input_states.items())
            # # for i in range (len(self.sender.value)):
            # #            - CHECK EACH MATRIX AND ASSIGN??

    def _instantiate_parameter_states(self, context=None):

        super()._instantiate_parameter_states(context=context)

        # FIX: UPDATE FOR LEARNING
        # FIX: UPDATE WITH MODULATION_MODS
        # FIX: MOVE THIS TO MappingProjection.__init__;
        # FIX: AS IT IS, OVER-WRITES USER ASSIGNMENT OF FUNCTION IN params dict FOR MappingProjection
        matrix = get_matrix(self._parameter_states[MATRIX].value)
        initial_rate = matrix * 0.0

        self._parameter_states[MATRIX].function_object = AccumulatorIntegrator(owner=self._parameter_states[MATRIX],
                                                                            initializer=matrix,
                                                                            # rate=initial_rate
                                                                               )

        self._parameter_states[MATRIX]._function = self._parameter_states[MATRIX].function_object.function

    def _instantiate_receiver(self, context=None):
        """Determine matrix needed to map from sender to receiver

        Assign specification to self.matrix_spec attribute
        Assign matrix to self.matrix attribute

        """
        self.reshapedWeightMatrix = False

        # Get sender and receiver lengths
        # Note: if either is a scalar, manually set length to 1 to avoid TypeError in call to len()
        try:
            mapping_input_len = len(self.variable)
        except TypeError:
            mapping_input_len = 1
        try:
            receiver_len = len(self.receiver.variable)
        except TypeError:
            receiver_len = 1

        # Compare length of MappingProjection output and receiver's variable to be sure matrix has proper dimensions
        try:
            mapping_output_len = len(self.value)
        except TypeError:
            mapping_output_len = 1

        # FIX: CONVERT ALL REFS TO paramsCurrent[FUNCTION_PARAMS][MATRIX] TO self.matrix (CHECK THEY'RE THE SAME)
        # FIX: CONVERT ALL REFS TO matrix_spec TO self._matrix_spec
        # FIX: CREATE @PROPERTY FOR self._learning_spec AND ASSIGN IN INIT??
        # FIX: HOW DOES mapping_output_len RELATE TO receiver_len?/

        if self._matrix_spec is AUTO_ASSIGN_MATRIX:
            if mapping_input_len == receiver_len:
                self._matrix_spec = IDENTITY_MATRIX
            else:
                self._matrix_spec = FULL_CONNECTIVITY_MATRIX

        # Length of the output of the Projection doesn't match the length of the receiving input state
        #    so consider reshaping the matrix
        if mapping_output_len != receiver_len:

            if 'projection' in self.name or 'Projection' in self.name:
                projection_string = ''
            else:
                projection_string = 'projection'

            if not isinstance(self._matrix_spec, str):
                raise ProjectionError("Matrix ")

            elif self._matrix_spec == IDENTITY_MATRIX or self._matrix_spec == HOLLOW_MATRIX:
                # Identity matrix is not reshapable
                raise ProjectionError("Output length ({}) of \'{}{}\' from {} to mechanism \'{}\'"
                                      " must equal length of it InputState ({}) to use {}".
                                      format(mapping_output_len,
                                             self.name,
                                             projection_string,
                                             self.sender.name,
                                             self.receiver.owner.name,
                                             receiver_len,
                                             self._matrix_spec))
            else:
                # Flag that matrix is being reshaped
                self.reshapedWeightMatrix = True
                if self.prefs.verbosePref:
                    print("Length ({}) of the output of {}{} does not match the length ({}) "
                          "of the InputState for the receiver {}; the width of the matrix (number of columns); "
                          "the width of the matrix (number of columns) will be adjusted to accomodate the receiver".
                          format(mapping_output_len,
                                 self.name,
                                 projection_string,
                                 receiver_len,
                                 self.receiver.owner.name))

                self._matrix = get_matrix(self._matrix_spec, mapping_input_len, receiver_len, context=context)

                # Since matrix shape has changed, output of self.function may have changed, so update self.value
                self._update_value()

        super()._instantiate_receiver(context=context)

    def execute(self, input=None, clock=CentralClock, time_scale=None, params=None, context=None):
        """
        If there is a functionParameterStates[LEARNING_PROJECTION], update the matrix ParameterState:

        - it should set params[PARAMETER_STATE_PARAMS] = {kwLinearCombinationOperation:SUM (OR ADD??)}
          and then call its super().execute
        - use its value to update MATRIX using CombinationOperation (see State update ??execute method??)

        Assumes that if ``self.learning_mechanism`` is assigned *and* ParameterState[MATRIX] has been instantiated
        then learningSignal exists;  this averts duck typing which otherwise would be required for the most
        frequent cases (i.e., *no* learningSignal).

        """

        # IMPLEMENTATION NOTE (7/28/17 CW): The execute() method in AutoAssociativeProjection is heavily based on
        # this one, so if you make a change here, please make it there as well.

        # (7/18/17 CW) note that we don't let MappingProjections related to System inputs execute here (due to a
        # minor bug with execution ID): maybe we should just fix this bug instead, if it's useful to do so
        if "System" not in str(self.sender.owner):
            self._update_parameter_states(runtime_params=params, time_scale=time_scale, context=context)

        # Check whether error_signal has changed
        if self.learning_mechanism and self.learning_mechanism.status == CHANGED:

            # Assume that if learning_mechanism attribute is assigned,
            #    both a LearningProjection and ParameterState[MATRIX] to receive it have been instantiated
            matrix_parameter_state = self._parameter_states[MATRIX]

            # Assign current MATRIX to parameter state's base_value, so that it is updated in call to execute()
            setattr(self, '_'+MATRIX, self.matrix)

            # FIX: UPDATE FOR LEARNING BEGIN
            #    ??DELETE ONCE INTEGRATOR FUNCTION IS IMPLEMENTED
            # Pass params for ParameterState's function specified by instantiation in LearningProjection
            weight_change_params = matrix_parameter_state.paramsCurrent

            # Update parameter state: combines weightChangeMatrix from LearningProjection with matrix base_value
            matrix_parameter_state.update(weight_change_params, context=context)

            # Update MATRIX
            self.matrix = matrix_parameter_state.value
            # FIX: UPDATE FOR LEARNING END

            # # TEST PRINT
            # print("\n### WEIGHTS CHANGED FOR {} TRIAL {}:\n{}".format(self.name, CentralClock.trial, self.matrix))
            # # print("\n@@@ WEIGHTS CHANGED FOR {} TRIAL {}".format(self.name, CentralClock.trial))
            # TEST DEBUG MULTILAYER
            # print("\n{}\n### WEIGHTS CHANGED FOR {} TRIAL {}:\n{}".
            #       format(self.__class__.__name__.upper(), self.name, CentralClock.trial, self.matrix))


        return self.function(self.sender.value, params=params, context=context)

    @property
    def matrix(self):
        # return self.function.__self__.matrix
        return self.function_object.matrix

    @matrix.setter
    def matrix(self, matrix):
        if not (isinstance(matrix, np.matrix) or
                    (isinstance(matrix,np.ndarray) and matrix.ndim == 2) or
                    (isinstance(matrix,list) and np.array(matrix).ndim == 2)):
            raise MappingError("Matrix parameter for {} ({}) MappingProjection must be "
                               "an np.matrix, a 2d np.array, or a correspondingly configured list".
                               format(self.name, matrix))

        matrix = np.array(matrix)

        # FIX: Hack to prevent recursion in calls to setter and assign_params
        self.function.__self__.paramValidationPref = PreferenceEntry(False, PreferenceLevel.INSTANCE)

        # self.function.__self__.matrix = matrix
        self.function_object.matrix = matrix

        # (7/19/17 CW) patch! without this patch, setting myMappingProjection.matrix was not really working because
        # the Accumulator Integrator function of the "matrix" ParameterState of myMappingProjection was just ignoring
        # the variable. So this patch directly sets the 'variable' attribute of the integrator in order to
        # fix this bug and make setting myMappingProjection.matrix effective.
        # REMOVED 7/26/17 CW: feel free to remove all this commented block
        # if MATRIX in self._parameter_states.key_values:
        #     if ACCUMULATOR_INTEGRATOR in str(type(self._parameter_states[MATRIX].function_object)):
        #         self._parameter_states[MATRIX].function_object.variable = matrix
        #         self._parameter_states[MATRIX].value = self._parameter_states[MATRIX]._execute({}, context=INITIALIZING)

    @property
    def _matrix_spec(self):
        """Returns matrix specification in self.paramsCurrent[FUNCTION_PARAMS][MATRIX]

        Returns matrix param for MappingProjection, getting second item if it is
         an unnamed (matrix, projection) tuple
        """
        return self._get_param_value_from_tuple(self.paramsCurrent[FUNCTION_PARAMS][MATRIX])

    @_matrix_spec.setter
    def _matrix_spec(self, value):
        """Assign matrix specification for self.paramsCurrent[FUNCTION_PARAMS][MATRIX]

        Assigns matrix param for MappingProjection, assigning second item if it is
         a 2-item tuple or unnamed (matrix, projection) tuple
        """

        # Specification is a two-item tuple, so validate that 2nd item is:
        # *LEARNING* or *LEARNING_PROJECTION* keyword, LearningProjection subclass, or instance of a LearningPojection
        from PsyNeuLink.Components.Projections.ModulatoryProjections.LearningProjection import LearningProjection
        if (isinstance(self.paramsCurrent[FUNCTION_PARAMS][MATRIX], tuple) and
                    len(self.paramsCurrent[FUNCTION_PARAMS][MATRIX]) is 2 and
                (self.paramsCurrent[FUNCTION_PARAMS][MATRIX][1] in {LEARNING, LEARNING_PROJECTION}
                 or isinstance(self.paramsCurrent[FUNCTION_PARAMS][MATRIX][1], LearningProjection) or
                     (inspect.isclass(self.paramsCurrent[FUNCTION_PARAMS][MATRIX][1]) and
                          issubclass(self.paramsCurrent[FUNCTION_PARAMS][MATRIX][1], LearningProjection)))
            ):
            self.paramsCurrent[FUNCTION_PARAMS].__additem__(MATRIX,
                                                            (value, self.paramsCurrent[FUNCTION_PARAMS][MATRIX][1]))

        else:
            self.paramsCurrent[FUNCTION_PARAMS].__additem__(MATRIX, value)
