import pygame
from .ChessPiece import ChessPiece

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_knight.png")

    def is_valid_move(self,start_row, start_col, end_row, end_col, board):
        if(abs(start_row-end_row)==2):
            if(abs(end_col-start_col)==1):
                if(board[end_row][end_col] is not None):
                    return board[end_row][end_col].color != self.color
                return True
        elif(abs(start_row-end_row)==1):
            if(abs(end_col-start_col)==2):
                if(board[end_row][end_col] is not None):
                    return board[end_row][end_col].color != self.color
                return True
        return False
