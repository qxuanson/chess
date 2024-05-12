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
        
        Config.game_start_sound.play()
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.RenderPromoteWindow(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // Config.SQUARE_SIZE
                    clicked_col = dragger.mouseX // Config.SQUARE_SIZE
                    
                    #promote pawn
                    if board.pieceToPromote != None and clicked_col == board.pieceToPromote.position.x:
                        choice = clicked_row
                        print('promote pawn col', choice)
                        if choice <= 3 and board.player == 0:
                            # promote pawn
                            board.PromotePawn(board.pieceToPromote, choice)
                            # refresh screen
                            # refresh screen
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            pygame.display.update()
                        elif choice > 3 and board.player == 1:
                            # promote pawn
                            board.PromotePawn(board.pieceToPromote, 7-choice)
                            # refresh screen
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            pygame.display.update()
                    
                    # if clicked square has a piece ?
                    elif board.squares[clicked_col][clicked_row].has_piece():
                        piece = board.squares[clicked_col][clicked_row].piece
                        #check player
                        if piece.color == board.player:
                            board.calc_moves(piece)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // Config.SQUARE_SIZE
                    motion_col = event.pos[0] // Config.SQUARE_SIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        release_row = dragger.mouseY // Config.SQUARE_SIZE
                        release_col = dragger.mouseX // Config.SQUARE_SIZE
                        release_piece = board.squares[release_col][release_row].piece
                        initial = Square(dragger.initial_col, dragger.initial_row, dragger.piece)
                        final = Square(release_col, release_row, release_piece)
                        if initial == final:
                            dragger.undrag_piece()
                        else:
                            move = Move(initial, final)
                            
                            if board.valid_move(dragger.piece, move):
                                board.move(dragger.piece, move)
                                #show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)

                    dragger.undrag_piece()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()


main = Main()
main.mainloop()