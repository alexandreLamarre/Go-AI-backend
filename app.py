GAME_CACHE = {}


import flask
from src.Go import Go
app = flask.Flask(__name__)

@app.route("/input", methods=["POST"])
def createBoard():
    req = flask.request.get_json()
    go_board = Go(req["board"])
    GAME_CACHE[req["id"]] = go_board
    # print(GAME_CACHE[req["id"]])
    # print(req)
    return flask.jsonify("true")

@app.route("/playmoveplayer", methods=["POST"])
def playNextMove():
    req = flask.request.get_json()
    print(req)
    go_board = GAME_CACHE[req["id"]]
    board, message = go_board.play_move(req["player"], req["x"], req["y"])
    return flask.jsonify({"board": board, "message":message})

@app.route("/playMoveAI")
def playNextMoveAI(uuid, player, AItype):
    go_board = GAME_CACHE[uuid]

if __name__ == "__main__":
    app.run()
