"""
Game Engine class for managing the main Tetris game logic.
"""
import random
from typing import Optional, Dict, Any
from .tetromino import Tetromino, TETROMINO_SHAPES
from .game_board import GameBoard


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
        self.move_delay: float = 0.1  # Delay between horizontal moves (reduced for better responsiveness)
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
        # Disable input when game is over (Requirement 6.3)
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