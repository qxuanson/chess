from setting import Config
from texture import *
from position import Position, OnBoard


class Piece:
    def __init__(self, position, color):
        # 0 -> White, 1 -> Black
        self.position = position
        self.color = color
        self.previousMove = None
        self.code = None
        self.moved = False
        self.moves = []
        self.captures = []
        self.movs = []

    def print_name(self):
        print(self.code)

    def add_mov(self, mov):
        self.movs.append(mov)

    def add_capture(self, capture):
        self.captures.append(capture)

    def add_move(self, move):
        self.moves.append(move)

    def updatePosition(self, position):
        self.position.x = position.x
        self.position.y = position.y

    def GetPatternMoves(self, board, patterns):
        moves = []
        captures = []
        for pattern in patterns:
            m, c = self.generator(board, pattern[0], pattern[1])
            moves =  moves+ m
            captures = captures+ c
        return moves, captures

    def generator(self, board, dx, dy):
        moves = []
        captures = []
        pos = Position(self.position.x + dx, self.position.y + dy)

        while OnBoard(pos) and board.squares[pos.x][pos.y].piece == None:
            moves.append(pos.GetCopy())
            pos.x = pos.x + dx
            pos.y = pos.y + dy
        if OnBoard(pos) and board.squares[pos.x][pos.y].piece != None and board.squares[pos.x][pos.y].piece.color != self.color:
            captures.append(pos.GetCopy())

        # print(moves)

        return moves, captures

class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "p"
        self.value = 10 if color == 0 else -10
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.moves = []
        self.pieceMap = []

    def EnPassant(self, board, change):
        moves = []
        for i in (-1, 1):
            temp_pos = Position(self.position.x + i, self.position.y)
            if OnBoard(temp_pos):
                pieceToCapture = board.squares[temp_pos.x][temp_pos.y].piece
                if type(pieceToCapture) == Pawn and self.color != pieceToCapture.color:
                    previousmove = board.RecentMove()
                    if previousmove != None and previousmove[2] == self.code and previousmove[4].x == self.position.x + i\
                        and abs(previousmove[4].y - previousmove[3].y) == 2:
                        moves.append(Position(self.position.x + i, self.position.y + change))

        return moves

    def GetMoves(self, board):
        moves = []
        captures = []
        if self.color == 0:
            offset = -1
        else:
            offset = 1
        dy = self.position.y + offset
        # all the possible moves of a pawn
        if OnBoard(Position(self.position.x, dy)) and board.squares[self.position.x][dy].piece == None :
            moves.append(Position(self.position.x, dy))
            if self.previousMove == None:
                dy += offset
                if board.squares[self.position.x][dy].piece == None:
                    moves.append(Position(self.position.x, dy))

        dy = self.position.y + offset
        # diagonal captures
        for i in (-1, 1):
            dx = self.position.x + i
            if OnBoard(Position(dx, dy)) and board.squares[dx][dy].piece != None:
                if board.squares[dx][dy].piece.color != self.color:
                    captures.append(Position(dx, dy))
        # EN PASSANT CAPTURES
        special_moves = self.EnPassant(board, offset)
        captures += special_moves
        return moves, captures

class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "b"
        self.value = 30 if color == 0 else -30
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.moves = []
        self.pieceMap = []

    def GetMoves(self, board):
        moves, captures = self.DiagonalMoves(board)
        return moves, captures

    def DiagonalMoves(self, board):
        patterns = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        moves, captures = self.GetPatternMoves(board, patterns)
        return moves, captures

class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "r"
        self.value = 50 if color == 0 else -50
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.moves = []
        self.pieceMap = []

    def GetMoves(self, board):
        moves, captures = self.VertHorzMoves(board)
        return moves, captures

    def VertHorzMoves(self, board):
        patterns = ((-1, 0), (1, 0), (0, 1), (0, -1))
        return self.GetPatternMoves(board, patterns)

class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "n"
        self.value = 30 if color == 0 else -30
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.moves = []
        self.pieceMap = []

    def GetMoves(self, board):
        moves = []
        captures = []

        for i in range(-2, 3):
            if i != 0:
                for j in range(-2, 3):
                    if j != 0:
                        dx = self.position.x + i
                        dy = self.position.y + j
                        temp = Position(dx, dy)
                        if abs(i) != abs(j) and OnBoard(temp):
                            if board.squares[dx][dy].piece == None:
                                moves.append(temp.GetCopy())
                            else:
                                if board.squares[dx][dy].piece.color != self.color:
                                    captures.append(temp.GetCopy())
        return moves, captures

class Queen(Bishop, Rook, Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "q"
        self.value = 90 if color == 0 else -90
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.moves = []
        self.pieceMap = []

    def GetMoves(self, board):
        diagonal_moves, diagonal_captures = self.DiagonalMoves(board)
        r_moves, r_captures = self.VertHorzMoves(board)
        moves = diagonal_moves + r_moves
        captures = diagonal_captures + r_captures

        return moves, captures

class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "k"
        # self.value = 100 if color == 0 else -100
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.moves = []
        self.pieceMap = []
        self.value = 900 if color == 0 else -900

    def CanCastle(piece):
        return piece != None and piece.previousMove == None

    def Castle(self, board):
        castles = []
        rightRook = board.squares[7][self.position.y].piece
        leftRook = board.squares[0][self.position.y].piece

        # check if the king hasn't moved
        # check if there is no piece between the rooks
        # and the king
        if self.previousMove == None:
            # CASTLE LEFT
            if (board.squares[1][self.position.y].piece == None and board.squares[2][self.position.y].piece == None \
                and board.squares[3][self.position.y].piece == None) and King.CanCastle(leftRook):
                castles.append(Position(2, self.position.y))
            # CASTLE RIGHT
            if (board.squares[5][self.position.y].piece == None and board.squares[6][self.position.y].piece == None) \
                and King.CanCastle(rightRook):
                castles.append(Position(6, self.position.y))

        return castles

    def GetMoves(self, board):
        moves = []
        captures = []
        castles = self.Castle(board)

        for x in range(-1, 2):
            for y in range(-1, 2):
                dx = self.position.x + x
                dy = self.position.y + y
                temp = Position(dx, dy)
                if (x != 0 or y != 0) and OnBoard(temp):
                    if board.squares[dx][dy].piece == None:
                        moves.append(temp.GetCopy())
                    else:
                        if board.squares[dx][dy].piece.color != self.color:
                            captures.append(temp.GetCopy())
        moves += castles
        return moves, captures