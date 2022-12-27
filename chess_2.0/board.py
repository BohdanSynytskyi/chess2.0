import pygame as pg
import os
from piece import Pawn, Rook, King, Knight, Queen, Bishop

board = pg.image.load(os.path.join("pictures", 'board.png'))
board = pg.transform.scale(board, (800, 800))
previous_piece = (0, 0)


class Board:
    def __init__(self, rows, cols):
        self.mate = False
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.board[0][7] = Rook(0, 7, 'white')
        self.board[1][7] = Knight(1, 7, 'white')
        self.board[2][7] = Bishop(2, 7, 'white')
        self.board[3][7] = King(3, 7, 'white')
        self.board[4][7] = Queen(4, 7, 'white')
        self.board[5][7] = Bishop(5, 7, 'white')
        self.board[6][7] = Knight(6, 7, 'white')
        self.board[7][7] = Rook(7, 7, 'white')

        self.board[0][0] = Rook(0, 0, 'black')
        self.board[1][0] = Knight(1, 0, 'black')
        self.board[2][0] = Bishop(2, 0, 'black')
        self.board[3][0] = King(3, 0, 'black')
        self.board[4][0] = Queen(4, 0, 'black')
        self.board[5][0] = Bishop(5, 0, 'black')
        self.board[6][0] = Knight(6, 0, 'black')
        self.board[7][0] = Rook(7, 0, 'black')

        self.board[0][6] = Pawn(0, 6, "white")
        self.board[1][6] = Pawn(1, 6, "white")
        self.board[2][6] = Pawn(2, 6, "white")
        self.board[3][6] = Pawn(3, 6, "white")
        self.board[4][6] = Pawn(4, 6, "white")
        self.board[5][6] = Pawn(5, 6, "white")
        self.board[6][6] = Pawn(6, 6, "white")
        self.board[7][6] = Pawn(7, 6, "white")

        self.board[0][1] = Pawn(0, 1, "black")
        self.board[1][1] = Pawn(1, 1, "black")
        self.board[2][1] = Pawn(2, 1, "black")
        self.board[3][1] = Pawn(3, 1, "black")
        self.board[4][1] = Pawn(4, 1, "black")
        self.board[5][1] = Pawn(5, 1, "black")
        self.board[6][1] = Pawn(6, 1, "black")
        self.board[7][1] = Pawn(7, 1, "black")

        self.white_pieces = [self.board[0][7], self.board[1][7], self.board[2][7], self.board[3][7],
                             self.board[4][7], self.board[5][7], self.board[6][7], self.board[7][7],
                             self.board[0][6], self.board[1][6], self.board[2][6], self.board[3][6],
                             self.board[4][6], self.board[5][6], self.board[6][6], self.board[7][6], ]

        self.black_pieces = [self.board[0][0], self.board[1][0], self.board[2][0], self.board[3][0],
                             self.board[4][0], self.board[5][0], self.board[6][0], self.board[7][0],
                             self.board[0][1], self.board[1][1], self.board[2][1], self.board[3][1],
                             self.board[4][1], self.board[5][1], self.board[6][1], self.board[7][1], ]

        # self.white_pieces = [self.board[3][7]]
        # self.black_pieces = [self.board[3][0]]

    def draw(self, window):

        window.blit(board, (0, 0))

        for i in range(self.cols):
            for j in range(self.rows):
                if type(self.board[i][j]) != int:
                    self.board[i][j].draw(window)

        if self.mate:
            pg.draw.rect(window, (0, 0, 0), (200, 200, 400, 400), 5)

    def pawn_in_queen(self, x, y):

        if self.board[x][y].Pawn:
            if self.board[x][y].raw == 1 and self.board[x][y].colour == 'white':
                self.white_pieces.remove(self.board[x][y])
                self.board[x][y] = Queen(x, y, self.board[x][y].colour)
                self.white_pieces.append(self.board[x][y])
                self.board[x][y].enabled = False
            if self.board[x][y].raw == 6 and self.board[x][y].colour == 'black':
                self.black_pieces.remove(self.board[x][y])
                self.board[x][y] = Queen(x, y, self.board[x][y].colour)
                self.black_pieces.append(self.board[x][y])
                self.board[x][y].enabled = False

    def check_mate(self, colour):
        if colour == 'white':
            for piece in self.black_pieces:
                piece.move(self.board)
                if piece.possible_moves != {}:
                    piece.possible_moves = {}
                    return 0
        if colour == 'black':
            for piece in self.white_pieces:
                piece.move(self.board)
                if piece.possible_moves != {}:
                    piece.possible_moves = {}
                    return 0

        self.mate = True

    # activates pieces according to colour
    def disable_pieces(self, colour):
        if colour == 'white':
            for piece in self.white_pieces:
                piece.enabled = False
            for piece in self.black_pieces:
                piece.enabled = True
        elif colour == 'black':
            for piece in self.black_pieces:
                piece.enabled = False
            for piece in self.white_pieces:
                piece.enabled = True

    def selected(self, x, y):
        global previous_piece
        # unselecting all pieces
        for i in range(self.rows):
            for j in range(self.cols):
                if type(self.board[i][j]) != int and (i, j) != (x, y):
                    self.board[i][j].isselected = False

        if type(self.board[x][y]) != int:
            # if beaten piece is selected
            if self.board[x][y].danger:
                self.disable_pieces(self.board[previous_piece[0]][previous_piece[1]].colour)

                # deletes beaten piece from a colour list
                if self.board[x][y].colour == 'white':
                    self.white_pieces.remove(self.board[x][y])
                elif self.board[x][y].colour == 'black':
                    self.black_pieces.remove(self.board[x][y])

                self.board[previous_piece[0]][previous_piece[1]].change_place(self.board, x, y)
                self.check_mate(self.board[x][y].colour)
                previous_piece = (0, 0)

            elif not self.board[x][y].isselected and self.board[x][y].enabled:
                self.board[x][y].isselected = True
                if previous_piece != (0, 0):
                    self.board[previous_piece[0]][previous_piece[1]].unselected(self.board)
                self.board[x][y].move(self.board)
                self.board[x][y].selected(self.board)
                previous_piece = (x, y)
            elif not self.board[x][y].enabled:
                if previous_piece != (0, 0):
                    self.board[previous_piece[0]][previous_piece[1]].unselected(self.board)
                    previous_piece = (0, 0)

            elif self.board[x][y].enabled:
                self.board[x][y].isselected = False
                self.board[x][y].unselected(self.board)
                previous_piece = (0, 0)

        elif self.board[x][y] == 1:
            self.disable_pieces(self.board[previous_piece[0]][previous_piece[1]].colour)
            self.pawn_in_queen(previous_piece[0],previous_piece[1])
            self.board[previous_piece[0]][previous_piece[1]].change_place(self.board, x, y)

            self.check_mate(self.board[x][y].colour)

            previous_piece = (0, 0)

        elif previous_piece != (0, 0):
            self.board[previous_piece[0]][previous_piece[1]].unselected(self.board)
            previous_piece = (0, 0)



