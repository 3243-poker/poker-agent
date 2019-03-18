from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import time
import pprint

NB_SIMULATION = 400

class HonestPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        start = time.time()

        # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
        # pp = pprint.PrettyPrinter(indent=2)
        # print("------------ROUND_STATE(RANDOM)--------")
        # pp.pprint(round_state)
        # print("------------HOLE_CARD----------")
        # pp.pprint(hole_card)
        # print("------------VALID_ACTIONS----------")
        # pp.pprint(valid_actions)
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=2,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate >= 0.66 and len(valid_actions) == 3:
            action = valid_actions[2]
        elif win_rate >= 0.33:
            action = valid_actions[1]  # fetch CALL action info
        else:
            action = valid_actions[0]  # fetch FOLD action info
        end = time.time()
        print("\n Time taken to try 100 simulations: %.4f seconds" %(end-start))
        return action['action']

    def receive_game_start_message(self, game_info):
        pass
        #self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass