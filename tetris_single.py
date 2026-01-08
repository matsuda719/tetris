#!/usr/bin/env python3
"""
Simple Tetris Game - Single File Version
学習用の簡単なTetrisゲームをPythonとPygameで実装（1ファイル版）

操作方法:
- ←/→: 左右移動
- ↓: 高速落下
- ↑: 回転
- R: ゲームオーバー時にリスタート

依存関係: pygame
インストール: pip install pygame
実行: python tetris_single.py
"""
import pygame
import random
import sys
from typing import List, Dict, Tuple, Optional, Any


# =============================================================================
# Tetromino Shapes and Class
# =============================================================================

# Tetromino shape definitions
TETROMINO_SHAPES: Dict[str, List[List[str]]] = {
    'I': [
        ['....', 'IIII', '....', '....'],
        ['..I.', '..I.', '..I.', '..I.']
    ],
    'O': [
        ['OO', 'OO']
    ],
    'T': [
        ['.T.', 'TTT', '...'],
        ['.T.', '.TT', '.T.'],
        ['...', 'TTT', '.T.'],
        ['.T.', 'TT.', '.T.']
    ],
    'S': [
        ['.SS', 'SS.', '...'],
        ['.S.', '.SS', '..S']
    ],
    'Z': [
        ['ZZ.', '.ZZ', '...'],
        ['..Z', '.ZZ', '.Z.']
    ],
    'J': [
        ['J..', 'JJJ', '...'],
        ['.JJ', '.J.', '.J.'],
        ['...', 'JJJ', '..J'],
        ['.J.', '.J.', 'JJ.']
    ],
    'L': [
        ['..L', 'LLL', '...'],
        ['.L.', '.L.', '.LL'],
        ['...', 'LLL', 'L..'],
        ['LL.', '.L.', '.L.']
    ]
}


class Tetromino:
    """
    Represents a Tetromino piece with shape, position, and rotation.
    """
    
    def __init__(self, shape_type: str):
        """
        Initialize a Tetromino with the specified shape type.
        
        Args:
            shape_type: One of 'I', 'O', 'T', 'S', 'Z', 'J', 'L'
        """
        if shape_type not in TETROMINO_SHAPES:
            raise ValueError(f"Invalid shape type: {shape_type}")
            
        self.shape_type: str = shape_type
        self.shape: List[List[str]] = TETROMINO_SHAPES[shape_type]
        self.x: int = 0
        self.y: int = 0
        self.rotation: int = 0
    
    def rotate(self) -> None:
        """
        Rotate the tetromino clockwise by 90 degrees.
        """
        max_rotations = len(self.shape)
        self.rotation = (self.rotation + 1) % max_rotations
    
    def move(self, dx: int, dy: int) -> None:
        """
        Move the tetromino by the specified offset.
        
        Args:
            dx: Horizontal movement (positive = right)
            dy: Vertical movement (positive = down)
        """
        self.x += dx
        self.y += dy
    
    def get_rotated_shape(self) -> List[str]:
        """
        Get the current rotated shape of the tetromino.
        
        Returns:
            List of strings representing the current shape
        """
        return self.shape[self.rotation]
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """
        Get the absolute positions of all blocks in this tetromino.
        
        Returns:
            List of (x, y) tuples representing block positions
        """
        blocks = []
        current_shape = self.get_rotated_shape()
        
        for row_idx, row in enumerate(current_shape):
            for col_idx, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    blocks.append((self.x + col_idx, self.y + row_idx))
        
        return blocks


# =============================================================================
# Game Board Class
# =============================================================================

class GameBoard:
    """
    Represents the Tetris game board (10x20 grid).
    """
    
    def __init__(self, width: int = 10, height: int = 20):
        """
        Initialize the game board.
        
        Args:
            width: Board width in blocks (default: 10)
            height: Board height in blocks (default: 20)
        """
        self.width: int = width
        self.height: int = height
        self.grid: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, piece: Tetromino, x: int, y: int) -> bool:
        """
        Check if a tetromino can be placed at the specified position.
        
        Args:
            piece: The tetromino to check
            x: X position to check
            y: Y position to check
            
        Returns:
            True if the position is valid, False otherwise
        """
        # Temporarily move piece to check position
        original_x, original_y = piece.x, piece.y
        piece.x, piece.y = x, y
        
        try:
            blocks = piece.get_blocks()
            
            for block_x, block_y in blocks:
                # Check boundaries
                if not self._is_within_boundaries(block_x, block_y):
                    return False
                
                # Check collision with existing blocks
                if self._has_block_collision(block_x, block_y):
                    return False
            
            return True
        finally:
            # Restore original position
            piece.x, piece.y = original_x, original_y
    
    def _is_within_boundaries(self, x: int, y: int) -> bool:
        """
        Check if the given coordinates are within the board boundaries.
        
        Args:
            x: X coordinate to check
            y: Y coordinate to check
            
        Returns:
            True if within boundaries, False otherwise
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def _has_block_collision(self, x: int, y: int) -> bool:
        """
        Check if there's a collision with an existing block at the given position.
        
        Args:
            x: X coordinate to check
            y: Y coordinate to check
            
        Returns:
            True if there's a collision, False otherwise
        """
        if not self._is_within_boundaries(x, y):
            return True  # Out of bounds is considered a collision
        
        return self.grid[y][x] != 0
    
    def can_move_piece(self, piece: Tetromino, dx: int, dy: int) -> bool:
        """
        Check if a piece can be moved by the specified offset.
        
        Args:
            piece: The tetromino to check
            dx: Horizontal movement offset
            dy: Vertical movement offset
            
        Returns:
            True if the move is valid, False otherwise
        """
        new_x = piece.x + dx
        new_y = piece.y + dy
        return self.is_valid_position(piece, new_x, new_y)
    
    def can_rotate_piece(self, piece: Tetromino) -> bool:
        """
        Check if a piece can be rotated at its current position.
        
        Args:
            piece: The tetromino to check
            
        Returns:
            True if rotation is valid, False otherwise
        """
        # Save current rotation
        original_rotation = piece.rotation
        
        try:
            # Try rotation
            max_rotations = len(piece.shape)
            test_rotation = (piece.rotation + 1) % max_rotations
            piece.rotation = test_rotation
            
            # Check if rotated position is valid
            return self.is_valid_position(piece, piece.x, piece.y)
        finally:
            # Restore original rotation
            piece.rotation = original_rotation
    
    def place_piece(self, piece: Tetromino, x: int, y: int) -> None:
        """
        Place a tetromino on the board at the specified position.
        
        Args:
            piece: The tetromino to place
            x: X position to place the piece
            y: Y position to place the piece
        """
        # Temporarily move piece to placement position
        original_x, original_y = piece.x, piece.y
        piece.x, piece.y = x, y
        
        try:
            blocks = piece.get_blocks()
            
            for block_x, block_y in blocks:
                if 0 <= block_x < self.width and 0 <= block_y < self.height:
                    # Use a non-zero value to represent occupied cells
                    self.grid[block_y][block_x] = 1
        finally:
            # Restore original position
            piece.x, piece.y = original_x, original_y
    
    def clear_lines(self) -> int:
        """
        Clear all complete lines and return the number of lines cleared.
        
        Returns:
            Number of lines cleared
        """
        lines_cleared = 0
        row = self.height - 1
        
        while row >= 0:
            if self.is_line_full(row):
                # Remove the full line
                del self.grid[row]
                # Add a new empty line at the top
                self.grid.insert(0, [0 for _ in range(self.width)])
                lines_cleared += 1
                # Don't decrement row since we removed a line
            else:
                row -= 1
        
        return lines_cleared
    
    def is_line_full(self, row: int) -> bool:
        """
        Check if a specific row is completely filled.
        
        Args:
            row: Row index to check
            
        Returns:
            True if the row is full, False otherwise
        """
        if row < 0 or row >= self.height:
            return False
        
        return all(cell != 0 for cell in self.grid[row])
    
    def get_grid_copy(self) -> List[List[int]]:
        """
        Get a copy of the current grid state.
        
        Returns:
            Deep copy of the grid
        """
        return [row[:] for row in self.grid]


# =============================================================================
# Game Engine Class
# =============================================================================

class GameEngine:
    """
    Main game engine that controls the Tetris game logic.
    """
    
    def __init__(self):
        """
        Initialize the game engine.
        """
        self.board: GameBoard = GameBoard()
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.game_over: bool = False
        self.fall_time: float = 0.0
        self.fall_interval: float = 1.0  # 1 second between automatic falls
        self.score: int = 0
        self.lines_cleared: int = 0
        
        # Input handling timing
        self.move_delay: float = 0.1  # Delay between horizontal moves
        self.move_time: float = 0.0
        self.last_keys: Dict[str, bool] = {
            'left': False,
            'right': False,
            'down': False,
            'up': False
        }
        
        # Initialize with first pieces
        self.spawn_new_piece()
        self.next_piece = self._generate_random_piece()
    
    def update(self, dt: float) -> None:
        """
        Update the game state.
        
        Args:
            dt: Delta time since last update in seconds
        """
        if self.game_over:
            return
        
        self.fall_time += dt
        self.move_time += dt
        
        # Automatic fall
        if self.fall_time >= self.fall_interval:
            self._try_move_current_piece(0, 1)
            self.fall_time = 0.0
    
    def handle_input(self, keys: Dict[str, bool]) -> None:
        """
        Handle player input with proper timing controls.
        
        Args:
            keys: Dictionary of key states
        """
        # Disable input when game is over
        if self.game_over:
            return
        
        # Handle rotation (only on key press, not while held)
        if keys.get('up', False) and not self.last_keys.get('up', False):
            self._try_rotate_current_piece()
        
        # Handle horizontal movement with timing
        if self.move_time >= self.move_delay:
            if keys.get('left', False):
                self._try_move_current_piece(-1, 0)
                self.move_time = 0.0
            elif keys.get('right', False):
                self._try_move_current_piece(1, 0)
                self.move_time = 0.0
        
        # Handle down movement (faster than automatic fall)
        if keys.get('down', False):
            if self.move_time >= self.move_delay * 0.3:  # Faster down movement
                self._try_move_current_piece(0, 1)
                self.move_time = 0.0
        
        # Store current key states for next frame
        self.last_keys = keys.copy()
    
    def spawn_new_piece(self) -> None:
        """
        Spawn a new tetromino at the top of the board.
        """
        if self.next_piece is not None:
            self.current_piece = self.next_piece
        else:
            self.current_piece = self._generate_random_piece()
        
        # Position at top center of board
        self.current_piece.x = self.board.width // 2 - 2
        self.current_piece.y = 0
        
        # Generate next piece
        self.next_piece = self._generate_random_piece()
        
        # Check for game over
        if not self.board.is_valid_position(self.current_piece, 
                                          self.current_piece.x, 
                                          self.current_piece.y):
            self.game_over = True
    
    def check_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Returns:
            True if game is over, False otherwise
        """
        return self.game_over
    
    def _generate_random_piece(self) -> Tetromino:
        """
        Generate a random tetromino.
        
        Returns:
            A new random Tetromino instance
        """
        shape_type = random.choice(list(TETROMINO_SHAPES.keys()))
        return Tetromino(shape_type)
    
    def _try_move_current_piece(self, dx: int, dy: int) -> bool:
        """
        Try to move the current piece by the specified offset.
        
        Args:
            dx: Horizontal movement
            dy: Vertical movement
            
        Returns:
            True if move was successful, False otherwise
        """
        if self.current_piece is None:
            return False
        
        # Use enhanced collision detection
        if self.board.can_move_piece(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True
        else:
            # If moving down failed, place the piece
            if dy > 0:
                self._place_current_piece()
            return False
    
    def _try_rotate_current_piece(self) -> bool:
        """
        Try to rotate the current piece clockwise.
        
        Returns:
            True if rotation was successful, False otherwise
        """
        if self.current_piece is None:
            return False
        
        # Use enhanced collision detection
        if self.board.can_rotate_piece(self.current_piece):
            self.current_piece.rotate()
            return True
        else:
            return False
    
    def _place_current_piece(self) -> None:
        """
        Place the current piece on the board and handle line clearing.
        """
        if self.current_piece is None:
            return
        
        # Place piece on board
        self.board.place_piece(self.current_piece, 
                             self.current_piece.x, 
                             self.current_piece.y)
        
        # Clear completed lines
        lines_cleared = self.board.clear_lines()
        self.lines_cleared += lines_cleared
        self.score += lines_cleared * 100  # Simple scoring
        
        # Spawn new piece
        self.spawn_new_piece()
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current game state.
        
        Returns:
            Dictionary containing current game state
        """
        return {
            'board': self.board.get_grid_copy(),
            'current_piece': self.current_piece,
            'next_piece': self.next_piece,
            'score': self.score,
            'lines_cleared': self.lines_cleared,
            'game_over': self.game_over
        }


# =============================================================================
# Game Display Class
# =============================================================================

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


# =============================================================================
# Main Game Loop
# =============================================================================

def main():
    """
    Main game loop.
    """
    # Initialize game components
    game_engine = GameEngine()
    game_display = GameDisplay()
    
    # Game loop variables
    clock = pygame.time.Clock()
    running = True
    
    # Input tracking for continuous movement
    keys_held = {
        'left': False,
        'right': False,
        'down': False,
        'up': False
    }
    
    try:
        while running:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    # Handle key press events - only set flags, don't move immediately
                    if event.key == pygame.K_LEFT:
                        keys_held['left'] = True
                    elif event.key == pygame.K_RIGHT:
                        keys_held['right'] = True
                    elif event.key == pygame.K_DOWN:
                        keys_held['down'] = True
                    elif event.key == pygame.K_UP:
                        keys_held['up'] = True
                    elif event.key == pygame.K_r and game_engine.game_over:
                        # Restart game
                        game_engine = GameEngine()
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        keys_held['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        keys_held['right'] = False
                    elif event.key == pygame.K_DOWN:
                        keys_held['down'] = False
                    elif event.key == pygame.K_UP:
                        keys_held['up'] = False
            
            # Update game logic
            game_engine.update(dt)
            
            # Handle continuous input (for held keys)
            game_engine.handle_input(keys_held)
            
            # Render
            game_display.clear_screen()
            game_display.draw_board(game_engine.board)
            game_display.draw_piece(game_engine.current_piece)
            game_display.draw_next_piece(game_engine.next_piece)
            
            game_state = game_engine.get_game_state()
            game_display.draw_score(game_state['score'], game_state['lines_cleared'])
            
            if game_engine.game_over:
                game_display.draw_game_over()
            
            game_display.update_display()
    
    finally:
        game_display.quit()
        sys.exit()


if __name__ == "__main__":
    main()