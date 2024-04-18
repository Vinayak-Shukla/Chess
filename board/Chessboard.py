import pygame
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Knight import Knight
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Bishop import Bishop

WHITE = (88, 42, 13)
BLACK = (240, 20, 63)
white = "white"
black = "black"

class Chessboard:
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.square_size = width // 8
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Chessboard")
        self.board = self.create_board()
        self.selected_piece = None
        self.selected_square = None
        self.current_turn = white  # Start with white's turn
        self.possible_moves = None

    def create_board(self):
        board = []
        # Create an empty board
        for _ in range(8):
            row = [None] * 8
            board.append(row)
        
        # Place pieces on the board
        board[1] = [Pawn(white) for _ in range(8)]
        board[6] = [Pawn(black) for _ in range(8)]
        board[0] = [Rook(white), Knight(white), Bishop(white), Queen(white), King(white), Bishop(white), Knight(white), Rook(white)]
        board[7] = [Rook(black), Knight(black), Bishop(black), Queen(black), King(black), Bishop(black), Knight(black), Rook(black)]
        return board

    def draw(self):
        # Draw the chessboard
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

        # Draw the pieces
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    piece.draw(self.screen, col * self.square_size, row * self.square_size, self.square_size)

        if self.selected_piece is not None:
            row, col = self.selected_square
            pygame.draw.rect(self.screen, (255, 255, 0), (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 4)
            if self.possible_moves is not None:
                for row, col in self.possible_moves[self.selected_square]:
                    pygame.draw.circle(self.screen, (120,0,120), (col * self.square_size + self.square_size//2, row * self.square_size + self.square_size//2), 25)


    
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
                    self.resize(event)
                #Selecting a piece to move
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_next_turn(self.current_turn)

            self.draw()

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
    
    def handle_next_turn(self, color):
        x, y = pygame.mouse.get_pos()
        row = y // self.square_size
        col = x // self.square_size

        self.possible_moves = self.get_valid_moves_for_every_piece(color)
        if self.selected_piece is None:
            print("in select")
            if self.board[row][col] is not None and self.board[row][col].color == color:
                self.selected_piece = self.board[row][col]
                self.selected_piece.selected = True
                self.selected_square = (row, col)
                print(self.possible_moves[self.selected_square])
        else:
            if((row, col) not in self.possible_moves[self.selected_square]):
                self.selected_piece = None
            elif (row, col) in self.possible_moves[self.selected_square]: 
                if(self.selected_piece.has_moved is False):
                    self.selected_piece.has_moved = True
                if(isinstance(self.selected_piece, King)):
                    if(self.selected_piece.has_moved is False):
                        self.board[row][col-1] = self.board[row][7]   
                        self.board[row][7] = None            
                        self.selected_piece.has_moved = True
                self.board[row][col] = self.selected_piece
                self.board[self.selected_square[0]][self.selected_square[1]] = None
                self.selected_piece.selected = False
                self.selected_piece = None
                self.possible_moves = None
                if(color==white):
                    if((not self.is_king_in_check(black)) or (self.is_king_in_check(black) and not self.is_checkmate(black))):
                        self.current_turn = black
                    else:
                        print("Checkmate! White wins!")
                else:
                    if((not self.is_king_in_check(white)) or (self.is_king_in_check(white) and not self.is_checkmate(white))):
                        self.current_turn = white
                    else:
                        print("Checkmate! Black wins!")

    def is_king_in_check(self, color):
        king_row, king_col = (-1, -1)
        for row in range(8):
            for col in range(8):
                if(isinstance(self.board[row][col], King) and self.board[row][col].color == color):
                    king_row = row
                    king_col = col
        for row in range(8):
            for col in range(8):
                if(self.board[row][col] is not None and self.board[row][col].color != color):
                    if(self.board[row][col].is_valid_move(row, col, king_row, king_col, self.board)):
                        return True
        return False
    
    def get_valid_moves_for_every_piece(self, color):
        valid_moves = {}
        for row in range(8):
            for col in range(8):
                if(self.board[row][col] is not None and self.board[row][col].color == color):
                    moves = self.get_all_valid_moves_for_a_piece(row, col)
                    valid_moves[(row, col)] = moves
        return valid_moves
    
    def get_all_valid_moves_for_a_piece(self, row, col):

        moves = self.get_all_possible_moves_for_a_piece(row, col)
        color = self.board[row][col].color
        piece = self.board[row][col]
        actual_moves = []
        for move_row, move_col in moves:
                temp_piece = self.board[move_row][move_col]
                self.board[move_row][move_col] = piece
                self.board[row][col] = None
                if(not self.is_king_in_check(color)):
                    actual_moves.append((move_row, move_col))
                self.board[row][col] = piece
                self.board[move_row][move_col] = temp_piece
        return actual_moves

    def get_all_possible_moves_for_a_piece(self, row, col):
        moves = []
        piece = self.board[row][col]
        for end_row in range(8):
            for end_col in range(8):
                if(piece.is_valid_move(row, col, end_row, end_col, self.board)):
                    moves.append((end_row, end_col))
        return moves
    
    def is_checkmate(self, color):
        moves = self.get_valid_moves_for_every_piece(color)
        if(not any(moves.values())):
                return True
        return False
    
    def resize(self, event):
        self.width, self.height = event.size
        self.square_size = min(self.width, self.height) // 8
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
