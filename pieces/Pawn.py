import pygame
from .ChessPiece import ChessPiece

white = "white"
black = "black"

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_pawn.png")
        self.canEnPassant = False
        self.enPassantSquare = None

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        if(self.canEnPassant):
            if((end_row, end_col) == self.enPassantSquare):
                return True
        # Pawn moves one square forward
        if start_col == end_col and end_row - start_row == 1 and self.color == white:
            # Check if the destination square is empty
            return board[end_row][end_col] is None
        
        if start_col == end_col and end_row - start_row == -1 and self.color == black:
            # Check if the destination square is empty
            return board[end_row][end_col] is None
        # Pawn moves two squares forward from starting position
        elif start_col == end_col and abs(end_row - start_row) == 2:
            # Check if the pawn is in its starting position and the destination squares are empty
            if start_row == 1 and self.color == white:
                return board[end_row][end_col] is None and board[end_row - 1][end_col] is None
            elif start_row == 6 and self.color == black:
                return board[end_row][end_col] is None and board[end_row + 1][end_col] is None
        # Pawn captures diagonally
        elif abs(end_col - start_col) == 1 and end_row - start_row == 1 and self.color == white:
            # Check if there is an opponent's piece on the destination square
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color
        
        elif abs(end_col - start_col) == 1 and end_row - start_row == -1 and self.color == black:
            # Check if there is an opponent's piece on the destination square
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color
        
        
        return False
