"""
Game Display class for rendering the Tetris game using Pygame.
"""
import pygame
from typing import Optional, Tuple
from .game_board import GameBoard
from .tetromino import Tetromino


class GameDisplay:
    """
    Handles all visual rendering for the Tetris game.
    """
    
    # Color definitions
    COLORS = {
        0: (0, 0, 0),        # Empty - Black
        1: (255, 255, 255),  # Placed blocks - White
        'I': (0, 255, 255),  # Cyan
        'O': (255, 255, 0),  # Yellow
        'T': (128, 0, 128),  # Purple
        'S': (0, 255, 0),    # Green
        'Z': (255, 0, 0),    # Red
        'J': (0, 0, 255),    # Blue
        'L': (255, 165, 0),  # Orange
        'background': (32, 32, 32),  # Dark gray
        'grid': (64, 64, 64),        # Gray
        'text': (255, 255, 255)      # White
    }
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """
        Initialize the display system.
        
        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
        """
        pygame.init()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
        self.block_size: int = 30
        
        # Calculate board position (centered)
        self.board_x = (screen_width - 10 * self.block_size) // 2
        self.board_y = (screen_height - 20 * self.block_size) // 2
        
        # Initialize font
        self.font = pygame.font.Font(None, 36)
        
        pygame.display.set_caption("Simple Tetris")
    
    def draw_board(self, board: GameBoard) -> None:
        """
        Draw the game board.
        
        Args:
            board: The GameBoard to render
        """
        # Draw board background
        board_rect = pygame.Rect(self.board_x - 2, self.board_y - 2, 
                               board.width * self.block_size + 4, 
                               board.height * self.block_size + 4)
        pygame.draw.rect(self.screen, self.COLORS['grid'], board_rect, 2)
        
        # Draw grid cells
        for row in range(board.height):
            for col in range(board.width):
                x = self.board_x + col * self.block_size
                y = self.board_y + row * self.block_size
                
                cell_value = board.grid[row][col]
                color = self.COLORS[cell_value]
                
                # Draw cell
                cell_rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, color, cell_rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, self.COLORS['grid'], cell_rect, 1)
    
    def draw_piece(self, piece: Tetromino) -> None:
        """
        Draw a tetromino piece.
        
        Args:
            piece: The Tetromino to render
        """
        if piece is None:
            return
        
        color = self.COLORS.get(piece.shape_type, self.COLORS[1])
        blocks = piece.get_blocks()
        
        for block_x, block_y in blocks:
            # Only draw blocks that are within the board area
            if 0 <= block_x < 10 and 0 <= block_y < 20:
                x = self.board_x + block_x * self.block_size
                y = self.board_y + block_y * self.block_size
                
                block_rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, color, block_rect)
                pygame.draw.rect(self.screen, self.COLORS['grid'], block_rect, 1)
    
    def draw_next_piece(self, piece: Tetromino) -> None:
        """
        Draw the next piece preview.
        
        Args:
            piece: The next Tetromino to render
        """
        if piece is None:
            return
        
        # Draw "Next" label
        next_text = self.font.render("Next:", True, self.COLORS['text'])
        next_x = self.board_x + 12 * self.block_size
        next_y = self.board_y + 2 * self.block_size
        self.screen.blit(next_text, (next_x, next_y))
        
        # Draw next piece
        color = self.COLORS.get(piece.shape_type, self.COLORS[1])
        current_shape = piece.get_rotated_shape()
        
        preview_x = next_x
        preview_y = next_y + 40
        
        for row_idx, row in enumerate(current_shape):
            for col_idx, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    x = preview_x + col_idx * (self.block_size // 2)
                    y = preview_y + row_idx * (self.block_size // 2)
                    
                    block_rect = pygame.Rect(x, y, self.block_size // 2, self.block_size // 2)
                    pygame.draw.rect(self.screen, color, block_rect)
                    pygame.draw.rect(self.screen, self.COLORS['grid'], block_rect, 1)
    
    def draw_game_over(self) -> None:
        """
        Draw the game over screen.
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.font.render("GAME OVER", True, self.COLORS['text'])
        text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(game_over_text, text_rect)
        
        # Draw restart instruction
        restart_text = self.font.render("Press R to restart", True, self.COLORS['text'])
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_score(self, score: int, lines_cleared: int) -> None:
        """
        Draw the current score and lines cleared.
        
        Args:
            score: Current score
            lines_cleared: Number of lines cleared
        """
        score_text = self.font.render(f"Score: {score}", True, self.COLORS['text'])
        lines_text = self.font.render(f"Lines: {lines_cleared}", True, self.COLORS['text'])
        
        score_x = self.board_x + 12 * self.block_size
        score_y = self.board_y + 8 * self.block_size
        
        self.screen.blit(score_text, (score_x, score_y))
        self.screen.blit(lines_text, (score_x, score_y + 40))
    
    def clear_screen(self) -> None:
        """
        Clear the screen with background color.
        """
        self.screen.fill(self.COLORS['background'])
    
    def update_display(self) -> None:
        """
        Update the display (flip buffers).
        """
        pygame.display.flip()
    
    def quit(self) -> None:
        """
        Clean up pygame resources.
        """
        pygame.quit()