import pygame
from .ChessPiece import ChessPiece

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_rook.png")
        
    def is_valid_move(self,start_row, start_col, end_row, end_col, board):
        if(start_col == end_col):
            for i in range(min(end_row,start_row)+1, max(start_row, end_row)):
                if(board[i][start_col] is not None ):
                    return False
            if(board[end_row][end_col] is not None):
                return board[end_row][end_col].color != self.color
            return True
        elif(start_row==end_row):
            for i in range(min(end_col,start_col)+1,max(start_col,end_col)):
                if(board[start_row][i] is not None):
                    return False
            if(board[end_row][end_col] is not None):
                return board[end_row][end_col].color != self.color
            return True
        return False
