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

    # def set_move(self, player, move, x, y):
    #     if(move == "pass" and not(self.previousMove)):
    #         self.previousMove = true
    #     elif(move == "pass" and self.previousMove):
    #         self.gameOver
    #     else:
    #         self.play(player,x,y)

    # def play(self, player, x, y):
    #     self.board[y][x] = player
    #     self.updateBoard(x,y)

    def place_stone(self,player,x,y):
        new_board = list(list(board_row for board_row in self.board))
        new_board[y][x] = player
        return new_board

    def is_on_board(self,x,y):
        return (x % len(self.board) == x) and (y % len(self.board) == y)

    def get_valid_neighbors(self,x,y):
        possible_neighbors = ((x+1,y), (x-1,y), (x,y+1), (x, y-1))
        return [self.board[p[1]][p[0]] for p in possible_neighbors if self.is_on_board(p[0],p[1])]

    def find_reached(self,board,x,y):
        color = board[y][x]
        chain = set((x,y))
        reached = set()
        frontier = [(x,y)]
        while(frontier):
            current_pos = frontier.pop()
            chain.add(current_pos)
            for node in self.neighbors[current_pos[1]][current_pos[0]]:
                if board[node[1]][node[0]] == color and not node in chain:
                    frontier.append((node[0], node[1]))
                elif board[fn] != color:
                    reached.add((node[0], node[1]))

        return chain, reached

    def check_captures(self,board, x,y):
        chain, reached = self.find_reached(board,x,y)
        non_empty = 0
        for i in range(len(reached)):
            if(board[reached[1]][reached[0]]):
                non_empty += 1
        if non_empty == len(reached):
            for i in range(len(chain)):
                board[chain[1]][chain[0]] = 0
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
        if(self.board[y][x]):
            output += "Illegal move"
            return self.board, output

        board = self.place_stone(player,x,y)
        opponent = self.swap_players(player)

        player_stones = []
        opponent_stones = []

        for node in self.neighbors[y][x]:
            if(board[y][x] == player):
                player_stones.append((x,y))
            if(board[y][x] == opponent):
                opponent_stones.append((x,y))
        chain = {}
        for s in opponent_stones:
            board, chain = self.check_captures(board, s[0],s[1])
            output += str(chain)
        if output:
            color = ""
            if(player == 1): color = "White"
            if(player == 2): color = "Black"
            output = color + " captured :" + output
        output2 = ""
        for s in player_stones:
            board,chain = self.check_captures(board, s[0],s[1])
            output2 += str(chain)
        if output2:
            if(player == 1): color = "White"
            if(player == 2): color = "Black"
            output2 = color + " captured : " + output2

        self.board = board
        return board, output+output2
