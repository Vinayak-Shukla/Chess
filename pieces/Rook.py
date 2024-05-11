import pygame
from .ChessPiece import ChessPiece

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_rook.png")
        
    def is_valid_move(self,start_row, start_col, end_row, end_col, board):
        if(self.can_move_in_straight_lines(start_row, start_col, end_row, end_col, board)):
            return True
        else:
            return False