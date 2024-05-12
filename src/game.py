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


        # highlight if in Check
        # white king in check
        if self.board.checkWhiteKing:
            x = self.board.WhiteKing.position.x * Config.SQUARE_SIZE
            y = self.board.WhiteKing.position.y * Config.SQUARE_SIZE
            pygame.draw.rect(self.screen, (240, 111, 150), [x, y, Config.SQUARE_SIZE, Config.SQUARE_SIZE])
            self.screen.blit(self.board.WhiteKing.sprite, (x, y))
        # black king in check
        elif self.board.checkBlackKing:
            x = self.board.BlackKing.position.x * Config.SQUARE_SIZE
            y = self.board.BlackKing.position.y * Config.SQUARE_SIZE
            pygame.draw.rect(self.screen, (240, 111, 150), [x, y, Config.SQUARE_SIZE, Config.SQUARE_SIZE])
            self.screen.blit(self.board.BlackKing.sprite, (x, y))

        self.RenderPromoteWindow()


    def show_last_move(self, surface):
         # draw previous position
        nPosition, oldPosition = self.board.RecentMovePositions()
        if oldPosition and nPosition:
            x1 = oldPosition.x * Config.SQUARE_SIZE 
            y1 = oldPosition.y * Config.SQUARE_SIZE
            x2 = nPosition.x * Config.SQUARE_SIZE
            y2 = nPosition.y * Config.SQUARE_SIZE
            pygame.draw.rect(self.screen, (244,247,116), [x1, y1, Config.SQUARE_SIZE, Config.SQUARE_SIZE])
            pygame.draw.rect(self.screen, (172, 195, 51), [x2, y2, Config.SQUARE_SIZE, Config.SQUARE_SIZE])
        for x in range(Config.SIZE):
            for y in range(Config.SIZE):
                x_pos = x * Config.SQUARE_SIZE
                y_pos = y * Config.SQUARE_SIZE
                if self.board.squares[x][y].piece != None:
                    self.screen.blit(self.board.squares[x][y].piece.sprite, (x_pos, y_pos))

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

    def RenderPromoteWindow(self):
        if self.board.pieceToPromote:
            if self.board.pieceToPromote.color == 0:
                x = self.board.pieceToPromote.position.x * Config.SQUARE_SIZE
                y = self.board.pieceToPromote.position.y * Config.SQUARE_SIZE
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, Config.SQUARE_SIZE , Config.SQUARE_SIZE * 4])
                for i in range(4):
                    piece = self.board.whitePromotions[i]
                    self.screen.blit(piece.sprite, (x, i * Config.SQUARE_SIZE))
                    bottomY = i * Config.SQUARE_SIZE - 1
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, Config.SQUARE_SIZE , 2])
            else:
                x = self.board.pieceToPromote.position.x * Config.SQUARE_SIZE
                y = (self.board.pieceToPromote.position.y - 3) * Config.SQUARE_SIZE
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, Config.SQUARE_SIZE , Config.SQUARE_SIZE * 4])
                for i in range(4):
                    piece = self.board.blackPromotions[i]
                    self.screen.blit(piece.sprite, (x, (i+4) * Config.SQUARE_SIZE))
                    bottomY = (i + 4) * Config.SQUARE_SIZE - 1
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, Config.SQUARE_SIZE , 2])
