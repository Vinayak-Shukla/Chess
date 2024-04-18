import pygame
from .ChessPiece import ChessPiece

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(f"images/{color}_bishop.png")

    def is_valid_move(self,start_row, start_col, end_row, end_col, board):
        if(abs(start_col-end_col)==abs(start_row-end_row)):
            row_increment = 1 if end_row > start_row else -1
            col_increment = 1 if end_col > start_col else -1
            row, col = start_row + row_increment, start_col + col_increment
            while row != end_row and col != end_col:
                if board[row][col] is not None:
                    return False  # There is a piece blocking the path
                row += row_increment
                col += col_increment
            # Check if the destination square is empty or has an opponent's piece
            return board[end_row][end_col] is None or board[end_row][end_col].color != self.color
