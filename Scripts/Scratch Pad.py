import numpy as np

class ScratchPadError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

# ----------------------------------------------- PsyNeuLink -----------------------------------------------------------
#
#region TEST INSTANTATION OF System() @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from Functions.Mechanisms.AdaptiveIntegrator import AdaptiveIntegratorMechanism
# from Functions.Utility import Integrator
#
# a = AdaptiveIntegratorMechanism([[0],[0]], params={FUNCTION_PARAMS:{Integrator.RATE:0.1}})
#
# init = [0,0,0]
# stim = [1,1,1]
#
# old = init
# new = stim
#
# for i in range(100):
#     old = a.execute([old,new])
#     print (old)
#
# print (a.execute([,[0, 2, 0][1, 1, 1]]))
#endregion

#region TEST INSTANTATION OF System() @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# from Functions.System import System_Base
# from Functions.Mechanisms.DDM import DDM
#
# mech = DDM()
#
# a = System_Base()
# a.execute()
#
#endregion

#region TEST MECHANISM @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# from Functions.Mechanisms.Mechanism import Mechanism, mechanism
# from Functions.Mechanisms.DDM import DDM

# x = Mechanism(context=kwValidate)
# test = isinstance(x,Mechanism)
# temp = True
#
#endregion

#region TEST PROCESS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# #
# from Functions.Process import *
# # from Functions.Mechanisms.DDM import DDM
# from Functions.Mechanisms.ProcessingMechanisms.Transfer import Transfer
#
# my_transfer = Transfer()
#
# x = Process_Base(params={CONFIGURATION:[my_transfer]})
#
# for i in range(100):
#     x.execute([1])
#
# endregion

#region TEST LinearCombination FUNCTION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from Functions.Utility import *
# #
# x = LinearCombination()
# print (x.execute(([1, 1],[2, 2])))

#endregion

#region TEST RL @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from PsyNeuLink.Functions.Utilities.Utility import *
#
# rl = Reinforcement([[0,0,0], [0,0,0], [0]])
# print(rl.execute([[0,0,0], [0, 0, 1], [7]]))
#

#endregion

#region TEST SoftMax FUNCTION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from PsyNeuLink.Functions.Utilities.Utility import *
# #
# x = SoftMax(output=SoftMax.PROB)
# y = x.execute([-11, 2, 3])
# print ("SoftMax execute return value: \n", y)
#
# # z = x.derivative(x.execute([-11, 2, 3]))
# # z = x.derivative(y)
# # z = x.derivative(output=y, input=[-11, 2, 3])
#
# # print ("SoftMax derivative return value: \n", z)

#endregion

#region TEST BackProp FUNCTION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from Functions.Utility import *
#
# x = BackPropagation()
# print (x.execute(variable=[[1, 2],[0.5, 0],[5, 6]]))
#
# # y = lambda input,output: output*(np.ones_like(output)-output)
# # print (y(2, [0.25, 0.5]))
#
#
#endregion

#region TEST ReportOUtput Pref @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from PsyNeuLink.Functions.Process import *
# from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.Transfer import Transfer
# from PsyNeuLink.Functions.Utilities.Utility import Linear
#
# my_mech = Transfer(function=Linear())
#
# my_process = process(configuration=[my_mech])
#
# my_mech.reportOutputPref = False
#
# # FIX: CAN'T CHANGE reportOutputPref FOR PROCESS USE LOCAL SETTER (DEFAULT WORKS)
# my_process.reportOutputPref = False
# my_process.verbosePref = False
#
# my_process.execute()

#endregion


#region TEST Matrix Assignment to Mapping Projection @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from PsyNeuLink.Functions.Process import *
# from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.Transfer import Transfer
# from PsyNeuLink.Functions.Utilities.Utility import Linear
# from PsyNeuLink.Functions.Projections.Mapping import Mapping
#
# my_mech = Transfer(function=Linear())
# my_mech2 = Transfer(function=Linear())
# my_projection = Mapping(sender=my_mech,
#                         receiver=my_mech2,
#                         matrix=np.ones((1,1)))
#
# my_process = process(configuration=[my_mech, my_mech2])
#
#
# my_process.execute()

#endregion

#region TEST Matrix Assignment to Mapping Projection @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

from PsyNeuLink.Functions.Process import *
from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.Transfer import Transfer
from PsyNeuLink.Functions.Utilities.Utility import Linear, Logistic
from PsyNeuLink.Functions.Projections.Mapping import Mapping

color_naming = Transfer(default_input_value=[0,0],
                        function=Linear,
                        name="Color Naming"
                        )

word_reading = Transfer(default_input_value=[0,0],
                        function=Logistic,
                        name="Word Reading")

verbal_response = Transfer(default_input_value=[0,0],
                           function=Logistic)

color_pathway = Mapping(sender=color_naming,
                        receiver=verbal_response,
                        matrix=IDENTITY_MATRIX,
                        )

word_pathway = Mapping(sender=word_reading,
                       receiver=verbal_response,
                        matrix=IDENTITY_MATRIX
                       )

Stroop_process = process(default_input_value=[[1,2.5]],
                         configuration=[color_naming, word_reading, verbal_response])


Stroop_process.execute()

# endregion


# ----------------------------------------------- UTILITIES ------------------------------------------------------------

#region TEST typecheck: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

import typecheck as tc

# @tc.typecheck
# def foo2(record:(int,int,bool), rgb:tc.re("^[rgb]$")) -> tc.any(int,float) :
#     # don't expect the following to make much sense:
#     a = record[0]; b = record[1]
#     return a/b if (a/b == float(a)/b) else float(a)/b
#
# # foo2((4,10,True), "r")   # OK
# # foo2([4,10,True], "g")   # OK: list is acceptable in place of tuple
# # foo2((4,10,1), "rg")     # Wrong: 1 is not a bool, string is too long
# # # foo2(None,     "R")      # Wrong: None is no tuple, string has illegal character
#
#
# from enum import Enum
# # class Weightings(AutoNumber):
# class Weightings(Enum):
#     LINEAR        = 'hello'
#     SCALED        = 'goodbye'
#     TIME_AVERAGED = 'you say'
#
# @tc.typecheck
# def foo3(test:tc.re('hello')):
#     a = test
#
# foo3('hello')
# # foo3('goodbye')
# # foo3(test=3)
#
# @tc.typecheck
# def foo4(test:Weightings=Weightings.SCALED):
#     a = test
#
# # foo4(test=Weightings.LINEAR)
# foo4(test='LINEAR')

# @tc.typecheck
# def foo5(test:tc.any(int, float)=2):
#     a = test
#
# foo5(test=1)

# options = ['Happy', 'Sad']

# @tc.typecheck
# def foo6(arg:tc.enum('Happy', 'Sad')):
#     a = arg
#
# foo6(arg='Ugh')

# @tc.typecheck
# # def foo7(arg:tc.optional(tc.any(int, float, tc.seq_of(tc.any(int, float))))):
# def foo7(arg:tc.optional(tc.any(int, float, tc.list_of(tc.any(int, float)), np.ndarray))):
#     a = arg
#
# foo7(np.array([1,'a']))
#

# a = NotImplemented
# if isinstance(a, type(NotImplemented)):
#     print ("TRUE")

#endregion


#region TEST Function definition in class: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class a:
#     def __init__(self):
#         a.attrib1 = True
#
#     def class_function(string):
#         return 'RETURN: ' + string
#
# print (a.class_function('hello'))
#
#endregion

#region TEST Save function args: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# def first_function(sender=NotImplemented,
#                   receiver=NotImplemented,
#                   params=NotImplemented,
#                   name=NotImplemented,
#                   prefs=NotImplemented,
#                   context=None):
#     saved_args = locals()
#     return saved_args
#
# def second_function(sender=NotImplemented,
#                   receiver=NotImplemented,
#                   params=NotImplemented,
#                   name=NotImplemented,
#                   prefs=NotImplemented,
#                   context=None):
#     saved_args = locals()
#     return saved_args
#
# a = first_function(sender='something')
# print ('a: ', a)
# a['context']='new context'
# print ('a: ', a)
# b = second_function(**a)
# print ('b: ', b)
#
#

#endregion

#region TEST Attribute assignment: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class a:
#     def __init__(self):
#         a.attrib1 = True
#
# x = a()
# print ('attrib1: ', x.attrib1)
# x.attrib2 = False
# print ('attrib2: ', x.attrib2)

#endregion

#region TEST np.array ASSIGNMENT: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# test = np.array([[0]])
# print (test)
# test[0] = np.array([5])
# print (test)

#endregion

#region TEST next: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class a:
#     pass
# b = a()
# c = a()
# l = ['hello', 1, b, 2, 'test', 3, c, 4, 'goodbye']
#
# x = [item for item in l if isinstance(item, a)]
# print (x)


# x = iter(l)
# # x = iter(['test', 'goodbye'])
# i = 0
# # while next((s for s in x if isinstance(s, int)), None):
#
# y = []
# z = next((s for s in x if isinstance(s, a)), None)
# while z:
#     y.append(z)
#     z = next((s for s in x if isinstance(s, a)), None)
#
# print (y)
# print (len(y))


# print (next((s for s in x if isinstance(s, int)), None))
# print (next((s for s in x if isinstance(s, int)), None))
# print (next((s for s in x if isinstance(s, int)), None))
# print (next((s for s in x if isinstance(s, int)), None))

#endregion

#region TEST BREAK IN FOR LOOP: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# i = 0
# for i in range(10):
#     if i == 2:
#         break
# print (i)

#endregion

#region TEST np.array DOT PRODUCT: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# # output_error = np.array([3, 1])
# # weight_matrix = np.array([[1, 2], [3, 4], [5, 6]])
#
# # sender_error = 5, 13, 21
#
# # receivers = np.array([[1, 2]]).reshape(2,1)
# receivers = np.array([3,1])
# weights = np.array([[1, 2], [3, 4], [5, 6]])
# print ('receivers: \n', receivers)
# print ('weights: \n', weights)
# print ('dot product: \n', np.dot(weights, receivers))

#endregion

#region TEST PRINT W/O RETURN @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# # for item in [1,2,3,4]:
# #     print(item, " ", end="")
# #
# # print("HELLO", "GOOBAH", end="")
#
#
# print("HELLO ", end="")
# print("GOOBAH", end="")
# print(" AND FINALLY")
#
#endregion

#region TEST PHASE_SPEC @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# def phaseSpecFunc(freq_spec, phase_spec, phase_max):
#     for time in range(20):
#         if (time % (phase_max + 1)) == phase_spec:
#             print (time, ": FIRED")
#         else:
#             print (time, ": -----")
#
# phaseSpecFunc(freq_spec=1,
#               phase_spec=1,
#               phase_max=3)

#endregion

#region TEST CUSTOM LIST THAT GETS ITEM FROM ANOTHER LIST @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from collections import UserList
#
# # class mech_list(UserList):
# #     def __init__(self):
# #         super(mech_list, self).__init__()
# #         self.mech_tuples = mech_tuples()
# #
# #     def __getitem__(self, item):
# #         return self.mech_tuples.tuples_list[item][0]
# #
# #     def __setitem__(self, key, value):
# #         raise ("MyList is read only ")
# #
# # class mech_tuples:
# #     def __init__(self):
# #         # self.tuples_list = myList()
# #         self.tuples_list = [('mech 1', 1), ('mech 2', 2)]
#
# # x = mech_list(mech_tuples())
# # print (x[0])
#
# class mech_list(UserList):
#     def __init__(self, source_list):
#         super(mech_list, self).__init__()
#         self.mech_tuples = source_list
#
#     def __getitem__(self, item):
#         return self.mech_tuples.tuples_list[item][0]
#
#     def __setitem__(self, key, value):
#         raise ("MyList is read only ")
#
# class system:
#     def __init__(self):
#         self.tuples_list = [('mech 1', 1), ('mech 2', 2)]
#         self.mech_list = mech_list(self)
#
# x = system()
# print (x.mech_list[1])
#
#endregion

#region TEST ERROR HANDLING: NESTED EXCEPTIONS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#
# MonitoredOutputStatesOption = dict
# target_set = {
#     MONITORED_OUTPUT_STATES:'state that is monitored',
#     # FUNCTION_PARAMS:{WEIGHTS:[1]}
#               }
#
# try:
#     # It IS a MonitoredOutputStatesOption specification
#     if isinstance(target_set[MONITORED_OUTPUT_STATES], MonitoredOutputStatesOption):
#         # Put in a list (standard format for processing by instantiate_monitored_output_states)
#         # target_set[MONITORED_OUTPUT_STATES] = [target_set[MONITORED_OUTPUT_STATES]]
#         print ("Assign monitored States")
#     # It is NOT a MonitoredOutputStatesOption specification, so assume it is a list of Mechanisms or States
#     else:
#         # for item in target_set[MONITORED_OUTPUT_STATES]:
#         #     self.validate_monitored_state(item, context=context)
#         # Insure that number of weights specified in WEIGHTS functionParams equals the number of monitored states
#         print ('Validated monitored states')
#         try:
#             num_weights = len(target_set[FUNCTION_PARAMS][WEIGHTS])
#         except KeyError:
#             # raise ScratchPadError('Key error for assigning weights')
#             pass
#         else:
#             # num_monitored_states = len(target_set[MONITORED_OUTPUT_STATES])
#             # if not True:
#             if True:
#                 raise ScratchPadError("Weights not equal")
# except KeyError:
#     pass

#endregion

#region TEST ERROR HANDLING @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#

# myMatrix = np.matrix('1 2 3; 4 5 q')

# try:
#     myMatrix = np.matrix('1 2 3; 4 5 6')
# except (TypeError, ValueError) as e:
#     print ("Error message: {0}".format(e))

# try:
#     myMatrix = np.atleast_2d(['a', 'b'], ['c'])
# except TypeError as e:
#     print ("Array Error message: {0}".format(e))

# try:
#     myMatrix = np.matrix([[1, 2, 3], ['a', 'b', 'c']])
# except TypeError as e:
#     print ("Matrix Error message: {0}".format(e))
#
#
# print ("\nmyMatrix: \n", myMatrix)
#
#endregion

#region TEST ERROR HANDLING: INSTANTIATING A CUSTOM EXCEPTION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# try:
#     raise TypeError('help')
# except:
#     print ("Exeption raised!")

#endregion

#region TEST FIND TERMINALS IN GRAPH @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#          A
#         /
#       B
#      / \
#    C    D
#   /
# E

# graph = {"B": {"A"},
#          "C": {"B"},
#          "D": {"B"},
#          "E": {"C"},
#          "A": set()}
#
# B    C
#  \  /
#   A

# graph = {
#     "A": {"B", "C"},
#     "B": set(),
#     "C": set()
# }

# receiver_mechs = set(list(graph.keys()))
#
# print ("receiver_mechs: ", receiver_mechs)
#
# sender_mechs = set()
# for receiver, sender in graph.items():
#     sender = graph[receiver]
#     sender_mechs = sender_mechs.union(sender)
#
# print ("sender_mechs: ", sender_mechs)
#
# terminal_mechs = receiver_mechs-sender_mechs
#
# print ('terminal_mechs: ', terminal_mechs )
#
# from toposort import toposort, toposort_flatten
#
# print("\nList of sets from toposort: ", list(toposort(graph))) # list of sets
# print("toposort_flatten (not sorted): ", toposort_flatten(graph, sort=False)) # a particular order
# print("toposort_flatten (sorted): ", toposort_flatten(graph, sort=True)) # a particular order

# from itertools import chain
# # graph ={'B': {'A', 'F'}, 'C': {'B'}, 'D': {'B'}, 'E': {'C'}}
# terminals = [k for k in graph.keys() if k not in chain(*graph.values())]
# print ("\nterminals: ", terminals)


#endregion

#region TEST TOPOSORT @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# # from toposort import toposort, toposort_flatten
# # # #
# # # graph = {"C": {"B","D"},  # Note: ignores neste' sets
# # #         "C": { "A"},
# # #         "C": {"C''"},
# # #         "B": {"A'"},
# # #         "B":{"A"},
# # #         "C''":{"A'"}, # ADDED
# # #         "A":set(),
# # #         "A'":set(),
# # #         "C''":{"B''"},
# # #         "B''":{"A''"},
# # #         "A''":set(),
# # #         "D": { "B"}
# # #          }
# # #         # "D":set()}
# # #
# # #
# # #          E
# # #         /
# # #    D   C
# # #     \ / \
# # #      B   Y
# # #     / \
# # #    A   X
# # #
# # graph = {"B": {"A", "X"},
# #          "C": {"B", "Y"},
# #          "D": {"B"},
# #          "E": {"C"}}
# # #
# import re
# print()
# print( list(toposort(graph))) # list of sets
# print(toposort_flatten(graph)) # a particular order
# # print( re.sub('[\"]','',str(list(toposort(graph))))) # list of sets
# # print( re.sub('[\"]','',str(toposort_flatten(graph)))) # a particular order

#
# OUTPUT:
# [{A, A', A''}, {B'', B}, {C''}, {C}]
# [A, A', A'', B, B'', C'', C]

# #endregion

#region TEST **kwARG PASSING  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# def function(arg1=1, arg2=2, **kwargs):
#     print ("arg 1: {}\narg 2: {}\nkwargs: {}\ntype of kwargs: {}".format(arg1, arg2, kwargs, type(kwargs)))
#
# function(**{'arg1':3, 'arg2':4})
#
# arg_dict = {'arg1':5, 'arg2':6, 'arg3':7}
# function(**arg_dict)

# def function(arg1=1, arg2=2):
#     print ("\targ 1: {}\n\targ 2: {}".format(arg1, arg2))
#
# print("\nArgs passed as **{'arg1':5, 'arg2':6}:")
# function(**{'arg1':5, 'arg2':6})
#
# print("\nArgs passed as *(7, 8):")
# function(*(7, 8))
#
# print("\nArgs passed as **{kwArg1:9, kwArg2:10}:")
# kwArg1 = 'arg1'
# kwArg2 = 'arg2'
# function(**{kwArg1:9, kwArg2:10})

#endregion

#region TEST @PROPERTY APPEND FOR SETTER @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class attribute_list(list):
#     def append(self, value):
#         print ('ACCESSED ATTRIBUTE APPEND')
#         super(attribute_list, self).append(value)
#
# class a:
#     def __init__(self):
#         self._attribute = attribute_list()
#         self._attribute.append('happy')
#
#     @property
#     def attribute(self):
#         return self._attribute
#
#     @attribute.setter
#     def attribute(self, value):
#         print ('ACCESSED SETTER')
#         self._attribute.append(value)
#
#     def add(self, value):
#         self.attribute = value
#
#
# x = a()
# # items = ['happy', 'sad']
# # for i in items:
# #     x.attribute = i
#
# x.attribute.append('sad')
# print(x.attribute)
#

#endregion

#region TEST HIERARCHICAL property -- WORKS! @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class a:
#     def __init__(self):
#         self._attribute = None
#
#     # @property
#     # def attribute(self):
#     def getattribute(self):
#         print ('RETRIEVING PARENT attribute')
#         return self._attribute
#
#     # @attribute.setter
#     # def attribute(self, value):
#     def setattribute(self, value):
#         print ('SETTING PARENT TO: ', value)
#         self._attribute = value
#         print ('PARENT SET TO: ', self._attribute)
#
#     attribute = property(getattribute, setattribute, "I'm the attribute property")
#
# class b(a):
#     # def __init__(self):
#     #     self.attrib = 1
#     #     self._attribute = None
#     # @property
#     # def attribute(self):
#     def getattribute(self):
#         print ('RETRIEVING CHILD attribute')
#         return super(b, self).getattribute()
#
#     # @attribute.setter
#     # def attribute(self, value):
#     def setattribute(self, value):
#         # super(b, self).attribute(value)
#         # super(b,self).__set__(value)
#         super(b,self).setattribute(value)
#         print ('SET CHILD TO: ', self._attribute)
#         # self._attribute = value
#
#     attribute = property(getattribute, setattribute, "I'm the attribute property")
#
# x = a()
# x.attribute = 1
# x.attribute = 1
# print (x.attribute)
# y = b()
# y.attribute = 2
# print (y.attribute)


#endregion

#region TEST HIERARCHICAL property -- FROM BRYN @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class A(object):
#     def __init__(self):
#         self._foo = 1
#     @property
#     def foo(self):
#         return self._foo
#
#     @foo.setter
#     def foo(self, value):
#         self._foo = value
#
#
# class B(A):
#     @A.foo.setter
#     def foo(self, value):
#         A.foo.__set__(self, value * 2)
#
#
# if __name__ == '__main__':
#     a = A()
#     b = B()
#     a.foo = 5
#     b.foo = 5
#     print("a is %d, b is %d" % (a.foo, b.foo))

#endregion

#region TEST setattr for @property @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# class a:
#     # def __init__(self):
#     #     self.attrib = 1
#     @property
#     def attribute(self):
#         return self._attribute
#
#     @attribute.setter
#     def attribute(self, value):
#         print ('SETTING')
#         self._attribute = value
#
# x = a()
# # x.attribute = 1
# setattr(x, 'attribute', 2)
# print (x.attribute)
# print (x._attribute)
#endregion

#region TEST setattr @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class a:
#     def __init__(self):
#         a.foo = 3
#
# x = a()
# setattr(x, 'foo', 4)
# print (x.foo)
# print (x.__dict__)

# #endregion

#region TEST ARITHMETIC @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# x = np.array([10,10])
# y = np.array([1,2])
# q = np.array([2,3])
#
# z = LinearCombination(x,
#                       param_defaults={LinearCombination.OPERATION: LinearCombination.Operation.PRODUCT},
#                       context='TEST')
# print (z.execute([x, y, q]))

# #endregion

#region TEST LINEAR @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# x = np.array([10,10])
# y = np.array([1,2])
# q = np.array([2,3])
#
# z = Linear(x, context='TEST')
# print (z.execute([x]))
#
# #endregion

#region TEST iscompatible @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# a = 1
# b = LogEntry.OUTPUT_VALUE
#
# # if iscompatible(a,b, **{kwCompatibidlityType:Enum}):
# if iscompatible(a,b):
#     print('COMPATIBLE')
# else:
#     print('INCOMPATIBLE')
#
# #endregion

#region TEST OVER-WRITING OF LOG @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#

# class a:
#
#     attrib = 1
#
#     class LogEntry(IntEnum):
#         NONE            = 0
#         TIME_STAMP      = 1 << 0
#
#     def __init__(self):
#         self.attrib = 2
#
#
# class b(a):
#
#     class LogEntry(IntEnum):
#         OUTPUT_VALUE    = 1 << 2
#         DEFAULTS = 3
#
#     def __init__(self):
#         self.pref = self.LogEntry.DEFAULTS
#
# x = a()
# y = b()
#
# z = b.LogEntry.OUTPUT_VALUE
# print (z)

#endregion

#region TEST SHARED TUPLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# from collections import namedtuple
#
# TestTuple = namedtuple('TestTuple', 'first second')
#
# class a:
#     def __init__(self):
#         # self.tuple_a = TestTuple('hello','world')
#         self.tuple_a = 5
#
# x = a()
#
# class b:
#     def __init__(self):
#         self.tuple_a = x.tuple_a
#
# class c:
#     def __init__(self):
#         setattr(self, 'tuple_a', x.tuple_a)
#
# y=b()
# z=c()
# x.tuple_a = 6
#
# print (y.tuple_a)
# print (z.tuple_a)
#
#
#endregion

#region TEST PREFS GETTER @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# class prefs:
#     def __init__(self):
#         self.pref_attrib = 'PREF ATTRIB'
#
# class a:
#     def __init__(self):
#         self._prefs = prefs()
#
#     @property
#     def prefs(self):
#         print ("accessed")
#         return self._prefs
#
#endregion
#region @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# # - TEST: Preferences:
#
# # x = DDM()
# # x.prefs.inspect()
#
# DDM_prefs = FunctionPreferenceSet(
#                 reportOutput_pref=PreferenceEntry(True,PreferenceLevel.SYSTEM),
#                 verbose_pref=PreferenceEntry(True,PreferenceLevel.SYSTEM),
#                 kpFunctionRuntimeParams_pref=PreferenceEntry(ModulationOperation.MULTIPLY,PreferenceLevel.TYPE)
#                 )
# DDM_prefs.inspect()
# # DDM.classPreferences = DDM_prefs
# #
# # DDM_prefs.inspect()
# # print (DDM_prefs.verbosePref)
#

#endregion
#region @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# # - TEST:  GET ATTRIBUTE LIST
#
# class x:
#     def __init__(self):
#         self.attrib1 = 'hello'
#         self.attrib2 = 'world'
#
# a = x()
#
# print (a.__dict__.values())
#
# for item in a.__dict__.keys():
#     if 'attrib' in item:
#         print (item)
#
# for item, value in a.__dict__.items():
#     if 'attrib' in item:
#         print (value)

#endregion
#region @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# - TEST:  PROPERTY GETTER AND SETTER

# ************
# 
# EXAMPLE:
# 
# class ClassProperty(property):
#     def __get__(self, cls, owner):
#         return self.fget.__get__(None, owner)()
# 
# class foo(object):
#     _var=5
#     def getvar(cls):
#         return cls._var
#     getvar=classmethod(getvar)
#     def setvar(cls,value):
#         cls._var=value
#     setvar=classmethod(setvar)
#     var=ClassProperty(getvar,setvar)
# 
# assert foo.getvar() == 5
# foo.setvar(4)
# assert foo.getvar() == 4
# assert foo.var == 4
# foo.var = 3
# assert foo.var == 3
# However, the setters don't actually work:
# 
# foo.var = 4
# assert foo.var == foo._var # raises AssertionError
# foo._var is unchanged, you've simply overwritten the property with a new value.
# 
# You can also use ClassProperty as a decorator:
# 
# class Foo(object):
#     _var = 5
# 
#     @ClassProperty
#     @classmethod
#     def var(cls):
#         return cls._var
# 
#     @var.setter
#     @classmethod
#     def var(cls, value):
#         cls._var = value
# 
# assert foo.var == 5
# 
# **************
# 
# BETTER EXAMPLE:

# class foo(object):
#     _var = 5
#     class __metaclass__(type):
#     	pass
#     @classmethod
#     def getvar(cls):
#     	return cls._var
#     @classmethod
#     def setvar(cls, value):
#     	cls._var = value
# 

# class foo(object):
#     _var = 5
#     class __metaclass__(type):
#     	@property
#     	def var(cls):
#     		return cls._var
#     	@var.setter
#     	def var(cls, value):
#     		cls._var = value



# class a:
#     _cAttrib = 5
#
#     def __init__(self):
#         self._iAttrib = 2
#         pass
#
#     @property
#     def iAttrib(self):
#         return self._iAttrib
#
#     @iAttrib.setter
#     def iAttrib(self, value):
#         print('iAttrib SET')
#         self._iAttrib = value
#
#     @property
#     def cAttrib(self):
#         return self._cAttrib
#
#     @cAttrib.setter
#     def cAttrib(self, value):
#         print('cAttrib SET')
#         self._cAttrib = value

# class classProperty(property):
#     def __get__(self, cls, owner):
#         return self.fget.__get__(None, owner)()

# class a(object):
#     _c_Attrib=5
    # def get_c_Attrib(cls):
    #     return cls.__c_Attrib
    # get_c_Attrib=classmethod(get_c_Attrib)
    # def set_c_Attrib(cls,value):
    #     cls.__c_Attrib=value
    # set_c_Attrib=classmethod(set_c_Attrib)
    # _c_Attrib=ClassProperty(get_c_Attrib, set_c_Attrib)

# test = 0
# class a(object):
# 
#     _c_Attrib=5
# 
#     @classProperty
#     @classmethod
#     def c_Attrib(cls):
#         test = 1
#         return cls._c_Attrib
# 
#     @c_Attrib.setter
#     @classmethod
#     def c_Attrib(cls, value):
#         test = 1
#         print ('Did something')
#         cls._c_Attrib = value
# 

# test = 0
# class a(object):
#     _c_Attrib = 5
#     class __metaclass__(type):
#         @property
#         def c_Attrib(cls):
#             return cls._c_Attrib
#         @c_Attrib.setter
#         def c_Attrib(cls, value):
#             pass
#             # cls._c_Attrib = value
# 

# test = 0
# class a(object):
#     _c_Attrib = 5
#     class __metaclass__(type):
#         pass
#     @classmethod
#     def getc_Attrib(cls):
#         return cls._c_Attrib
#     @classmethod
#     def setc_Attrib(cls, value):
#         test = 1
#         cls._c_Attrib = value
#

# class classproperty(object):
#     def __init__(self, getter):
#         self.getter= getter
#     def __get__(self, instance, owner):
#         return self.getter(owner)
#
# class a(object):
#     _c_Attrib= 4
#     @classproperty
#     def c_Attrib(cls):
#         return cls._c_Attrib
#
# x = a()
#
# a.c_Attrib = 22
# print ('\na.c_Attrib: ',a.c_Attrib)
# print ('x.c_Attrib: ',x.c_Attrib)
# print ('a._c_Attrib: ',a._c_Attrib)
# print ('x._c_Attrib: ',x._c_Attrib)
#
# x.c_Attrib = 101
# x._c_Attrib = 99
# print ('\nx.c_Attrib: ',x.c_Attrib)
# print ('x._c_Attrib: ',x._c_Attrib)
# print ('a.c_Attrib: ',a.c_Attrib)
# print ('a._c_Attrib: ',a._c_Attrib)
#
# a.c_Attrib = 44
# a._c_Attrib = 45
# print ('\nx.c_Attrib: ',x.c_Attrib)
# print ('x._c_Attrib: ',x._c_Attrib)
# print ('a.c_Attrib: ',a.c_Attrib)
# print ('a._c_Attrib: ',a._c_Attrib)

# ------------


# class classproperty(object):
#     def __init__(self, getter):
#         self.getter= getter
#     def __get__(self, instance, owner):
#         return self.getter(owner)
#
# class a(object):
#     # classPrefs= 4
#     @classproperty
#     def c_Attrib(cls):
#         try:
#             return cls.classPrefs
#         except:
#             cls.classPrefs = 'CREATED'
#             return cls.classPrefs

# x = a()
# print (x.classPrefs)
# print (a.classPrefs)
#
# a.c_Attrib = 22
# print ('\na.c_Attrib: ',a.c_Attrib)
# print ('x.c_Attrib: ',x.c_Attrib)
# print ('a.classPrefs: ',a.classPrefs)
# print ('x.classPrefs: ',x.classPrefs)
#
# x.c_Attrib = 101
# x.classPrefs = 99
# print ('\nx.c_Attrib: ',x.c_Attrib)
# print ('x.classPrefs: ',x.classPrefs)
# print ('a.c_Attrib: ',a.c_Attrib)
# print ('a.classPrefs: ',a.classPrefs)
#
# a.c_Attrib = 44
# a.classPrefs = 45
# print ('\nx.c_Attrib: ',x.c_Attrib)
# print ('x.classPrefs: ',x.classPrefs)
# print ('a.c_Attrib: ',a.c_Attrib)
# print ('a.classPrefs: ',a.classPrefs)
#
#
#

#endregion

#region TEST:  DICTIONARY MERGE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# # -
#
#
# # a = {'hello':1}
# a = {}
# # b = {'word':2}
# b = {}
# # c = {**a, **b} # AWAITING 3.5
# c = {}
# c.update(a)
# c.update(b)
# if (c):
#     print(c)
# else:
#     print('empty')
#
#
#
#endregion

# #region TEST: SEQUENTIAL ERROR HANDLING @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# # state_params = None
# state_params = {}
# # state_params = {'Already there': 0}
# state_spec = {'hello': {'deeper dict':1}}
# key = 'goodbye'
# # key = 'hello'
#
# try:
#     state_params.update(state_spec[key])
# # state_spec[kwStateParams] was not specified
# except KeyError:
#         pass
# # state_params was not specified
# except (AttributeError):
#     try:
#         state_params = state_spec[key]
#     # state_spec[kwStateParams] was not specified
#     except KeyError:
#         state_params = {}
# # state_params was specified but state_spec[kwStateParams] was not specified
# except TypeError:
#     pass
# #endregion
#
# print(state_params)

#region TEST:  ORDERED DICTIONARY ORDERING @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# from collections import OrderedDict
#
# a = OrderedDict()
# a['hello'] = 1
# a['world'] = 2
#
# for x in a:
#     print ('x: ', x)
#
# print ("a: ", a)
# print (list(a.items())[0], list(a.items())[1])
#
# b = {'hello':1, 'world':2}
#
# print ("b: ", b)
#
#endregion


#region TEST:  add a parameterState to a param after an object is instantiated @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# from Functions.Mechanisms.DDM import DDM
# from Functions.States.ParameterState import ParameterState
#
# x = DDM()
# state = x.instantiate_state(state_type=ParameterState,
#                               state_name='DDM_TEST_PARAM_STATE',
#                               state_spec=100.0,
#                               constraint_value=0.0,
#                               constraint_value_name='DDM T0 CONSTRAINT',
#                               context='EXOGENOUS SPEC')
# x.parameterStates['DDM_TEST_PARAM_STATE'] = state

# x.instantiate_state_list(state_type=ParameterState,
#                                    state_param_identifier='DDM_TEST',
#                                    constraint_value=0.0,
#                                    constraint_value_name='DDM T0 CONSTRAINT',
#                                    context='EXOGENOUS SPEC')

#endregion

#region TEST OF AutoNumber IntEnum TYPE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# #
#
# from enum import IntEnum
# class AutoNumber(IntEnum):
#     """Autonumbers IntEnum type
#
#     Adapted from AutoNumber example for Enum at https://docs.python.org/3/library/enum.html#enum.IntEnum:
#     Notes:
#     * Start of numbering changed to 0 (from 1 in example)
#     * obj based on int rather than object
#     """
#     def __new__(cls):
#         # Original example:
#         # value = len(cls.__members__) + 1
#         # obj = object.__new__(cls)
#         value = len(cls.__members__)
#         obj = int.__new__(cls)
#         obj._value_ = value
#         return obj
#
# class DDM_Output(AutoNumber):
#     DDM_DECISION_VARIABLE = ()
#     DDM_RT_MEAN = ()
#     DDM_ER_MEAN = ()
#     DDM_RT_CORRECT_MEAN = ()
#     DDM_RT_CORRECT_VARIANCE = ()
#     TOTAL_COST = ()
#     TOTAL_ALLOCATION = ()
#     NUM_OUTPUT_VALUES = ()
#
# class DDM_Output_Int(IntEnum):
#     DDM_DECISION_VARIABLE = 0
#     DDM_RT_MEAN = 1
#     DDM_ER_MEAN = 2
#     DDM_RT_CORRECT_MEAN = 3
#     DDM_RT_CORRECT_VARIANCE = 4
#     TOTAL_COST = 5
#     TOTAL_ALLOCATION = 6
#     NUM_OUTPUT_VALUES = 7
#
# x = DDM_Output.NUM_OUTPUT_VALUES
# # x = DDM_Output_Int.NUM_OUTPUT_VALUES
#
# print (x.value)

#endregion

#region TEST OF RIGHT REPLACE (rreplace) @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#

# def rreplace(myStr, old, new, count):
#     return myStr[::-1].replace(old[::-1], new[::-1], count)[::-1]
#
# new_str = rreplace('hello-1', '-1', '-2', 1)
# print(new_str)

#endregion

#region TEST OF OrderedDict @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# from collections import OrderedDict
# from collections import Counter
#
# # class OrderedCounter(Counter, OrderedDict):
# #     'Counter that remembers the order elements are first encountered'
# #
# #     def __repr__(self):
# #         return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))
# #
# #     def __reduce__(self):
# #         return self.__class__, (OrderedDict(self),)
#
#
# a = OrderedDict({'hello': 1,
#                  'goodbye': 2
#                  })
# a['I say'] = 'yes'
# a['You say'] = 'no'
#
# print ('dict: ', a)
#
# print (list(a.items()))
#
# for key, value in a.items():
#     print('value of {0}: '.format(key), value)
#
# print("keys.index('hello'): ", list(a.keys()).index('hello'))
# print('keys.index(1): ', list(a.values()).index(1))
# print("keys.index('I say'): ", list(a.keys()).index('I say'))
# print("keys.index('yes'): ", list(a.values()).index('yes'))
#
# print("list(values): ", list(a.values()))
# print("values[0]: ", list(a.values())[0])
# print("values[2]: ", list(a.values())[2])
#
#
#
# # for item in a if isinstance(a, list) else list(a.items()[1]:
# #     print (item)
#
# # a = [1, 2, 3]
# #
# #
# # for key, value in a.items() if isinstance(a, dict) else enumerate(a):
# #     print (value)
# #
# #
# # # for value in b:
# # for key, value in enumerate(b):
# #     print (value)
# #
# #
# # d.values().index('cat')
# # d.keys().index('animal')
# # list(d.keys()).index("animal")
# #
#
# #endregion

#region PREFERENCE TESTS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#
# from Globals.Preferences.PreferenceSet import *
# from Globals.Preferences.FunctionPreferenceSet import *
#
# class a(object):
#     prefs = None
#     def __init__(self):
#         a.prefs = FunctionPreferenceSet(owner=a,
#                                         log_pref=PreferenceEntry(1,PreferenceLevel.SYSTEM),
#                                         level=PreferenceLevel.SYSTEM)
#
# class b(a):
#     prefs = None
#     def __init__(self):
#         super(b, self).__init__()
#         b.prefs = FunctionPreferenceSet(owner=b,
#                                         log_pref=PreferenceEntry(5,PreferenceLevel.CATEGORY),
#                                         level=PreferenceLevel.CATEGORY)
#
# class c(b):
#     prefs = None
#     def __init__(self):
#         super(c, self).__init__()
#         c.prefs = FunctionPreferenceSet(owner=self,
#                                         log_pref=PreferenceEntry(3,PreferenceLevel.INSTANCE),
#                                         level=PreferenceLevel.INSTANCE)
#         self.prefs = c.prefs
#
#
# x = c()
#
# x.prefs.logLevel = PreferenceLevel.CATEGORY
# y = x.prefs.logPref
# print (y)
#
# x.prefs.logLevel = PreferenceLevel.INSTANCE
# y = x.prefs.logPref
# print (x.prefs.logPref)
#
# print ("system: ", x.prefs.get_pref_setting_for_level(kpLogPref, PreferenceLevel.SYSTEM))
# print ("category: ", x.prefs.get_pref_setting_for_level(kpLogPref, PreferenceLevel.CATEGORY))
# print ("instance: ", x.prefs.get_pref_setting_for_level(kpLogPref, PreferenceLevel.INSTANCE))
#
# # # print ("system: ", b.prefs.get_pref_setting(b.prefs.logEntry, PreferenceLevel.CATEGORY))
# # # print ("system: ", x.prefs.get_pref_setting(x.prefs.logEntry, PreferenceLevel.SYSTEM))
# # # print ("category: ", x.prefs.get_pref_setting(x.prefs.logEntry, PreferenceLevel.CATEGORY))
# # # print ("instance: ", x.prefs.get_pref_setting(x.prefs.logEntry, PreferenceLevel.INSTANCE))
#

#endregion

#region ATTEMPT TO ASSIGN VARIABLE TO NAME OF ATTRIBUTE: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#
#
# y = 'x'
#
# class a:
#
#     def __init__(self, y):
#         z = getattr(self,y)
#
#     @property
#     def z(self):
#         return self._x
#
#     @z.setter
#     def z(self, value):
#         self._x = value
#
# b = a(y)
# q = getattr(a,y)
# q = 3
# print (a.q)


# from Functions.States.InputState import InputState
#
# test = InputState(value=1)
# x = 1

# def func_b():
#     print('hello from b')
#
# class a:
#     def __init__(self):
#         self.func_a = func_b
#
#     def func_a(self):
#         print('hello from a')
#
# x = a()
# x.__class__.func_a(a)
# a.func_a(a)
# c = a.func_a
# c(a)
#

# # a = 'hello'
# class b:
#     pass
#
# class a(b):
#     pass
# # a = [1]
# # test = {'goodbye':2}
#
# try:
#     issubclass(a, b)
# except TypeError:
#     if isinstance(a, str):
#         try:
#             print(test[a])
#         except KeyError:
#             print("got to KeyError nested in TypeError")
#     else:
#         print("got to string else")
#
# else:
#     print("got to outer try else")

# class i():
#     attrib = 0
#     pass
#
# class a(i):
#     pass
#
# x = i()
# y = i()
#
# x.attrib = [1,1]
# y.attrib = [1,2,3]
# print ('x: ', x.attrib, 'y: ', y.attrib)


# z = 'goo'
# x = {'hello':1}
# try:
#     y.a = x[z]
# except KeyError:
#     print('key error')
# except AttributeError:
#     print('attrib error')
# else:
#     print('OK')
#
#
#                     try:
#                         self.paramClassDefaults[FUNCTION] = self.execute
#                     except KeyError:
#                         message = ("{0} missing from {1}".format(required_param, self.name))
#                         self.execute =
#                         xxx
#                     except AttributeError:
# # IMPLEMENTATION NOTE:  *** PARSE ERROR HERE:  WARN IF KEY ERROR, AND ASSIGN FUNCTION;  EXCEPT IF ATTRIBUTE ERROR
#                         raise FunctionError("Either {0} must be specified in paramClassDefaults or"
#                                             " <class.function> must be implemented for {1}".
#                                             format(required_param, self.name))
#                     else:
#                         self.requiredParamClassDefaultTypes[required_param].append(type(self.execute))
#                         if self.functionSettings & FunctionSettings.VERBOSE:
#










# class TestClass(object):
#     def __init__(self):
#         # self.prop1 = None
#         pass
#
#     @property
#     def prop1(self):
#         print ("I was here")
#         return self._prop1
#
#     @prop1.setter
#     def prop1(self, value):
#         print ("I was there")
#         self._prop1 = value
#
#
# a = TestClass()
# a._prop1 = 1
# a.prop1 = 2
# print (a.prop1)
# print (a._prop1)
#

# class C(object):
#     def __init__(self):
#         self._x = None
#
#     @property
#     def x(self):
#         """I'm the 'x' property."""
#         print ("I was here")
#         return self._x
#
#     @x.setter
#     def x(self, value):
#         print ("I was there")
#         self._x = value
#
#
# a = C()
# a.x = 2
# y = a.x
# print (y)







    # return SubTestClass()
#
#
# class TestClass(arg=NotImplemented):
#     def __init__(self):
#         print("Inited Test Class")
#
#
# class SubTestClass(TestClass):
#     def __init__(self):
#         super(SubTestClass, self).__init__()
#         print("Inited Sub Test Class")



# class x:
#       def __init__(self):
#             self.execute = self.execute
#             print("x: self.execute {0}: ",self.execute)
#
# class z(x):
#
#       def __init__(self):
#             super(z, self).__init__()
#             print("z: self.execute {0}: ",self.execute)
#
#       def function(self):
#             pass
#
# y =  z()
#

# paramDict = {'number':1, 'list':[0], 'list2':[1,2], 'number2':2}
#
# def get_params():
#       return (dict((param, value) for param, value in paramDict.items()
#                     if isinstance(value,list) ))
#
#
# print(get_params()['list2'])

# q = z()
#
# class b:
#       pass
#
# print(issubclass(z, x))

# print("x: ",x)
# print("type x: ",type(x))
# print("y: ",y)
# print("type x: ",type(y))
# print(isinstance(y, x))

# test = {'key1':1}
# try:
#       x=test["key2"]
#       x=test["key1"]
# except KeyError:
#       print("passed")
# print(x)

# ***************************************** OLD TEST SCRIPT ************************************************************

# from Functions.Projections.ControlSignal import *
#
# # Initialize controlSignal with some settings
# settings = ControlSignalSettings.DEFAULTS | \
#            ControlSignalSettings.DURATION_COST | \
#            ControlSignalSettings.LOG
# identity = []
# log_profile = ControlSignalLog.ALL
#
# # Set up ControlSignal
# x = ControlSignal_Base("Test Control Signal",
#                        {kwControlSignalIdentity: identity,
#                         kwControlSignalSettings: settings,
#                         kwControlSignalAllocationSamplingRange: NotImplemented,
#                         kwControlSignalLogProfile: log_profile}
#                        )
#
# # Can also change settings on the fly (note:  ControlSignal.OFF is just an enum defined in the ControlSignal module)
# x.set_adjustment_cost(OFF)
#
# # Assign transfer_functions for cost functions
# x.assign_function(kwControlSignalIntensityFunction,
#                   Function.Linear(NotImplemented,
#                                   {Function.Linear.SLOPE : 1,
#                                    Function.Linear.INTERCEPT : 0})
#                   )
# x.assign_function(kwControlSignalIntensityCostFunction,
#                   Function.Linear(NotImplemented,
#                                   {Function.Linear.SLOPE : 1,
#                                    Function.Linear.INTERCEPT : 1})
#                   )
# x.assign_function(kwControlSignalDurationCostFunction,
#                   Function.Integrator(NotImplemented,
#                                       {Function.Integrator.RATE : 0.5,
#                                        Function.Integrator.kwWeighting : Function.Integrator.Weightings.SCALED})
#                   )
#
# # Display some values in controlSignal (just to be sure it is set up OK)
# print("Intensity Function: ", x.functions[kwControlSignalIntensityFunction].name)
# print("Initial Intensity: ", x.intensity)
#
# # Add KVO:
# #  Main will observe ControlSignal.kpIntensity;
# #  the observe_value_at_keypath method in Main will be called each time ControlSignal.kpIntensity changes
# x.add_observer_for_keypath(Main,kpIntensity)
#
#
# # Assign testFunction to be a linear function, that returns the current value of an object property (intensity_cost)
# # It is called and printed out after each update of the control signal below;  note that it returns the updated value
# # Note: the function (whether a method or a lambda function) must be in a list so it is not called before being passed
# testFunction_getVersion = Function.Linear([x.get_intensity_cost])
# testFunction_lambdaVersion = Function.Linear([lambda: x.intensityCost])
# label = x.get_intensity_cost
#
# print("\nINITIAL {0}".format(x.durationCost))
#
# #Print out test of function with object property assigned as its default variable argument
# getVersion = testFunction_getVersion.function()
# print("{0}: {1}\n".format(label, getVersion))
# lambdaVersion = testFunction_lambdaVersion.function()
# print("{0}: {1}\n".format(label, lambdaVersion))
#
# # Initial allocation value
# z = 3
#
# Main.CentralClock.time_step = 0
# x.update_control_signal(z)
# getVersion = testFunction_getVersion.function()
# print("{0}: {1}\n".format(label, getVersion))
# lambdaVersion = testFunction_lambdaVersion.function()
# print("{0}: {1}\n".format(label, lambdaVersion))
#
# #Update control signal with new allocation value
# Main.CentralClock.time_step = 1
# x.update_control_signal(z+1)
# getVersion = testFunction_getVersion.function()
# print("{0}: {1}\n".format(label, getVersion))
# lambdaVersion = testFunction_lambdaVersion.function()
# print("{0}: {1}\n".format(label, lambdaVersion))
#
#
# #Update control signal with new allocation value
# Main.CentralClock.time_step = 2
# x.update_control_signal(z-2)
# getVersion = testFunction_getVersion.function()
# print("{0}: {1}\n".format(label, getVersion))
# lambdaVersion = testFunction_lambdaVersion.function()
# print("{0}: {1}\n".format(label, lambdaVersion))
#
# #Show all entries in log
# print("\n")
# x.log.print_all_entries()
#
# # q = lambda: x.intensity
# # print(q())
# print((lambda: x.intensity)())
# x.intensity = 99
# print((lambda: x.intensity)())
#
#
#
# # test DDM call from Matlab
# print("importing matlab...")
# import matlab.engine
# eng1=matlab.engine.start_matlab('-nojvm')
# print("matlab imported")
#
#
# drift = 0.1
# bias = 0.5
# thresh = 3.0
# noise = 0.5
# T0 = 200
#
#
# t = eng1.ddmSim(drift,bias,thresh,noise,T0,1,nargout=5)
#
# #run matlab function and print output
# #t=eng1.gcd(100.0, 80.0, nargout=3)
# print(t)
#
# print("AFTER MATLAB")
# #end
#
# exit()



