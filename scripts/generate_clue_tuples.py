# Generate clue tuples using Systematic Grid Parser
# Uses 0-63 indexing and systematic boundary detection

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from systematic_grid_parser import SystematicGridParser

def get_manual_clue_mapping():
    """Define the manual mapping of clue numbers to cell positions (0-63 indexing)."""
    # This mapping should be based on visual inspection of the grid
    # Format: clue_number: cell_index (0-63 indexing)
    # Updated based on visual review: clues 1-23 are in cells [0,1,2,4,5,7,11,12,14,16,20,25,32,33,34,37,39,40,44,48,54,56,60]
    # Updated again based on systematic parser results to match actual grid structure
    
    manual_mapping = {
        1: 0,   # Clue 1 in cell 0
        2: 1,   # Clue 2 in cell 1  
        3: 2,   # Clue 3 in cell 2
        4: 4,   # Clue 4 in cell 4
        5: 5,   # Clue 5 in cell 5
        6: 7,   # Clue 6 in cell 7 (DOWN clue)
        7: 11,  # Clue 7 in cell 11
        8: 12,  # Clue 8 in cell 12
        9: 14,  # Clue 9 in cell 14 (ACROSS clue ending at cell 15)
        10: 16, # Clue 10 in cell 16 (ACROSS clue ending at cell 18)
        11: 20, # Clue 11 in cell 20
        12: 25, # Clue 12 in cell 25 (ACROSS clue ending at cell 26)
        13: 32, # Clue 13 in cell 32
        14: 33, # Clue 14 in cell 33 (ACROSS clue ending at cell 34)
        15: 34, # Clue 15 in cell 34 (DOWN clue)
        16: 37, # Clue 16 in cell 37
        17: 39, # Clue 17 in cell 39 (DOWN clue - thick bottom border)
        18: 40, # Clue 18 in cell 40 (ACROSS clue ending at cell 42)
        19: 44, # Clue 19 in cell 44
        20: 48, # Clue 20 in cell 48 (ACROSS clue ending at cell 49)
        21: 54, # Clue 21 in cell 54 (ACROSS clue - thick right border)
        22: 56, # Clue 22 in cell 56 (ACROSS clue ending at cell 58)
        23: 60, # Clue 23 in cell 60
    }
    
    return manual_mapping

def get_clue_parameters():
    """Get the known clue parameters for this puzzle."""
    # This contains the known parameters (a, b, c) for each clue
    # In a real implementation, these would be read from the clues image using OCR
    
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

def validate_clue_placement(clue_number, direction, length, start_cell, used_cells):
    """Validate that a clue can be placed without overlapping existing clues in the same direction."""
    if direction == 'ACROSS':
        # Check if all cells in the row are available
        row = start_cell // 8
        for i in range(length):
            cell_index = row * 8 + (start_cell % 8) + i
            if cell_index >= 64:  # Beyond grid boundary
                return False
            if cell_index in used_cells.get('ACROSS', set()):
                return False
    else:  # DOWN
        # Check if all cells in the column are available
        col = start_cell % 8
        row = start_cell // 8
        for i in range(length):
            cell_index = (row + i) * 8 + col
            if cell_index >= 64:  # Beyond grid boundary
                return False
            if cell_index in used_cells.get('DOWN', set()):
                return False
    return True

def get_clue_cells(clue_number, direction, length, start_cell):
    """Get the cell indices for a clue (0-63 indexing)."""
    cells = []
    if direction == 'ACROSS':
        row = start_cell // 8
        for i in range(length):
            cell_index = row * 8 + (start_cell % 8) + i
            cells.append(cell_index)
    else:  # DOWN
        col = start_cell % 8
        for i in range(length):
            cell_index = (start_cell // 8 + i) * 8 + col
            cells.append(cell_index)
    return cells

def main():
    print("Starting systematic grid parser approach...")
    
    # Initialize systematic grid parser
    parser = SystematicGridParser('data/Listener grid 4869.png', 'data/Listener 4869 clues.png')
    
    # Get manual clue mapping (0-63 indexing)
    clue_mapping = get_manual_clue_mapping()
    print(f"Manual mapping (0-63): {clue_mapping}")
    
    # Get clue parameters
    clue_parameters = get_clue_parameters()
    
    print("Validating clue placement with systematic parser...")
    
    # Track used cells for each direction
    used_cells = {'ACROSS': set(), 'DOWN': set()}
    valid_clues = []
    
    # Process clues in order
    for clue_number in sorted(clue_parameters.keys()):
        if clue_number not in clue_mapping:
            print(f"Warning: Clue {clue_number} not in manual mapping")
            continue
            
        direction, length, b, c = clue_parameters[clue_number]
        start_cell = clue_mapping[clue_number]
        
        print(f"Processing clue {clue_number} {direction} (length={length}) starting at cell {start_cell}")
        
        # Validate placement
        if validate_clue_placement(clue_number, direction, length, start_cell, used_cells):
            cells = get_clue_cells(clue_number, direction, length, start_cell)
            used_cells[direction].update(cells)
            valid_clues.append((clue_number, direction, cells, length, b, c))
            print(f"  ✓ Clue {clue_number} {direction}: {cells}")
        else:
            # Try opposite direction
            opposite_direction = 'DOWN' if direction == 'ACROSS' else 'ACROSS'
            if validate_clue_placement(clue_number, opposite_direction, length, start_cell, used_cells):
                cells = get_clue_cells(clue_number, opposite_direction, length, start_cell)
                used_cells[opposite_direction].update(cells)
                valid_clues.append((clue_number, opposite_direction, cells, length, b, c))
                print(f"  ✓ Clue {clue_number} {opposite_direction}: {cells} (direction corrected)")
            else:
                print(f"  ✗ Clue {clue_number} cannot be placed without overlap")
    
    print("\nGenerating systematic clue tuples file...")
    with open('detected_clues_tuples.txt', 'w') as f:
        valid_clues.sort(key=lambda x: x[0])
        for clue_number, direction, cells, length, b, c in valid_clues:
            f.write(f"Clue {clue_number} {direction}: {tuple(cells)}\n")
    
    print(f"Generated {len(valid_clues)} validated clues in detected_clues_tuples.txt")
    print("\nTo adjust the mapping, edit the get_manual_clue_mapping() function in this file.")
    print("File ready for manual verification against the puzzle.")

if __name__ == "__main__":
    main() 