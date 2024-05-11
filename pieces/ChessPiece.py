import pygame

white = "white"
black = "black"

class ChessPiece:
    def __init__(self, color):
        self.color = color
        self.image = None  # Placeholder for piece image
        self.has_moved = False
    
    def draw(self, screen, x, y, square_size):
        # Draw the piece on the chessboard
        if self.image is not None:
            piece_rect = self.image.get_rect()
            piece_rect.center = (x + square_size // 2, y + square_size // 2)
            screen.blit(self.image, piece_rect)
        else:
            pygame.draw.circle(screen, self.color, (x + square_size // 2, y + square_size // 2), square_size // 3)
    
    def can_move_diagonally(self, start_row, start_col, end_row, end_col, board):
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
        
    def can_move_in_straight_lines(self,start_row, start_col, end_row, end_col, board):
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
    
    def can_move_in_L_shape(self, start_row, start_col, end_row, end_col, board):
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
    
    def can_move_straight_one_square(self, start_row, start_col, end_row, end_col, board):
        if start_col == end_col and end_row - start_row == 1 and self.color == white:
            return board[end_row][end_col] is None
        elif start_col == end_col and end_row - start_row == -1 and self.color == black:
            return board[end_row][end_col] is None
        return False
        
    def can_move_straight_two_squares_start_only(self, start_row, start_col, end_row, end_col, board):
        if start_col == end_col and abs(end_row - start_row) == 2:
            if start_row == 1 and self.color == white:
                return board[end_row][end_col] is None and board[end_row - 1][end_col] is None
            elif start_row == 6 and self.color == black:
                return board[end_row][end_col] is None and board[end_row + 1][end_col] is None
        return False
    
    def can_capture_diagonally(self, start_row, start_col, end_row, end_col, board):
        if abs(end_col - start_col) == 1 and end_row - start_row == 1 and self.color == white:
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color
        elif abs(end_col - start_col) == 1 and end_row - start_row == -1 and self.color == black:
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color
        return False
        
    def can_move_to_adjacent_square(self, start_row, start_col, end_row, end_col, board):
        if(abs(start_col-end_col)<=1 and abs(start_row-end_row)<=1):
            return board[end_row][end_col] is None or board[end_row][end_col].color != self.color
        
