import pygame as pg
from board import Board
from bot import Bot

bot1 = Bot()
bot2 = Bot()
board1 = Board(8, 8)
base_rect = (100, 100, 700, 700)
square_side = (base_rect[3] - base_rect[1])/8


def click(x, y):
    new_x = int((x - base_rect[0]) / square_side)
    new_y = int((y - base_rect[1]) / square_side)
    return new_x, new_y


def redraw_gamewindow():
    global board1
    board1.draw(win)
    win.fill((128, 128, 128), (300, 50, 300, 40))
    Font = pg.font.SysFont('timesnewroman', 40)
    text = Font.render('%s move' % board1.enabled_colour, False, 'white')
    win.blit(text, (300, 50))
    pg.display.update()


def main():
    run = True
    while run:

        redraw_gamewindow()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # following code enables bot for black pieces
            # if board1.enabled_colour == 'black':
            #     piece, move = bot1.random_move(board1.black_next_moves)
            #     board1.selected(piece.col, piece.raw)
            #     board1.selected(move[0], move[1])

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                x1, y1 = click(x, y)
                board1.selected(x1, y1)

            # if board1.mate:
            #     run = False
            #     print('mate!!!')


pg.init()
win = pg.display.set_mode((800, 800))
pg.display.set_caption('Chess')
win.fill((128, 128, 128))
main()
