import pygame
from .ChessPiece import ChessPiece

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_pawn.png")
        self.canEnPassant = False
        self.enPassantSquare = None

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        if(self.can_move_straight_two_squares_start_only(start_row, start_col, end_row, end_col, board) or
           self.can_move_straight_one_square(start_row, start_col, end_row, end_col, board) or
           self.can_capture_diagonally(start_row, start_col, end_row, end_col, board) or
           ((self.canEnPassant and (end_row, end_col) == self.enPassantSquare))
           ):
            return True
        else:
            return False
