import pygame as pg
from board import Board

board1 = Board(8, 8)


def click(x, y):
    new_x = int(x / 100)
    new_y = int(y / 100)
    return new_x, new_y


def redraw_gamewindow():
    global board1
    board1.draw(win)
    pg.display.update()


def main():
    run = True
    while run:

        redraw_gamewindow()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # if board1.mate:
            #     run = False
            #     print('mate!!!')

            if event.type == pg.MOUSEMOTION:
                pass

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                x1, y1 = click(x, y)
                board1.selected(x1, y1)


pg.init()
win = pg.display.set_mode((800, 800))
pg.display.set_caption('Chess')
win.fill((255, 255, 255))
main()

