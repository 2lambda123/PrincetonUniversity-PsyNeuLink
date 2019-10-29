import numpy as np
import psyneulink as pnl

# -*- coding: utf-8 -*-
"""Rumelpy_for_Jon

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z_v_If7hB9HPzqM4zO51avauyoLwtUIx
"""

# Stimuli and Relations
# [Use for Homework 1a.]

nouns = ['oak', 'pine', 'rose', 'daisy', 'canary', 'robin', 'salmon', 'sunfish']
relations = ['is', 'has', 'can']
is_list = ['living', 'living thing', 'plant', 'animal', 'tree', 'flower', 'bird', 'fish', 'big', 'green', 'red',
           'yellow']
has_list = ['roots', 'leaves', 'bark', 'branches', 'skin', 'feathers', 'wings', 'gills', 'scales']
can_list = ['grow', 'move', 'swim', 'fly', 'breathe', 'breathe underwater', 'breathe air', 'walk', 'photosynthesize']
descriptors = [nouns, is_list, has_list, can_list]

truth_nouns = np.identity(len(nouns))

truth_is = np.zeros((len(nouns), len(is_list)))

truth_is[0, :] = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
truth_is[1, :] = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
truth_is[2, :] = [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
truth_is[3, :] = [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
truth_is[4, :] = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
truth_is[5, :] = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
truth_is[6, :] = [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0]
truth_is[7, :] = [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]

truth_has = np.zeros((len(nouns), len(has_list)))

truth_has[0, :] = [1, 1, 1, 1, 0, 0, 0, 0, 0]
truth_has[1, :] = [1, 1, 1, 1, 0, 0, 0, 0, 0]
truth_has[2, :] = [1, 1, 0, 0, 0, 0, 0, 0, 0]
truth_has[3, :] = [1, 1, 0, 0, 0, 0, 0, 0, 0]
truth_has[4, :] = [0, 0, 0, 0, 1, 1, 1, 0, 0]
truth_has[5, :] = [0, 0, 0, 0, 1, 1, 1, 0, 0]
truth_has[6, :] = [0, 0, 0, 0, 0, 0, 0, 1, 1]
truth_has[7, :] = [0, 0, 0, 0, 0, 0, 0, 1, 1]

truth_can = np.zeros((len(nouns), len(can_list)))

truth_can[0, :] = [1, 0, 0, 0, 0, 0, 0, 0, 1]
truth_can[1, :] = [1, 0, 0, 0, 0, 0, 0, 0, 1]
truth_can[2, :] = [1, 0, 0, 0, 0, 0, 0, 0, 1]
truth_can[3, :] = [1, 0, 0, 0, 0, 0, 0, 0, 1]
truth_can[4, :] = [1, 1, 0, 1, 1, 0, 1, 1, 0]
truth_can[5, :] = [1, 1, 0, 1, 1, 0, 1, 1, 0]
truth_can[6, :] = [1, 1, 1, 0, 1, 1, 0, 0, 0]
truth_can[7, :] = [1, 1, 1, 0, 1, 1, 0, 0, 0]

truths = [[truth_nouns], [truth_is], [truth_has], [truth_can]]


def gen_input_vals(nouns, relations):

    rumel_nouns_bias=np.vstack((np.identity(len(nouns)),np.ones((1,len(nouns)))))
    rumel_nouns_bias=rumel_nouns_bias.T

    rumel_rels_bias=np.vstack((np.identity(len(relations)),np.ones((1,len(relations)))))
    rumel_rels_bias=rumel_rels_bias.T
    return (rumel_nouns_bias, rumel_rels_bias)

nouns_onehot, rels_onehot = gen_input_vals(nouns, relations)

r_nouns = np.shape(nouns_onehot)[0]
c_nouns = np.shape(nouns_onehot)[1]
r_rels = np.shape(rels_onehot)[0]
c_rels = np.shape(rels_onehot)[1]

# Build Transfer Mechanisms

#In order to build in biases, we add an extra node to every layer, including the inputs

#For the input layers, we will use linear transfer mechanisms

n_units=16

#This number of hidden units is taken directly from Rumelhart's paper

nouns_in = pnl.TransferMechanism(name="nouns_in",
                                 default_variable=np.zeros(c_nouns)
                                )

rels_in = pnl.TransferMechanism(name="rels_in",
                                default_variable=np.zeros(c_rels)
                               )

#For the hidden layers, we will be using logistic functions

hn = pnl.TransferMechanism(name="hidden_nouns",
                           size=9,
                           function=pnl.Logistic()
                            )

hm = pnl.TransferMechanism(name="hidden_mixed",
                           size=n_units,
                           function=pnl.Logistic()
                            )

out_sig_I = pnl.TransferMechanism(name="sig_outs_I",
                                  size=len(nouns),
                                  function=pnl.Logistic()
                                    )

out_sig_is = pnl.TransferMechanism(name="sig_outs_is",
                                   size=len(is_list),
                                   function=pnl.Logistic()
                                    )

out_sig_has = pnl.TransferMechanism(name="sig_outs_has",
                                    size=len(has_list),
                                    function=pnl.Logistic()
                                    )

out_sig_can = pnl.TransferMechanism(name="sig_outs_can",
                                    size=len(can_list),
                                    function=pnl.Logistic()
                                    )

# Here we create random matrices to connect the mechanisms to each other


map_nouns_hn = pnl.MappingProjection(
                                matrix=np.random.rand(c_nouns,c_nouns),
                                name="map_nouns_hn",
                                sender=nouns_in,
                                receiver=hn
                                )

map_rels_hm = pnl.MappingProjection(
                                matrix=np.random.rand(c_rels,n_units),
                                name="map_rel_hm",
                                sender=rels_in,
                                receiver=hm
                                )

map_hn_hm = pnl.MappingProjection(
                                matrix=np.random.rand(c_nouns,n_units),
                                name="map_hn_hm",
                                sender=hn,
                                receiver=hm
                                )

map_hm_I = pnl.MappingProjection(
                                matrix=np.random.rand(n_units,len(nouns)),
                                name="map_hm_I",
                                sender=hm,
                                receiver=out_sig_I
                                )

map_hm_is = pnl.MappingProjection(
                                matrix=np.random.rand(n_units,len(is_list)),
                                name="map_hm_is",
                                sender=hm,
                                receiver=out_sig_is
                                )

map_hm_has = pnl.MappingProjection(
                                matrix=np.random.rand(n_units,len(has_list)),
                                name="map_hm_has",
                                sender=hm,
                                receiver=out_sig_has
                                )

map_hm_can = pnl.MappingProjection(
                                matrix=np.random.rand(n_units,len(can_list)),
                                name="map_hm_can",
                                sender=hm,
                                receiver=out_sig_can
                                )

#This block of code constructs the network

RumelNet = pnl.AutodiffComposition(
        param_init_from_pnl=True,
        patience=10,
        min_delta=0.00001,
        learning_rate=1,
        randomize=False
        )
    
    
RumelNet.add_node(nouns_in)
RumelNet.add_node(rels_in)
RumelNet.add_node(hn)
RumelNet.add_node(hm)
RumelNet.add_node(out_sig_I)
RumelNet.add_node(out_sig_is)
RumelNet.add_node(out_sig_has)
RumelNet.add_node(out_sig_can)

RumelNet.add_projection(sender=nouns_in, projection=map_nouns_hn, receiver=hn)
RumelNet.add_projection(sender=rels_in, projection=map_rels_hm, receiver=hm)
RumelNet.add_projection(sender=hn, projection=map_hn_hm, receiver=hm)
RumelNet.add_projection(sender=hm, projection=map_hm_I, receiver=out_sig_I)
RumelNet.add_projection(sender=hm, projection=map_hm_is, receiver=out_sig_is)
RumelNet.add_projection(sender=hm, projection=map_hm_has, receiver=out_sig_has)
RumelNet.add_projection(sender=hm, projection=map_hm_can, receiver=out_sig_can)

RumelNet.show_graph(output_fmt='jupyter')

# We wish to train our network on pairs of inputs: a noun and a relation.
# On each run, we would like to set the targets for the RELEVANT outputs to be
# the associated truth tables and the targets for the IRRELEVANT outputs to be
# a set of "neutral" targets, producing a somewhat "nonsense" response.

# To get a better grasp on this concept:
# Consider the case that a person asks you which out of the "has" list a robin
# posseses. You will respond, likely correctly, with some of those attributes and
# you will not list any of the "can" attributes, because they're not related to
# the question.

# This is a skill we learn early in life. When asked a simple, closed-form
# question in elementary school, we were not rewarded in the same way for giving
# an answer that was related to the question, but did not actually answer it.
# If the question was, "can a canary fly?" and we gave the answer, "a canary is
# a yellow living thing with wings that can breathe air", we wouldn't technically
# be wrong, but we would also not have answered the question.

# We want to train the network in a similar fashion.

# This block of code creates the targets that will be assigned to outputs irrelevant
# to the input pairs.


irrel_is = np.ones((len(nouns), len(is_list))) * .5
irrel_has = np.ones((len(nouns), len(has_list))) * .5
irrel_can = np.ones((len(nouns), len(can_list))) * .5

# This block of code trains the network using a set of three loops. The innermost
# pair of loops takes each noun and creates the appropriate training inputs and outputs associated
# with its "is", "has", and "can" relations. It will also be associated with an
# identity output.

# After constructing the dictionaries, the middle loop, associated with the nouns,
# trains the network on the dictionaries for n_epochs.

# The outermost loop simply repeats the training on each noun for a set number of
# repetitions.

# You are encouraged to experiment with changing the number of repetitions and
# epochs to see how the network learns best.

# You will find that this code takes a few minutes to run. We have placed flags
# in the loops so you can see that it's not stuck.

n_epochs=5
tot_reps=200

for reps in range(tot_reps):
  print('Training rep: ',reps + 1, ' of: ', tot_reps)
  for noun in range(len(nouns)):
    
    inputs_dict = {}

    targets_dict = {}
    targets_dict[out_sig_is] = []
    targets_dict[out_sig_has] = []
    targets_dict[out_sig_can] = []

    inputs_dict[nouns_in] = []
    targets_dict[out_sig_I] = []
    inputs_dict[rels_in] = []

    for i in range(len(relations)):

      if i==0:
        rel = 'is'

        targ_is = truth_is[noun],
        targ_has = irrel_has[noun],
        targ_can = irrel_can[noun],
        
        targ_is=np.reshape(targ_is,np.amax(np.shape(targ_is)))
        targ_has=np.reshape(targ_has,np.amax(np.shape(targ_has)))
        targ_can=np.reshape(targ_can,np.amax(np.shape(targ_can)))

      elif i==1:
        rel = 'has'

        targ_is = irrel_is[noun] ,
        targ_has = truth_has[noun],
        targ_can = irrel_can[noun],
        
        targ_is=np.reshape(targ_is,np.amax(np.shape(targ_is)))
        targ_has=np.reshape(targ_has,np.amax(np.shape(targ_has)))
        targ_can=np.reshape(targ_can,np.amax(np.shape(targ_can)))


      else:
        rel = 'can'

        targ_is = irrel_is[noun] ,
        targ_has = irrel_has[noun],
        targ_can = truth_can[noun],
        
        targ_is=np.reshape(targ_is,np.amax(np.shape(targ_is)))
        targ_has=np.reshape(targ_has,np.amax(np.shape(targ_has)))
        targ_can=np.reshape(targ_can,np.amax(np.shape(targ_can)))


      targets_dict[out_sig_is].append(targ_is)
      targets_dict[out_sig_has].append(targ_has)
      targets_dict[out_sig_can].append(targ_can)

      inputs_dict[nouns_in].append(nouns_onehot[noun])
      targets_dict[out_sig_I].append(truth_nouns[noun])
      inputs_dict[rels_in].append(rels_onehot[i])

    
    result = RumelNet.run(inputs=[{'inputs': inputs_dict,
                                'targets': targets_dict,
                                'epochs': n_epochs}],do_logging=True)

##################### THIS IS WHERE VISUALIZATION CODE STARTS ##################

# As with previous nets, this cell prints the losses of the network over time.
# Make sure you understand why the losses are noisy.

# If you find your loss isn't to your satisfaction, you can run the previous cell again
# to train your network for another batch.

exec_id = RumelNet.default_execution_id
losses = RumelNet.parameters.losses.get(exec_id)

plt.xlabel('Epoch Number')
plt.ylabel('Loss Value')
plt.title('Losses for the Rumelhart Network')
plt.plot(losses)
print('last lost was: ',losses[-1])

# This code block collects all output data from the network and sorts it into logs of
# outputs from the runs on which each output type was relevant.
# This process retains only those outputs for "is" where the network will have been
# training on a noun-is pair, and so on for all noun-relation pairs.

# If you would like to access the outputs for irrelevant outputs (the "has" output
# from an "is" or "can" run, for example) it is also available in the variables
# created in this cell.

data_I=out_sig_I.log.nparray()[1,1]
data_is=out_sig_is.log.nparray()[1,1]
data_has=out_sig_has.log.nparray()[1,1]
data_can=out_sig_can.log.nparray()[1,1]

data_I=np.array(data_I[1][1::])
data_I=np.matrix(data_I)

data_is=np.array(data_is[1][1::])
data_is=np.matrix(data_is)
                 
data_has=np.array(data_has[1][1::])
data_has=np.matrix(data_has)

data_can=np.array(data_can[1][1::])
data_can=np.matrix(data_can)

log_length=np.shape(data_I)[0]

I_rel_log=data_I[0,:].T
is_rel_log=data_is[0,:].T
has_rel_log=data_has[1,:].T
can_rel_log=data_can[2,:].T

for i in range(int(log_length / len(relations)) - 1):
  I_rel_log = np.append(I_rel_log,data_I[3 * (i + 1), :].T, 1)
  is_rel_log = np.append(is_rel_log,data_is[3 * (i + 1), :].T, 1)
  has_rel_log = np.append(has_rel_log,data_has[3 * (i + 1) + 1, :].T, 1)
  can_rel_log = np.append(can_rel_log,data_can[3 * (i + 1) + 2, :].T, 1)
  
  # This cell plots the last output values from the network for each noun/relation pair
# This will show you what the network has learned with regards to the properties of
# each noun.

for i in range(len(nouns)):
  n=-i
  
  plt.stem(I_rel_log[:, n - 1])
  
  plt.title(nouns[n - 1])
  plt.ylabel('Strength of Association')
  plt.xticks(np.arange(len(nouns)), nouns,rotation=35)
  plt.yticks(np.arange(0,1.1,.1))
  plt.show()

  
  plt.stem(is_rel_log[:, n - 1])
  
  plt.title([nouns[n - 1], ' is:'])
  plt.ylabel('Strength of Association')
  plt.xticks(np.arange(len(is_list)), is_list,rotation=35)
  plt.yticks(np.arange(0,1.1,.1))
  plt.show()
  
  plt.stem(has_rel_log[:, n - 1])
  
  plt.title([nouns[n - 1], ' has:'])
  plt.ylabel('Strength of Association')
  plt.xticks(np.arange(len(has_list)), has_list,rotation=35)
  plt.yticks(np.arange(0,1.1,.1))
  plt.show()

  plt.stem(can_rel_log[:, n - 1])
  
  plt.title([nouns[n - 1], ' can:'])
  plt.ylabel('Strength of Association')
  plt.xticks(np.arange(len(can_list)), can_list,rotation=35)
  plt.yticks(np.arange(0,1.1,.1))
  plt.show()
