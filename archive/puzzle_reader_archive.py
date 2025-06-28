# ARCHIVED: Original puzzle reader with 1-64 indexing
# This file contains the previous puzzle reading logic for reference
# New implementation will use the systematic approach with 0-63 indexing

# Copy of the current puzzle_reader.py logic for archival purposes
# This approach had issues with cell indexing inconsistency and poor boundary detection

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from crossword_solver import Clue, CrosswordGrid
import matplotlib.pyplot as plt
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

@dataclass
class GridCell:
    """Represents a cell in the 8x8 grid with index 1-64 (ARCHIVED - new version uses 0-63)"""
    index: int  # 1-64, left to right, top to bottom
    row: int    # 0-7
    col: int    # 0-7
    value: Optional[int] = None
    clue_number: Optional[int] = None

@dataclass
class ListenerClue:
    """Represents a clue in the Listener format"""
    number: int
    direction: str  # 'ACROSS' or 'DOWN'
    length: int
    cell_indices: Tuple[int, ...]  # Tuple of cell indices (1-64) this clue occupies
    parameters: Tuple[int, int, int]  # (a, b, c) for find_solutions
    possible_solutions: List[int] = None

class ListenerPuzzleReader:
    """ARCHIVED: Original puzzle reader with 1-64 indexing and heuristic clue detection"""
    
    def __init__(self, grid_image_path: str, clues_image_path: str = None):
        self.grid_image_path = grid_image_path
        self.clues_image_path = clues_image_path
        self.grid_image = cv2.imread(grid_image_path)
        self.clues_image = cv2.imread(clues_image_path) if clues_image_path else None
        self.grid_size = 8
        self.cells: List[GridCell] = []
        self.clues: Dict[str, List[ListenerClue]] = {
            'ACROSS': [],
            'DOWN': []
        }
        
        # Initialize cells with indices 1-64 (ARCHIVED - new version uses 0-63)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                index = row * self.grid_size + col + 1  # 1-64
                cell = GridCell(index=index, row=row, col=col)
                self.cells.append(cell)

    # ... rest of the archived methods would go here ...
    # This is just a placeholder to show the structure
    
    def extract_clues(self) -> None:
        """ARCHIVED: Extract clues using heuristic detection"""
        print("ARCHIVED: This method used heuristic clue detection")
        print("New implementation will use systematic OCR and boundary detection")

# Note: This archived version had issues with:
# 1. 1-64 indexing inconsistency
# 2. Heuristic clue detection instead of systematic approach
# 3. Poor boundary detection
# 4. Cell overlap problems 