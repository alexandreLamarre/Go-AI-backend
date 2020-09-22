import random
from src.dlgo.agent.base import Agent
from src.dlgo.agent.helpers import is_point_an_eye
from src.dlgo.goboard_slow import Move
from src.dlgo.gotypes import Point

class RandomBot(Agent):
    def select_move(self, game_state):
        ''' Choose a random valid move that preserves Bot's eyes'''
        candidates = game_state.legal_moves()
        return random.choice(candidates)