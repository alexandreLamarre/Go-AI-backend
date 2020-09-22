from copy import deepcopy

class Go:
    def __init__(self, board):
        self.board = board
        self.neighbors = []
        for i in range(len(board)):
            neighbor_row = []
            for j in range(len(board)):
                neighbor_row.append(self.get_valid_neighbors(i,j))
            self.neighbors.append(neighbor_row)
        self.previousMove = None
        self.gameOver = False

    def get_board(self):
        return self.board

    def place_stone(self,player,x,y):
        new_board = deepcopy(self.board)
        new_board[x][y] = player
        return new_board

    def is_on_board(self,x,y):
        return (x % len(self.board) == x) and (y % len(self.board) == y)

    def get_valid_neighbors(self,x,y):
        possible_neighbors = ((x+1,y), (x-1,y), (x,y+1), (x, y-1))
        return [(p[0],p[1]) for p in possible_neighbors if self.is_on_board(p[0],p[1])]

    def find_reached(self,board,x,y):
        color = board[x][y]
        chain = set((x,y))
        reached = set()
        frontier = [(x,y)]
        while(frontier):
            current_pos = frontier.pop()
            chain.add(current_pos)
            for node in self.neighbors[current_pos[0]][current_pos[1]]:
                if board[node[0]][node[1]] == color and not node in chain:
                    frontier.append((node[0], node[1]))
                elif board[node[1]][node[0]] != color:
                    reached.add((node[0], node[1]))

        return chain, reached

    def check_captures(self,board, x,y):
        chain, reached = self.find_reached(board,x,y)
        non_empty = 0
        for el in reached:
            if(board[el[0]][el[1]]):
                non_empty += 1
        if non_empty == len(reached):
            for i in range(len(chain)):
                board[chain[0]][chain[1]] = 0
            return board, chain
        else:
            return board, {}

    def swap_players(self,player):
        if player == 1:
            return 2
        if player == 2:
            return 1

    def play_move(self,player,x,y):
        output = ""
        if(self.board[x][y]):
            output += "\n Illegal move"
            played = False
            return self.board, output, played
        board = self.place_stone(player,x,y)
        played = True
        opponent = self.swap_players(player)
        color = ""
        if(player == 1): color = "White"
        if(player == 2): color = "Black"
        output += "\n" + color + " moved to" + "({}, {})".format(x,y)



        self.board = board
        return board, output, played #+output2
