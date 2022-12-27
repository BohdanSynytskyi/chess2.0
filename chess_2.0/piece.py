
import pygame as pg
import os


white_pawn = pg.image.load(os.path.join("pictures", 'white_pawn.png'))
white_king = pg.image.load(os.path.join("pictures", 'white_king.png'))
white_queen = pg.image.load(os.path.join("pictures", 'white_queen.png'))
white_rook = pg.image.load(os.path.join("pictures", 'white_rook.png'))
white_knight = pg.image.load(os.path.join("pictures", 'white_knight.png'))
white_bishop = pg.image.load(os.path.join("pictures", 'white_bishop.png'))

black_pawn = pg.image.load(os.path.join("pictures", 'black_pawn.png'))
black_king = pg.image.load(os.path.join("pictures", 'black_king.png'))
black_queen = pg.image.load(os.path.join("pictures", 'black_queen.png'))
black_rook = pg.image.load(os.path.join("pictures", 'black_rook.png'))
black_knight = pg.image.load(os.path.join("pictures", 'black_knight.png'))
black_bishop = pg.image.load(os.path.join("pictures", 'black_bishop.png'))

w = [white_pawn, white_king, white_queen, white_rook, white_knight, white_bishop]
b = [black_pawn, black_king, black_queen, black_rook, black_knight, black_bishop]

W = []
B = []

for i in w:
    i = pg.transform.scale(i, (100, 100))
    W.append(i)

for i in b:
    i = pg.transform.scale(i, (100, 100))
    B.append(i)


class Piece:
    img = -1

    check_white_king = False
    check_black_king = False

    # this variable remains 0 if there is no possible move and declares mate
    check_mate = 0

    def __init__(self, col, raw, colour):
        self.raw = raw
        self.col = col
        self.colour = colour
        self.isselected = False
        self.possible_moves = {}
        self.danger = False
        self.enabled = True if self.colour == "white" else False
        self.King = False
        self.Pawn = False

    def move(self, board):
        pass

    # mark squares with piece's possible moves as 1 if there is no piece and
    # changes attribute danger if there is an enemy piece
    def selected(self, board):
        for (i, j), k in self.possible_moves.items():
            if k == 0:
                board[i][j] = 1
            else:
                board[i][j].danger = True

    # unmark squares with piece's possible moves after
    # deselection and restores value of not clicked squares
    def unselected(self, board):
        for (i, j), k in self.possible_moves.items():
            if type(k) == int:
                board[i][j] = 0
            else:
                board[i][j].danger = False
        self.isselected = False
        self.possible_moves = {}  # clears all previous moves

    # function returns all possible moves of the other color
    def check_func(self, board):

        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) != int:
                    if self.colour == "black":
                        if board[i][j].colour != self.colour and board[i][j].King and not Piece.check_white_king:
                            diction = {(i, j): board[i][j]}
                            if board[i][j].check_if_save(board, diction) == {}:
                                Piece.check_white_king = True

                        elif Piece.check_black_king and board[i][j].King:
                            Piece.check_black_king = False

                    elif self.colour == "white":
                        if board[i][j].colour != self.colour and board[i][j].King and not Piece.check_black_king:
                            diction = {(i, j): board[i][j]}
                            if board[i][j].check_if_save(board, diction) == {}:
                                Piece.check_black_king = True

                        elif Piece.check_white_king and board[i][j].King:
                            Piece.check_white_king = False

    # selects only moves which save the king, activates only when king has check
    def block_move(self, board, colour, diction):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) != int:
                    if board[i][j].colour == colour and board[i][j].King:
                        diction1 = board[i][j].check_if_save2(board, diction, self.col, self.raw, self)

                        return diction1

    # making amendments to the board and to piece's location after move
    def change_place(self, board, x, y):

        x0 = self.col
        y0 = self.raw
        self.unselected(board)

        board[x][y] = self
        board[x0][y0] = 0
        self.col = x
        self.raw = y

        if self.Pawn:
            self.first_move = False

        self.check_func(board)

    # drawing piece class objects
    def draw(self, window):
        if self.colour == 'white':
            drawthis = W[self.img]
        else:
            drawthis = B[self.img]

        start_x = self.col * 100
        start_y = self.raw * 100

        if self.isselected:
            pg.draw.rect(window, (255, 0, 0), (start_x, start_y, 100, 100), 2)
            for move, value in self.possible_moves.items():
                if value == 0:
                    pg.draw.circle(window, (255, 0, 0), (move[0]*100+50, move[1]*100+50), 10)

        if self.King:
            if self.check_white_king and self.colour == 'white':
                pg.draw.rect(window, (255, 70, 0), (start_x, start_y, 100, 100), 2)
            elif self.check_black_king and self.colour == 'black':
                pg.draw.rect(window, (255, 70, 0), (start_x, start_y, 100, 100), 2)

        if self.danger:
                pg.draw.rect(window, (255, 255, 0), (start_x, start_y, 100, 100), 2)

        window.blit(drawthis, (start_x, start_y))


class Pawn(Piece):
    img = 0

    def __init__(self, col, raw, colour):
        super().__init__(col, raw, colour)
        self.first_move = True
        self.Pawn = True

    # create possible moves
    def move(self, board):
        x = self.col
        y = self.raw

        # move for white pawn
        if self.colour == "white":
            if self.first_move and board[x][y - 2] == 0 and board[x][y - 1] == 0:
                self.possible_moves[x, y - 2] = 0

            if y > 0 and board[x][y - 1] == 0:
                self.possible_moves[x, y - 1] = 0

            if y > 0 and x < 7 and type(board[x + 1][y - 1]) != int:
                if board[x + 1][y - 1].colour != self.colour:
                    self.possible_moves[x + 1, y - 1] = board[x + 1][y - 1]
            if y > 0 and x > 0 and type(board[x - 1][y - 1]) != int:
                if board[x - 1][y - 1].colour != self.colour:
                    self.possible_moves[x - 1, y - 1] = board[x - 1][y - 1]


        # move for black pawn
        elif self.colour == "black":
            if self.first_move and board[x][y + 2] == 0 and board[x][y + 1] == 0:
                self.possible_moves[x, y + 2] = 0

            if y < 7 and board[x][y + 1] == 0:
                self.possible_moves[x, y + 1] = 0

            if y < 7 and x < 7 and type(board[x + 1][y + 1]) != int:
                if board[x + 1][y + 1].colour != self.colour:
                    self.possible_moves[x + 1, y + 1] = board[x + 1][y + 1]
            if y < 7 and x > 0 and type(board[x - 1][y + 1]) != int:
                if board[x - 1][y + 1].colour != self.colour:
                    self.possible_moves[x - 1, y + 1] = board[x - 1][y + 1]


        if self.colour == 'white' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)

        elif self.colour == 'black' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)


class King(Piece):
    img = 1

    def __init__(self, col, raw, colour):
        super().__init__(col, raw, colour)
        self.King = True

    # function returns new dict with all save moves
    def check_if_save(self, board, diction):

        new_dict = {}
        # loop puts king in all possible moves and checks if there is no move of enemy pieces in this place
        for x, y in diction.keys():
            enemy_moves = []
            board[x][y] = self
            board[self.col][self.raw] = 0
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if type(board[i][j]) != int:

                        if board[i][j].colour != self.colour and (x, y) != (i, j):
                            board[i][j].move(board)
                            enemy_moves.extend(board[i][j].possible_moves.keys())
                            board[i][j].possible_moves = {}

            board[x][y] = diction[(x, y)]
            board[self.col][self.raw] = self
            if (x, y) not in enemy_moves:
                new_dict[x, y] = diction[x, y]
        return new_dict

    def check_if_save2(self, board, diction, x0, y0, piece):

        new_dict = {}
        # loop puts king in all possible moves and checks if there is no move of enemy pieces in this place
        for x, y in diction.keys():
            enemy_moves = []
            board[x][y] = board[x0][y0]
            board[x0][y0] = 0
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if type(board[i][j]) != int:

                        if board[i][j].colour != self.colour:
                            board[i][j].move(board)
                            enemy_moves.extend(board[i][j].possible_moves.keys())
                            board[i][j].possible_moves = {}
            board[x][y] = diction[x, y]
            board[x0][y0] = piece
            if (self.col, self.raw) not in enemy_moves:
                new_dict[x, y] = diction[x, y]
        return new_dict

    def move(self, board):
        x = self.col
        y = self.raw
        # UP LEFT
        if y > 0 and x > 0:
            x1 = x - 1
            y1 = y - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # UP
        if y > 0:
            x1 = x
            y1 = y - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # UP RIGHT
        if y > 0 and x < 7:
            x1 = x + 1
            y1 = y - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # RIGHT
        if x < 7:
            x1 = x + 1
            y1 = y
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # DOWN RIGHT
        if y < 7 and x < 7:
            x1 = x + 1
            y1 = y + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # DOWN
        if y < 7:
            x1 = x
            y1 = y + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # DOWN LEFT
        if y < 7 and x > 0:
            x1 = x - 1
            y1 = y + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # LEFT
        if x > 0:
            x1 = x - 1
            y1 = y
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]

        # checks moves of only enabled king
        if self.enabled:
            self.possible_moves = self.check_if_save(board, self.possible_moves)


class Queen(Piece):
    img = 2

    def move(self, board):

        x1 = self.col
        y1 = self.raw
        # UP
        while y1 > 0:
            x1 = x1
            y1 = y1 - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # DOWN
        x1 = self.col
        y1 = self.raw
        while y1 < 7:
            x1 = x1
            y1 = y1 + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break
        # RIGHT
        x1 = self.col
        y1 = self.raw
        while x1 < 7:
            x1 = x1 + 1
            y1 = y1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # LEFT
        x1 = self.col
        y1 = self.raw
        while x1 > 0:
            x1 = x1 - 1
            y1 = y1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break
        # UP RIGHT
        x1 = self.col
        y1 = self.raw

        while y1 > 0 and x1 < 7:
            x1 = x1 + 1
            y1 = y1 - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # UP LEFT
        x1 = self.col
        y1 = self.raw
        while y1 > 0 and x1 > 0:
            x1 = x1 - 1
            y1 = y1 - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break
        # DOWN LEFT
        x1 = self.col
        y1 = self.raw
        while y1 < 7 and x1 > 0:
            x1 = x1 - 1
            y1 = y1 + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # DOWN RIGHT
        x1 = self.col
        y1 = self.raw
        while y1 < 7 and x1 < 7:
            x1 = x1 + 1
            y1 = y1 + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        if self.colour == 'white' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)

        elif self.colour == 'black' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)


class Rook(Piece):
    img = 3

    def move(self, board):

        x1 = self.col
        y1 = self.raw
        # UP
        while y1 > 0:
            x1 = x1
            y1 = y1 - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # DOWN
        x1 = self.col
        y1 = self.raw
        while y1 < 7:
            x1 = x1
            y1 = y1 + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break
        # RIGHT
        x1 = self.col
        y1 = self.raw
        while x1 < 7:
            x1 = x1 + 1
            y1 = y1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # LEFT
        x1 = self.col
        y1 = self.raw
        while x1 > 0:
            x1 = x1 - 1
            y1 = y1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        if self.colour == 'white' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)

        elif self.colour == 'black' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)


class Knight(Piece):
    img = 4

    def move(self, board):
        x = self.col
        y = self.raw
        # UP LEFT
        if y >= 2 and x > 0:
            x1 = x - 1
            y1 = y - 2
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # UP RIGHT
        if y >= 2 and x < 7:
            x1 = x + 1
            y1 = y - 2
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # LEFT UP
        if y >= 1 and x >= 2:
            x1 = x - 2
            y1 = y - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # RIGHT UP
        if y >= 1 and x <= 5:
            x1 = x + 2
            y1 = y - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # DOWN LEFT
        if y <= 5 and x > 0:
            x1 = x - 1
            y1 = y + 2
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
        # DOWN RIGHT
        if y <= 5 and x < 7:
            x1 = x + 1
            y1 = y + 2
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]

        # LEFT DOWN
        if y < 7 and x >= 2:
            x1 = x - 2
            y1 = y + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]

        # RIGHT DOWN
        if y < 7 and x <= 5:
            x1 = x + 2
            y1 = y + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]

        if self.colour == 'white' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)

        elif self.colour == 'black' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)


class Bishop(Piece):
    img = 5

    def move(self, board):

        x1 = self.col
        y1 = self.raw
        # UP RIGHT
        while y1 > 0 and x1 < 7:
            x1 = x1 + 1
            y1 = y1 - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # UP LEFT
        x1 = self.col
        y1 = self.raw
        while y1 > 0 and x1 > 0:
            x1 = x1 - 1
            y1 = y1 - 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break
        # DOWN LEFT
        x1 = self.col
        y1 = self.raw
        while y1 < 7 and x1 > 0:
            x1 = x1 - 1
            y1 = y1 + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        # DOWN RIGHT
        x1 = self.col
        y1 = self.raw
        while y1 < 7 and x1 < 7:
            x1 = x1 + 1
            y1 = y1 + 1
            if board[x1][y1] == 0:
                self.possible_moves[x1, y1] = 0
            elif board[x1][y1].colour != self.colour:
                self.possible_moves[x1, y1] = board[x1][y1]
                break
            else:
                break

        if self.colour == 'white' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)

        elif self.colour == 'black' and self.enabled:
            self.possible_moves = self.block_move(board, self.colour, self.possible_moves)

