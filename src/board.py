from setting import Config
from square import Square
from piece import *
from move import Move
from setting import Config
from position import Position
import math

class Board:

    def __init__(self):
        self.player = 0
        self.squares = []
        self.historic = []
        self.moveIndex = 1
        self.last_move = None
        self._create()
        self._add_pieces(0) #white pieces
        self._add_pieces(1) #black pieces
        self.WhiteKing = None
        self.BlackKing = None
        for squares in self.squares:
            for square in squares:
                if square.piece != None:
                    if square.piece.color == 0 and square.piece.code == "k":
                        self.WhiteKing = square.piece
                    elif square.piece.color == 1 and square.piece.code == "k":
                        self.BlackKing = square.piece
        self.winner = None
        self.pieceToPromote = None
        self.checkWhiteKing = False
        self.checkBlackKing = False
        self.whitePromotions = [Queen(Position(0, 0), 0), Bishop(Position(0, 1), 0), Knight(Position(0, 2), 0), Rook(Position(0, 3), 0)]
        self.blackPromotions = [Rook(Position(0, 7), 1), Knight(Position(0, 6), 1), Bishop(Position(0, 5), 1), Queen(Position(0, 4), 1)]

    def calc_moves(self, piece):
        moves, captures = self.GetAllowedMoves(piece, isAI=False)
        piece.add_capture(captures)
        moves.extend(captures)
        for move in moves:
            initial = Square(piece.position.x, piece.position.y, piece)
            final_piece = self.squares[move.x][move.y].piece
            final = Square(move.x, move.y, final_piece)
            mov = Move(initial, final)
            piece.add_move(move)

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.Move(piece, Position(final.row, final.col))

        #self.squares[initial.row][initial.col].piece = None
        #self.squares[final.row][final.col].piece = piece
        
        #move
        piece.moved = True

        #clear
        piece.moves = []
        
        self.last_move = move


    def valid_move(self, piece, move):
        final = move.final
        pos = Position(final.row, final.col)
        print('final position', final.row, final.col)
        if pos in piece.moves:
            check = True
        else:
            check = False
        print('check valid move', check)
        return check
    
    def Move(self, piece, position):
        if position != None:
            position = position.GetCopy()
            # print(position)
            if self.isCastling(piece, position.GetCopy()):
                self.CastleKing(piece, position.GetCopy())
            elif self.isEnPassant(piece, position.GetCopy()):
                self.squares[position.x][piece.position.y].piece = None
                Config.castle_sound.play()
                self.MovePiece(piece, position)
                self.historic[-1][2] = piece.code + " EP"
            else:
                if self.squares[position.x][position.y].piece != None:
                    Config.capture_sound.play()
                else:
                    Config.move_sound.play()
                self.MovePiece(piece, position)
            # check for promotion
            if type(piece) == Pawn and (piece.position.y == 0 or piece.position.y == 7):
                self.pieceToPromote = piece
            else:
                self.SwitchTurn()
            self.Check()

    def MovePiece(self, piece, position):
        position = position.GetCopy()
        self.squares[piece.position.x][piece.position.y].piece = None
        old_position = piece.position.GetCopy()
        piece.updatePosition(position)
        self.squares[position.x][position.y].piece = piece
        self.historic.append([self.moveIndex, piece.color, piece.code, old_position, piece.position, piece])
        piece.previousMove = self.moveIndex
        self.moveIndex += 1
        self.checkBlackKing = False
        self.checkWhiteKing = False

    def GetPiece(self, coord):
        return self.squares[coord.x][coord.y].piece
    
    def SetPiece(self, position, piece):
        self.squares[position.x][position.y].piece = piece

    def SwitchTurn(self):
        # switch between 0 and 1
        # (0 + 1) * -1 + 2 = 1
        # (1 + 1) * -1 + 2 = 0
        self.player = (self.player + 1 ) * -1 + 2
        # CHECK IF THE PLAYER LOST OR NOT
        self.IsCheckmate()

    def RecentMove(self):
        return None if not self.historic else self.historic[-1]

    def RecentMovePositions(self):
        if not self.historic or len(self.historic) < 1:
            return None, None
        pos = self.historic[-1][3]
        oldPos = self.historic[-1][4]

        return pos.GetCopy(), oldPos.GetCopy()
    
    def AllowedMoveList(self, piece, moves, isAI):
        allowed_moves = []
        for move in moves:
            if self.VerifyMove(piece, move.GetCopy(), isAI):
                allowed_moves.append(move.GetCopy())
        return allowed_moves
    
    def GetAllowedMoves(self, piece, isAI=False):
        moves, captures = piece.GetMoves(self)
        allowed_moves = self.AllowedMoveList(piece, moves.copy(), isAI)
        allowed_captures = self.AllowedMoveList(piece, captures.copy(), isAI)
        print(allowed_moves, allowed_captures)
        return allowed_moves, allowed_captures
    
    def VerifyMove(self, piece, move, isAI):
        # verify the move by going through all the possible outcomes
        # This function will return False if the opponent will reply by capturing the king
        position = move.GetCopy()
        oldPosition = piece.position.GetCopy()
        captureEnPassant = None
        # print(f"new: {move}, old: {oldPosition}")
        capturedPiece = self.squares[position.x][position.y].piece
        if self.isEnPassant(piece, position):
            captureEnPassant = self.squares[position.x][oldPosition.y].piece
            self.squares[position.x][oldPosition.y].piece = None

        self.squares[oldPosition.x][oldPosition.y].piece = None
        self.squares[position.x][position.y].piece = piece
        # print(f"pos: {position}, old: {oldPosition}")
        piece.updatePosition(move)
        EnemyCaptures = self.GetEnemyCaptures(self.player)
        if self.isCastling(piece, oldPosition):
            if math.fabs(position.x - oldPosition.x) == 2 and not self.VerifyMove(piece, Position(5, position.y), isAI) \
                or math.fabs(position.x - oldPosition.x) == 3 and not self.VerifyMove(piece, Position(3, position.y), isAI) \
                or self.IsInCheck(piece):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                return False

        for pos in EnemyCaptures:
            if (self.WhiteKing.position == pos and piece.color == 0) \
                or (self.BlackKing.position == pos and piece.color == 1):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                if captureEnPassant != None:
                    self.squares[position.x][oldPosition.y].piece = captureEnPassant
                return False
        self.UndoMove(piece, capturedPiece, oldPosition, position)
        if captureEnPassant != None:
            self.squares[position.x][oldPosition.y].piece = captureEnPassant
        return True

    def GetEnemyCaptures(self, player):
        captures = []
        for squares in self.squares:
            for square in squares:
                if square.piece != None and square.piece.color != player:
                    moves, piececaptures = square.piece.GetMoves(self)
                    captures = captures + piececaptures
        return captures
    
    def UndoMove(self, piece, captured, oldPos, pos):
        self.squares[oldPos.x][oldPos.y].piece = piece
        self.squares[pos.x][pos.y].piece = captured
        piece.updatePosition(oldPos)

    def isCastling(self,king, position):
        return type(king) == King and abs(king.position.x - position.x) > 1
    
    def isEnPassant(self, piece, newPos):
        if type(piece) != Pawn:
            return False
        moves = None
        if piece.color == 0:
            moves = piece.EnPassant(self, -1)
        else:
            moves = piece.EnPassant(self, 1)
        return newPos in moves

    def IsInCheck(self, piece):
        return type(piece) == King and \
                ((piece.color == 0 and self.checkWhiteKing) or (piece.color == 1 and self.checkBlackKing))
    
    def Check(self):
        if self.player == 0:
            king = self.WhiteKing
        else:
            king = self.BlackKing

        for squares in self.squares:
            for square in squares:
                if square.piece != None and square.piece.color != self.player:
                    moves, captures = self.GetAllowedMoves(square.piece)
                    if king.position in captures:
                        Config.checkmate_sound.play()
                        if self.player == 1:
                            self.checkBlackKing = True
                            return
                        else:
                            self.checkWhiteKing = True
                            return

    def IsCheckmate(self):
        for squares in self.squares:
            for square in squares:
                if square.piece != None and square.piece.color == self.player:
                    moves, captures = self.GetAllowedMoves(square.piece)
                    # if there's any legal move left
                    # then it's not checkmate
                    if moves or captures:
                        return False
        self.Check()
        if self.checkWhiteKing:
            # black won
            self.winner = 1
        elif self.checkBlackKing:
            # white won
            self.winner = 0
        else:
            # it's a draw
            self.winner = -1
        return True
    
    def PromotePawn(self, pawn, choice):
        if choice == 0:
            self.squares[pawn.position.x][pawn.position.y].piece = Queen(pawn.position.GetCopy(), pawn.color)
        elif choice == 1:
            self.squares[pawn.position.x][pawn.position.y].piece = Bishop(pawn.position.GetCopy(), pawn.color)
        elif choice == 2:
            self.squares[pawn.position.x][pawn.position.y].piece = Knight(pawn.position.GetCopy(), pawn.color)
        elif choice == 3:
            self.squares[pawn.position.x][pawn.position.y].piece = Rook(pawn.position.GetCopy(), pawn.color)
        Config.castle_sound.play()
        self.SwitchTurn()
        self.Check()
        self.pieceToPromote = None

    def CastleKing(self, king, position):
        position = position.GetCopy()
        # print("castled")
        # print(position)
        if position.x == 2 or position.x == 6:
            if position.x == 2:
                rook = self.squares[0][king.position.y].piece
                self.MovePiece(king, position)
                self.squares[0][rook.position.y].piece = None
                rook.position.x = 3
                # print("black castled")
            else:
                rook = self.squares[7][king.position.y].piece
                self.MovePiece(king, position)
                self.squares[7][rook.position.y].piece = None
                rook.position.x = 5
                # print("white castled")

            rook.previousMove = self.moveIndex - 1
            self.squares[rook.position.x][rook.position.y].piece = rook
            self.historic[-1][2] = king.code + " C"
            Config.castle_sound.play()

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(Config.COLS)]

        for row in range(Config.ROWS):
            for col in range(Config.COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6,7) if color == 0 else (1,0)

        #Pawns
        for col in range(Config.COLS):
            self.squares[col][row_pawn] = Square(col, row_pawn, Pawn(Position(col, row_pawn), color))

        #Knights
        self.squares[1][row_other] = Square(1, row_other, Knight(Position(1, row_other), color))
        self.squares[6][row_other] = Square(6, row_other, Knight(Position(6, row_other), color))

        #Bishops
        self.squares[2][row_other] = Square(2, row_other, Bishop(Position(2, row_other), color))
        self.squares[5][row_other] = Square(5, row_other, Bishop(Position(5, row_other), color))

        #Rooks
        self.squares[0][row_other] = Square(0, row_other, Rook(Position(0, row_other), color))
        self.squares[7][row_other] = Square(7, row_other, Rook(Position(7, row_other), color))
        
        #Queen
        self.squares[3][row_other] = Square(3, row_other, Queen(Position(3, row_other), color))

        #King
        self.squares[4][row_other] = Square(4, row_other, King(Position(4, row_other), color))