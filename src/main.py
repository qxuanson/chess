import pygame
import sys
from setting import Config
from game import Game
from square import Square
from move import Move
from board import Board
from position import Position, OnBoard

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(pygame.image.load('assets/images/icon.ico'))
        self.game = Game()


    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        

        while True:
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // Config.SQUARE_SIZE
                    clicked_col = dragger.mouseX // Config.SQUARE_SIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_col][clicked_row].has_piece():
                        piece = board.squares[clicked_col][clicked_row].piece
                        board.calc_moves(piece)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        # show methods 
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()


main = Main()
main.mainloop()