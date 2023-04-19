#!/usr/bin/env python

import sys

import pygame as pg

from board import Board


class App:
    """docstring for App."""

    def __init__(self):

        self.startPG()

        ##Define Colors

        self.bg_col = (246,246,246)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.black = (0,0,0)
        self.gray = (163,163,163)
        self.own_col = (0,21,145)

        ##Setup Board

        self.gameBoard = Board('some_sudoku.csv', board_n=-1)

        self.margin = 50
        self.sqWidth = min((self.xmax-self.margin*2)/self.gameBoard.board.shape[1],(self.ymax-self.margin*2)/self.gameBoard.board.shape[0])

        self.numfont = pg.font.SysFont('Arial Regular', 45)

    def startPG(self):
        ##Setup pygame

        pg.init()

        self.xmax = 700
        self.ymax = 700
        self.res = (self.xmax,self.ymax)

        self.scr = pg.display.set_mode(self.res)
        pg.display.set_caption("Sudoku")

        pg.font.init()

    def stopPG(self):

        ##Terminate App
        pg.font.quit()
        pg.quit()
        sys.exit()

    def run(self, FPS=30):
        running = True

        fpsClock=pg.time.Clock()
        t0 = 0.001*pg.time.get_ticks()

        select_pos = (0,0)

        while running:

            t = 0.001*pg.time.get_ticks()
            dt = (t-t0)

            pg.event.pump()
            # ------------------ PyGame Draw ------------------

            self.scr.fill(self.bg_col)

            for v_i in range(self.gameBoard.board.shape[1]+1):
                linewidth = 5 if v_i % 3 == 0 else 1
                pg.draw.line(self.scr,self.gray,(self.margin+v_i*self.sqWidth,self.margin),(self.margin+v_i*self.sqWidth,self.ymax-self.margin),width=linewidth)
            for h_i in range(self.gameBoard.board.shape[0]+1):
                linewidth = 5 if h_i % 3 == 0 else 1
                pg.draw.line(self.scr,self.gray,(self.margin,self.margin+h_i*self.sqWidth),(self.xmax-self.margin,self.margin+h_i*self.sqWidth),width=linewidth)

            for i, row in enumerate(self.gameBoard.board):
                for j, number in enumerate(row):
                    if number != 0:
                        color = self.black if number>0 else self.own_col
                        textSurface = self.numfont.render(str(abs(number)), False, color)
                        textRect = textSurface.get_rect()
                        textRect.center = (self.margin+(j+0.5)*self.sqWidth,self.margin+(i+0.5)*self.sqWidth)
                        self.scr.blit(textSurface,textRect)
            try:
                s = pg.Surface((self.sqWidth,self.sqWidth))
                s.set_alpha(64)
                s.fill((255,255,0))
                self.scr.blit(s, (self.margin+select_pos[1]*self.sqWidth,self.margin+select_pos[0]*self.sqWidth))
            except (NameError, TypeError):
                pass


            # ------------------ PyGame Events ------------------

            numberKeys = [pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5,pg.K_6,pg.K_7,pg.K_8,pg.K_9]
            for event in pg.event.get():
                #print(event)
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                elif event.type == pg.MOUSEBUTTONUP:
                    mouse_pos = self.mouse2idx(pg.mouse.get_pos())
                    select_pos = mouse_pos if mouse_pos is not None else select_pos
                elif event.type == pg.KEYDOWN and event.key == pg.K_s and not self.gameBoard.solved:
                    ts0 = 0.001*pg.time.get_ticks()
                    self.gameBoard.solve_board(0)
                    ts1 = 0.001*pg.time.get_ticks()
                    dts = ts1 - ts0
                    print(f'Time to solve: {dts:.2f} s')
                    self.gameBoard.solved = True
                elif event.type == pg.KEYDOWN and event.key in numberKeys:
                    self.gameBoard.board[select_pos] = -(event.key - 48) if app.gameBoard.board[select_pos]<=0 else app.gameBoard.board[select_pos]
                elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                    self.gameBoard.board[select_pos] = 0 if app.gameBoard.board[select_pos]<=0 else app.gameBoard.board[select_pos]
                elif event.type == pg.KEYDOWN and event.key == pg.K_l:
                    self.gameBoard.set_board()
                elif event.type == pg.KEYDOWN and event.key == pg.K_u:
                    self.gameBoard.unset_board()

            pg.display.update()

            t0 = t

            fpsClock.tick(FPS)

    def mouse2idx(self, pos:tuple) -> tuple:
        if pos[0]<self.margin or pos[0]>(self.xmax-self.margin) or pos[1]<self.margin or pos[1]>(self.ymax-self.margin):
            return None
        idx_x = (pos[0]-self.margin)*self.gameBoard.board.shape[1]//(self.xmax-self.margin*2)
        idx_y = (pos[1]-self.margin)*self.gameBoard.board.shape[0]//(self.ymax-self.margin*2)
        return idx_y,idx_x

if __name__ == '__main__':
    app = App()
    app.run()
    app.stopPG()
