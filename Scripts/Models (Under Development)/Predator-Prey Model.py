import timeit
import numpy as np
from psyneulink import *

from gym_forager.envs.forager_env import ForagerEnv

# Runtime Switches:
RENDER = True
PNL_COMPILE = False

# *********************************************************************************************************************
# *********************************************** CONSTANTS ***********************************************************
# *********************************************************************************************************************


# These should probably be replaced by reference to ForagerEnv constants:
obs_len = 3
obs_coords = 2
action_len = 2
player_idx = 0
player_obs_start_idx = player_idx * obs_len
player_value_idx = player_idx * obs_len + obs_coords
player_coord_slice = slice(player_obs_start_idx,player_value_idx)
predator_idx = 1
predator_obs_start_idx = predator_idx * obs_len
predator_value_idx = predator_idx * obs_len + obs_coords
predator_coord_slice = slice(predator_obs_start_idx,predator_value_idx)
prey_idx = 2
prey_obs_start_idx = prey_idx * obs_len
prey_value_idx = prey_idx * obs_len + obs_coords
prey_coord_slice = slice(prey_obs_start_idx,prey_value_idx)

player_len = prey_len = predator_len = obs_coords


# *********************************************************************************************************************
# **************************************  MECHANISMS AND COMPOSITION  *************************************************
# *********************************************************************************************************************

# Perceptual Mechanisms
player_obs = ProcessingMechanism(size=prey_len, function=GaussianDistort, name="PLAYER OBS")
prey_obs = ProcessingMechanism(size=prey_len, function=GaussianDistort, name="PREY OBS")
predator_obs = TransferMechanism(size=predator_len, function=GaussianDistort, name="PREDATOR OBS")

# Value and Reward Mechanisms (not yet used;  for future use)
values = TransferMechanism(size=3, name="AGENT VALUES")
reward = TransferMechanism(name="REWARD")

# Action Mechanism
#    Use ComparatorMechanism to compute direction of action as difference of coordinates between player and prey:
#    note: unitization is done in main loop, to allow compilation of LinearCombination function) (TBI)
greedy_action_mech = ComparatorMechanism(name='ACTION',sample=player_obs,target=prey_obs)

# Create Composition
agent_comp = Composition(name='PREDATOR-PREY COMPOSITION')
agent_comp.add_c_node(player_obs)
agent_comp.add_c_node(predator_obs)
agent_comp.add_c_node(prey_obs)
agent_comp.add_c_node(greedy_action_mech)

# ControlMechanism
#   function for ObjectiveMechanism
dist = Distance(metric=EUCLIDEAN)
def dist_diff_fct(variable):
    if variable is None:
        return 0
    player_coord = variable[0]
    predator_coord = variable[1]
    prey_coord = variable[2]
    dist_to_predator = dist([player_coord, predator_coord])
    dist_to_prey = dist([player_coord, prey_coord])
    return dist_to_predator - dist_to_prey
ocm = OptimizationControlMechanism(# features=[prey_obs, predator_obs],
                                   features={SHADOW_EXTERNAL_INPUTS: [prey_obs, predator_obs]},
                                   agent_rep=agent_comp,
                                   function=GridSearch,
                                   objective_mechanism=ObjectiveMechanism(function=dist_diff_fct,
                                                                          monitored_output_states=[player_obs,
                                                                                                   predator_obs,
                                                                                                   prey_obs]),
                                   control_signals=[ControlSignal(projections=(VARIANCE,player_obs),
                                                                  allocation_samples=[0, 1, 10, 100]),
                                                    ControlSignal(projections=(VARIANCE,predator_obs),
                                                                  allocation_samples=[0, 1, 10, 100]),
                                                    ControlSignal(projections=(VARIANCE,prey_obs),
                                                                  allocation_samples=[0, 1, 10, 100]),
                                                    ]
                                   )
agent_comp.add_model_based_optimizer(ocm)
agent_comp.enable_model_based_optimizer = True

# agent_comp.show_graph(show_mechanism_structure='ALL')
# agent_comp.show_graph()


# *********************************************************************************************************************
# ******************************************   RUN SIMULATION  ********************************************************
# *********************************************************************************************************************

num_trials = 4

def main():
    env = ForagerEnv()
    reward = 0
    done = False
    if RENDER:
        env.render()  # If visualization is desired
    else:
        print("Running simulation...")
    steps = 0
    start_time = timeit.default_timer()
    for _ in range(num_trials):
        observation = env.reset()
        while True:
            if PNL_COMPILE:
                BIN_EXECUTE = 'LLVM'
            else:
                BIN_EXECUTE = 'Python'
            run_results = agent_comp.run(inputs={player_obs:[observation[player_coord_slice]],
                                                 predator_obs:[observation[predator_coord_slice]],
                                                 prey_obs:[observation[prey_coord_slice]],
                                                 },
                                         bin_execute=BIN_EXECUTE
                                         )
            action = np.where(run_results[0]==0,0,run_results[0]/np.abs(run_results[0]))
            # action = np.squeeze(np.where(greedy_action_mech.value==0,0,
            #                              greedy_action_mech.value[0]/np.abs(greedy_action_mech.value[0])))
            observation, reward, done, _ = env.step(action)
            if done:
                break
    stop_time = timeit.default_timer()
    print(f'{steps / (stop_time - start_time):.1f} steps/second, {steps} total steps in '
          f'{stop_time - start_time:.2f} seconds')
    if RENDER:
        env.render()  # If visualization is desired

if __name__ == "__main__":
    main()
