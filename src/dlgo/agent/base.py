import enum

class Agent:
    ''' Super class for any go AI'''
    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3