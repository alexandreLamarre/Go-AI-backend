from src.dlgo import gotypes
from src.dlgo.agent.base import Agent, GameResult

MIN_SCORE = float('-inf')
MAX_SCORE = float('inf')

class AlphaBeta(Agent):

    def select_move(self, game_state):
        pass

    def alpha_beta_result(self, game_state, max_depth, best_black, best_white, eval_fn):

        if game_state.is_over():
            if game_state.winner() == game_state.next_player:
                return MAX_SCORE
            else:
                return MIN_SCORE

        if(max_depth == 0):
            return eval_fn(game_state)

        best_so_far = MIN_SCORE
        for candidate_move in game_state.legal_moves():
            next_state = game_state.apply_move(candidate_move)
            opponent_best_result = self.alpha_beta_result(next_state, max_depth -1, best_black, best_white, eval_fn)
            our_result = -1*opponent_best_result

            if our_result > best_so_far:
                best_so_far = our_result
            if game_state.next_player == gotypes.Player.white:
                if best_so_far > best_white:
                    best_white = best_so_far
                outcome_for_black = -best_so_far
                if outcome_for_black < best_black:
                    return best_so_far
            elif game_state.next_player == gotypes.Player.black:
                if best_so_far> best_black:
                    best_black = best_so_far
                outcome_for_white = -best_so_far
                if outcome_for_white < best_white:
                    return best_so_far

        return best_so_far
