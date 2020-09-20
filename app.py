GAME_CACHE = {}


from flask import Flask
from src.Go import Go
app = Flask(__name__)

@app.route("/createNewBoard")
def createBoard(uuid, board):
     go_board = Go(board)
     GAME_CACHE[uuid] = go_board

@app.route("/playMovePlayer")
def playNextMove(uuid, player):
    go_board = GAME_CACHE[uuid]

    return go_board.get_board, "meaningful message"

@app.route("/playMoveAI")
def playNextMoveAI(uuid, player, AItype):
    go_board = GAME_CACHE[uuid]
    return go_board.get_board, "meaningful message "

if __name__ == "__main__":
    app.run()
