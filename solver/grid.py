"""
Grid Structure Module

Manages crossword grid structure, including:
- Cell indices and layout
- Clue positions
- Border calculations
"""

from typing import Dict, List, Tuple, Set


class GridManager:
    """Manages grid structure and calculations for crossword puzzles."""
    
    def __init__(self, grid_size: int = 8):
        """
        Initialize grid manager.
        
        Args:
            grid_size: Number of cells per row/column (default 8x8 grid)
        """
        self.grid_size = grid_size
        self.total_cells = grid_size * grid_size
    
    def cell_to_row_col(self, cell_index: int) -> Tuple[int, int]:
        """Convert cell index to (row, col) coordinates."""
        return (cell_index // self.grid_size, cell_index % self.grid_size)
    
    def row_col_to_cell(self, row: int, col: int) -> int:
        """Convert (row, col) coordinates to cell index."""
        return row * self.grid_size + col
    
    def is_valid_cell(self, cell_index: int) -> bool:
        """Check if cell index is valid."""
        return 0 <= cell_index < self.total_cells


def get_grid_structure() -> List[Tuple[int, str, Tuple[int, ...]]]:
    """
    Get the grid structure for Listener 4869 puzzle.
    
    Returns:
        List of tuples: (clue_number, direction, cell_indices)
        
    Note:
        This is currently hardcoded for Listener 4869.
        In future versions, this will be loaded from a configuration file
        or provided by user input from photo markup.
    """
    return [
        (1, "ACROSS", (0, 1, 2, 3)),
        (1, "DOWN", (0, 8, 16, 24)),
        (2, "DOWN", (1, 9)),
        (3, "DOWN", (2, 10, 18, 26)),
        (4, "ACROSS", (4, 5, 6, 7)),
        (5, "DOWN", (5, 13, 21, 29)),
        (6, "DOWN", (7, 15, 23, 31)),
        (7, "DOWN", (11, 19, 27, 35, 43, 51)),
        (8, "DOWN", (12, 20, 28, 36, 44, 52)),
        (9, "ACROSS", (14, 15)),
        (10, "ACROSS", (16, 17, 18, 19)),
        (11, "ACROSS", (20, 21, 22, 23)),
        (12, "ACROSS", (25, 26, 27, 28, 29, 30)),
        (13, "DOWN", (32, 40, 48, 56)),
        (14, "ACROSS", (33, 34, 35, 36, 37, 38)),
        (15, "DOWN", (34, 42, 50, 58)),
        (16, "DOWN", (37, 45, 53, 61)),
        (17, "DOWN", (39, 47, 55, 63)),
        (18, "ACROSS", (40, 41, 42, 43)),
        (19, "ACROSS", (44, 45, 46, 47)),
        (20, "ACROSS", (48, 49)),
        (21, "DOWN", (54, 62)),
        (22, "ACROSS", (56, 57, 58, 59)),
        (23, "ACROSS", (60, 61, 62, 63))
    ]


def calculate_grid_borders(grid_clues: List[Tuple[int, str, Tuple[int, ...]]]) -> Dict[str, Set[int]]:
    """
    Calculate thick border positions based on clue structure.
    
    Args:
        grid_clues: List of (number, direction, cell_indices) tuples
        
    Returns:
        Dictionary with keys 'thick_right', 'thick_bottom', 'thick_left', 'thick_top'
        mapping to sets of cell indices that should have thick borders
        
    Example:
        >>> clues = get_grid_structure()
        >>> borders = calculate_grid_borders(clues)
        >>> 3 in borders['thick_right']  # Cell 3 has thick right border
        True
    """
    # Initialize border sets
    thick_right_cells = set()
    thick_bottom_cells = set()
    thick_left_cells = set()
    thick_top_cells = set()
    
    # Process ACROSS clues to find thick right borders
    across_clues = [clue for clue in grid_clues if clue[1] == 'ACROSS']
    for number, direction, cell_indices in across_clues:
        if len(cell_indices) > 0:
            last_cell = cell_indices[-1]
            # Add right border unless it's at the right edge or special case
            if last_cell % 8 != 7 and last_cell not in {30, 38}:
                thick_right_cells.add(last_cell)
    
    # Process DOWN clues to find thick bottom borders
    down_clues = [clue for clue in grid_clues if clue[1] == 'DOWN']
    for number, direction, cell_indices in down_clues:
        if len(cell_indices) > 0:
            last_cell = cell_indices[-1]
            # Add bottom border unless it's at the bottom edge
            if last_cell < 56:
                thick_bottom_cells.add(last_cell)
    
    # Handle isolated cells (cells surrounded by thick borders)
    _add_isolated_cell_borders(9, thick_left_cells, thick_right_cells, thick_bottom_cells, thick_top_cells)
    _add_isolated_cell_borders(14, thick_left_cells, thick_right_cells, thick_bottom_cells, thick_top_cells)
    _add_isolated_cell_borders(49, thick_left_cells, thick_right_cells, thick_bottom_cells, thick_top_cells)
    
    # Add specific borders for cell pair separations
    _add_cell_pair_borders(
        thick_left_cells, thick_right_cells, thick_bottom_cells, thick_top_cells
    )
    
    return {
        'thick_right': thick_right_cells,
        'thick_bottom': thick_bottom_cells,
        'thick_left': thick_left_cells,
        'thick_top': thick_top_cells
    }


def _add_isolated_cell_borders(
    cell_index: int,
    thick_left: Set[int],
    thick_right: Set[int],
    thick_bottom: Set[int],
    thick_top: Set[int]
) -> None:
    """Add borders for isolated cells based on their specific requirements."""
    if cell_index == 9:
        thick_left.add(9)
        thick_right.add(9)
        thick_bottom.add(9)
    elif cell_index == 14:
        thick_left.add(14)
        thick_top.add(14)
        thick_bottom.add(14)
    elif cell_index == 49:
        thick_top.add(49)
        thick_bottom.add(49)
        thick_right.add(49)


def _add_cell_pair_borders(
    thick_left: Set[int],
    thick_right: Set[int],
    thick_bottom: Set[int],
    thick_top: Set[int]
) -> None:
    """Add borders for cell pairs that need special separation."""
    # Cells 11 and 12 separation
    thick_top.add(11)
    thick_left.add(11)
    thick_right.add(11)
    thick_top.add(12)
    thick_right.add(12)
    
    # Cells 30 and 38 separation
    thick_right.add(30)
    thick_top.add(30)
    thick_right.add(38)
    thick_bottom.add(38)
    thick_bottom.add(30)
    
    # Cells 51 and 52 separation
    thick_left.add(51)
    thick_right.add(51)
    thick_right.add(52)
    thick_bottom.add(51)
    thick_bottom.add(52)
    
    # Cells 25 and 33 separation
    thick_left.add(25)
    thick_top.add(25)
    thick_left.add(33)
    thick_bottom.add(33)
    thick_bottom.add(25)
    
    # Cell 54 borders
    thick_left.add(54)
    thick_top.add(54)
    thick_right.add(54)
