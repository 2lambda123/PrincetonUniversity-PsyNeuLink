# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# *******************************************  AutoAssociativeProjection ***********************************************

"""
.. _Auto_Associative_Overview:

Intro
-----

I am basically just a MappingProjection, except I'm intended to be used as a recurrent projection. I thus require
that my matrix (with which I multiply my input to produce my output) is a square matrix. By default I point to/from the
primary input state and output state of my owner. But you can specify the input and output state as well.
"""

from PsyNeuLink.Globals.Keywords import AUTO_ASSOCIATIVE_PROJECTION, DEFAULT_MATRIX, AUTO, CROSS, CHANGED, PARAMS_CURRENT
from PsyNeuLink.Components.Projections.Projection import *
from PsyNeuLink.Components.Projections.PathwayProjections.PathwayProjection import PathwayProjection_Base
from PsyNeuLink.Components.Projections.PathwayProjections.MappingProjection import MappingProjection
from PsyNeuLink.Components.Functions.Function import *
from PsyNeuLink.Components.States.State import _instantiate_state
from PsyNeuLink.Components.States.ParameterState import ParameterState
from PsyNeuLink.Scheduling.TimeScale import CentralClock

parameter_keywords.update({AUTO_ASSOCIATIVE_PROJECTION})
projection_keywords.update({AUTO_ASSOCIATIVE_PROJECTION})

class AutoAssociativeError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

class AutoAssociativeProjection(MappingProjection):
    """
    Insert docs here
    """

    componentType = AUTO_ASSOCIATIVE_PROJECTION
    className = componentType
    suffix = " " + className

    classPreferenceLevel = PreferenceLevel.TYPE

    # necessary?
    paramClassDefaults = MappingProjection.paramClassDefaults.copy()

    @tc.typecheck
    def __init__(self,
                 owner=None,
                 sender=None,
                 receiver=None,
                 matrix=DEFAULT_MATRIX,
                 auto=None,
                 cross=None,
                 params=None,
                 name=None,
                 prefs: is_pref_set = None,
                 context=None):

        if owner is not None:
            if not isinstance(owner, Mechanism):
                raise AutoAssociativeError('Owner of AutoAssociative Mechanism must either be None or a Mechanism')
            if sender is None:
                sender = owner
            if receiver is None:
                receiver = owner

        if isinstance(cross, list):
            cross = np.array(cross)

        params = self._assign_args_to_param_dicts(auto=auto, cross=cross, function_params={MATRIX: matrix}, params=params)

        super().__init__(sender=sender,
                         receiver=receiver,
                         matrix=matrix,
                         params=params,
                         name=name,
                         prefs=prefs,
                         context=context)

    def _instantiate_attributes_before_function(self, context=None):
        """
        """

        super()._instantiate_attributes_before_function(context=context)

        # using `matrix`, instantiate ParameterStates for auto and cross if they haven't already been instantiated
        # this can occur if auto and cross were None in the initialization call
        param_keys = self._parameter_states.key_values
        specified_matrix = get_matrix(self.params[FUNCTION_PARAMS]['matrix'], self.size[0], self.size[0])

        if AUTO not in param_keys:
            d = np.diagonal(specified_matrix).copy()
            state = _instantiate_state(owner=self,
                                       state_type=ParameterState,
                                       state_name=AUTO,
                                       state_spec=d,
                                       state_params=None,
                                       constraint_value=d,
                                       constraint_value_name=AUTO,
                                       context=context)
            if state is not None:
                self._parameter_states[AUTO] = state
            else:
                raise AutoAssociativeError("Failed to create ParameterState for `auto` attribute for {} \"{}\"".
                                           format(self.__class__.__name__, self.name))
        if CROSS not in param_keys:
            m = specified_matrix.copy()
            np.fill_diagonal(m, 0.0)
            state = _instantiate_state(owner=self,
                                       state_type=ParameterState,
                                       state_name=CROSS,
                                       state_spec=m,
                                       state_params=None,
                                       constraint_value=m,
                                       constraint_value_name=CROSS,
                                       context=context)
            if state is not None:
                self._parameter_states[CROSS] = state
            else:
                raise AutoAssociativeError("Failed to create ParameterState for `cross` attribute for {} \"{}\"".
                                           format(self.__class__.__name__, self.name))

    def _instantiate_attributes_after_function(self, context=None):
        """Create self.matrix based on auto and cross, if specified
        """

        super()._instantiate_attributes_after_function(context=context)
        auto = self.params[AUTO]
        cross = self.params[CROSS]
        if auto is not None and cross is not None:
            a = get_auto_matrix(auto, size=self.size[0])
            if a is None:
                raise AutoAssociativeError("The `auto` parameter of {} {} was invalid: it was equal to {}, and was of "
                                           "type {}. Instead, the `auto` parameter should be a number, 1D array, "
                                           "2d array, 2d list, or numpy matrix".
                                           format(self.__class__.__name__, self.name, auto, type(auto)))
            c = get_cross_matrix(cross, size=self.size[0])
            if c is None:
                raise AutoAssociativeError("The `cross` parameter of {} {} was invalid: it was equal to {}, and was of "
                                           "type {}. Instead, the `cross` parameter should be a number, 1D array of "
                                           "length one, 2d array, 2d list, or numpy matrix".
                                           format(self.__class__.__name__, self.name, cross, type(cross)))
            self.matrix = a + c
        elif auto is not None:
            self.matrix = get_auto_matrix(auto, size=self.size[0])
            if self.matrix is None:
                raise AutoAssociativeError("The `auto` parameter of {} {} was invalid: it was equal to {}, and was of "
                                           "type {}. Instead, the `auto` parameter should be a number, 1D array, "
                                           "2d array, 2d list, or numpy matrix".
                                           format(self.__class__.__name__, self.name, auto, type(auto)))

        elif cross is not None:
            self.matrix = get_cross_matrix(cross, size=self.size[0])
            if self.matrix is None:
                raise AutoAssociativeError("The `cross` parameter of {} {} was invalid: it was equal to {}, and was of "
                                           "type {}. Instead, the `cross` parameter should be a number, 1D array of "
                                           "length one, 2d array, 2d list, or numpy matrix".
                                           format(self.__class__.__name__, self.name, cross, type(cross)))

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

        self._update_parameter_states(runtime_params=params, time_scale=time_scale, context=context)

        param_keys = self._parameter_states.key_values
        if AUTO not in param_keys or CROSS not in param_keys:
            raise AutoAssociativeError("Auto or Cross ParameterState not found in {} \"{}\"; here are names of the "
                                       "current ParameterStates for {}: {}".format(self.__class__.__name__, self.name,
                                                                           self.name, param_keys))

        # read auto and cross from their ParameterStates, and put them into `auto_matrix` and `cross_matrix`
        raw_auto = self._parameter_states[AUTO].value
        auto_matrix = get_auto_matrix(raw_auto=raw_auto, size=self.size[0])
        if auto_matrix is None:
            raise AutoAssociativeError("The `auto` parameter of {} {} was invalid: it was equal to {}, and was of "
                                       "type {}. Instead, the `auto` parameter should be a number, 1D array, "
                                       "2d array, 2d list, or numpy matrix".
                                       format(self.__class__.__name__, self.name, raw_auto, type(raw_auto)))

        raw_cross = self._parameter_states[CROSS].value
        cross_matrix = get_cross_matrix(raw_cross = raw_cross, size = self.size[0])
        if cross_matrix is None:
            raise AutoAssociativeError("The `cross` parameter of {} {} was invalid: it was equal to {}, and was of "
                                       "type {}. Instead, the `cross` parameter should be a number, 1D array of "
                                       "length one, 2d array, 2d list, or numpy matrix".
                                       format(self.__class__.__name__, self.name, raw_cross, type(raw_cross)))
        self.matrix = auto_matrix + cross_matrix

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


# a helper function that takes a specification of `cross` and returns a hollow matrix with the right values
# (possibly also used by RecurrentTransferMechanism.py)
def get_cross_matrix(raw_cross, size):
    if isinstance(raw_cross, numbers.Number):
        return get_matrix(HOLLOW_MATRIX, size, size) * raw_cross
    elif ((isinstance(raw_cross, np.ndarray) and raw_cross.ndim == 1) or
              (isinstance(raw_cross, list) and np.array(raw_cross).ndim == 1)):
        if len(raw_cross) != 1:
            return None
        return get_matrix(HOLLOW_MATRIX, size, size) * raw_cross[0]
    elif (isinstance(raw_cross, np.matrix) or
              (isinstance(raw_cross, np.ndarray) and raw_cross.ndim == 2) or
              (isinstance(raw_cross, list) and np.array(raw_cross).ndim == 2)):
        # we COULD add a validation here to ensure raw_cross is hollow, but it would slow stuff down.
        return np.array(raw_cross)
    else:
        return None

# similar to get_cross_matrix() above
def get_auto_matrix(raw_auto, size):
    if isinstance(raw_auto, numbers.Number):
        return np.diag(np.full(size, raw_auto))
    elif ((isinstance(raw_auto, np.ndarray) and raw_auto.ndim == 1) or
              (isinstance(raw_auto, list) and np.array(raw_auto).ndim == 1)):
        if len(raw_auto) == 1:
            return np.diag(np.full(size, raw_auto[0]))
        else:
            if len(raw_auto) != size:
                return None
            return np.diag(raw_auto)
    elif (isinstance(raw_auto, np.matrix) or
              (isinstance(raw_auto, np.ndarray) and raw_auto.ndim == 2) or
              (isinstance(raw_auto, list) and np.array(raw_auto).ndim == 2)):
        # we COULD add a validation here to ensure raw_auto is diagonal, but it would slow stuff down.
        return np.array(raw_auto)
    else:
        return None