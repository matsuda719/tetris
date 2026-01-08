"""
Game Board class for managing the Tetris playing field.
"""
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from tetromino import Tetromino


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
    
    def is_valid_position(self, piece: 'Tetromino', x: int, y: int) -> bool:
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
    
    def can_move_piece(self, piece: 'Tetromino', dx: int, dy: int) -> bool:
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
    
    def can_rotate_piece(self, piece: 'Tetromino') -> bool:
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
    
    def place_piece(self, piece: 'Tetromino', x: int, y: int) -> None:
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
    
    def check_collision_at(self, piece: 'Tetromino', x: int, y: int) -> str:
        """
        Check what type of collision would occur at the given position.
        
        Args:
            piece: The tetromino to check
            x: X position to check
            y: Y position to check
            
        Returns:
            'none' if no collision, 'boundary' for boundary collision, 
            'block' for block collision
        """
        # Temporarily move piece to check position
        original_x, original_y = piece.x, piece.y
        piece.x, piece.y = x, y
        
        try:
            blocks = piece.get_blocks()
            
            for block_x, block_y in blocks:
                # Check boundaries first
                if not self._is_within_boundaries(block_x, block_y):
                    return 'boundary'
                
                # Check collision with existing blocks
                if self.grid[block_y][block_x] != 0:
                    return 'block'
            
            return 'none'
        finally:
            # Restore original position
            piece.x, piece.y = original_x, original_y
    
    def is_position_occupied(self, x: int, y: int) -> bool:
        """
        Check if a specific grid position is occupied.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if occupied, False if empty or out of bounds
        """
        if not self._is_within_boundaries(x, y):
            return False
        
        return self.grid[y][x] != 0