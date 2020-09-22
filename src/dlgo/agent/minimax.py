from src.dlgo.agent.base import Agent,GameResult

class Minimax(Agent):
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        for possible_move in game_state.legal_moves():
            pass



