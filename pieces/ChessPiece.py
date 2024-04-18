import pygame

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
