#!/usr/bin/python

from optparse import OptionParser
import numpy as np
import time
	

    
def main(agent, game):

	print "Initialization . . "
	max_episodes = np.inf
	max_steps = np.inf
	recent_rewards_range = 1000
	satisfactory_mean_reward = 1.1
	test_n = 50
	print_stats = True

	mlp_args={}
	
	mlp_args['epsilon_decay_start_step'] = 500000
	mlp_args['epsilon_decay_steps'] = 5000000
	mlp_args['start_epsilon'] = 1.0
	mlp_args['end_epsilon'] = min( 0.1, max(mlp_args['start_epsilon'],0.1))
	network_params={}
	network_params['depth'] = 1
	network_params['hidden_units'] = 40
	network_params['input_dropout'] = False
	network_params['hidden_dropout'] = False
	network_params['input_dropout_p'] = 0.2
	network_params['hidden_dropout_p'] = 0.5
	network_params['loss_function'] = 'sgd'
	network_params['momentum'] = 0.3
	network_params['learning_rate'] = 0.01

	mlp_args['network_params'] = network_params

	import agents
	import games
	if game ==  'dotshooting':
	   	
		game = games.ShootingDotGame(width = 3,height = 3 , max_moves = 50, miss_penalty = 0, living_reward = -1, hit_reward = 150, random_background = False)
	else:
		print "Unsupported game."
		exit(1)

	mlp_args['game'] = game
	
	if agent ==  'mlpqlearner':
		learner=agents.MLPQLearner(**mlp_args)
		
	elif agent ==  'random':
		learner = agents.RandomAgent(game)
	elif agent ==  'human':
		learner = agents.HumanAgent(game)
	else:
		print "Unsupported agent."
		exit(1)

###########################################################################
	print("\nLEARNING")
	print("LearnOn | \tLearn Off")

	recent_rewards = []
	recent_norm_rewards = []
	played_episodes = 0
	logging_frequency = recent_rewards_range
	

	start = time.time()
	while  True:
		#retain only last recentRewardRange episodes rewards
		if len(recent_rewards)>recent_rewards_range:
			recent_rewards = recent_rewards[1:]
		if len(recent_norm_rewards)>recent_rewards_range:
			recent_norm_rewards = recent_norm_rewards[1:]

		episode_reward, episode_normalized_reward = learner.run_episode()
		recent_rewards.append(episode_reward)
		recent_norm_rewards.append(episode_normalized_reward)
		played_episodes+= 1

		recent_mean = np.mean(recent_rewards)
		recent_norm_mean = np.mean(recent_norm_rewards)

		# Some output once for a while
		if played_episodes% logging_frequency == 0:
			#test without learning and exploration
			learner.explore = False
			learner.learning_mode = False
			test_rewards = []
			norm_test_rewards = []
			for i in range(test_n):
				norm_test_reward, test_reward = learner.run_episode()
				test_rewards.append(test_reward)
				norm_test_rewards.append(norm_test_reward)

			learner.explore = True
			learner.learning_mode = True
			test_mean = np.mean( test_rewards )
			norm_test_mean = np.mean( norm_test_rewards )
			print(str(round(recent_norm_mean,4)) + " " + str(round(recent_mean,4)) + " |  \t" + str( round(test_mean,4) )+ "\t" + str(norm_test_mean))
			if print_stats:
				print(" ep:"+ str(played_episodes)+",stps:"+str(learner.steps)+", "+str(learner.actions_stats_learning)+str(learner.actions_stats_test) + ", epsilon= "+ str(learner.epsilon))
				learner.clear_actions_stats()

		#finish if satisfactory_mean_reward is reached
		if len(recent_norm_rewards)>recent_rewards_range and  recent_norm_mean >= satisfactory_mean_reward:
			print("Satisfactory mean reward ("+str(satisfactory_mean_reward)+ ") reached.")
			break
		if played_episodes >= max_episodes:
			print(str(max_episodes)+" episodes reached.")
			break
		if learner.steps >= max_steps:
			print( str(learner.steps) +" steps reached.")
			break

	end = time.time()
	print("\nLearning time: "+ str(round(end-start,2)) + "s")
	#play 100 test episodes without exploration
	print("\nFinal Testing:")
	rewards = []
	norm_rewards = []

	test_n = 100
	learner.explore = False
	learner.learning_mode = False
	for i in range(test_n):
		reward, norm_reward = learner.run_episode()
		rewards.append(reward)
		norm_rewards.append(norm_reward)
		#print reward
	print(str(np.mean(rewards)) + "\t" + str(round(np.mean(norm_rewards),4)))


if __name__ ==  '__main__':
    
    
    option_parser = OptionParser()
    option_parser.add_option("-a", "--agent", dest = "agent",
                  help = "agent name", metavar = "AGENT", type = "string", default = "mlpqlearner")
    option_parser.add_option("-g", "--game", dest = "game",
                  help = "game name", metavar = "GAME", type = "string", default = "dotshooting")
    (options, args) = option_parser.parse_args()
    
    args = {}
    args["agent"] = options.agent
    args["game"] = options.game
    main(**args)