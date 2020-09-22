from src.dlgo.gotypes import Player, Point
from collections import namedtuple

class TerritoryScoring():
    ''' Object that computes attributes used for territory scoring using
        a flood-fill generated dict of points: status'''
    def __init__(self, territory_map):
        self.black_territory = 0
        self.white_territory = 0
        self.black_stones = 0
        self.white_stones = 0
        for point,status in territory_map.items():
            if status == Player.black:
                self.black_stones += 1
            elif status == Player.white:
                self.white_stones += 1
            elif status == "tw":
                self.white_territory += 1
            elif status == "tb":
                self.black_territory += 1




def evaluate_territory(board):
    status = {}
    for r  in range(1, board.num_rows + 1):
        for c in range(1, board.num_cols + 1):
            p = Point(row =r, col = c)
            if p in status:
                continue
            stone = board.get(p)
            if stone is not None:
                status[p] = board.get(p)
            else:
                group, neighbors = flood_fill(p, board)
                if len(neighbors) == 1:
                    neighbor_stone = neighbors.pop()
                    stone_str = 'b' if neighbor_stone == Player.black else 'w'
                    fill_status = 't'+stone_str
                else:
                    fill_status = None
                for point in group:
                    status[point] = fill_status

    return TerritoryScoring(status)


def flood_fill(start, board, visited = None):
    if visited is None:
        visited = {}
    if start in visited:
        return [],set()
    all_points = [start]
    all_borders = set()
    visited[start] = True
    here = board.get(start)
    neighbors = [(-1, 0), (1,0), (0, -1), (0,1)]
    for x,y in neighbors:
        next_p = Point(row = x+start.row, col = y+start.col)
        if not board.is_on_grid(next_p):
            continue
        neighbor = board.get(next_p)
        if neighbor == here:
            points,borders = flood_fill(next_p, board, visited)
            all_points += points
            all_borders |= borders
        else:
            all_borders.add(neighbor)
    return all_points, all_borders


class GameResult(namedtuple('GameResult', 'b w komi')):
    @property
    def winner(self):
        if self.b > self.w + self.komi:
            return Player.black
        return Player.white


def final_game_score(game_state):
    territory = evaluate_territory(game_state.board)
    return GameResult(territory.black_stones+territory.black_territory,
                      territory.white_territory + territory.white_stones,
                      komi = 7.5)