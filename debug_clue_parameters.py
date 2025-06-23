#!/usr/bin/env python3
"""
Debug script to check clue parameters and identify issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from systematic_grid_parser import parse_grid
from crossword_solver import ListenerClue
from typing import Dict, Tuple

def load_clue_parameters(filename: str) -> Dict[Tuple[int, str], Tuple[int, int, int]]:
    """Load clue parameters from file."""
    parameters = {}
    
    try:
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
                            parameters[(number, current_direction)] = (0, 0, 0)  # Placeholder
                        else:
                            b_c = parts[1].split(':')
                            if len(b_c) == 2:
                                b = int(b_c[0])
                                c = int(b_c[1])
                                parameters[(number, current_direction)] = (0, b, c)  # Placeholder for 'a'
    except FileNotFoundError:
        print(f"ERROR: File {filename} not found!")
        return {}
    except Exception as e:
        print(f"ERROR loading parameters: {e}")
        return {}
    
    return parameters

def create_clue_id(number: int, direction: str) -> str:
    """Create unique clue ID like 'A1', 'D1'"""
    prefix = "A" if direction == "ACROSS" else "D"
    return f"{prefix}{number}"

def main():
    """Debug clue parameters"""
    print("=== CLUE PARAMETERS DEBUG ===")
    print()
    
    # Load parameters from file
    print("Loading parameters from file...")
    clue_params = load_clue_parameters("Listener 4869 clues.txt")
    
    print(f"Loaded {len(clue_params)} parameter entries:")
    for (number, direction), (a, b, c) in clue_params.items():
        clue_id = create_clue_id(number, direction)
        if b == 0 and c == 0:
            print(f"  {clue_id}: Unclued (placeholder)")
        else:
            print(f"  {clue_id}: a={a}, b={b}, c={c}")
    
    print()
    
    # Parse grid
    print("Parsing grid...")
    grid_clues = parse_grid()
    
    print(f"Found {len(grid_clues)} clues in grid:")
    for number, direction, cell_indices in grid_clues:
        clue_id = create_clue_id(number, direction)
        print(f"  {clue_id}: {len(cell_indices)} cells at {cell_indices}")
    
    print()
    
    # Create clue objects and check parameters
    print("Creating clue objects...")
    clues = []
    
    for number, direction, cell_indices in grid_clues:
        clue_id = create_clue_id(number, direction)
        param_key = (number, direction)
        
        # Initialize parameters
        a = len(cell_indices)
        b = 0
        c = 0
        
        if param_key in clue_params:
            a_file, b, c = clue_params[param_key]
            # Update 'a' (length) from the actual cell count
            a = len(cell_indices)
            parameters = (a, b, c)
        else:
            # If no parameters found, treat as unclued
            parameters = (a, 0, 0)
        
        # Create clue object
        clue = ListenerClue(clue_id, direction, cell_indices, parameters)
        clues.append(clue)
        
        # Check if this should be unclued
        if clue.is_undefined:
            print(f"  {clue_id}: MARKED AS UNCLUED")
            print(f"    Parameters: a={a}, b={b}, c={c}")
            print(f"    Expected: Check if this should be unclued")
        else:
            print(f"  {clue_id}: CLUED")
            print(f"    Parameters: a={a}, b={b}, c={c}")
            print(f"    Solutions: {len(clue.valid_solutions)}")
        
        print()
    
    # Check for missing clues
    print("Checking for missing clues...")
    for (number, direction) in clue_params:
        clue_id = create_clue_id(number, direction)
        found = any(c.clue_id == clue_id for c in clues)
        if not found:
            print(f"  WARNING: {clue_id} in parameters but not found in grid")
    
    print()
    print("=== SUMMARY ===")
    print(f"Total clues in parameters: {len(clue_params)}")
    print(f"Total clues in grid: {len(grid_clues)}")
    print(f"Total clue objects created: {len(clues)}")
    
    clued_count = sum(1 for c in clues if not c.is_undefined)
    unclued_count = sum(1 for c in clues if c.is_undefined)
    print(f"Clued clues: {clued_count}")
    print(f"Unclued clues: {unclued_count}")

if __name__ == "__main__":
    main() 