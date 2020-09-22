from src.dlgo import gotypes

def capture_diff(game_state):
    black_stones = 0
    white_stones = 0
    for r in range(1, game_state.board.num_rows+ 1):
        for c in range(1, game_state.board.num_cols):
            p = gotypes.Point(r,c)
            color = game_state.board.get(p)
            if color == gotypes.Player.black:
                black_stones += 1
            elif color == gotypes.Player.white:
                white_stones += 1

    diff = black_stones - white_stones
    if game_state.next_player == gotypes.Player.black: return diff
    return -diff