from src.dlgo import agent
from src.dlgo import goboard_slow
from src.dlgo import goboard
from src.dlgo import gotypes
from src.dlgo import goboard_fast
from src.dlgo.agent.naive import RandomBot
from src.dlgo.agent.alphabeta import AlphaBeta
from src.dlgo.agent import heuristics
from src.dlgo.agent.MCTSagent import MCTSAgent
from Game import Game

GAME_CACHE = {}

import flask
from flask_socketio import SocketIO, emit

app = flask.Flask(__name__)
#TODO: set up kubernetes cluster then pass in id to cors

corsAllowed = "*"
socketio = SocketIO(app, cors_allowed_origins = corsAllowed)

@app.route("/input", methods=["POST"])
def createBoard():
    req = flask.request.get_json()
    print("Server request: {}".format(req))
    game = goboard.GameState.new_game(req['boardsize'])
    GAME_CACHE[req['id']] = game
    print("Cached game: {}".format(GAME_CACHE))
    return flask.jsonify("true")

@app.route("/playmoveplayer/<move_type>", methods=["POST"])
def playNextMove(move_type):
    req = flask.request.get_json()
    # print("Server request: {}".format(req))
    # fetch the game
    output_message = ""
    completed_play = True
    game = GAME_CACHE[req["id"]]
    game_over = False
    ## define the player
    if(req['player'] == 1): player = gotypes.Player.black
    else: player = gotypes.Player.white
    ## fetch the move
    if(move_type == "point"):
        point_to_play = gotypes.Point(row = req['x']+1, col = req['y']+1)
        player_move = goboard_fast.Move.play(point_to_play)
    elif(move_type == "pass"):player_move = goboard_fast.Move.pass_turn()
    else: player_move = goboard_fast.Move.resign()


    ##check the move is valid
    valid_move = game.is_valid_move_player(player_move)
    self_capture = game.is_move_self_capture(player,player_move)
    violate_ko = game.does_move_violate_ko(player, player_move)

    if(valid_move and not self_capture and not violate_ko):
        game = game.apply_move(player_move)
        player_string = "White" if req['player'] == 2 else "Black"
        if player_move.is_play: output_message += "\n\n" + player_string +"  ({}, {})".format(player_move.point.row, player_move.point.col)
        if player_move.is_pass: output_message += "\n\n"+ player_string + " passed"
        if player_move.is_resign: output_message += "\n\n" + player_string+ " resigned"
    else:
        if(not valid_move): output_message += "\n\n Illegal move (not valid)"
        if(self_capture): output_message += "\n\n Illegal move (self-capture)"
        if(violate_ko): output_message += "\n\n Illegal move (ko)"
        completed_play = False
    GAME_CACHE[req['id']] = game
    new_board =board_grid_to_2d(game.board)
    if game.is_over(): game_over = True
    # print(new_board)
    # print(output_message)
    winner = game.winner()
    if winner == gotypes.Player.black: winner = "\n\n Black wins"
    if winner == gotypes.Player.white: winner = "\n\n White wins"
    return flask.jsonify({"board": new_board, "message": output_message, "valid": completed_play, "over": game_over, "winner": winner})

@app.route("/playmoveai", methods=["POST"])
def playNextMoveAI():
    req = flask.request.get_json()
    # print("Server request : {}".format(req))
    player_string = "White" if req['player'] == 2 else "Black"
    output_message = ""
    game_over = False
    game = GAME_CACHE[req["id"]]
    if not game.is_over():
        num_simulations = 500
        print(num_simulations)
        bot = MCTSAgent(num_simulations)
        bot_move = bot.select_move(game)
        if(bot_move.is_pass): output_message += "\n\n" + "Bot({})".format(player_string) + "Passes"
        if(bot_move.is_resign): output_message += "\n\n Bot({})".format(player_string) + "Resigns"
        if(bot_move.is_play): output_message += "\n\n Bot({})".format(player_string) + "  ({},{})".format(bot_move.point.row,
                                                                                                    bot_move.point.col)

        game = game.apply_move(bot_move)
        new_board = board_grid_to_2d(game.board)
        GAME_CACHE[req['id']] = game
    # print(new_board)
    else:
        game_over = True
        new_board = board_grid_to_2d(game.board)
    if game.is_over(): game_over = True
    print("Game over: {}".format(game_over))
    winner = game.winner()
    if winner == gotypes.Player.black: winner = "\n\n Black wins"
    if winner == gotypes.Player.white: winner = "\n\n White wins"
    return flask.jsonify({"board": new_board, "message": output_message, "over": game_over, "winner": winner})

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

@socketio.on("connect")
def handleConnection():
    print("Incoming connection...")


## handles player versus player connections
@socketio.on("connected")
def handleConnected(data):
    print("incoming connected json", data)
    username = data["data"]["username"]
    boardSize = int(data["data"]["boardSize"])
    gameId = data["data"]["gameId"]
    message = "\n" + username + " connected."

    player = None
    if not gameId in GAME_CACHE.keys():
        GAME_CACHE[gameId] = Game(boardSize)
        player = GAME_CACHE[gameId].assignPlayer(username)
    else:
        player = GAME_CACHE[gameId].assignPlayer(username)
        if player is not None:
            startData = dict()
            startData["players"] = [GAME_CACHE[gameId].black, GAME_CACHE[gameId].white]
            emit("gameStart", startData, broadcast= True)
    # Data sent back to client:
    sendData = dict()
    sendData["data"] = message
    sendData["gameId"] = gameId
    emit("successfulConnection")
    emit("Message", sendData, broadcast=True)

## handles player versus player disconnections/leaves
@socketio.on("disconnected")
def handleDisconnected(data):
    print("incoming disconnected json", data)
    username = data["data"]["username"]
    gameId = data["data"]["gameId"]
    message = "\n" + username + " left."

    sendData = dict()
    sendData["gameId"] = gameId
    sendData["data"] = message
    emit("Message", sendData, broadcast= True)
    if GAME_CACHE[gameId].isPlayer(username) is not None and GAME_CACHE[gameId].started:
        if not GAME_CACHE[gameId].gameState.isOver():
            winner = GAME_CACHE[gameId].otherPlayer(username)
        else:
            winner = GAME_CACHE[gameId].gameState.winner()
            sendData["winner"] = winner
        emit("handleWin", sendData, broadcast= True)
    elif GAME_CACHE[gameId].isPlayer(username):
        GAME_CACHE.pop(gameId)



@socketio.on("broadcastMessage")
def handleBroadcast(data):
    username = data["data"]["user"]
    msg = data["data"]["message"]
    gameId = data["data"]["gameId"]
    sendData = dict()
    sendData["data"] = msg
    sendData["gameId"] = gameId
    sendData["user"] = username
    emit("Message", sendData, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
