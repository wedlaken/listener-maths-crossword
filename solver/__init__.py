"""
Listener Maths Crossword Solver Package

This package contains the refactored interactive solver components:
- grid: Grid structure and border calculations
- renderers: HTML/CSS generation
- puzzle_data: Puzzle configuration and data
- solver_app: Main application orchestration
"""

__version__ = "2.0.0"

from .grid import GridManager, get_grid_structure, calculate_grid_borders
from .renderers import (
    generate_base_grid_html,
    generate_grid_html,
    generate_anagram_grid_html,
    generate_clue_column_html,
    generate_clues_html,
    generate_anagram_clues_html,
    create_clue_id,
    get_clue_number_at_cell
)

__all__ = [
    # Grid functions
    'GridManager',
    'get_grid_structure',
    'calculate_grid_borders',
    # Renderer functions
    'generate_base_grid_html',
    'generate_grid_html',
    'generate_anagram_grid_html',
    'generate_clue_column_html',
    'generate_clues_html',
    'generate_anagram_clues_html',
    'create_clue_id',
    'get_clue_number_at_cell'
]
