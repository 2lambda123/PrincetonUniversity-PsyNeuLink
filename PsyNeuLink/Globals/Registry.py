# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
#
# ***********************************************  Registry ************************************************************
#
import PsyNeuLink.Functions.Function
from collections import namedtuple
from inspect import isclass

# IMPLEMENTATION NOTE:
# - Implement Registry as class, and each Registry as subclass
# - Implement RegistryPreferenceSet as PreferenceSet subclass, and assign prefs attribute to each Registry object

DEFAULT_REGISTRY_VERBOSITY = False
from PsyNeuLink.Globals.Keywords import *
RegistryVerbosePrefs = {
    kwPreferenceSet: DEFAULT_REGISTRY_VERBOSITY,
    kwFunctionPreferenceSet: DEFAULT_REGISTRY_VERBOSITY,
    kwProcessFunctionCategory: DEFAULT_REGISTRY_VERBOSITY,
    kwMechanismFunctionCategory: DEFAULT_REGISTRY_VERBOSITY,
    kwStateFunctionCategory: DEFAULT_REGISTRY_VERBOSITY,
    kwInputState: DEFAULT_REGISTRY_VERBOSITY,
    kwParameterState: DEFAULT_REGISTRY_VERBOSITY,
    kwOutputState: DEFAULT_REGISTRY_VERBOSITY,
    kwDDM: DEFAULT_REGISTRY_VERBOSITY,
    kwProjectionFunctionCategory: DEFAULT_REGISTRY_VERBOSITY,
    CONTROL_SIGNAL: DEFAULT_REGISTRY_VERBOSITY,
    MAPPING: DEFAULT_REGISTRY_VERBOSITY,
    kwUtilityFunctionCategory: DEFAULT_REGISTRY_VERBOSITY,
}

RegistryEntry = namedtuple('RegistryTuple', 'subclass, instanceDict, instanceCount, default')

def rreplace(myStr, old, new, count):
    return myStr[::-1].replace(old[::-1], new[::-1], count)[::-1]


class RegistryError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


def register_category(entry,
                      base_class,
                      name=NotImplemented,
                      registry=NotImplemented,
                      context='Registry'):
# MODIFIED 9/10/16 END
# DOCUMENT:
    """Maintains registry of subclasses for base_class, names instances incrementally, and sets default

    Arguments:
    - entry (object or class)
    - base_class (parent class for entry)
    - registry (dict)

# DOCUMENTATION:
             - Naming procedure / conventions
             - Default procedure /conventions

             TBI:
             - sub group option:  allows instances to be sub-grouped by the attribute passed in sub_group_attr arg

             If sub_group_attr, then:
                 - instead of implementing instance dict directly, implement subgroup dict
                 - when an entry is made, check for owner in sub-dict
                 - if no owner, create entry for owner, instance dict for that owner, and log instance in instance dict
                 - if owner is found, but no instances, create instance dict for that owner
                 - if owner and instance dict exist, make entry

                 - implement instance dict within subgroup



# IMPLEMENTATION NOTE:
        ADD DEFAULT MANAGEMENT (USEFUL AT LEAST FOR PROCESS... OTHERS ARE CONTEXT-SPECIFIC)
        # # MechanismRegistry ------------------------------------------------------------------------
        # #
        # # Dictionary of registered Mechanism subclasses; each entry has:
        # #     - key: Mechanism function type name (functionType)
        # #     - value: MechanismEntry tuple (mechanism, instanceCount, default)
        # #              Notes:
        # #              * instanceCount is incremented each time a new default instance is created
        # #              * only one default is allowed;  if a mechanism registers itself as default,
        # #                  that displaces whatever was the default previously;  initially it is DDM
        #
        # # MechanismRegistry = {DefaultReceiver.name:(DefaultReceiverMechanism, 1)}
        #

    :param entry:
    :param default:
    :return:
    """

    if not issubclass(base_class, object):
        raise RegistryError("base_class ({0}) for registry must be a subclass of Function".format(base_class))

    # if registry is NotImplemented:
    #     try:
    #         registry = base_class.registry
    #     except AttributeError:
    #         raise RegistryError("{0} must be a dict".format(registry))

    if not isinstance(registry, dict):
        raise RegistryError("Registry ({0}) for {1} must be a dict".format(registry,base_class.__name__))

    # if sub_group_attr:
    #     if not isinstance(sub_group_attr, str):
    #         raise RegistryError("sub_group_attr arg ({0}) must be a str that is the name of an attribute of {1} ".
    #                             format(sub_group_attr,entry.__class__.__name__))
    #     try:
    #         sub_group = getattr(entry,sub_group_attr)
    #     except AttributeError:
    #         raise RegistryError("sub_group_attr arg ({0}) must be an attribute of {1} ".
    #                             format(sub_group_attr,entry.__class__.__name__))
    #
    # If entry is an instance (presumably of a function type of the base class):
    if isinstance(entry, base_class):

        function_type_name = entry.__class__.__name__

        # Function type is registered (i.e., there is an entry for function_type_name)
        if function_type_name in registry:
            register_instance(entry=entry,
                              name=name,
                              base_class=base_class,
                              registry=registry,
                              sub_dict=function_type_name)

        # If function type is not already registered in registry, then:
        else:
            # Set instance's name to first instance:
            # If name was not provided, assign functionType-1 as default;
            if not name or name is NotImplemented:
                entry.name = entry.functionType + "-1"
            else:
                entry.name = name

            # Create instance dict:
            instanceDict = {entry.name: entry}

            # Register function type with instance count of 1:
            registry[function_type_name] = RegistryEntry(type(entry), instanceDict, 1, False)


    # If entry is a reference to the function type (rather than an instance of it)
    elif issubclass(entry, base_class):
        function_type_name = entry.__name__
        # If it is already there, ignore
        if function_type_name in registry:
            pass
        # If it is not there:
        # - create entry for function type in registry
        # - instantiate empty instanceDict
        # - set instance count = 0
        else:
            registry[function_type_name] = RegistryEntry(entry, {}, 0, False)

    else:
        raise RegistryError("Requested entry {0} not of type {1}".format(entry, base_class))


def register_instance(entry, name, base_class, registry, sub_dict):

            # Get and increment instanceCount
            instanceCount = registry[sub_dict].instanceCount + 1

            # If instance does not have a name, set instance's name to "function_type_name-1"
            if not name or name is NotImplemented:
                entry.name = sub_dict+'-1'
            else:
                entry.name = name

            # Check for instance name in instanceDict for its function type;
            # - if name exists, add numerical suffix if none, and increment if already present
            old_entry_name = entry.name
            while entry.name in registry[sub_dict].instanceDict:
                try:
                    # Check if name ends in '-number'
                    numerical_suffix = [int(s) for s in entry.name.rsplit('-') if s.isdigit()][-1]
                except IndexError:
                    # Otherwise, add '-1' as suffix
                    entry.name = entry.name+'-1'
                else:
                # If so, replace only final occurence of '-number' with '-number+1'
                    if numerical_suffix:
                        # entry.name.rreplace('-'+str(numerical_suffix),'-'+str(numerical_suffix+1),1)
                        entry.name = rreplace(entry.name, '-'+str(numerical_suffix),'-'+str(numerical_suffix+1),1)
                        if RegistryVerbosePrefs[base_class.__name__]:
                            print("Object named {0} already registered; current one will be re-named {1}.".
                                  format(old_entry_name, entry.name))

            # Add instance to instanceDict:
            registry[sub_dict].instanceDict.update({entry.name: entry})

            # Update instanceCount in registry:
            registry[sub_dict] = registry[sub_dict]._replace(instanceCount=instanceCount)

# def set_default_mechanism(mechanism_subclass):
#     """Sets DefaultMechanism to specified function type
#
#     :param mechanism_subclass:
#     :return:
#     """
#
#     if not (issubclass(mechanism_subclass, Mechanism)):
#         raise MechanismError("Requested mechanism {0} not of type {1}".format(mechanism_subclass, type(Mechanism)))
#
#     # Remove existing default flag
#     old_default_name = NotImplemented
#     for function_type_name in MechanismRegistry:
#         if MechanismRegistry[function_type_name].default:
#             old_default_name = function_type_name
#             MechanismRegistry[function_type_name] = MechanismRegistry[function_type_name]._replace(default=False)
#
#
#     # Flag specified function type as default
#     try:
#         MechanismRegistry[mechanism_subclass.functionType] =\
#             MechanismRegistry[mechanism_subclass.functionType]._replace(default=True)
#     # Not yet registered, so do so as default
#     except KeyError:
#         register_mechanism_subclass(mechanism_subclass)
#         MechanismRegistry[mechanism_subclass.functionType] =\
#             MechanismRegistry[mechanism_subclass.functionType]._replace(default=True)

#     # Assign to DefaultMechanism
#     Functions.DefaultMechanism = MechanismRegistry[mechanism_subclass.name].mechanismSubclass
# mechanism_subclass
#     # Issue warning
#     if self.prefs.verbosePref:
#         print("{0} set as new default mechanism ({1}) removed)".format(mechanism_subclass.name, old_default_name))

