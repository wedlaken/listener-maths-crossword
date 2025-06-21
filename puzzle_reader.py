# New Puzzle Reader using Systematic Grid Parser
# Uses 0-63 indexing and systematic boundary detection

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from crossword_solver import Clue, CrosswordGrid
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
from systematic_grid_parser import SystematicGridParser, ClueTuple

# Initialize colorama for colored terminal output
init()

@dataclass
class GridCell:
    """Represents a cell in the 8x8 grid with index 0-63"""
    index: int  # 0-63, left to right, top to bottom
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
    cell_indices: Tuple[int, ...]  # Tuple of cell indices (0-63) this clue occupies
    parameters: Tuple[int, int, int]  # (a, b, c) for find_solutions
    possible_solutions: List[int] = None

class ListenerPuzzleReader:
    """New puzzle reader using systematic grid parser with 0-63 indexing"""
    
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
        
        # Initialize cells with 0-63 indexing
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                index = row * self.grid_size + col  # 0-63
                cell = GridCell(index=index, row=row, col=col)
                self.cells.append(cell)
        
        # Initialize systematic grid parser
        self.systematic_parser = SystematicGridParser(grid_image_path, clues_image_path)

    def read_clues_from_image(self) -> Dict[int, Tuple[str, int, int, int]]:
        """Read clue parameters from the clues image."""
        if self.clues_image is None:
            print("No clues image provided")
            return {}
        
        # This is a placeholder - in a real implementation, you'd use OCR
        # to read the actual clue parameters from the image
        # For now, return the known parameters for this puzzle
        
        clue_parameters = {
            1: ('ACROSS', 4, 2, 1),
            2: ('DOWN', 2, 1, 0),
            3: ('DOWN', 4, 3, 2),
            4: ('ACROSS', 4, 2, 1),
            5: ('ACROSS', 3, 1, 0),
            6: ('DOWN', 3, 2, 1),
            7: ('DOWN', 4, -1, -1),  # UNCLUE/UNDEFINED
            8: ('DOWN', 4, -1, -1),  # UNCLUE/UNDEFINED
            9: ('ACROSS', 3, 1, 0),
            10: ('DOWN', 7, 4, 3),
            11: ('DOWN', 7, 4, 3),
            12: ('ACROSS', 4, -1, -1),  # UNCLUE/UNDEFINED
            13: ('DOWN', 7, 4, 3),
            14: ('ACROSS', 4, -1, -1),  # UNCLUE/UNDEFINED
            15: ('ACROSS', 4, 2, 1),
            16: ('ACROSS', 3, 1, 0),
            17: ('ACROSS', 5, 3, 2),
            18: ('ACROSS', 4, 2, 1),
            19: ('ACROSS', 3, 1, 0),
            20: ('ACROSS', 4, 2, 1),
            21: ('ACROSS', 4, 2, 1),
            22: ('DOWN', 3, 2, 1),
            23: ('ACROSS', 3, 1, 0),
            24: ('DOWN', 4, 2, 1),
        }
        
        return clue_parameters

    def extract_clues(self) -> None:
        """Extract clues using the systematic grid parser."""
        print("Extracting clues using systematic grid parser...")
        
        # Use the systematic parser to get grid structure
        self.systematic_parser.parse_grid_structure()
        
        # Get clue parameters
        clue_parameters = self.read_clues_from_image()
        
        # Convert systematic parser results to ListenerClue format
        for clue_tuple in self.systematic_parser.get_all_clues():
            if clue_tuple.number in clue_parameters:
                direction, length, b, c = clue_parameters[clue_tuple.number]
                
                # Create ListenerClue object
                listener_clue = ListenerClue(
                    number=clue_tuple.number,
                    direction=clue_tuple.direction,
                    length=clue_tuple.length,
                    cell_indices=clue_tuple.cell_indices,
                    parameters=(length, b, c)
                )
                
                self.clues[clue_tuple.direction].append(listener_clue)
                
                # Update cell clue numbers
                for cell_index in clue_tuple.cell_indices:
                    if 0 <= cell_index < 64:
                        self.cells[cell_index].clue_number = clue_tuple.number
        
        print(f"Extracted {len(self.systematic_parser.across_clues)} ACROSS clues and {len(self.systematic_parser.down_clues)} DOWN clues")

    def print_grid_ascii(self) -> None:
        """Print an ASCII representation of the grid with cell indices and clue numbers."""
        print("\nGrid Structure (showing cell indices 0-63 and clue numbers):")
        print("=" * 60)
        
        # Print column numbers
        print("   ", end="")
        for col in range(self.grid_size):
            print(f"{col:3} ", end="")
        print("\n")
        
        for row in range(self.grid_size):
            print(f"{row:2} ", end="")
            for col in range(self.grid_size):
                cell = next((c for c in self.cells if c.row == row and c.col == col), None)
                if cell and cell.clue_number:
                    print(f"{cell.index:2}*", end="")  # * indicates clue number
                else:
                    print(f"{cell.index:2} ", end="")
            print()
        
        # Print clue summary
        print("\nClue Summary:")
        print("-" * 30)
        
        # Get all clues and sort by number
        all_clues = []
        for direction in ['ACROSS', 'DOWN']:
            for clue in self.clues[direction]:
                all_clues.append(clue)
        
        all_clues.sort(key=lambda x: x.number)
        
        for clue in all_clues:
            print(f"Clue {clue.number} {clue.direction}: {clue.cell_indices}")

    def show_detected_clues(self) -> None:
        """Show the detected clues in a formatted way."""
        print("\nDetected Clues:")
        print("=" * 50)
        
        for direction in ['ACROSS', 'DOWN']:
            print(f"\n{direction} Clues:")
            for clue in sorted(self.clues[direction], key=lambda x: x.number):
                print(f"  Clue {clue.number}: {clue.cell_indices} (length={clue.length}, b={clue.parameters[1]}, c={clue.parameters[2]})")

    def create_crossword_grid(self) -> CrosswordGrid:
        """Create a CrosswordGrid object from the detected clues."""
        grid = CrosswordGrid(self.grid_size)
        
        for direction in ['ACROSS', 'DOWN']:
            for clue in self.clues[direction]:
                # Convert to Clue format expected by CrosswordGrid
                crossword_clue = Clue(
                    number=clue.number,
                    direction=clue.direction,
                    length=clue.length,
                    cell_indices=clue.cell_indices,
                    parameters=clue.parameters
                )
                grid.add_clue(crossword_clue)
        
        return grid

    def process_puzzle(self) -> Optional[CrosswordGrid]:
        """Process the puzzle and return a CrosswordGrid object."""
        try:
            self.extract_clues()
            self.print_grid_ascii()
            self.show_detected_clues()
            return self.create_crossword_grid()
        except Exception as e:
            print(f"Error processing puzzle: {e}")
            return None

def main():
    """Test the new puzzle reader with systematic grid parser."""
    print("Testing new puzzle reader with systematic grid parser...")
    
    reader = ListenerPuzzleReader('Listener grid 4869.png', 'Listener 4869 clues.png')
    grid = reader.process_puzzle()
    
    if grid:
        print(f"\nSuccessfully created CrosswordGrid with {len(grid.clues['ACROSS'])} ACROSS and {len(grid.clues['DOWN'])} DOWN clues")
    else:
        print("Failed to process puzzle")

if __name__ == "__main__":
    main() 