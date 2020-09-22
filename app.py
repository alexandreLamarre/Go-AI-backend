from src.dlgo import agent
from src.dlgo import goboard_slow
from src.dlgo import gotypes
from src.dlgo.agent.naive import RandomBot



GAME_CACHE = {}


import flask
from src.Go import Go
app = flask.Flask(__name__)

@app.route("/input", methods=["POST"])
def createBoard():
    req = flask.request.get_json()
    print("Server request: {}".format(req))
    game = goboard_slow.GameState.new_game(req['boardsize'])
    GAME_CACHE[req['id']] = game
    print("Cached game: {}".format(GAME_CACHE))
    return flask.jsonify("true")

@app.route("/playmoveplayer", methods=["POST"])
def playNextMove():
    req = flask.request.get_json()
    # print("Server request: {}".format(req))
    # fetch the game
    output_message = ""
    game = GAME_CACHE[req["id"]]
    ## define the player
    if(req['player'] == 1): player = gotypes.Player.black
    else: player = gotypes.Player.white
    ## fetch the move
    point_to_play = gotypes.Point(row = req['x']+1, col = req['y']+1)
    player_move = goboard_slow.Move.play(point_to_play)

    ##check the move is valid
    valid_move = game.is_valid_move(player_move)
    if valid_move:self_capture = game.is_move_self_capture(player,player_move)
    else: self_capture = False
    if not self_capture and valid_move: violate_ko = game.does_move_violate_ko(player, player_move)
    else: violate_ko = False
    if(valid_move and not self_capture and not violate_ko):
        game = game.apply_move(player_move)
        player_string = "White" if req['player'] == 2 else "Black"
        if player_move.is_play: output_message += "\n" + player_string +"  ({}, {})".format(player_move.point.row, player_move.point.col)
        if player_move.is_pass: output_message += "\n "+ player_string + " passed"
        if player_move.is_resign: output_message += "\n" + player_string+ " resigned"
    else:
        output_message += "\n Illegal move"
    GAME_CACHE[req['id']] = game
    new_board =board_grid_to_2d(game.board)
    # print(new_board)
    # print(output_message)
    return flask.jsonify({"board": new_board, "message": output_message})

@app.route("/playmoveai", methods=["POST"])
def playNextMoveAI():
    req = flask.request.get_json()
    # print("Server request : {}".format(req))
    player_string = "White" if req['player'] == 2 else "Black"
    output_message = ""
    game = GAME_CACHE[req["id"]]
    bot = RandomBot()
    bot_move = bot.select_move(game)
    if(bot_move.is_pass): output_message += "\n Bot({})".format(player_string) + "Passes"
    if(bot_move.is_resign): output_message += "\n Bot({})".format(player_string) + "Resigns"
    if(bot_move.is_play): output_message += "\n Bot({})".format(player_string) + "  ({},{})".format(bot_move.point.row,
                                                                                                bot_move.point.col)
    # print(bot_move)
    # print(bot_move.is_pass)
    # print(bot_move.is_resign)
    # print(bot_move.is_play)
    game = game.apply_move(bot_move)
    new_board = board_grid_to_2d(game.board)
    GAME_CACHE[req['id']] = game
    # print(new_board)
    return flask.jsonify({"board": new_board, "message": output_message })

def board_grid_to_2d(board):
    new_board = []
    for row in range(1, board.num_rows+1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col = col))
            line.append(stone_to_num(stone))
        new_board.append(line)

    return new_board


def stone_to_num(stone):
    if stone == None: return 0
    if stone == gotypes.Player.white: return 2
    if stone == gotypes.Player.black: return 1
    return stone

if __name__ == "__main__":
    app.run()
