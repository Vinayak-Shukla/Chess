import pygame
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Knight import Knight
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Bishop import Bishop
import time

WHITE = (88, 42, 13)
BLACK = (240, 20, 63)
white = "white"
black = "black"

class Chessboard:
    def __init__(self, width=800, height=800):
        pygame.init()
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
    
    
    def update(self, board):
        self.board = board

    def draw(self, selected_piece=None, selected_square=None, possible_moves=None):
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

        if selected_piece is not None:
            row, col = selected_square
            pygame.draw.rect(self.screen, (255, 255, 0), (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 4)
            if possible_moves is not None:
                for row, col in possible_moves[selected_square]:
                    pygame.draw.circle(self.screen, (120,0,120), (col * self.square_size + self.square_size//2, row * self.square_size + self.square_size//2), 25)

    def resize(self, event):
        self.width, self.height = event.size
        self.square_size = min(self.width, self.height) // 8
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        
        
                
