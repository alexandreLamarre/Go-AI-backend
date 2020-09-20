GAME_CACHE = {}


from flask import Flask, request, jsonify
from src.Go import Go
app = Flask(__name__)

@app.route("/createNewBoard", methods=["POST"])
def createBoard():
    content = request.json()
    # go_board = Go(board)
    # GAME_CACHE[uuid] = go_board

@app.route("/playMovePlayer")
def playNextMove(uuid, player):
    go_board = GAME_CACHE[uuid]



@app.route("/playMoveAI")
def playNextMoveAI(uuid, player, AItype):
    go_board = GAME_CACHE[uuid]

if __name__ == "__main__":
    app.run()
