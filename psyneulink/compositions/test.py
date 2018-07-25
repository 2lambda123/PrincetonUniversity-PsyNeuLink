# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 17:48:49 2018

@author: karan
"""

from psyneulink.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.components.functions.function import Linear, Logistic, ReLU, SoftMax
from psyneulink.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.compositions.composition import Composition
from toposort import toposort


import numpy as np

mech1 = TransferMechanism(name='mech1',
                          default_variable=np.zeros(10),
                          )

mech2 = TransferMechanism(name='mech2',
                          default_variable=np.zeros(10),
                          )

mech3 = TransferMechanism(name='mech3',
                          default_variable=np.zeros(10),
                          )

big_mech = TransferMechanism(name='big_mech',
                             default_variable=np.zeros(15),
                             function=Logistic()
                             )

proj1 = MappingProjection(matrix=np.random.rand(10,15),
                          name='proj1',
                          sender=mech1,
                          receiver=big_mech
                          )

proj2 = MappingProjection(matrix=np.random.rand(10,15),
                          name='proj2',
                          sender=mech2,
                          receiver=big_mech
                          )

proj3 = MappingProjection(matrix=np.random.rand(10,15),
                          name='proj3',
                          sender=mech3,
                          receiver=big_mech
                          )

'''
print(big_mech)
print(big_mech.variable)
print(np.shape(big_mech.variable))
print(big_mech.input_states)
print(big_mech.external_input_states)
print(big_mech.external_input_values)
print(np.shape(big_mech.external_input_values))
print("hello")
print(big_mech.external_input_states[0].variable)
print(big_mech.external_input_states[0].value)
print(big_mech.input_states[0])
print(big_mech.input_states[0].variable)
print(np.shape(big_mech.input_states[0].variable))
print(big_mech.input_states[0].value)
print(np.shape(big_mech.input_states[0].value))
print("\n")
print("\n")
print("\n")
'''

compy = Composition()

print(compy._graph_processing)
print("\n")
print("\n")

compy.add_c_node(mech1)
compy.add_c_node(mech2)
compy.add_c_node(mech3)
compy.add_c_node(big_mech)
compy.add_projection(mech1, proj1, big_mech)
compy.add_projection(mech2, proj2, big_mech)
compy.add_projection(mech3, proj3, big_mech)


'''
for i in range(len(compy._graph_processing.vertices)):
    vertex = compy._graph_processing.vertices[i]
    print(vertex)
    print(vertex.component)
    print(vertex.parents)
    print(vertex.children)
    print("\n")

print("\n")
print("\n")
print("\n")

for i in range(len(compy.graph.vertices)):
    print(compy.graph.vertices[i])

print("\n")
print("\n")
print("\n")
'''
'''
a = 10
b = 3
if not (a > 3 and b > 13):
    print("butts")
'''

inputs_dict = {}
inputs_dict[mech1] = np.ones(10)
inputs_dict[mech2] = np.ones(10)
inputs_dict[mech3] = np.ones(10)

compy.input_CIM.reportOutputPref = True
compy.output_CIM.reportOutputPref = True
output = compy.run(inputs=inputs_dict)
print("\n")
print(output)

print("\n")
print("\n")

# check if mechanism can have vector bias

n = np.ones(10)

test_mech = TransferMechanism(name='test_mech',
                             default_variable=np.zeros(10),
                             noise=n,
                             function=Logistic(gain=1, bias=n)
                             )

print(test_mech.execute(np.ones(10)))

















                          