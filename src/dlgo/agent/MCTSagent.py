from src.dlgo.agent.base import Agent
from src.dlgo.datatypes.mcts import MCTSNode
from src.dlgo.gotypes import Player, Point
from src.dlgo.goboard import Move
from src.dlgo.agent.naive import RandomBot
from src.dlgo import goboard
import os
import math

def uct_bound(parent_rollouts, child_rollouts, win_pct, temperature):
    exploration = math.sqrt(math.log(parent_rollouts)/ child_rollouts)
    return win_pct + temperature * exploration

class MCTSAgent(Agent):

    def __init__(self, num_rounds, temperature = 1.5):
        Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state):
        root = MCTSNode(game_state)

        for i in range(self.num_rounds):
            node = root
            while(not node.can_add_child() and (not node.is_terminal())):
                node = self.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.game_state)

            while node is not None:
                node.record_win(winner)
                node = node.parent

        best_move = None
        best_pct = - 1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_child(self, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)

        best_score = -1
        best_child = None
        for child in node.children:
            winrate = child.winning_frac(node.game_state.next_player)
            exploration_factor = math.sqrt(math.log(total_rollouts)/ child.num_rollouts)
            uct_bound = winrate + self.temperature*exploration_factor
            if uct_bound > best_score:
                best_score = uct_bound
                best_child = child

        return best_child

    @staticmethod
    def simulate_random_game(game):
        bots = {
            Player.black : RandomBot(),
            Player.white: RandomBot()
        }
        while not game.is_over():
            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)

        return game.winner()

if __name__ == "__main__":
    game = goboard.GameState.new_game(5)
    start_time = os.times()[0]
    bot = MCTSAgent(1000)
    bot_move = bot.select_move(game)
    new_state = game.apply_move(Move.play(Point(row =1, col =1)))
    end_time = os.times()[0]
    print("{} seconds".format(end_time- start_time))