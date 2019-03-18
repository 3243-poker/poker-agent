from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.card import Card
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate, gen_deck
import testrun
import random

NB_SIMULATION = 400
rate = {}

class GeneticPlayer(BasePokerPlayer):
    
    coeff = [0, 0, 0, 0, 0] #curr_round, money_diff, rng, win_rate, curr_street
    

    def __init__(self, config):
        self.coeff = config[:]
        # self.rate = table
        self.curr_round = 0
        self.curr_money_diff = 0
        self.curr_street = 0
        self.rng = 0
        self.win_rate = 0
    
    def declare_action(self, valid_actions, hole_card, round_state):
        self.rng = random.randint(0, 10)
        community_card = round_state['community_card']
        # if (len(community_card) == 0):
        #     hole_card = sorted(hole_card, key = lambda x: Card.from_str(x).to_id())
        #     #print(Card.from_str(hole_card[0]).to_id(), Card.from_str(hole_card[1]).to_id())
        #     self.win_rate = self.rate[hole_card[0] + hole_card[1]]
        # else:
        self.win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=2,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )
        
        act = [0, 0, 0]
        for i in range(3):
            act[i] += self.coeff[i * 5 + 0] * self.normalize(self.curr_round, 0, 1000)
            act[i] += self.coeff[i * 5 + 1] * self.normalize(self.curr_money_diff, -10000, 10000)
            act[i] += self.coeff[i * 5 + 2] * self.normalize(self.curr_street, 1, 4)
            act[i] += self.coeff[i * 5 + 3] * self.normalize(self.rng, 0, 10)
            act[i] += self.coeff[i * 5 + 4] * self.normalize(self.win_rate, 0, 1)
        if len(valid_actions) == 3:
            action = valid_actions[act.index(max(act))]
        else:
            #len = 2
            action = valid_actions[act.index(max(act[:2]))]
        print(action['action'])
        return action['action']
        '''
        if win_rate >= 0.66 and len(valid_actions) == 3:
            action = valid_actions[2]
        elif win_rate >= 0.33:
            action = valid_actions[1]  # fetch CALL action info
        else:
            action = valid_actions[0]  # fetch FOLD action info
        return action['action']
        '''
    def normalize(self, v, small, big):
        return (v - ((big + small) / 2)) / (big - small)

    def receive_game_start_message(self, game_info):
        pass
        #self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.current_round = round_count
        pass

    def receive_street_start_message(self, street, round_state):
        if street == "preflop":
            self.curr_street = 1
        elif street == "flop":
            self.curr_street = 2
        elif street == "turn":
            self.curr_street = 3
        elif street == "river":
            self.curr_street = 4

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        player1 = round_state["seats"][0]["stack"]
        player2 = round_state["seats"][1]["stack"]
        self.curr_money_diff = player2 - player1 # I assume I'm always player 2.
        #print(curr_money_diff)
        
class GeneticTrainer():
    
    # def __init__(self, table):
    #     self.table = table
    #     self.coeff = []
    #     self.fitness = []
    #     self.cycles = 10
    
    def __init__(self):
        self.coeff = []
        self.cycles = 10
    
    def main(self):
        for i in range(10):
            self.coeff += [[[random.random() - 0.5, random.random() - 0.5, random.random() - 0.5, random.random() - 0.5, random.random() - 0.5,
                             random.random() - 0.5, random.random() - 0.5, random.random() - 0.5, random.random() - 0.5, random.random() - 0.5,
                             random.random() - 0.5, random.random() - 0.5, random.random() - 0.5, random.random() - 0.5, random.random() - 0.5], 0]]
        print(self.coeff)
        for i in range(self.cycles):
            self.fight()
            self.reproduce()
            self.mutate()
        print(self.coeff)
    
    def fight(self):
        for i in range(10):
            for j in range(i+1, 10):
                print("Player", str(i), self.coeff[i])
                print("Player", str(j), self.coeff[j])
                perf = testrun.testperf(self.coeff[i][0], self.coeff[j][0])
                self.coeff[i][1] += perf
                self.coeff[j][1] += -1 * perf
    
    def reproduce(self):
        self.coeff = sorted(self.coeff, key = lambda x: int(x[1]))[:5]
        newlist = []
        for i in range(5):
            for j in range(i+1, 5):
                newlist += [[self.cross(i,j), 0]]
        self.coeff = newlist[:]
        print(self.coeff)
    
    def cross(self, i, j):
        child = []
        crossoverpt = random.randint(1, 13)
        for k in range(crossoverpt):
            child += [self.coeff[i][0][k]]
        for k in range(crossoverpt, 15):
            child += [self.coeff[j][0][k]]
        return child
    
    def mutate(self):
        for i in range(10):
            r = random.randint(0, 100)
            if r > 80:
                #mutate
                idx = random.randint(0, 14)
                mult = (random.random() - 0.5) * 4
                self.coeff[i][0][idx] *= mult
                self.coeff[i][0][idx] = min(1, self.coeff[i][0][idx])
                self.coeff[i][0][idx] = max(-1, self.coeff[i][0][idx])
                
def precompute():
    rate = {}
    suit = ['C', 'D', 'H', 'S']
    val = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    card = []
    for i in suit:
        for j in val:
            card += [i + j]
    print(card)
    for i in range(52):
        for j in range(52):
            if i == j:
                continue
            card1 = card[i]
            card2 = card[j]
            print(card1, card2)
            win_rate = estimate_hole_card_win_rate(
                nb_simulation=1000,
                nb_player=2,
                hole_card=gen_cards([card1, card2]),
            )
            rate[card1 + card2] = win_rate
    print(len(rate))
    return rate;
            
if __name__ == '__main__':
    #rate = precompute()
    #x = GeneticTrainer(rate)
    x = GeneticTrainer()
    x.main()

def my_handler(event, context):
    context1 = event['config1']
    context2 = event['config2']
    perf = testrun.testperf(context1, context2)
    return {
        'perf': perf
    }