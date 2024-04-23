class PieceMovementLogic():

    def get_valid_moves_for_every_piece(self, color, board):
        valid_moves = {}
        for row in range(8):
            for col in range(8):
                if(board[row][col] is not None and board[row][col].color == color):
                    moves = self.get_all_valid_moves_for_a_piece(row, col, board)
                    valid_moves[(row, col)] = moves

        return valid_moves
    
    def get_all_valid_moves_for_a_piece(self, row, col, board):

        moves = self.get_all_possible_moves_for_a_piece(row, col, board)
        color = board[row][col].color
        piece = board[row][col]
        actual_moves = []
        for move_row, move_col in moves:
                temp_piece = board[move_row][move_col]
                board[move_row][move_col] = piece
                board[row][col] = None
                if(not self.is_king_in_check(color, board)):
                    actual_moves.append((move_row, move_col))
                board[row][col] = piece
                board[move_row][move_col] = temp_piece
        return actual_moves

    def get_all_possible_moves_for_a_piece(self, row, col, board):
        moves = []
        piece = board[row][col]
        for end_row in range(8):
            for end_col in range(8):
                if(piece.is_valid_move(row, col, end_row, end_col, board)):
                    moves.append((end_row, end_col))
        return moves
    
    def is_king_in_check(self, color, board):
        from pieces.King import King

        king_row, king_col = (-1, -1)
        for row in range(8):
            for col in range(8):
                if(isinstance(board[row][col], King) and board[row][col].color == color):
                    king_row = row
                    king_col = col
        for row in range(8):
            for col in range(8):
                if(board[row][col] is not None and board[row][col].color != color):
                    if(board[row][col].is_valid_move(row, col, king_row, king_col, board)):
                        return True
        return False
    
    def has_any_moves(self, color, board):
        moves = self.get_valid_moves_for_every_piece(color, board)
        return any(moves.values())
    def is_checkmate(self, color, board):
        return self.is_king_in_check(color, board) and not self.has_any_moves(color,board)
    
    def is_stalemate(self, color, board):
        return not self.is_king_in_check(color,board) and not self.has_any_moves(color, board)
        
    
    
    def is_square_attacked(self, row, col, color, board):
        moves = self.get_valid_moves_for_every_piece(self.opposite(color), board)
        return (row,col) in moves.values()
    
    def opposite(self, color):
        if(color=="white"):
            return "black"
        elif(color=="black"):
            return "white"
        return "ERROR"
    
    def end_en_passant(self, color, board):
        from pieces.Pawn import Pawn
        
        for row in range(8):
            for col in range(8):
                if(isinstance(board[row][col], Pawn)):
                    board[row][col].canEnPassant=False
                    board[row][col].enPassantSquare=None