import pygame
from .ChessPiece import ChessPiece
from .Rook import Rook

class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_king.png")
        
    #TODO - fix castling recursion glitch
    def is_valid_move(self,start_row, start_col, end_row, end_col, board, opposite=False):
        if(abs(start_col-end_col)<=1 and abs(start_row-end_row)<=1):
            return board[end_row][end_col] is None or board[end_row][end_col].color != self.color
        
        if(self.has_moved is False and opposite is False):
            can_castle, side = self.can_castle(start_row,start_col,end_row,end_col,board)
            if(can_castle):
                self.castle_check = True
                return True
            if(side is None):
                return False
        else:
            self.castle_check = False
        return False
    
    def can_castle(self, start_row, start_col, end_row, end_col, board):
        if not self.has_moved and abs(end_col - start_col) == 2 and start_row == end_row:
            if end_col - start_col == 2:  # Short castling
                if self.can_castle_short(start_row, start_col, board):
                    return True, "short"
            elif end_col - start_col == -2:  # Long castling
                if self.can_castle_long(start_row, start_col, board):
                    return True, "long"
        return False, None


    
    def can_castle_short(self, row, col, board):
        from game.PieceMovementLogic import PieceMovementLogic
        pieceMovementLogicObj = PieceMovementLogic()
        # Check if short castling is possible
        # Conditions: King and rook have not moved, squares between them are empty, and not in check
        if isinstance(board[row][7], Rook) and not board[row][7].has_moved:
            if all(board[row][col] is None for col in range(col + 1, 7)):
                # Check if the squares the king moves through are not attacked
                if(pieceMovementLogicObj.is_square_attacked(row, col,self.color,board)):
                   return False
                return True
        return False

    def can_castle_long(self, row, col, board):
        from game.PieceMovementLogic import PieceMovementLogic
        pieceMovementLogicObj = PieceMovementLogic()
        # Check if long castling is possible
        # Conditions: King and rook have not moved, squares between them are empty, and not in check
        if isinstance(board[row][0], Rook) and not board[row][0].has_moved:
            if all(board[row][col] is None for col in range(1, col)):
                # Check if the squares the king moves through are not attacked
                if(pieceMovementLogicObj.is_square_attacked(row, col,self.color, board)):
                   return False

                return True
        return False
    
        