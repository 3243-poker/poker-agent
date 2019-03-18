from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import random as rand
import pprint
import math

class RandomPlayer(BasePokerPlayer):

  def declare_action(self, valid_actions, hole_card, round_state):
    # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
    # pp = pprint.PrettyPrinter(indent=2)
    # print("------------ROUND_STATE(RANDOM)--------")
    # pp.pprint(round_state)
    # print("------------HOLE_CARD----------")
    # pp.pprint(hole_card)
    # print("------------VALID_ACTIONS----------")
    # pp.pprint(valid_actions)
    cutoff_depth = 10
    action, payoff = minimax(valid_actions, hole_card, round_state, cutoff_depth, True, -1*math.inf, math.inf)
    # print("------------ACTION(RANDOM)--------")
    # pp.pprint(action)
    # print("-------------------------------")
    return action  # action returned here is sent to the poker engine
    
  def minimax(valid_actions, hole_card, round_state, curr_depth, is_max_player, alpha, beta):
    if curr_depth == 0:
      return eval_func(valid_actions, hole_card, round_state, is_max_player)
    best_action = 0
    payoff = 0
    if is_max_player:
      max_eval = -1*math.inf
      child_states = [fold_state, call_state, raise_state] # how to write this?!?!?!
      for i in range(3):
        child = child_states[i]
        _, curr_eval = minimax(valid_actions, hole_card, child, curr_depth-1, False, alpha, beta)
        if curr_eval > max_eval:
          max_eval = curr_eval
          best_action = i
        alpha = max(alpha, curr_eval)
        if beta <= alpha:
          break
      payoff = max_eval
    else:
      min_eval = math.inf
      child_states = [fold_state, call_state, raise_state] # how to write this?!?!?!
      for i in range(3):
        child = child_states[i]
        _, curr_eval = minimax(valid_actions, hole_card, child, curr_depth-1, True, alpha, beta)
        if curr_eval < max_eval:
          min_eval = curr_eval
          best_action = i
        beta = min(beta, curr_eval)
        if beta <= alpha:
          break
      payoff = min_eval
    return valid_actions[best_action]["action"], payoff
    
  
    
  def eval_func(valid_actions, hole_card, round_state, is_max_player):
    return 
    

  def receive_game_start_message(self, game_info):
    pass

  def receive_round_start_message(self, round_count, hole_card, seats):
    pass

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    pass

def setup_ai():
  return RandomPlayer()

def minimax(