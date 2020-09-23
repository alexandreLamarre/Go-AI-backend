from src.dlgo import gotypes
from src.dlgo.agent.base import Agent, GameResult
import random

NINF = float('-inf')
INF = float('inf')

class AlphaBeta(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        if game_state.is_over(): return None
        best_moves = []
        best_outcome = None
        alpha = NINF
        beta = INF
        #self.alphabeta(game_state, self.max_depth, NINF, INF, game_state.next_player, self.eval_fn)
        for move in game_state.legal_moves():
            next_state = game_state.apply_move(move)
            value = self.alphabeta(next_state, self.max_depth, alpha, beta, next_state.next_player, self.eval_fn, next_state.next_player)

            best_value = -value
            if(not best_moves) or (best_value > best_outcome):
                best_moves = [move]
                best_outcome = best_value
                ## update alpha/beta bounds
            elif best_outcome == best_value:
                best_moves.append(move)

        return random.choice(best_moves)

    def alphabeta(self, game_state, depth, alpha, beta, player, eval_fn, original_player):

        if game_state.is_over():
            if game_state.winner() == original_player: return INF
            return NINF

        if depth == 0:
            return eval_fn(game_state)

        if player == original_player:
            value = NINF
            for move in game_state.legal_moves():
                value = max(value, self.alphabeta(game_state.apply_move(move), depth-1, alpha, beta, player.other,
                                                  eval_fn, original_player))
                alpha = max(alpha, value)
                if alpha > beta:
                    break
            return value
        else:
            value = INF
            for move in game_state.legal_moves():
                value = min(value, self.alphabeta(game_state.apply_move(move), depth -1, alpha, beta, player.other,
                                                  eval_fn, original_player))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
