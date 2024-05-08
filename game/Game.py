import pygame
from board.Chessboard import Chessboard
from pieces.King import King
from pieces.Pawn import Pawn
from pieces.Knight import Knight
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Bishop import Bishop
from .PieceMovementLogic import PieceMovementLogic

white = "white"
black = "black"

class Game():
    def __init__(self):
        self.boardObj = Chessboard()
        self.board = self.boardObj.create_board()
        self.piece_validity_check = PieceMovementLogic()
        self.selected_piece = None
        self.selected_square = None
        self.current_turn = white
        self.possible_moves = None
        self.opponent_possible_moves = None
        self.square_size = self.boardObj.square_size
        self.canEnPassant = False
    
    def handle_events(self):
        # Loop until the user clicks the close button
        running = True
        while running:
            for event in pygame.event.get():
                #Quitting
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Update dimensions if the window is resized
                    self.boardObj.resize(event)
                #Selecting a piece to move
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_next_turn(self.current_turn)

            self.boardObj.draw(self.selected_piece, self.selected_square, self.possible_moves)

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
    
    #TODO - simplify and divide this into smaller functions for readability
    def handle_next_turn(self, color):
        x, y = pygame.mouse.get_pos()
        row = y // self.square_size
        col = x // self.square_size

        self.possible_moves = self.piece_validity_check.get_valid_moves_for_every_piece(color, self.board)
        
        if self.selected_piece is None:
            self.select_piece(row, col, color)
            
        else:
            if((row, col) not in self.possible_moves[self.selected_square]):
                self.selected_piece = None
            elif (row, col) in self.possible_moves[self.selected_square]:
                if(isinstance(self.selected_piece, King)):
                    castling, side = self.selected_piece.can_castle(self.selected_square[0], self.selected_square[1], row, col, self.board)
                    if(castling):
                        if(side=="short"):
                            self.move_piece(row, 7, row, col-1)
                        elif(side=="long"):
                            self.move_piece(row,0,row,col+1)
                if(isinstance(self.selected_piece, Pawn)):
                    if(self.selected_piece.canEnPassant == True):
                        if((row,col) == self.selected_piece.enPassantSquare):
                            if(color==white):
                                self.board[row-1][col] = None
                            else:
                                self.board[row+1][col] = None                      
                    elif(abs(row - self.selected_square[0]) == 2):
                        if(self.check_adjacent_opposite_pawn(row,col+1,color)):
                            self.canEnPassant = True
                            self.board[row][col+1].canEnPassant = True
                            if(color=="white"):
                                self.board[row][col+1].enPassantSquare = (row-1,col)
                            else:
                                self.board[row][col+1].enPassantSquare = (row+1,col)
                            print(row, col)
                        if(self.check_adjacent_opposite_pawn(row,col-1,color)):
                            self.canEnPassant = True
                            self.board[row][col-1].canEnPassant = True
                            if(color=="white"):
                                self.board[row][col-1].enPassantSquare = (row-1,col)
                            else:
                                self.board[row][col-1].enPassantSquare = (row+1,col)
                    elif((color=="white" and row == 7) or (color=="black" and row == 0)):
                        buttons = self.boardObj.draw_promotion_pieces(color)
                        self.handle_promotion(buttons)

                self.move_piece(self.selected_square[0],self.selected_square[1],row,col)
                if(self.selected_piece.has_moved is False):
                    self.selected_piece.has_moved = True
                self.reset_selected_piece()
                self.boardObj.update(self.board)
                if(self.canEnPassant):
                    self.canEnPassant = False
                else:
                    self.piece_validity_check.end_en_passant(color, self.board)
                #TODO-create displays for winning/stalemate for visual indicators
                if(not self.valid_next_turn(self.opposite(color))):
                    if(self.piece_validity_check.is_checkmate(self.opposite(color), self.board)):
                            print(f"Checkmate! {self.color} wins!")
                    elif(self.piece_validity_check.is_stalemate(self.opposite(color), self.board)):
                        print("It's a draw! Stalemate!")
                    else:
                        print("Something went terribly wrong for us to end up here!")
                else:
                    self.current_turn = self.opposite(color)
                

    def opposite(self, color):
        if(color=="white"):
            return "black"
        elif(color=="black"):
            return "white"
        return "ERROR"
    
    
    def select_piece(self, row, col, color):
        if self.board[row][col] is not None and self.board[row][col].color == color:
                self.selected_piece = self.board[row][col]
                self.selected_piece.selected = True
                self.selected_square = (row, col)

    def move_piece(self, start_row, start_col, row, col):
        self.board[row][col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
    

    def reset_selected_piece(self):
        self.selected_piece.selected = False
        self.selected_piece = None
        self.possible_moves = None
        
    def check_adjacent_opposite_pawn(self, row, col, color):
        if(col>7 or col < 0):
            return False
        if(isinstance(self.board[row][col], Pawn)):
            return self.board[row][col].color == self.opposite(color)
        
    def valid_next_turn(self, color):
        if(self.piece_validity_check.has_any_moves(self.opposite(color), self.board)):
            return True
        return False
    
    def handle_promotion(self, buttons):
        running = True
        while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a button was clicked
                        for piece, rect in buttons.items():
                            if rect.collidepoint(event.pos):
                                print(f"Promote to {piece}")
                                self.promote(self.selected_piece,piece)
                                running = False

    #TODO - change the if else to switch for readability
    def promote(self, current, new):
        color = self.selected_piece.color
        if(new == "Knight"):
            self.selected_piece = Knight(color)
            self.board[self.selected_square[0]][self.selected_square[1]] = self.selected_piece
        elif(new == "Queen"):
            self.selected_piece = Queen(color)
            self.board[self.selected_square[0]][self.selected_square[1]] = self.selected_piece
        elif(new == "Rook"):
            self.selected_piece = Rook(color)
            self.board[self.selected_square[0]][self.selected_square[1]] = self.selected_piece
        elif(new == "Bishop"):
            self.selected_piece = Bishop(color)
            self.board[self.selected_square[0]][self.selected_square[1]] = self.selected_piece