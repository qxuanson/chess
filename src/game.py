import pygame

from setting import Config
from board import Board
from piece import *
from dragger import Dragger

class Game:

    def __init__(self):
        self.next_player = 0
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()

    # Show methods

    def show_bg(self, surface):
        for row in range(Config.ROWS):
            for col in range(Config.COLS):
                if (row + col) % 2 == 0:
                    color = Config.themes["light"]
                else:
                    color = Config.themes["dark"]

                rect = (col * Config.SQUARE_SIZE, row * Config.SQUARE_SIZE, Config.SQUARE_SIZE, Config.SQUARE_SIZE)

                pygame.draw.rect(surface, color, rect)
    
    def show_pieces(self, surface):
        for row in range(Config.ROWS):
            for col in range(Config.COLS):
                if self.board.squares[col][row].has_piece():
                    piece = self.board.squares[col][row].piece

                    if piece is not self.dragger.piece:
                        img_center = col * Config.SQUARE_SIZE + Config.SQUARE_SIZE // 2, row * Config.SQUARE_SIZE + Config.SQUARE_SIZE // 2
                        surface.blit(piece.sprite, piece.sprite.get_rect(center=img_center))
                    
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                x = move.x * Config.SQUARE_SIZE
                y = move.y * Config.SQUARE_SIZE

                pygame.draw.rect(surface, '#C86464', [x, y, Config.SQUARE_SIZE, Config.SQUARE_SIZE])

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = (244,247,116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                # rect
                rect = (pos.row * Config.SQUARE_SIZE, pos.col * Config.SQUARE_SIZE, Config.SQUARE_SIZE, Config.SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * Config.SQUARE_SIZE, self.hovered_sqr.row * Config.SQUARE_SIZE, Config.SQUARE_SIZE, Config.SQUARE_SIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]
