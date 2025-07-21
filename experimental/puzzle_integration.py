"""
Puzzle Integration Script
Combines systematic grid parser with existing ListenerPuzzle class
Uses 0-63 indexing consistently throughout
"""

import sys
import os

from utils import parse_grid
from utils import ListenerPuzzle, ListenerClue
from typing import Dict, Tuple, List, Optional

def load_clue_parameters(filename: str) -> Dict[Tuple[int, str], Tuple[int, int, int]]:
    """
    Load clue parameters from file.
    Returns dict mapping (number, direction) -> (a, b, c) parameters.
    """
    parameters = {}
    
    with open(filename, 'r') as f:
        current_direction = None
        for line in f:
            line = line.strip()
            if line == "Across":
                current_direction = "ACROSS"
            elif line == "Down":
                current_direction = "DOWN"
            elif line and current_direction:
                parts = line.split()
                if len(parts) >= 2:
                    number = int(parts[0])
                    if parts[1] == "Unclued":
                        # Special case for unclued clues - use (length, 0, 0)
                        # We'll determine length from the grid parser
                        parameters[(number, current_direction)] = (0, 0, 0)  # Placeholder
                    else:
                        # Parse b:c format
                        b_c = parts[1].split(':')
                        if len(b_c) == 2:
                            b = int(b_c[0])
                            c = int(b_c[1])
                            # We'll determine 'a' (length) from the grid parser
                            parameters[(number, current_direction)] = (0, b, c)  # Placeholder for 'a'
    
    return parameters

def create_clue_id(number: int, direction: str) -> str:
    """Create unique clue ID like 'A1', 'D1'"""
    prefix = "A" if direction == "ACROSS" else "D"
    return f"{prefix}{number}"

def integrate_puzzle():
    """Integrate grid parser with crossword solver"""
    
    # Parse the grid to get clue information
    print("Parsing grid...")
    grid_clues = parse_grid()
    
    # Load clue parameters
    print("Loading clue parameters...")
    clue_params = load_clue_parameters("data/clue_parameters_4869.txt")
    
    # Create puzzle
    puzzle = ListenerPuzzle()
    
    # Process each clue from the grid parser
    for clue_info in grid_clues:
        number, direction, cell_indices = clue_info
        
        # Create unique clue ID
        clue_id = create_clue_id(number, direction)
        
        # Get parameters for this clue
        param_key = (number, direction)
        if param_key in clue_params:
            a, b, c = clue_params[param_key]
            # Update 'a' (length) from the actual cell count
            a = len(cell_indices)
            parameters = (a, b, c)
        else:
            # If no parameters found, treat as unclued
            a = len(cell_indices)
            parameters = (a, 0, 0)
        
        # Create clue object
        clue = ListenerClue(clue_id, direction, cell_indices, parameters)
        
        # Add to puzzle
        puzzle.add_clue(clue)
        
        print(f"Added {clue}")
    
    # Check for any clues in parameters that weren't found in grid
    print("\nChecking for missing clues...")
    for (number, direction) in clue_params:
        clue_id = create_clue_id(number, direction)
        if not puzzle.has_clue(clue_id):
            print(f"Warning: Clue {clue_id} in parameters but not found in grid")
    
    return puzzle

def main():
    """Main integration function"""
    print("=== Listener Maths Crossword Integration ===")
    
    # Create integrated puzzle
    puzzle = integrate_puzzle()
    
    print(f"\nPuzzle created with {len(puzzle.clues)} clues")
    
    # Try to solve
    print("\nAttempting to solve...")
    solved = puzzle.solve()
    
    if solved:
        print("Puzzle solved successfully!")
        puzzle.print_solution()
    else:
        print("Puzzle not fully solved. Current state:")
        puzzle.print_solution()
        
        # Show remaining clues
        print("\nRemaining clues:")
        for clue in puzzle.clues:
            if not clue.is_solved():
                print(f"  {clue}")

if __name__ == "__main__":
    main() 