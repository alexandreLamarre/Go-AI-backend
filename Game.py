from src.dlgo import goboard
import random
class Game:
    def __init__(self, boardSize):
        self.gameState = goboard.GameState.new_game(boardSize)
        self.black = None
        self.white = None
        self.started = False

    # returns 1 if the player is assigned black
    # returns 2 if the player is assigned white
    # returns None if both players are already assigned
    def assignPlayer(self, name):
        if self.black is None and self.white is None:
            player = random.random() * 2
            player = int(player)
            if player == 0:
                self.black = name
                return 1
            else:
                self.white = name
                return 2
        elif self.black is None:
            self.black = name
            return 1
        elif self.white is None:
            self.white = name
            return 2
        return None

    def isPlayer(self, name):
        if self.black == name:
            return 1
        if self.white == name:
            return 2

    def otherPlayer(self, name):
        if self.black == name:
            return 2
        if self.white == name:
            return 1

