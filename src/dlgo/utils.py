import platform
import subprocess

import numpy as np

class MoveAge():
    def __init__(self, board):
        self.move_ages = np.ones((board.num_rows, board.num_cols))

    def get(self, row, col):
        return self.move_ages[row,col]

    def reset_age(self, point):
        self.move_ages[point.row-1, point.col-1] = -1

    def add(self, point):
        self.move_ages[point.row-1, point.col-1] = 0

    def increment_all(self):
        self.move_ages[self.move_ages > -1] += 1