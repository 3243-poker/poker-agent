import sys
sys.path.insert(0, './pypokerengine/api/')
import game
setup_config = game.setup_config
start_poker = game.start_poker
import time
from argparse import ArgumentParser


""" =========== *Remember to import your agent!!! =========== """
from garbagealgorithm import GeneticPlayer
# from smartwarrior import SmartWarrior
""" ========================================================= """

#def testperf(config1, config2, table):		
def testperf(config1, config2):	
	# Init to play 500 games of 1000 rounds
	num_game = 1
	max_round = 1000
	initial_stack = 10000
	smallblind_amount = 20

	# Init pot of players
	agent1_pot = 0
	agent2_pot = 0

	# Setting configuration
	config = setup_config(max_round=1000, initial_stack=initial_stack, small_blind_amount=smallblind_amount)
	
	player1 = GeneticPlayer(config1)
	player2 = GeneticPlayer(config2)
	
	# Register players
	config.register_player(name="RandomPlayer", algorithm=player1)
	config.register_player(name="HonestPlayer", algorithm=player2);
	#config.register_player(name=agent_name2, algorithm=RaisedPlayer())
	# config.register_player(name=agent_name1, algorithm=agent1())
	# config.register_player(name=agent_name2, algorithm=agent2())
	

	# Start playing num_game games
	for game in range(1, num_game+1):
		print("Game number: ", game)
		game_result = start_poker(config, verbose=0)
		#print(game_result)
		agent1_pot = agent1_pot + game_result['players'][0]['stack']
		agent2_pot = agent2_pot + game_result['players'][1]['stack']
	return agent1_pot - agent2_pot

	#print("\n After playing {} games of {} rounds, the results are: ".format(num_game, max_round))
	# print("\n Agent 1's final pot: ", agent1_pot)
	#print("\n " + agent_name1 + "'s final pot: ", agent1_pot)
	#print("\n " + agent_name2 + "'s final pot: ", agent2_pot)

	# print("\n ", game_result)
	# print("\n Random player's final stack: ", game_result['players'][0]['stack'])
	# print("\n " + agent_name + "'s final stack: ", game_result['players'][1]['stack'])

	#if (agent1_pot<agent2_pot):
	#	print("\n Congratulations! " + agent_name2 + " has won.")
	#elif(agent1_pot>agent2_pot):
	#	print("\n Congratulations! " + agent_name1 + " has won.")
		# print("\n Random Player has won!")
	#else:
	#	Print("\n It's a draw!") 