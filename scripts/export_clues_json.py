#!/usr/bin/env python3
"""
Export clue objects to JSON for review
"""

import sys
import os
import json
import re
from typing import Dict, Tuple, List

from utils import parse_grid
from utils import ListenerClue

def load_clue_parameters(filename: str) -> Dict[Tuple[int, str], Tuple[int, int, int]]:
    """Load clue parameters from file."""
    clue_params = {}
    try:
        # Update path to data directory
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', filename)
        with open(data_path, 'r') as f:
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
                            clue_params[(number, current_direction)] = (0, 0, 0)
                        else:
                            b_c = parts[1].split(':')
                            if len(b_c) == 2:
                                b = int(b_c[0])
                                c = int(b_c[1])
                                clue_params[(number, current_direction)] = (0, b, c)
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
    
    return clue_params

def create_clue_id(number: int, direction: str) -> str:
    """Create unique clue ID like 'A1', 'D1'"""
    prefix = "A" if direction == "ACROSS" else "D"
    return f"{prefix}{number}"

def clue_to_dict(clue: ListenerClue) -> dict:
    """Convert a ListenerClue to a dictionary for JSON export."""
    return {
        "clue_id": clue.clue_id,
        "direction": clue.direction,
        "cell_indices": list(clue.cell_indices),
        "length": clue.length,
        "b": clue.b,
        "c": clue.c,
        "is_undefined": clue.is_undefined,
        "original_solution_count": clue.original_solution_count,
        "valid_solutions": list(clue.valid_solutions),
        "is_solved": clue.is_solved(),
        "solution": clue.get_solution(),
        "rejected_solutions": list(clue.rejected_solutions),
        "tried_solutions": list(clue.tried_solutions)
    }

def main():
    """Export all clue objects to JSON, excluding unclued clues."""
    print("=== EXPORTING CLUE OBJECTS TO JSON ===")
    
    # Parse grid and load parameters
    if parse_grid is None:
        print("ERROR: parse_grid function not available (missing OpenCV dependency)")
        print("Please install OpenCV: pip install opencv-python")
        return
    
    grid_clues = parse_grid()
    clue_params = load_clue_parameters("data/Listener 4869 clues.txt")
    
    # Define unclued clues to exclude
    unclued_clues = {
        (7, "DOWN"),   # Clue 7 DOWN
        (8, "DOWN"),   # Clue 8 DOWN  
        (12, "ACROSS"), # Clue 12 ACROSS
        (14, "ACROSS")  # Clue 14 ACROSS
    }
    
    # Create clue objects (excluding unclued clues)
    clues = []
    
    for number, direction, cell_indices in grid_clues:
        # Skip unclued clues
        if (number, direction) in unclued_clues:
            print(f"Skipping unclued clue: {number} {direction}")
            continue
            
        clue_id = create_clue_id(number, direction)
        param_key = (number, direction)
        
        if param_key in clue_params:
            a, b, c = clue_params[param_key]
            a = len(cell_indices)  # Update from actual length
            parameters = (a, b, c)
        else:
            a = len(cell_indices)
            parameters = (a, 0, 0)
        
        clue = ListenerClue(clue_id, direction, cell_indices, parameters)
        clues.append(clue)
    
    # Convert to JSON-serializable format
    clues_data = []
    for clue in clues:
        clue_dict = clue_to_dict(clue)
        clues_data.append(clue_dict)
    
    # Create summary data
    summary = {
        "total_clues": len(clues),
        "solved_clues": len([c for c in clues if c.is_solved()]),
        "unsolved_clues": len([c for c in clues if not c.is_solved()]),
        "clued_clues": len([c for c in clues if not c.is_undefined]),
        "unclued_clues": len([c for c in clues if c.is_undefined]),
        "excluded_unclued_clues": len(unclued_clues)
    }
    
    # Create full export
    export_data = {
        "summary": summary,
        "excluded_unclued_clues": list(unclued_clues),
        "clues": clues_data
    }
    
    # Write to JSON file
    output_file = "clue_objects_export.json"
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"Exported {len(clues)} clue objects to {output_file}")
    print(f"Excluded {len(unclued_clues)} unclued clues: {unclued_clues}")
    print(f"Summary: {summary}")
    
    # Also print a quick overview
    print(f"\nQuick overview:")
    for clue in sorted(clues, key=lambda c: c.clue_id):
        status = "SOLVED" if clue.is_solved() else f"{len(clue.valid_solutions)} solutions"
        if clue.is_solved():
            print(f"  {clue.clue_id}: {status} = {clue.get_solution()}")
        else:
            print(f"  {clue.clue_id}: {status}")

if __name__ == "__main__":
    main() 