"""
Tetromino class for managing tetromino shapes and operations.
"""
from typing import List, Dict, Tuple


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