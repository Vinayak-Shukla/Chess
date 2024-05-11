import pygame
from .ChessPiece import ChessPiece

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_queen.png")

    def is_valid_move(self,start_row, start_col, end_row, end_col, board):
        if(self.can_move_diagonally(start_row, start_col, end_row, end_col, board) 
           or self.can_move_in_straight_lines(start_row, start_col, end_row, end_col, board)):
            return True
        else:
            return False