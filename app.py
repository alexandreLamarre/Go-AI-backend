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
    print("Server request: {}".format(req))
    # game = GAME_CACHE[req["id"]]

    return flask.jsonify({"recieved": True})

@app.route("/playmoveai", methods=["POST"])
def playNextMoveAI():
    req = flask.request.get_json()
    print("Server request : {}".format(req))
    game = GAME_CACHE[req["id"]]
    bot = RandomBot()
    bot_move = bot.select_move(game)
    print(bot_move)
    print(bot_move.is_pass)
    print(bot_move.is_resign)
    print(bot_move.is_play)
    game = game.apply_move(bot_move)

    return flask.jsonify({"received": True})

if __name__ == "__main__":
    app.run()
