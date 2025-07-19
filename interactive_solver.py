#!/usr/bin/env python3
"""
Interactive Crossword Solver
Allows human users to manually select solutions from computed solution sets
and place them in the grid, leveraging both computational power and human intuition.
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
import webbrowser
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Removed systematic_grid_parser import - using hardcoded grid structure instead
from clue_classes import ListenerClue, ClueFactory, ClueManager, ClueParameters, AnagramClue

# Simple ClueTuple class for compatibility
class ClueTuple:
    """Simple clue tuple for compatibility with ClueFactory"""
    def __init__(self, number: int, direction: str, cell_indices: Tuple[int, ...], length: int, parameters: Tuple[int, int, int]):
        self.number = number
        self.direction = direction
        self.cell_indices = cell_indices
        self.length = length
        self.parameters = parameters
from listener import get_prime_factors_with_multiplicity

# Removed load_clue_parameters function - no longer needed
# All clue data is now loaded from Listener 4869 clues.txt

def get_grid_structure() -> List[Tuple[int, str, Tuple[int, ...]]]:
    """Get the grid structure for the crossword puzzle."""
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

def calculate_grid_borders(grid_clues: List[Tuple[int, str, Tuple[int, ...]]]) -> Dict[str, set]:
    """Calculate border classes for the grid based on clue structure."""
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
            if last_cell % 8 != 7 and last_cell not in {30, 38}:
                thick_right_cells.add(last_cell)
    
    # Process DOWN clues to find thick bottom borders
    down_clues = [clue for clue in grid_clues if clue[1] == 'DOWN']
    for number, direction, cell_indices in down_clues:
        if len(cell_indices) > 0:
            last_cell = cell_indices[-1]
            if last_cell < 56:
                thick_bottom_cells.add(last_cell)
    
    # Handle isolated cells
    isolated_cells = {9, 14, 49}
    for cell_index in isolated_cells:
        if cell_index == 9:
            thick_left_cells.add(9)
            thick_right_cells.add(9)
            thick_bottom_cells.add(9)
        elif cell_index == 14:
            thick_left_cells.add(14)
            thick_top_cells.add(14)
            thick_bottom_cells.add(14)
        elif cell_index == 49:
            thick_top_cells.add(49)
            thick_bottom_cells.add(49)
            thick_right_cells.add(49)
    
    # Add specific borders for cell pair separations
    # Cells 11 and 12 separation
    thick_top_cells.add(11)
    thick_left_cells.add(11)
    thick_right_cells.add(11)
    thick_top_cells.add(12)
    thick_right_cells.add(12)
    
    # Cells 30 and 38 separation
    thick_right_cells.add(30)
    thick_top_cells.add(30)
    thick_right_cells.add(38)
    thick_bottom_cells.add(38)
    thick_bottom_cells.add(30)
    
    # Cells 51 and 52 separation
    thick_left_cells.add(51)
    thick_right_cells.add(51)
    thick_right_cells.add(52)
    thick_bottom_cells.add(51)
    thick_bottom_cells.add(52)

    # Cells 25 and 33 separation
    thick_left_cells.add(25)
    thick_top_cells.add(25)
    thick_left_cells.add(33)
    thick_bottom_cells.add(33)
    thick_bottom_cells.add(25)
    
    # Cell 54 borders
    thick_left_cells.add(54)
    thick_top_cells.add(54)
    thick_right_cells.add(54)
    
    return {
        'thick_right': thick_right_cells,
        'thick_bottom': thick_bottom_cells,
        'thick_left': thick_left_cells,
        'thick_top': thick_top_cells
    }

def generate_base_grid_html(solved_cells: Dict[int, str] = None, 
                           grid_clues: List[Tuple[int, str, Tuple[int, ...]]] = None,
                           additional_classes: str = "",
                           additional_attributes: str = "",
                           cell_additional_classes: str = "",
                           cell_additional_attributes: str = "") -> str:
    """Generate base HTML for the crossword grid with shared logic."""
    if solved_cells is None:
        solved_cells = {}
    if grid_clues is None:
        grid_clues = get_grid_structure()
    
    # Calculate borders
    borders = calculate_grid_borders(grid_clues)
    
    # Generate grid HTML
    grid_html = [f'<div class="crossword-grid{additional_classes}"{additional_attributes}>']
    
    for row in range(8):
        grid_html.append('  <div class="grid-row">')
        for col in range(8):
            cell_index = row * 8 + col
            
            # Get clue number for this cell (only if it's the first cell of a clue)
            clue_number = get_clue_number_at_cell(cell_index, grid_clues)
            
            # Check if cell is solved
            cell_value = solved_cells.get(cell_index, '')
            
            # Determine border classes
            border_classes = []
            if cell_index in borders['thick_right']:
                border_classes.append('thick-right')
            if cell_index in borders['thick_bottom']:
                border_classes.append('thick-bottom')
            if cell_index in borders['thick_left']:
                border_classes.append('thick-left')
            if cell_index in borders['thick_top']:
                border_classes.append('thick-top')
            
            border_class = ' '.join(border_classes)
            
            # Create cell with additional classes and attributes
            cell_html = f'    <div class="grid-cell {border_class}{cell_additional_classes}" data-cell="{cell_index}"{cell_additional_attributes}>'
            if clue_number:
                cell_html += f'<div class="grid-clue-number">{clue_number}</div>'
            if cell_value:
                cell_html += f'<div class="cell-value">{cell_value}</div>'
            cell_html += '</div>'
            
            grid_html.append(cell_html)
        
        grid_html.append('  </div>')
    
    grid_html.append('</div>')
    
    return '\n'.join(grid_html)

def load_clues_from_file(filename: str = "Listener 4869 clues.txt") -> Dict[Tuple[int, str], str]:
    """Load actual clue text from the clues file."""
    clues = {}
    current_direction = None
    
    try:
        # Update path to data directory
        data_path = os.path.join('data', filename)
        with open(data_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                if line == "Across":
                    current_direction = "ACROSS"
                elif line == "Down":
                    current_direction = "DOWN"
                elif current_direction and line[0].isdigit():
                    # Parse clue line like "1 6:2" or "12 Unclued"
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        number = int(parts[0])
                        clue_text = parts[1]
                        clues[(number, current_direction)] = clue_text
    except FileNotFoundError:
        print(f"Warning: Could not find clues file {filename}")
    
    return clues

def create_clue_id(number: int, direction: str) -> str:
    """Create a unique identifier for a clue."""
    return f"{number}_{direction}"

def get_clue_number_at_cell(cell_index: int, grid_clues: List[Tuple[int, str, Tuple[int, ...]]]) -> Optional[int]:
    """Get the clue number at a specific cell, if any."""
    for number, direction, cell_indices in grid_clues:
        if cell_indices[0] == cell_index:  # First cell of the clue
            return number
    return None

def load_clue_objects() -> Tuple[List[Tuple[int, str, Tuple[int, ...]]], Dict[Tuple[int, str], ListenerClue], ClueManager]:
    """Load clue objects using hardcoded grid structure and clue classes."""
    print("Loading grid structure and clue objects...")
    
    # Get hardcoded grid structure
    grid_clues = get_grid_structure()
    
    # Create clue manager
    clue_manager = ClueManager()
    
    # Load clue data from the single source of truth
    clues_text = load_clues_from_file()
    
    # Create ListenerClue objects
    clue_objects = {}
    
    for number, direction, cell_indices in grid_clues:
        clue_key = (number, direction)
        
        # Get clue parameters from the clues file
        if clue_key in clues_text:
            text = clues_text[clue_key]
            if text.lower() == 'unclued':
                # Create unclued clue
                clue = ClueFactory.from_tuple_and_parameters(
                    ClueTuple(number=number, direction=direction, cell_indices=cell_indices, length=len(cell_indices), parameters=(len(cell_indices), -1, -1)),
                    -1, -1  # Unclued parameters
                )
            else:
                # Parse "b:c" format for clued clues
                try:
                    b_c_parts = text.split(':')
                    if len(b_c_parts) == 2:
                        b = int(b_c_parts[0])
                        c = int(b_c_parts[1])
                        clue = ClueFactory.from_tuple_and_parameters(
                            ClueTuple(number=number, direction=direction, cell_indices=cell_indices, length=len(cell_indices), parameters=(len(cell_indices), b, c)),
                            b, c
                        )
                    else:
                        # Fallback for malformed clue text
                        clue = ClueFactory.from_tuple_and_parameters(
                            ClueTuple(number=number, direction=direction, cell_indices=cell_indices, length=len(cell_indices), parameters=(len(cell_indices), 1, 0)),
                            1, 0
                        )
                except ValueError:
                    # Fallback for parsing errors
                    clue = ClueFactory.from_tuple_and_parameters(
                        ClueTuple(number=number, direction=direction, cell_indices=cell_indices, length=len(cell_indices), parameters=(len(cell_indices), 1, 0)),
                        1, 0
                    )
        else:
            # Fallback for missing clue data
            clue = ClueFactory.from_tuple_and_parameters(
                ClueTuple(number=number, direction=direction, cell_indices=cell_indices, length=len(cell_indices), parameters=(len(cell_indices), 1, 0)),
                1, 0
            )
        
        clue_objects[(number, direction)] = clue
        clue_manager.add_clue(clue)
    
    return grid_clues, clue_objects, clue_manager

def generate_grid_html(solved_cells: Dict[int, str] = None) -> str:
    """Generate HTML for the crossword grid."""
    # Use shared grid generation with wrapper div
    base_grid = generate_base_grid_html(solved_cells)
    return f'<div class="grid-wrapper">\n{base_grid}\n</div>'

def generate_clue_column_html(clues: List, 
                             direction: str, 
                             title: str,
                             clue_id_prefix: str = "",
                             additional_classes: str = "",
                             grid_type: str = "initial") -> str:
    """Generate HTML for a column of clues (Across or Down) with shared logic."""
    html = [f'  <div class="clues-column">']
    html.append(f'    <h3>{title}</h3>')
    
    for clue in clues:
        # Generate clue ID with optional prefix
        base_clue_id = create_clue_id(clue.number, clue.direction)
        clue_id = f"{clue_id_prefix}{base_clue_id}" if clue_id_prefix else base_clue_id
        
        # Get clue-specific data
        if hasattr(clue, 'get_original_solution'):  # AnagramClue
            # Anagram clue logic
            original_solution = clue.get_original_solution()
            anagram_solutions = clue.get_anagram_solutions()
            clue_text = f"Original: {original_solution}"
            solution_count = len(anagram_solutions)
            status_class = "anagram-clue"
            solutions = anagram_solutions
            placeholder_text = "-- Select an anagram --"
        else:  # ListenerClue
            # Regular clue logic
            current_solutions = clue.get_valid_solutions()
            solution_count = len(current_solutions)
            clue_text = "Unclued" if clue.parameters.is_unclued else f"{clue.parameters.b}:{clue.parameters.c}"
            status_class = "multiple" if solution_count > 1 else "unclued" if clue.parameters.is_unclued else ""
            solutions = current_solutions
            placeholder_text = "-- Select a solution --"
        
        # Add additional classes
        if additional_classes:
            status_class = f"{status_class} {additional_classes}"
        
        # Generate clue HTML
        html.append(f'    <div class="clue {status_class}" data-clue="{clue_id}" data-grid-type="{grid_type}">')
        html.append('      <div class="clue-header">')
        html.append(f'        <span class="clue-number">{clue.number}.</span>')
        html.append(f'        <span class="clue-text">{clue_text}</span>')
        
        # Solution count display
        if hasattr(clue, 'get_original_solution'):  # AnagramClue
            html.append(f'        <span class="solution-count">({solution_count} anagrams)</span>')
        else:  # ListenerClue
            if not clue.parameters.is_unclued:
                solution_word = 'solution' if solution_count == 1 else 'solutions'
                html.append(f'        <span class="solution-count">{solution_count} {solution_word}</span>')
            else:
                html.append(f'        <span class="solution-count" id="unclued-count-{clue_id}"></span>')
        
        html.append('      </div>')
        
        # Generate solution dropdown/input
        if hasattr(clue, 'get_original_solution'):  # AnagramClue
            # Anagram solutions dropdown
            if solutions:
                html.append(f'      <div class="solution-dropdown" id="dropdown-{clue_id}" style="display: none;">')
                html.append(f'        <select class="solution-select" data-clue="{clue_id}">')
                html.append(f'          <option value="">{placeholder_text}</option>')
                for solution in solutions:
                    html.append(f'          <option value="{solution}">{solution}</option>')
                html.append(f'        </select>')
                html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
                html.append(f'      </div>')
        else:  # ListenerClue
            # Regular clue solutions
            if clue.parameters.is_unclued:
                # Unclued input and dropdown
                html.append(f'      <div class="solution-input" id="input-{clue_id}" style="display: none;">')
                html.append(f'        <input type="text" class="solution-text-input" data-clue="{clue_id}" placeholder="Enter {clue.length}-digit solution" maxlength="{clue.length}">')
                html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
                html.append(f'        <span class="unclued-error" id="error-{clue_id}" style="color: #b00; margin-left: 8px; display: none;"></span>')
                html.append(f'      </div>')
                html.append(f'      <div class="solution-dropdown" id="dropdown-{clue_id}" style="display: none;">')
                html.append(f'        <select class="solution-select" data-clue="{clue_id}">')
                html.append(f'          <option value="">{placeholder_text}</option>')
                html.append(f'        </select>')
                html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
                html.append(f'      </div>')
            else:
                # Regular solutions dropdown
                if solutions:
                    html.append(f'      <div class="solution-dropdown" id="dropdown-{clue_id}" style="display: none;">')
                    html.append(f'        <select class="solution-select" data-clue="{clue_id}">')
                    html.append(f'          <option value="">{placeholder_text}</option>')
                    for solution in solutions:
                        html.append(f'          <option value="{solution}">{solution}</option>')
                    html.append(f'        </select>')
                    html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
                    html.append(f'      </div>')
        
        html.append(f'    </div>')
    
    html.append('  </div>')
    return '\n'.join(html)

def generate_clues_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate HTML for the clues section using clue objects."""
    html = ['<div class="clues-section">']

    # Across clues
    across_clues = [clue for clue in clue_objects.values() if clue.direction == "ACROSS"]
    across_clues.sort(key=lambda x: x.number)
    html.append(generate_clue_column_html(across_clues, "ACROSS", "Across"))

    # Down clues
    down_clues = [clue for clue in clue_objects.values() if clue.direction == "DOWN"]
    down_clues.sort(key=lambda x: x.number)
    html.append(generate_clue_column_html(down_clues, "DOWN", "Down"))

    html.append('</div>')
    return '\n'.join(html)

def generate_anagram_grid_html(solved_cells: Dict[int, str] = None) -> str:
    """Generate HTML for the anagram crossword grid."""
    # Use shared grid generation with anagram-specific classes and attributes
    return generate_base_grid_html(
        solved_cells=solved_cells,
        additional_classes=" anagram-grid",
        additional_attributes=' id="anagram-grid"',
        cell_additional_classes=" anagram-cell",
        cell_additional_attributes=' data-anagram="true"'
    )

def generate_anagram_clues_html(anagram_clue_objects: Dict[Tuple[int, str], AnagramClue]) -> str:
    """Generate HTML for the anagram clues section using AnagramClue objects."""
    html = ['<div class="clues-section anagram-clues-section" id="anagram-clues-section">']

    # Across clues
    across_clues = [clue for clue in anagram_clue_objects.values() if clue.direction == "ACROSS"]
    across_clues.sort(key=lambda x: x.number)
    html.append(generate_clue_column_html(
        across_clues, "ACROSS", "Anagram Solutions - Across",
        clue_id_prefix="anagram_", grid_type="anagram"
    ))

    # Down clues
    down_clues = [clue for clue in anagram_clue_objects.values() if clue.direction == "DOWN"]
    down_clues.sort(key=lambda x: x.number)
    html.append(generate_clue_column_html(
        down_clues, "DOWN", "Anagram Solutions - Down",
        clue_id_prefix="anagram_", grid_type="anagram"
    ))

    html.append('</div>')
    return '\n'.join(html)

def generate_anagram_solutions_for_clue(original_solution: int, length: int, is_unclued: bool) -> List[int]:
    """Generate anagram solutions for a given clue."""
    if not original_solution:
        return []
    
    solution_str = str(original_solution)
    digits = list(solution_str)
    
    if length == 2:
        # For 2-digit numbers, just swap the digits
        swapped = digits[1] + digits[0]
        return [int(swapped)] if swapped != solution_str else []
    
    # Generate all permutations and eliminate duplicates using a set
    from itertools import permutations
    anagram_set = set()
    
    for perm in permutations(digits):
        anagram_str = ''.join(perm)
        if anagram_str != solution_str and anagram_str[0] != '0':
            anagram_num = int(anagram_str)
            
            if is_unclued:
                # For unclued clues, anagrams must be multiples of the original
                if anagram_num % original_solution == 0:
                    anagram_set.add(anagram_num)
            else:
                # For clued clues, any anagram is valid
                anagram_set.add(anagram_num)
    
    return sorted(list(anagram_set))

def find_anagram_multiples(original_number: int) -> List[int]:
    """Find multiples of the original number that are anagrams."""
    original_str = str(original_number)
    original_digits = sorted(original_str)
    multiples = []
    
    # Check multiples up to 10x the original number
    for i in range(2, 11):
        multiple = original_number * i
        multiple_str = str(multiple)
        
        # Check if it's an anagram (same digits in different order)
        if len(multiple_str) == len(original_str):
            multiple_digits = sorted(multiple_str)
            if multiple_digits == original_digits and multiple_str != original_str:
                multiples.append(multiple)
    
    return multiples

def create_anagram_clue_objects(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> Dict[Tuple[int, str], AnagramClue]:
    """Create AnagramClue objects from the initial clue objects."""
    anagram_clue_objects = {}
    
    for (number, direction), clue in clue_objects.items():
        try:
            # Create anagram clue from the original clue
            anagram_clue = AnagramClue(clue)
            anagram_clue_objects[(number, direction)] = anagram_clue
        except ValueError as e:
            # Skip clues that aren't solved yet
            print(f"Warning: Cannot create AnagramClue for {number}_{direction}: {e}")
            continue
    
    return anagram_clue_objects

def generate_interactive_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate the complete interactive HTML interface with constrained unclued solving."""
    
    # Convert clue objects to JSON for JavaScript
    clue_data = {}
    for (number, direction), clue in clue_objects.items():
        clue_data[f"{number}_{direction}"] = {
            'number': clue.number,
            'direction': clue.direction,
            'cell_indices': list(clue.cell_indices),
            'length': clue.length,
            'is_unclued': clue.parameters.is_unclued,
            'possible_solutions': list(clue.possible_solutions),
            'original_solution_count': clue.original_solution_count
        }
    
    # Initialize empty anagram clue data - will be populated dynamically
    anagram_clue_data = {}
    
    # Simple solver status (constraints are handled in JavaScript)
    solver_status = {
        'solved_cells': 0,
        'solved_clues': 0,
        'min_required_cells': 0,  # No constraint in current implementation
        'can_enter_unclued': True,
        'constraint_message': '',
        'total_candidates': 0,
        'available_factors': []
    }
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Crossword Solver</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            height: 100vh;
            overflow-y: auto;
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: relative;
            min-height: calc(100vh - 40px);
        }}
        
        .header {{
            display: none;
        }}
        
        .main-content {{
            display: flex;
            gap: 30px;
            align-items: flex-start;
            position: relative;
        }}
        
        .grid-section {{
            flex: 1;
        }}
        
        .info-section {{
            flex: 1;
            min-width: 400px;
        }}
        
        /* Mobile responsive design */
        @media (max-width: 768px) {{
            body {{
                margin: 0;
                padding: 10px;
            }}
            
            .container {{
                padding: 15px;
                max-width: 100%;
                min-height: calc(100vh - 20px);
            }}
            
            .main-content {{
                flex-direction: column;
                gap: 20px;
            }}
            
            .grid-section {{
                order: 1;
            }}
            
            .info-section {{
                order: 2;
                min-width: auto;
            }}
            
            .crossword-grid {{
                max-width: 100%;
                overflow-x: auto;
                display: block;
                margin: 0 auto;
            }}
            
            .grid-cell {{
                width: 42px !important;
                height: 42px !important;
                font-size: 16px !important;
                box-sizing: border-box;
            }}
            
            .cell-value {{
                font-size: 18px;
            }}
            
            .grid-clue-number {{
                font-size: 8px;
            }}
            
            .clues-section {{
                flex-direction: column;
                gap: 15px;
                width: 100%;
            }}
            
            .clues-column {{
                margin-bottom: 15px;
                width: 100%;
            }}
            
            .clue {{
                padding: 10px;
                margin-bottom: 10px;
            }}
            
            /* Improved clue layout for medium mobile screens */
            .clue-header {{
                flex-direction: row;
                align-items: center;
                gap: 8px;
                flex-wrap: wrap;
            }}
            
            .clue-text {{
                font-size: 14px;
                flex: 1;
                min-width: 0;
            }}
            
            .solution-count {{
                font-size: 11px;
                min-width: auto;
                white-space: nowrap;
            }}
            
            .solution-dropdown {{
                margin-top: 10px;
            }}
            
            .solution-select {{
                font-size: 14px;
                padding: 8px;
            }}
            
            .apply-solution {{
                padding: 8px 16px;
                font-size: 14px;
            }}
            
            .prime-factor-workpad {{
                margin-top: 20px;
                padding: 12px;
            }}
            
            .progress-section {{
                margin-top: 15px;
                padding: 12px;
            }}
            
            .undo-section {{
                margin-top: 15px;
                padding: 12px;
            }}
            
            .undo-button {{
                padding: 10px 20px;
                font-size: 14px;
                margin-bottom: 10px;
            }}
            
            .developer-section {{
                margin-top: 20px;
                padding: 12px;
                min-height: auto;
            }}
            
            .developer-section h3 {{
                font-size: 16px;
                margin-bottom: 15px;
            }}
            
            .dev-button {{
                padding: 8px 12px !important;
                font-size: 11px !important;
                margin-bottom: 8px;
            }}
            
            .dev-info {{
                font-size: 10px;
                margin-top: 10px;
            }}
        }}
        
        /* Medium mobile devices - optimize for devices like Moto Edge 50 Ultra */
        @media (max-width: 600px) and (min-width: 481px) {{
            .grid-cell {{
                width: 45px !important;
                height: 45px !important;
                font-size: 17px !important;
            }}
            
            .clue-header {{
                flex-direction: row;
                align-items: center;
                gap: 6px;
                flex-wrap: wrap;
            }}
            
            .clue-text {{
                font-size: 13px;
                flex: 1;
                min-width: 0;
            }}
            
            .solution-count {{
                font-size: 10px;
                white-space: nowrap;
            }}
        }}
        
        /* Small mobile devices - allow single line with wrapping */
        @media (max-width: 480px) {{
            .grid-cell {{
                width: 38px !important;
                height: 38px !important;
                font-size: 14px !important;
            }}
            
            .cell-value {{
                font-size: 16px;
            }}
            
            .grid-clue-number {{
                font-size: 7px;
            }}
            
            .clue {{
                padding: 8px;
            }}
            
            .clue-header {{
                flex-direction: row;
                align-items: center;
                gap: 6px;
                flex-wrap: wrap;
            }}
            
            .clue-text {{
                font-size: 13px;
                flex: 1;
                min-width: 0;
            }}
            
            .solution-count {{
                font-size: 10px;
                white-space: nowrap;
            }}
        }}
        
        /* Very small mobile devices - stack clues vertically */
        @media (max-width: 360px) {{
            .grid-cell {{
                width: 32px !important;
                height: 32px !important;
                font-size: 12px !important;
            }}
            
            .cell-value {{
                font-size: 14px;
            }}
            
            .grid-clue-number {{
                font-size: 6px;
            }}
            
            .container {{
                padding: 10px;
            }}
            
            .main-content {{
                gap: 15px;
            }}
            
            .clue-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }}
            
            .clue-text {{
                font-size: 12px;
                flex: none;
            }}
            
            .solution-count {{
                font-size: 9px;
            }}
        }}
        
        .grid-wrapper {{
            text-align: left;
            margin: 0;
        }}
        
        .crossword-grid {{
            display: inline-block;
            border: 3px solid #333;
            background-color: #333;
            max-width: 100%;
            box-sizing: border-box;
        }}
        
        .grid-row {{
            display: flex;
        }}
        
        .grid-cell {{
            width: 50px;
            height: 50px;
            background-color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            font-weight: bold;
            font-size: 18px;
            box-sizing: border-box;
            border-right: 1px solid #ccc;
            border-bottom: 1px solid #ccc;
        }}
        
        .grid-clue-number {{
            position: absolute;
            top: 2px;
            left: 2px;
            font-size: 10px;
            color: #666;
            font-weight: normal;
        }}
        
        .cell-value {{
            font-size: 20px;
            color: #333;
        }}
        
        .grid-cell:nth-child(8n) {{
            border-right: none;
        }}
        
        .grid-row:last-child .grid-cell {{
            border-bottom: none;
        }}
        
        .thick-right {{
            border-right: 3px solid #333 !important;
        }}
        
        .thick-bottom {{
            border-bottom: 3px solid #333 !important;
        }}
        
        .thick-left {{
            border-left: 3px solid #333 !important;
        }}
        
        .thick-top {{
            border-top: 3px solid #333 !important;
        }}
        
        .clues-section {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .clues-column {{
            flex: 1;
        }}
        
        .clues-column h3 {{
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }}
        
        .clue {{
            margin-bottom: 8px;
            padding: 8px;
            border-radius: 4px;
            background-color: #f9f9f9;
            cursor: pointer;
            transition: background-color 0.2s;
            border: 2px solid transparent;
        }}
        
        .clue:hover {{
            background-color: #e9e9e9;
        }}
        
        .clue.solved, .anagram-clue.solved {{
            background-color: #d4edda !important;
            color: #155724 !important;
            font-weight: bold !important;
        }}
        
        .clue.user-selected, .anagram-clue.user-selected {{
            background-color: #cce5ff !important;
            color: #004085 !important;
            font-weight: bold !important;
            border-left: 4px solid #007bff !important;
        }}
        
        .clue.algorithm-solved, .anagram-clue.algorithm-solved {{
            background-color: #d1ecf1 !important;
            color: #0c5460 !important;
            font-weight: bold !important;
            border-left: 4px solid #17a2b8 !important;
        }}
        
        .clue.multiple, .anagram-clue.multiple {{
            background-color: #fff3cd !important;
            color: #856404 !important;
        }}
        
        .clue.unclued, .anagram-clue.unclued {{
            background-color: #f8d7da !important;
            color: #721c24 !important;
            font-style: italic !important;
        }}
        
        .clue-header {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .clue-header .clue-number {{
            font-weight: normal;
            min-width: 20px;
            color: #888;
            font-size: 13px;
            flex-shrink: 0;
        }}
        
        .clue-text {{
            flex: 1;
            margin-left: 8px;
            font-weight: bold;
            font-size: 16px;
            color: #222;
        }}
        
        .solution-count {{
            font-size: 12px;
            color: #666;
            text-align: right;
            flex-shrink: 0;
            min-width: 90px;
        }}
        
        .solution-dropdown {{
            margin-top: 8px;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }}
        
        .solution-select {{
            width: 100%;
            padding: 4px;
            margin-bottom: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }}
        
        .solution-text-input {{
            width: 100%;
            padding: 4px;
            margin-bottom: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }}
        
        .apply-solution {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}
        
        .apply-solution:hover {{
            background-color: #0056b3;
        }}
        
        .apply-solution:disabled {{
            background-color: #6c757d;
            cursor: not-allowed;
        }}
        
        .progress-section {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 6px;
        }}
        
        .progress-section h3 {{
            margin-top: 0;
            color: #333;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background-color: #007bff;
            transition: width 0.3s ease;
        }}
        
        .progress-stats {{
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            color: #666;
        }}
        
        .notification {{
            position: absolute;
            bottom: 20px;
            left: 0;
            width: 400px;
            max-width: 45%;
            padding: 15px;
            border-radius: 6px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
            text-align: center;
        }}
        
        .notification.success {{
            background-color: #28a745;
        }}
        
        .notification.error {{
            background-color: #dc3545;
        }}
        
        .notification.info {{
            background-color: #17a2b8;
        }}
        
        .undo-section {{
            margin-top: 15px;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 6px;
            text-align: center;
        }}
        
        .undo-button {{
            background-color: #6c757d;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
        }}
        
        .undo-button:hover {{
            background-color: #5a6268;
        }}
        
        .undo-button:disabled {{
            background-color: #adb5bd;
            cursor: not-allowed;
        }}
        
        .history-info {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}
        
        .constraint-status {{
            margin-top: 10px;
            padding: 8px;
            background-color: #fff3cd;
            border-radius: 4px;
            border-left: 4px solid #ffc107;
            font-size: 14px;
            color: #666;
        }}
        
        /* Anagram grid styles */
        .anagram-grid {{
            border: 3px solid #28a745 !important;
            background-color: white !important;
        }}
        .anagram-cell .cell-value {{
            color: #333 !important;
        }}
        /* Make thick borders green in anagram grid */
        .anagram-grid .thick-right {{
            border-right: 3px solid #28a745 !important;
        }}
        .anagram-grid .thick-bottom {{
            border-bottom: 3px solid #28a745 !important;
        }}
        .anagram-grid .thick-left {{
            border-left: 3px solid #28a745 !important;
        }}
        .anagram-grid .thick-top {{
            border-top: 3px solid #28a745 !important;
        }}
        .anagram-clues-section h3 {{
            color: #28a745 !important;
            border-bottom: 2px solid #28a745 !important;
            background: none;
        }}
        .anagram-clue {{
            background-color: #f9f9f9 !important;
            border-left: 4px solid #28a745 !important;
            color: #222 !important;
        }}
        
        /* Ensure user-selected anagram clues override the default anagram styling */
        .anagram-clue.user-selected {{
            background-color: #cce5ff !important;
            color: #004085 !important;
            font-weight: bold !important;
            border-left: 4px solid #007bff !important;
        }}
        .anagram-solutions {{
            margin-top: 8px;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }}
        .anagram-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .anagram-solution {{
            background-color: #e9ecef;
            color: #333;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        .anagram-more {{
            color: #666;
            font-style: italic;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">


        <div class="main-content">
            <div class="grid-section">
                <div id="initial-grid-section">
                    <h3 style="color: #333; border-bottom: 2px solid #333; padding-bottom: 5px; margin-bottom: 15px;">Puzzle Grid</h3>
                    {generate_grid_html()}
                </div>
                <div id="anagram-grid-section" style="display: none; margin-top: 30px;">
                    <h3 style="color: #28a745; border-bottom: 2px solid #28a745;">Anagram Grid</h3>
                    {generate_anagram_grid_html()}
                    <div style="margin-top: 20px; text-align: center;">
                        <button id="check-anagram-grid" style="
                            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                            color: white;
                            border: none;
                            padding: 15px 30px;
                            border-radius: 25px;
                            font-size: 1.2em;
                            font-weight: bold;
                            cursor: pointer;
                            transition: transform 0.2s;
                            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            ✅ Check Anagram Grid
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="info-section">
                <div id="initial-clues-container">
                    {generate_clues_html(clue_objects)}
                </div>
                <div id="anagram-clues-container" style="display: none;">
                    <div class="clues-section anagram-clues-section" id="anagram-clues-section">
                        <div class="clues-column">
                            <h3>Anagram Solutions - Across</h3>
                            <div id="anagram-across-clues">
                                <p style="color: #666; font-style: italic;">Complete the initial grid to generate anagram solutions</p>
                            </div>
                        </div>
                        <div class="clues-column">
                            <h3>Anagram Solutions - Down</h3>
                            <div id="anagram-down-clues">
                                <p style="color: #666; font-style: italic;">Complete the initial grid to generate anagram solutions</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="prime-factor-workpad" style="margin-top: 15px; padding: 15px; background-color: #f8f9fa; border-radius: 6px; border: 2px solid #dee2e6;">
                    <h3 style="margin-top: 0; color: #495057; border-bottom: 2px solid #6c757d; padding-bottom: 8px;">🔢 Prime Factor Workpad</h3>
                    <div style="margin-bottom: 15px;">
                        <label for="workpad-number" style="display: block; margin-bottom: 5px; font-weight: bold; color: #495057;">Enter a number to factorize:</label>
                        <input type="number" id="workpad-number" placeholder="e.g., 142857" style="
                            width: 100%;
                            padding: 8px;
                            border: 1px solid #ced4da;
                            border-radius: 4px;
                            font-size: 14px;
                            margin-bottom: 10px;
                        ">
                        <button id="factorize-btn" style="
                            background-color: #007bff;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 14px;
                            margin-right: 10px;
                        ">Factorize</button>
                        <button id="clear-workpad" style="
                            background-color: #6c757d;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 14px;
                        ">Clear</button>
                    </div>
                    <div id="factorization-result" style="
                        background-color: white;
                        border: 1px solid #dee2e6;
                        border-radius: 4px;
                        padding: 12px;
                        min-height: 30px;
                        font-family: 'Courier New', monospace;
                        font-size: 14px;
                        color: #495057;
                    ">
                        <div style="color: #6c757d; font-style: italic;">Enter a number above to see its prime factorization</div>
                    </div>
                    <div id="factorization-stats" style="
                        margin-top: 10px;
                        padding: 8px;
                        background-color: #e9ecef;
                        border-radius: 4px;
                        font-size: 12px;
                        color: #495057;
                        display: none;
                    "></div>
                </div>
                
                <div class="progress-section">
                    <h3>Progress</h3>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <div class="progress-stats">
                        <div>Cells filled: 0/64 (0.0%)</div>
                        <div>Clues solved: 0/24</div>
                    </div>

                </div>
                <div class="undo-section">
                    <h3>Solution History</h3>
                    <button class="undo-button" id="undo-button" disabled>Undo Last Solution</button>
                    <div class="history-info" id="history-info">No solutions applied yet</div>
                </div>
                <div class="developer-section" style="margin-top: 15px; padding: 15px; background-color: #e9ecef; border-radius: 6px; text-align: center; min-height: 140px;">
                    <h3>Developer Tools</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 10px;">
                        <button class="dev-button" id="dev-fill-14a" style="
                            background-color: #28a745;
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 12px;
                            white-space: nowrap;
                        ">Fill 14A</button>
                        <button class="dev-button" id="dev-fill-complete" style="
                            background-color: #dc3545;
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 12px;
                            white-space: nowrap;
                        ">Fill Initial</button>
                        <button class="dev-button" id="dev-fill-anagram" style="
                            background-color: #ffc107;
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 12px;
                            white-space: nowrap;
                            display: none;
                        ">Fill Anagram</button>
                        <button class="dev-button" id="dev-toggle-anagram" style="
                            background-color: #17a2b8;
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 12px;
                            white-space: nowrap;
                        ">Toggle Anagram</button>
                        <button class="dev-button" id="dev-toggle-constraints" style="
                            background-color: #6f42c1;
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 12px;
                            white-space: nowrap;
                        ">Toggle Constraints</button>
                    </div>
                    <div class="dev-info" style="font-size: 11px; color: #666;">Use these buttons to quickly test the anagram grid</div>
                </div>

            </div>
        </div>
    </div>

    <script>
        // Interactive functionality
        let solvedCells = {{}};
        let anagramSolvedCells = {{}};  // Separate state for anagram grid
        let clueObjects = {json.dumps(clue_data)};
        let anagramClueObjects = {json.dumps(anagram_clue_data)};
        let solverStatus = {json.dumps(solver_status)};
        let minRequiredCells = {solver_status['min_required_cells']};
        let userSelectedSolutions = new Set();
        let anagramUserSelectedSolutions = new Set();  // Separate tracking for anagram solutions
        let originalSolutionCounts = {{}};
        let originalSolutions = {{}};
        let anagramConstraintsEnabled = true;  // Global flag to control constraint level
        for (const [clueId, clue] of Object.entries(clueObjects)) {{
            originalSolutionCounts[clueId] = clue.possible_solutions.length;
            originalSolutions[clueId] = [...clue.possible_solutions];
        }}
        let solutionHistory = [];
        let undoButton = null;
        let historyInfo = null;
        function saveState(clueId, solution) {{
            // Determine if this is an anagram solution
            const isAnagramSolution = clueId.startsWith('anagram_');
            
            const state = {{
                timestamp: new Date().toLocaleTimeString(),
                clueId: clueId,
                solution: solution,
                isAnagramSolution: isAnagramSolution,
                solvedCells: {{...solvedCells}},
                clueObjects: JSON.parse(JSON.stringify(clueObjects)),
                userSelectedSolutions: new Set(userSelectedSolutions),
                // Add anagram state to the saved state
                anagramSolvedCells: {{...anagramSolvedCells}},
                anagramClueObjects: JSON.parse(JSON.stringify(anagramClueObjects)),
                anagramUserSelectedSolutions: new Set(anagramUserSelectedSolutions)
            }};
            solutionHistory.push(state);
            updateUndoButton();
            console.log('Saved state:', state);
        }}
        function undoLastSolution() {{
            if (solutionHistory.length === 0) return;
            const lastState = solutionHistory.pop();
            console.log('Undoing solution:', lastState);
            
            // Restore initial grid state
            solvedCells = {{...lastState.solvedCells}};
            clueObjects = JSON.parse(JSON.stringify(lastState.clueObjects));
            userSelectedSolutions = new Set(lastState.userSelectedSolutions);
            
            // Restore anagram grid state (if it exists in the saved state)
            if (lastState.anagramSolvedCells) {{
                anagramSolvedCells = {{...lastState.anagramSolvedCells}};
            }}
            if (lastState.anagramClueObjects) {{
                anagramClueObjects = JSON.parse(JSON.stringify(lastState.anagramClueObjects));
            }}
            if (lastState.anagramUserSelectedSolutions) {{
                anagramUserSelectedSolutions = new Set(lastState.anagramUserSelectedSolutions);
            }}
            
            // Update displays
            updateGridDisplay();
            updateAllClueDisplays();
            
            // Update anagram grid display if anagram state exists
            if (lastState.anagramSolvedCells && Object.keys(lastState.anagramSolvedCells).length > 0) {{
                updateAnagramGridDisplay();
                updateAnagramClueDisplays();
            }}
            
            updateProgress();
            updateUndoButton();
            
            if (lastState.solution === 'DESELECT') {{
                // Undid deselect for clue
            }} else {{
                const gridType = lastState.isAnagramSolution ? 'anagram grid' : 'initial grid';
                // Undid solution
            }}
        }}
        function updateUndoButton() {{
            if (!undoButton) return;
            const canUndo = solutionHistory.length > 0;
            undoButton.disabled = !canUndo;
            if (canUndo) {{
                const lastState = solutionHistory[solutionHistory.length - 1];
                if (lastState.solution === 'DESELECT') {{
                    historyInfo.textContent = `Last action: Deselected clue ${{lastState.clueId}} at ${{lastState.timestamp}}`;
                }} else {{
                    const gridType = lastState.isAnagramSolution ? 'anagram' : 'initial';
                    historyInfo.textContent = `Last solution: ${{lastState.solution}} for ${{lastState.clueId}} (${{gridType}}) at ${{lastState.timestamp}}`;
                }}
            }} else {{
                historyInfo.textContent = 'No solutions applied yet';
            }}
        }}
        function updateGridDisplay() {{
            document.querySelectorAll('.cell-value').forEach(el => {{
                el.remove();
            }});
            for (const [cellIndex, digit] of Object.entries(solvedCells)) {{
                updateCellDisplay(parseInt(cellIndex), digit);
            }}
        }}
        
        function updateAnagramGridDisplay() {{
            // Clear all anagram cell values
            document.querySelectorAll('[data-anagram="true"] .cell-value').forEach(el => {{
                el.remove();
            }});
            // Update anagram grid with current anagramSolvedCells
            for (const [cellIndex, digit] of Object.entries(anagramSolvedCells)) {{
                updateAnagramCellDisplay(parseInt(cellIndex), digit);
            }}
        }}
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, setting up event listeners');
            window.solvingStartTime = Date.now();
            undoButton = document.getElementById('undo-button');
            historyInfo = document.getElementById('history-info');
            updateUndoButton();
            undoButton.addEventListener('click', undoLastSolution);
            document.getElementById('dev-fill-14a').addEventListener('click', fill14A);
            document.getElementById('dev-fill-complete').addEventListener('click', fillCompleteGrid);
            document.getElementById('dev-fill-anagram').addEventListener('click', fillAnagramGrid);
            document.getElementById('dev-toggle-anagram').addEventListener('click', toggleAnagramMode);
            document.getElementById('dev-toggle-constraints').addEventListener('click', toggleConstraints);
            document.getElementById('factorize-btn').addEventListener('click', factorizeNumber);
            document.getElementById('clear-workpad').addEventListener('click', clearWorkpad);
            document.getElementById('workpad-number').addEventListener('keypress', function(e) {{
                if (e.key === 'Enter') {{
                    factorizeNumber();
                }}
            }});
            
            // Show intro modal
            showIntroModal();
            
            // Add event listener for the anagram check button
            const checkAnagramBtn = document.getElementById('check-anagram-grid');
            if (checkAnagramBtn) {{
                checkAnagramBtn.addEventListener('click', function() {{
                    // Check if all anagram clues are solved
                    let allSolved = true;
                    for (const clue of Object.values(anagramClueObjects)) {{
                        if (!clue.possible_solutions || clue.possible_solutions.length !== 1) {{
                            allSolved = false;
                            break;
                        }}
                    }}
                    if (allSolved && Object.keys(anagramClueObjects).length > 0) {{
                        showAnagramCompletionCelebration();
                    }} else {{
                        showNotification('Not all anagram clues are solved yet!', 'error');
                    }}
                }});
            }}
            // Unified event handler for both initial and anagram clues
            document.addEventListener('click', function(e) {{
                const clueDiv = e.target.closest('.clue');
                if (!clueDiv) return;
                if (e.target.closest('.solution-dropdown') || e.target.closest('.solution-input') || e.target.closest('.deselect-dialog') || e.target.classList.contains('apply-solution') || e.target.classList.contains('deselect-solution')) {{
                    return;
                }}
                
                const clueId = clueDiv.getAttribute('data-clue');
                const gridType = clueDiv.getAttribute('data-grid-type');
                console.log('Clue clicked:', clueId, 'grid type:', gridType);
                
                // Check if this clue has a user-selected solution (either initial or anagram)
                if (userSelectedSolutions.has(clueId) || anagramUserSelectedSolutions.has(clueId)) {{
                    showDeselectDialog(clueId);
                    return;
                }}
                
                const dropdownDiv = document.getElementById(`dropdown-${{clueId}}`);
                const inputDiv = document.getElementById(`input-${{clueId}}`);
                
                // Hide all other dropdowns/inputs first
                document.querySelectorAll('.solution-dropdown, .solution-input, .deselect-dialog').forEach(d => {{
                    if (d !== dropdownDiv && d !== inputDiv) d.style.display = 'none';
                }});
                
                if (gridType === 'anagram') {{
                    // Handle anagram clues - always show dropdown if it exists
                    if (dropdownDiv) {{
                        const isHidden = dropdownDiv.style.display === 'none' || dropdownDiv.style.display === '';
                        dropdownDiv.style.display = isHidden ? 'block' : 'none';
                        console.log('Toggled anagram dropdown for', clueId, 'to', isHidden ? 'visible' : 'hidden');
                    }} else {{
                        console.log('No dropdown found for anagram clue:', clueId);
                    }}
                }} else {{
                    // Handle initial clues (existing logic)
                    const clue = clueObjects[clueId];
                    if (clue && clue.is_unclued) {{
                        // Handle unclued clues
                        if (dropdownDiv && inputDiv) {{
                            const candidates = getFilteredCandidatesForClue(clueId);
                            const candidateCount = candidates.length;
                            
                            // Hide both initially
                            dropdownDiv.style.display = 'none';
                            inputDiv.style.display = 'none';
                            
                            // Show appropriate interface based on candidate count
                            if (candidateCount <= 50) {{
                                // Show dropdown with candidates
                                const select = dropdownDiv.querySelector('select');
                                if (select) {{
                                    select.innerHTML = '<option value="">-- Select a solution --</option>';
                                    for (const candidate of candidates) {{
                                        const opt = document.createElement('option');
                                        opt.value = candidate;
                                        opt.textContent = candidate.toString().padStart(clue.length, '0');
                                        select.appendChild(opt);
                                    }}
                                }}
                                dropdownDiv.style.display = 'block';
                                console.log('Showing dropdown for', clueId, 'with', candidateCount, 'candidates');
                            }} else {{
                                // Show input box for manual entry
                                inputDiv.style.display = 'block';
                                console.log('Showing input box for', clueId, 'with', candidateCount, 'candidates');
                            }}
                        }}
                    }} else {{
                        // Handle clued clues - show dropdown if it exists
                        if (dropdownDiv) {{
                            const isHidden = dropdownDiv.style.display === 'none' || dropdownDiv.style.display === '';
                            dropdownDiv.style.display = isHidden ? 'block' : 'none';
                            console.log('Toggled dropdown for', clueId, 'to', isHidden ? 'visible' : 'hidden');
                        }}
                    }}
                }}
            }});
            // Unified apply button handler for both grid types
            document.addEventListener('click', function(e) {{
                if (e.target.classList.contains('apply-solution')) {{
                    e.stopPropagation();
                    const clueId = e.target.getAttribute('data-clue');
                    console.log('Apply button clicked for:', clueId);
                    const select = e.target.parentNode.querySelector('.solution-select');
                    const input = e.target.parentNode.querySelector('.solution-text-input');
                    let solution = '';
                    if (select) {{
                        solution = select.value;
                        console.log('Selected solution from dropdown:', solution);
                    }} else if (input) {{
                        solution = input.value;
                        console.log('Entered solution from input:', solution);
                    }}
                    if (solution) {{
                        applySolutionToGrid(clueId, solution);
                    }} else {{
                        showNotification('Please select or enter a solution first', 'error');
                    }}
                }}
            }});
        }});

        function updateCellDisplay(cellIndex, digit) {{
            const cell = document.querySelector(`[data-cell="${{cellIndex}}"]`);
            if (cell) {{
                let valueElement = cell.querySelector('.cell-value');
                if (!valueElement) {{
                    // Create the cell-value element if it doesn't exist
                    valueElement = document.createElement('div');
                    valueElement.className = 'cell-value';
                    cell.appendChild(valueElement);
                }}
                valueElement.textContent = digit;
            }}
        }}

        function updateAnagramCellDisplay(cellIndex, digit) {{
            const cell = document.querySelector(`[data-cell="${{cellIndex}}"][data-anagram="true"]`);
            if (cell) {{
                let valueElement = cell.querySelector('.cell-value');
                if (!valueElement) {{
                    // Create the cell-value element if it doesn't exist
                    valueElement = document.createElement('div');
                    valueElement.className = 'cell-value';
                    cell.appendChild(valueElement);
                }}
                valueElement.textContent = digit;
            }}
        }}

        function canEnterUncluedSolution(clueId) {{
            const clue = clueObjects[clueId];
            if (!clue || !clue.is_unclued) {{
                return {{ allowed: false, reason: 'Not an unclued clue' }};
            }}
            
            // No constraint - allow entering unclued solutions immediately
            return {{
                allowed: true,
                solvedCount: 0,
                requiredCount: 0,
                totalCells: clue.cell_indices.length,
                reason: ''
            }};
        }}
        
        function applySolutionToGrid(clueId, solution) {{
            console.log(`Applying solution "${{solution}}" to clue ${{clueId}}`);
            
            // Check if this is an anagram clue
            const isAnagramClue = clueId.startsWith('anagram_');
            
            // Save current state before applying solution
            saveState(clueId, solution);
            
            // Parse clue ID to get number and direction
            const [number, direction] = clueId.split('_');
            const clueNumber = parseInt(number);
            
            // Validate solution format
            if (!/^\\d+$/.test(solution)) {{
                showNotification('Solution must be a number', 'error');
                return;
            }}
            
            // Get clue object (either regular or anagram)
            let clue;
            if (isAnagramClue) {{
                clue = anagramClueObjects[clueId];
                if (!clue) {{
                    showNotification('Anagram clue not found', 'error');
                    return;
                }}
            }} else {{
                clue = clueObjects[clueId];
                if (!clue) {{
                    showNotification('Clue not found', 'error');
                    return;
                }}
            }}
            
            // Validate solution length
            if (solution.length !== clue.length) {{
                showNotification(`Solution must be ${{clue.length}} digits long`, 'error');
                return;
            }}
            
            // For unclued clues, check constraints and conflicts (skip for anagram clues)
            if (clue.is_unclued && !isAnagramClue) {{
                // Check constraint requirement first
                const constraintCheck = canEnterUncluedSolution(clueId);
                if (!constraintCheck.allowed) {{
                    showNotification(constraintCheck.reason, 'error');
                    
                    // Show error in the unclued clue's error span
                    const errorSpan = document.getElementById(`error-${{clueId}}`);
                    if (errorSpan) {{
                        errorSpan.textContent = constraintCheck.reason;
                        errorSpan.style.display = 'inline';
                    }}
                    return;
                }}
                
                const solutionStr = solution.padStart(clue.length, '0');
                const conflicts = [];
                
                // Check each cell position against already solved cells
                for (let i = 0; i < clue.cell_indices.length; i++) {{
                    const cellIndex = clue.cell_indices[i];
                    const digit = parseInt(solutionStr[i]);
                    
                    // If this cell is already solved, check if it conflicts
                    if (cellIndex in solvedCells) {{
                        if (solvedCells[cellIndex] !== digit) {{
                            // Find which clue this cell belongs to for better error message
                            let conflictingClue = '';
                            for (const [otherClueId, otherClue] of Object.entries(clueObjects)) {{
                                if (otherClue.cell_indices.includes(cellIndex)) {{
                                    conflictingClue = otherClueId;
                                    break;
                                }}
                            }}
                            conflicts.push(`Cell ${{cellIndex}} (clue ${{conflictingClue}}) already has value ${{solvedCells[cellIndex]}}, but your solution has ${{digit}}`);
                        }}
                    }}
                }}
                
                if (conflicts.length > 0) {{
                    const errorMsg = `Solution conflicts with existing values:\\n${{conflicts.join('\\n')}}`;
                    showNotification(errorMsg, 'error');
                    
                    // Show error in the unclued clue's error span
                    const errorSpan = document.getElementById(`error-${{clueId}}`);
                    if (errorSpan) {{
                        errorSpan.textContent = 'Conflicts with existing solutions';
                        errorSpan.style.display = 'inline';
                    }}
                    return;
                }}
                
                // Clear any previous error
                const errorSpan = document.getElementById(`error-${{clueId}}`);
                if (errorSpan) {{
                    errorSpan.style.display = 'none';
                }}
            }} else if (isAnagramClue) {{
                // For anagram clues, check if solution is valid for this clue
                if (!clue.possible_solutions.includes(parseInt(solution))) {{
                    showNotification('This anagram solution is not valid for this clue', 'error');
                    return;
                }}
            }} else {{
                // For regular clues, check if solution is valid for this clue
                if (!clue.possible_solutions.includes(parseInt(solution))) {{
                    showNotification('This solution is not valid for this clue', 'error');
                    return;
                }}
            }}
            
            // Apply solution to grid cells
            const solutionStr = solution.padStart(clue.length, '0');
            for (let i = 0; i < clue.cell_indices.length; i++) {{
                const cellIndex = clue.cell_indices[i];
                const digit = parseInt(solutionStr[i]);
                
                if (isAnagramClue) {{
                    // Apply to anagram grid
                    anagramSolvedCells[cellIndex] = digit;
                    updateAnagramCellDisplay(cellIndex, digit);
                }} else {{
                    // Apply to initial grid
                    solvedCells[cellIndex] = digit;
                    updateCellDisplay(cellIndex, digit);
                }}
            }}
            
                        // Mark clue as solved
            clue.possible_solutions = [parseInt(solution)];
            
            // Mark this as a user-selected solution
            if (isAnagramClue) {{
                anagramUserSelectedSolutions.add(clueId);
                // Update the anagram clue data structure to reflect the selection
                if (anagramClueObjects[clueId]) {{
                    anagramClueObjects[clueId].possible_solutions = [parseInt(solution)];
                    anagramClueObjects[clueId].anagram_solutions = [parseInt(solution)];
                }}
            }} else {{
            userSelectedSolutions.add(clueId);
            }}
            
            // Propagate constraints to crossing clues
            let eliminatedSolutions = [];
            if (!isAnagramClue) {{
                eliminatedSolutions = propagateConstraints(clueId, solution);
            }} else {{
                eliminatedSolutions = propagateAnagramConstraints(clueId, solution);
            }}
            
            // Update all clue displays
            updateAllClueDisplays();
            
            // Update anagram clue displays if this was an anagram solution
            if (isAnagramClue) {{
                updateAnagramClueDisplays();
            }}
            
            // Update progress
            updateProgress();
            
            // Show success message
            if (isAnagramClue) {{
                showNotification(`Anagram solution applied to anagram grid!`, 'success');
            }} else {{
                const eliminatedCount = eliminatedSolutions.length;
                if (eliminatedCount > 0) {{
                    showNotification(`Solution applied! Eliminated ${{eliminatedCount}} incompatible solutions from crossing clues.`, 'success');
                }} else {{
                    showNotification('Solution applied successfully!', 'success');
                }}
            }}
            
            // Update unclued clue displays after applying solution
            updateUncluedClueDisplays();
            
            // Hide the dropdown/input for both initial and anagram clues
            const dropdownDiv = document.getElementById(`dropdown-${{clueId}}`);
            const inputDiv = document.getElementById(`input-${{clueId}}`);
            if (dropdownDiv) dropdownDiv.style.display = 'none';
            if (inputDiv) inputDiv.style.display = 'none';
            
            // Also hide any deselect dialogs
            const deselectDialog = document.getElementById(`deselect-${{clueId}}`);
            if (deselectDialog) deselectDialog.style.display = 'none';
        }}

        function propagateConstraints(clueId, solution) {{
            const eliminatedSolutions = [];
            const clue = clueObjects[clueId];
            const solutionStr = solution.padStart(clue.length, '0');
            
            // Find all clues that share cells with this clue
            const crossingClues = [];
            for (const [otherClueId, otherClue] of Object.entries(clueObjects)) {{
                if (otherClueId !== clueId) {{
                    // Check if any cells overlap
                    const overlap = clue.cell_indices.filter(cell => 
                        otherClue.cell_indices.includes(cell)
                    );
                    if (overlap.length > 0) {{
                        crossingClues.push(otherClueId);
                    }}
                }}
            }}
            
            // Eliminate incompatible solutions from crossing clues
            for (const crossingClueId of crossingClues) {{
                const crossingClue = clueObjects[crossingClueId];
                const solutionsToRemove = [];
                
                for (const possibleSolution of crossingClue.possible_solutions) {{
                    const possibleStr = possibleSolution.toString().padStart(crossingClue.length, '0');
                    let incompatible = false;
                    
                    // Check each cell position
                    for (let i = 0; i < crossingClue.cell_indices.length; i++) {{
                        const cellIndex = crossingClue.cell_indices[i];
                        const digit = parseInt(possibleStr[i]);
                        
                        // If this cell is already solved, check compatibility
                        if (cellIndex in solvedCells) {{
                            if (solvedCells[cellIndex] !== digit) {{
                                incompatible = true;
                                break;
                            }}
                        }}
                    }}
                    
                    if (incompatible) {{
                        solutionsToRemove.push(possibleSolution);
                    }}
                }}
                
                // Remove incompatible solutions
                for (const solutionToRemove of solutionsToRemove) {{
                    crossingClue.possible_solutions = crossingClue.possible_solutions.filter(s => s !== solutionToRemove);
                    eliminatedSolutions.push({{clueId: crossingClueId, solution: solutionToRemove}});
                }}
            }}
            
            return eliminatedSolutions;
        }}

        function updateAllClueDisplays() {{
            // Update each clue's display based on current state
            for (const [clueId, clue] of Object.entries(clueObjects)) {{
                updateClueDisplay(clueId, clue);
            }}
        }}

        function updateClueDisplay(clueId, clue) {{
            const clueElement = document.querySelector(`[data-clue="${{clueId}}"]`);
            if (!clueElement) return;
            
                    // Update solution count - show count until committed, then show actual solution
        const countElement = clueElement.querySelector('.solution-count');
        if (countElement) {{
            if (!clue.is_unclued) {{
                if (clue.possible_solutions.length === 1 && userSelectedSolutions.has(clueId)) {{
                    // User has committed the solution - show the actual solution
                    countElement.textContent = `${{clue.possible_solutions[0]}}`;
                }} else {{
                    // Show count of solutions (singular when only one)
                    countElement.textContent = `${{clue.possible_solutions.length}} ${{clue.possible_solutions.length === 1 ? 'solution' : 'solutions'}}`;
                }}
            }}
            // For unclued clues, the count will be updated by updateUncluedClueDisplays()
        }}
            
            // Update clue styling based on solution count and user selection
            clueElement.className = 'clue';
            
            if (clue.possible_solutions.length === 1) {{
                if (userSelectedSolutions.has(clueId)) {{
                    // User manually selected this solution
                    clueElement.classList.add('user-selected');
                }} else {{
                    // Algorithm determined only one solution remains
                    clueElement.classList.add('algorithm-solved');
                }}
            }} else if (clue.possible_solutions.length > 1) {{
                if (userSelectedSolutions.has(clueId)) {{
                    // User selected a solution but there are still other possibilities
                    clueElement.classList.add('user-selected');
                }} else {{
                    // Multiple solutions available, no user selection
                    clueElement.classList.add('multiple');
                }}
            }} else if (clue.is_unclued) {{
                clueElement.classList.add('unclued');
            }}
            
            // Update dropdown options if it exists
            const dropdownDiv = document.getElementById(`dropdown-${{clueId}}`);
            if (dropdownDiv) {{
                const select = dropdownDiv.querySelector('.solution-select');
                if (select) {{
                    // Keep the first option (placeholder) and update only the solution options
                    const placeholderOption = select.querySelector('option[value=""]');
                    select.innerHTML = '';
                    
                    // Restore the placeholder option
                    if (placeholderOption) {{
                        select.appendChild(placeholderOption);
                    }} else {{
                        const newPlaceholder = document.createElement('option');
                        newPlaceholder.value = '';
                        newPlaceholder.textContent = '-- Select a solution --';
                        select.appendChild(newPlaceholder);
                    }}
                    
                    // Add the solution options
                    for (const solution of clue.possible_solutions) {{
                        const option = document.createElement('option');
                        option.value = solution;
                        option.textContent = solution.toString().padStart(clue.length, '0');
                        select.appendChild(option);
                    }}
                    
                    console.log(`Updated dropdown for ${{clueId}} with ${{clue.possible_solutions.length}} solutions`);
                }}
            }}
        }}

        function updateProgress() {{
            const filledCells = Object.keys(solvedCells).length;
            const percentage = (filledCells / 64) * 100;
            
            // Count solved clues (both user-selected and algorithm-determined)
            let solvedClues = 0;
            for (const clue of Object.values(clueObjects)) {{
                if (clue.possible_solutions.length === 1) {{
                    solvedClues++;
                }}
            }}
            
            document.querySelector('.progress-fill').style.width = percentage + '%';
            document.querySelector('.progress-stats').innerHTML = 
                `<div>Cells filled: ${{filledCells}}/64 (${{percentage.toFixed(1)}}%)</div>
                 <div>Clues solved: ${{solvedClues}}/24</div>`;
            
            // Check for puzzle completion
            if (filledCells === 64 && solvedClues === 24 && !window.puzzleCompleted) {{
                window.puzzleCompleted = true;
                showCompletionCelebration();
            }}
            
            // Update unclued clue displays
            updateUncluedClueDisplays();
        }}
        
        function showCompletionCelebration() {{
            // Create celebration modal
            const modal = document.createElement('div');
            modal.id = 'completion-celebration';
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 10000;
                animation: fadeIn 0.5s ease-in;
            `;
            
            // Add CSS animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                @keyframes slideIn {{
                    from {{ transform: translateY(-50px); opacity: 0; }}
                    to {{ transform: translateY(0); opacity: 1; }}
                }}
                @keyframes confetti {{
                    0% {{ transform: translateY(-100vh) rotate(0deg); }}
                    100% {{ transform: translateY(100vh) rotate(360deg); }}
                }}
                
                /* Mobile-specific modal styles */
                @media (max-width: 768px) {{
                    #completion-celebration > div {{
                        max-height: 90vh !important;
                        margin: 10px !important;
                        padding: 20px !important;
                    }}
                }}
                
                @media (max-width: 480px) {{
                    #completion-celebration > div {{
                        max-height: 95vh !important;
                        margin: 5px !important;
                        padding: 15px !important;
                    }}
                }}
            `;
            document.head.appendChild(style);
            
            // Calculate solving statistics
            const solvingTime = Math.round((Date.now() - window.solvingStartTime) / 1000);
            const solutionsApplied = solutionHistory.filter(s => s.solution !== 'DESELECT').length;
            const undoOperations = solutionHistory.filter(s => s.solution === 'DESELECT').length;
            
            modal.innerHTML = `
                <div style="
                    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                    color: white;
                    padding: 40px;
                    border-radius: 12px;
                    text-align: center;
                    max-width: 600px;
                    max-height: 85vh;
                    margin: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                    animation: slideIn 0.6s ease-out;
                    position: relative;
                    overflow-y: auto;
                    overflow-x: hidden;
                    border: 1px solid #495057;
                    box-sizing: border-box;
                    -webkit-overflow-scrolling: touch;
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        height: 4px;
                        background: linear-gradient(90deg, #28a745, #17a2b8, #007bff);
                        z-index: 1;
                    "></div>
                    
                    <h1 style="font-size: 2.2em; margin: 0 0 20px 0; color: #e9ecef; font-weight: 300; letter-spacing: 1px;">
                        🎉 Puzzle Complete! 🎉
                    </h1>
                    
                    <div style="
                        background: rgba(255,255,255,0.08);
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                        border: 1px solid rgba(255,255,255,0.1);
                    ">
                        <h3 style="margin: 0 0 15px 0; color: #28a745; font-weight: 500; font-size: 1.3em;">Solving Statistics</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: left; color: #e9ecef;">
                            <div><strong style="color: #17a2b8;">Time taken:</strong> ${{Math.floor(solvingTime/60)}}m ${{solvingTime%60}}s</div>
                            <div><strong style="color: #17a2b8;">Solutions applied:</strong> ${{solutionsApplied}}</div>
                            <div><strong style="color: #17a2b8;">Undo operations:</strong> ${{undoOperations}}</div>
                            <div><strong style="color: #17a2b8;">Completion rate:</strong> 100%</div>
                        </div>
                    </div>
                    
                    <div style="
                        background: rgba(255,255,255,0.08);
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                        border: 1px solid rgba(255,255,255,0.1);
                    ">
                        <h3 style="margin: 0 0 15px 0; color: #17a2b8; font-weight: 500; font-size: 1.3em;">Ready for the Next Challenge?</h3>
                        <p style="margin: 0 0 15px 0; line-height: 1.6; color: #e9ecef;">
                            Congratulations! You've successfully completed the first stage of the puzzle. 
                            But a new challenge lies ahead...
                        </p>
                        <div style="
                            background: rgba(23, 162, 184, 0.15);
                            padding: 15px;
                            border-radius: 8px;
                            border-left: 4px solid #17a2b8;
                            text-align: center;
                            font-style: normal;
                            color: #e9ecef;
                        ">
                            <strong style="color: #17a2b8;">The Anagram Challenge:</strong><br>
                            "Solvers must submit a grid in which every entry is an anagram of its counterpart in the initial grid 
                            (same digits in a different order). For each of the unclued six-digit entries, the anagram is a multiple 
                            of its original value. The 48 numbers used (24 initial + 24 anagrams) are all different, and none starts with zero."
                        </div>
                    </div>
                    
                    <div style="margin-top: 30px;">
                        <button onclick="showAnagramGridInline()" style="
                            background: linear-gradient(135deg, #28a745, #20c997);
                            color: white;
                            border: none;
                            padding: 15px 30px;
                            border-radius: 8px;
                            font-size: 1.1em;
                            font-weight: 500;
                            cursor: pointer;
                            margin-right: 15px;
                            transition: all 0.3s ease;
                            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
                        " onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 16px rgba(40, 167, 69, 0.4)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 12px rgba(40, 167, 69, 0.3)'">
                            🧩 Show Anagram Grid
                        </button>
                        <button onclick="hideCompletionCelebration()" style="
                            background: rgba(255,255,255,0.1);
                            color: white;
                            border: 1px solid rgba(255,255,255,0.2);
                            padding: 15px 30px;
                            border-radius: 8px;
                            font-size: 1.1em;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        " onmouseover="this.style.background='rgba(255,255,255,0.15)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                            Continue Solving
                        </button>
                    </div>
                </div>
            `;
            
            // Add gradient animation
            const gradientStyle = document.createElement('style');
            gradientStyle.textContent = `
                @keyframes gradientShift {{
                    0% {{ background-position: 0% 50%; }}
                    50% {{ background-position: 100% 50%; }}
                    100% {{ background-position: 0% 50%; }}
                }}
            `;
            document.head.appendChild(gradientStyle);
            
            // Add subtle glow animation for celebrations
            const modalContent = modal.querySelector('div');
            modalContent.style.animation = 'slideIn 0.6s ease-out, subtleGlow 3s ease-in-out infinite';
            
            document.body.appendChild(modal);
        }}
        
        function createConfetti() {{
            // Removed confetti for sophisticated design
            // The subtle glow animation provides sufficient celebration effect
        }}
        
        function hideCompletionCelebration() {{
            const modal = document.getElementById('completion-celebration');
            if (modal) {{
                modal.style.animation = 'fadeIn 0.5s ease-in reverse';
                setTimeout(() => {{
                    if (modal.parentNode) {{
                        modal.remove();
                    }}
                }}, 500);
            }}
        }}
        
        function showAnagramGridInline() {{
            // Hide celebration modal
            hideCompletionCelebration();
            
            // Generate anagram clues dynamically
            generateAnagramClues();
            
            // Show anagram grid section (do not hide initial grid)
            const anagramGridSection = document.getElementById('anagram-grid-section');
            if (anagramGridSection) {{
                anagramGridSection.style.display = 'block';
            }}

            
            // Hide original clues and show anagram clues
            const initialCluesContainer = document.getElementById('initial-clues-container');
            const anagramCluesContainer = document.getElementById('anagram-clues-container');
            if (initialCluesContainer) {{
                initialCluesContainer.style.display = 'none';
            }}
            if (anagramCluesContainer) {{
                anagramCluesContainer.style.display = 'block';
            }}
            
            // Reset progress bar to zero for anagram grid
            document.querySelector('.progress-fill').style.width = '0%';
            document.querySelector('.progress-stats').innerHTML = 
                `<div>Cells filled: 0/64 (0.0%)</div>
                 <div>Clues solved: 0/24</div>`;
            
            // Show anagram fill button
            document.getElementById('dev-fill-anagram').style.display = 'inline-block';
            
            // Scroll to anagram grid section
            if (anagramGridSection) {{
                anagramGridSection.scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}
        
        function generateAnagramClues() {{
            // Create anagram clue objects from solved clues
            const solvedClues = [];
            for (const [clueId, clue] of Object.entries(clueObjects)) {{
                if (clue.possible_solutions.length === 1) {{
                    // This clue is solved, create anagram data
                    const originalSolution = clue.possible_solutions[0];
                    const anagramSolutions = generateAnagramSolutionsForClue(originalSolution, clue.length, clue.is_unclued);
                    
                    anagramClueObjects[`anagram_${{clueId}}`] = {{
                        'number': clue.number,
                        'direction': clue.direction,
                        'cell_indices': clue.cell_indices,
                        'length': clue.length,
                        'is_unclued': clue.is_unclued,
                        'possible_solutions': anagramSolutions,
                        'original_solution_count': anagramSolutions.length,
                        'original_solution': originalSolution,
                        'anagram_solutions': anagramSolutions
                    }};
                    solvedClues.push({{clueId, originalSolution, anagramSolutions}});
                }}
            }}
            
            // Apply constraint elimination to anagram solutions
            applyAnagramConstraints();
            
            // Generate HTML for anagram clues using the updated anagramClueObjects
            generateAnagramCluesHTMLFromObjects();
        }}
        
        function generateAnagramSolutionsForClue(originalSolution, length, isUnclued) {{
            const originalStr = originalSolution.toString().padStart(length, '0');
            const anagrams = new Set(); // Use Set to eliminate duplicates
            
            if (length === 2) {{
                // For 2-digit numbers, just swap the digits
                const swapped = originalStr[1] + originalStr[0];
                if (swapped !== originalStr) {{
                    anagrams.add(parseInt(swapped));
                }}
            }} else {{
                // Generate all permutations except the original
                const digits = originalStr.split('');
                const perms = generatePermutations(digits);
                
                for (const perm of perms) {{
                    const anagramStr = perm.join('');
                    if (anagramStr !== originalStr && anagramStr[0] !== '0') {{
                        const anagramNum = parseInt(anagramStr);
                        
                        if (isUnclued) {{
                            // For unclued clues, anagrams must be multiples of the original
                            if (anagramNum % originalSolution === 0) {{
                                anagrams.add(anagramNum);
                            }}
                        }} else {{
                            // For clued clues, any anagram is valid
                            anagrams.add(anagramNum);
                        }}
                    }}
                }}
            }}
            
            return Array.from(anagrams).sort((a, b) => a - b);
        }}
        
        function generatePermutations(arr) {{
            if (arr.length <= 1) return [arr];
            
            const perms = [];
            for (let i = 0; i < arr.length; i++) {{
                const current = arr[i];
                const remaining = arr.slice(0, i).concat(arr.slice(i + 1));
                const remainingPerms = generatePermutations(remaining);
                
                for (const perm of remainingPerms) {{
                    perms.push([current, ...perm]);
                }}
            }}
            
            return perms;
        }}
        
        function applyAnagramConstraints() {{
            // Apply constraint elimination to anagram solutions with a more balanced approach
            for (const [anagramClueId, anagramClue] of Object.entries(anagramClueObjects)) {{
                const originalClueId = anagramClueId.replace('anagram_', '');
                const originalClue = clueObjects[originalClueId];
                
                if (!originalClue) continue;
                
                // For the anagram stage, we want to provide more choice to the user
                // Only apply constraints if there are already solved cells in the anagram grid AND constraints are enabled
                const hasSolvedAnagramCells = Object.keys(anagramSolvedCells).length > 0;
                
                if (hasSolvedAnagramCells && anagramConstraintsEnabled) {{
                    // Get available digits from crossing clues that are already solved
                    const availableDigits = getAvailableDigitsForAnagramClue(anagramClueId);
                    
                    // Filter anagram solutions based on available digits
                    const validAnagrams = [];
                    for (const anagram of anagramClue.anagram_solutions) {{
                        if (isAnagramValidWithConstraints(anagram, anagramClue, availableDigits)) {{
                            validAnagrams.push(anagram);
                        }}
                    }}
                    
                    // Update the anagram clue with filtered solutions
                    anagramClue.anagram_solutions = validAnagrams;
                    anagramClue.possible_solutions = validAnagrams;
                    
                    console.log(`Anagram clue ${{anagramClueId}}: ${{anagramClue.original_solution_count}} -> ${{validAnagrams.length}} valid anagrams (with constraints)`);
                }} else {{
                    // No solved cells yet - show all anagram solutions to give user choice
                    anagramClue.anagram_solutions = anagramClue.anagram_solutions || [];
                    anagramClue.possible_solutions = anagramClue.anagram_solutions;
                    
                    console.log(`Anagram clue ${{anagramClueId}}: ${{anagramClue.anagram_solutions.length}} anagrams available (no constraints yet)`);
                }}
            }}
        }}
        
        function getAvailableDigitsForAnagramClue(anagramClueId) {{
            const originalClueId = anagramClueId.replace('anagram_', '');
            const anagramClue = anagramClueObjects[anagramClueId];
            const originalClue = clueObjects[originalClueId];
            
            if (!anagramClue || !originalClue) return {{}};
            
            const availableDigits = {{}};
            
            // For each cell position in the anagram clue
            for (let i = 0; i < anagramClue.cell_indices.length; i++) {{
                const cellIndex = anagramClue.cell_indices[i];
                const availableDigitsForCell = new Set();
                
                // Find all clues that use this cell
                for (const [otherClueId, otherClue] of Object.entries(clueObjects)) {{
                    if (otherClueId !== originalClueId && otherClue.cell_indices.includes(cellIndex)) {{
                        // This is a crossing clue - get its anagram solutions
                        const crossingAnagramClueId = `anagram_${{otherClueId}}`;
                        const crossingAnagramClue = anagramClueObjects[crossingAnagramClueId];
                        
                        if (crossingAnagramClue) {{
                            // Get all possible digits at this position from crossing anagram solutions
                            for (const anagramSolution of crossingAnagramClue.anagram_solutions) {{
                                const anagramStr = anagramSolution.toString().padStart(crossingAnagramClue.length, '0');
                                const digitAtPosition = anagramStr[otherClue.cell_indices.indexOf(cellIndex)];
                                availableDigitsForCell.add(parseInt(digitAtPosition));
                            }}
                        }}
                    }}
                }}
                
                // If no crossing clues found, all digits are available
                if (availableDigitsForCell.size === 0) {{
                    for (let digit = 0; digit <= 9; digit++) {{
                        availableDigitsForCell.add(digit);
                    }}
                }}
                
                availableDigits[i] = Array.from(availableDigitsForCell);
            }}
            
            return availableDigits;
        }}
        
        function isAnagramValidWithConstraints(anagram, anagramClue, availableDigits) {{
            const anagramStr = anagram.toString().padStart(anagramClue.length, '0');
            
            // Check each digit position
            for (let i = 0; i < anagramClue.length; i++) {{
                const digit = parseInt(anagramStr[i]);
                const availableForPosition = availableDigits[i];
                
                if (!availableForPosition.includes(digit)) {{
                    return false;
                }}
            }}
            
            return true;
        }}
        
        function propagateAnagramConstraints(clueId, solution) {{
            const eliminatedSolutions = [];
            const anagramClue = anagramClueObjects[clueId];
            const originalClueId = clueId.replace('anagram_', '');
            const originalClue = clueObjects[originalClueId];
            
            if (!anagramClue || !originalClue) return eliminatedSolutions;
            
            const solutionStr = solution.toString().padStart(anagramClue.length, '0');
            
            // Find all anagram clues that share cells with this clue
            const crossingAnagramClues = [];
            for (const [otherAnagramClueId, otherAnagramClue] of Object.entries(anagramClueObjects)) {{
                if (otherAnagramClueId !== clueId) {{
                    // Check if any cells overlap
                    const overlap = anagramClue.cell_indices.filter(cell => 
                        otherAnagramClue.cell_indices.includes(cell)
                    );
                    if (overlap.length > 0) {{
                        crossingAnagramClues.push(otherAnagramClueId);
                    }}
                }}
            }}
            
            // Eliminate incompatible anagram solutions from crossing clues
            for (const crossingAnagramClueId of crossingAnagramClues) {{
                const crossingAnagramClue = anagramClueObjects[crossingAnagramClueId];
                const solutionsToRemove = [];
                
                for (const possibleAnagram of crossingAnagramClue.anagram_solutions) {{
                    const possibleStr = possibleAnagram.toString().padStart(crossingAnagramClue.length, '0');
                    let incompatible = false;
                    
                    // Check each cell position
                    for (let i = 0; i < crossingAnagramClue.cell_indices.length; i++) {{
                        const cellIndex = crossingAnagramClue.cell_indices[i];
                        const digit = parseInt(possibleStr[i]);
                        
                        // If this cell is already solved in the anagram grid, check compatibility
                        if (cellIndex in anagramSolvedCells) {{
                            if (anagramSolvedCells[cellIndex] !== digit) {{
                                incompatible = true;
                                break;
                            }}
                        }}
                    }}
                    
                    if (incompatible) {{
                        solutionsToRemove.push(possibleAnagram);
                    }}
                }}
                
                // Remove incompatible solutions
                for (const solutionToRemove of solutionsToRemove) {{
                    crossingAnagramClue.anagram_solutions = crossingAnagramClue.anagram_solutions.filter(s => s !== solutionToRemove);
                    crossingAnagramClue.possible_solutions = crossingAnagramClue.possible_solutions.filter(s => s !== solutionToRemove);
                    eliminatedSolutions.push({{clueId: crossingAnagramClueId, solution: solutionToRemove}});
                }}
            }}
            
            return eliminatedSolutions;
        }}
        
        function generateAnagramCluesHTML(solvedClues) {{
            // Separate clues by direction
            const acrossClues = solvedClues.filter(c => c.clueId.includes('_ACROSS'));
            const downClues = solvedClues.filter(c => c.clueId.includes('_DOWN'));
            
            // Generate across clues HTML
            const acrossContainer = document.getElementById('anagram-across-clues');
            if (acrossContainer) {{
                acrossContainer.innerHTML = '';
                for (const clue of acrossClues) {{
                    const clueId = `anagram_${{clue.clueId}}`;
                    const clueNumber = clue.clueId.split('_')[0];
                    
                    // Determine CSS class based on anagram count
                    let statusClass = '';
                    if (clue.anagramSolutions.length > 1) {{
                        statusClass = 'multiple'; // Multiple anagrams available
                    }} else if (clue.anagramSolutions.length === 1) {{
                        statusClass = ''; // Default state
                    }} else {{
                        statusClass = 'unclued'; // No anagrams available
                    }}
                    
                    const clueHTML = `
                        <div class="clue anagram-clue ${{statusClass}}" data-clue="${{clueId}}" data-grid-type="anagram">
                            <div class="clue-header">
                                <span class="clue-number">${{clueNumber}}.</span>
                                <span class="clue-text">${{clue.originalSolution}}</span>
                                <span class="solution-count">${{clue.anagramSolutions.length}} ${{clue.anagramSolutions.length === 1 ? 'anagram' : 'anagrams'}}</span>
                            </div>
                            ${{clue.anagramSolutions.length > 0 ? `
                                <div class="solution-dropdown" id="dropdown-${{clueId}}" style="display: none;">
                                    <select class="solution-select" data-clue="${{clueId}}">
                                        <option value="">-- Select an anagram --</option>
                                        ${{clue.anagramSolutions.map(anagram => `<option value="${{anagram}}">${{anagram}}</option>`).join('')}}
                                    </select>
                                    <button class="apply-solution" data-clue="${{clueId}}">Apply</button>
                                </div>
                            ` : ''}}
                        </div>
                    `;
                    acrossContainer.innerHTML += clueHTML;
                }}
            }}
            
            // Generate down clues HTML
            const downContainer = document.getElementById('anagram-down-clues');
            if (downContainer) {{
                downContainer.innerHTML = '';
                for (const clue of downClues) {{
                    const clueId = `anagram_${{clue.clueId}}`;
                    const clueNumber = clue.clueId.split('_')[0];
                    
                    // Determine CSS class based on anagram count
                    let statusClass = '';
                    if (clue.anagramSolutions.length > 1) {{
                        statusClass = 'multiple'; // Multiple anagrams available
                    }} else if (clue.anagramSolutions.length === 1) {{
                        statusClass = ''; // Default state
                    }} else {{
                        statusClass = 'unclued'; // No anagrams available
                    }}
                    
                    const clueHTML = `
                        <div class="clue anagram-clue ${{statusClass}}" data-clue="${{clueId}}" data-grid-type="anagram">
                            <div class="clue-header">
                                <span class="clue-number">${{clueNumber}}.</span>
                                <span class="clue-text">${{clue.originalSolution}}</span>
                                <span class="solution-count">${{clue.anagramSolutions.length}} ${{clue.anagramSolutions.length === 1 ? 'anagram' : 'anagrams'}}</span>
                            </div>
                            ${{clue.anagramSolutions.length > 0 ? `
                                <div class="solution-dropdown" id="dropdown-${{clueId}}" style="display: none;">
                                    <select class="solution-select" data-clue="${{clueId}}">
                                        <option value="">-- Select an anagram --</option>
                                        ${{clue.anagramSolutions.map(anagram => `<option value="${{anagram}}">${{anagram}}</option>`).join('')}}
                                    </select>
                                    <button class="apply-solution" data-clue="${{clueId}}">Apply</button>
                                </div>
                            ` : ''}}
                        </div>
                    `;
                    downContainer.innerHTML += clueHTML;
                }}
            }}
        }}
        
        function generateAnagramCluesHTMLFromObjects() {{
            // Generate HTML using the updated anagramClueObjects (after constraint elimination)
            const acrossClues = [];
            const downClues = [];
            
            for (const [clueId, clue] of Object.entries(anagramClueObjects)) {{
                if (clue.direction === 'ACROSS') {{
                    acrossClues.push({{clueId, clue}});
                }} else {{
                    downClues.push({{clueId, clue}});
                }}
            }}
            
            // Sort by clue number
            acrossClues.sort((a, b) => a.clue.number - b.clue.number);
            downClues.sort((a, b) => a.clue.number - b.clue.number);
            
            // Generate across clues HTML
            const acrossContainer = document.getElementById('anagram-across-clues');
            if (acrossContainer) {{
                acrossContainer.innerHTML = '';
                for (const {{clueId, clue}} of acrossClues) {{
                    const clueNumber = clue.number;
                    
                    // Determine CSS class based on filtered anagram count
                    let statusClass = '';
                    if (clue.anagram_solutions.length > 1) {{
                        statusClass = 'multiple'; // Multiple anagrams available
                    }} else if (clue.anagram_solutions.length === 1) {{
                        statusClass = ''; // Default state
                    }} else {{
                        statusClass = 'unclued'; // No anagrams available
                    }}
                    
                    const clueHTML = `
                        <div class="clue anagram-clue ${{statusClass}}" data-clue="${{clueId}}" data-grid-type="anagram">
                            <div class="clue-header">
                                <span class="clue-number">${{clueNumber}}.</span>
                                <span class="clue-text">${{clue.original_solution}}</span>
                                <span class="solution-count">${{clue.anagram_solutions.length}} ${{clue.anagram_solutions.length === 1 ? 'anagram' : 'anagrams'}}</span>
                            </div>
                            ${{clue.anagram_solutions.length > 0 ? `
                                <div class="solution-dropdown" id="dropdown-${{clueId}}" style="display: none;">
                                    <select class="solution-select" data-clue="${{clueId}}">
                                        <option value="">-- Select an anagram --</option>
                                        ${{clue.anagram_solutions.map(anagram => `<option value="${{anagram}}">${{anagram}}</option>`).join('')}}
                                    </select>
                                    <button class="apply-solution" data-clue="${{clueId}}">Apply</button>
                                </div>
                            ` : ''}}
                        </div>
                    `;
                    acrossContainer.innerHTML += clueHTML;
                }}
            }}
            
            // Generate down clues HTML
            const downContainer = document.getElementById('anagram-down-clues');
            if (downContainer) {{
                downContainer.innerHTML = '';
                for (const {{clueId, clue}} of downClues) {{
                    const clueNumber = clue.number;
                    
                    // Determine CSS class based on filtered anagram count
                    let statusClass = '';
                    if (clue.anagram_solutions.length > 1) {{
                        statusClass = 'multiple'; // Multiple anagrams available
                    }} else if (clue.anagram_solutions.length === 1) {{
                        statusClass = ''; // Default state
                    }} else {{
                        statusClass = 'unclued'; // No anagrams available
                    }}
                    
                    const clueHTML = `
                        <div class="clue anagram-clue ${{statusClass}}" data-clue="${{clueId}}" data-grid-type="anagram">
                            <div class="clue-header">
                                <span class="clue-number">${{clueNumber}}.</span>
                                <span class="clue-text">${{clue.original_solution}}</span>
                                <span class="solution-count">${{clue.anagram_solutions.length}} ${{clue.anagram_solutions.length === 1 ? 'anagram' : 'anagrams'}}</span>
                            </div>
                            ${{clue.anagram_solutions.length > 0 ? `
                                <div class="solution-dropdown" id="dropdown-${{clueId}}" style="display: none;">
                                    <select class="solution-select" data-clue="${{clueId}}">
                                        <option value="">-- Select an anagram --</option>
                                        ${{clue.anagram_solutions.map(anagram => `<option value="${{anagram}}">${{anagram}}</option>`).join('')}}
                                    </select>
                                    <button class="apply-solution" data-clue="${{clueId}}">Apply</button>
                                </div>
                            ` : ''}}
                        </div>
                    `;
                    downContainer.innerHTML += clueHTML;
                }}
            }}
        }}
        
        function hideAnagramGrid() {{
            // Hide anagram clues, show initial clues
            const initialCluesContainer = document.getElementById('initial-clues-container');
            const anagramCluesContainer = document.getElementById('anagram-clues-container');
            if (initialCluesContainer) {{
                initialCluesContainer.style.display = 'block';
            }}
            if (anagramCluesContainer) {{
                anagramCluesContainer.style.display = 'none';
            }}
            // Do NOT hide either grid
            // const anagramGridSection = document.getElementById('anagram-grid-section');
            // if (anagramGridSection) {{
            //     anagramGridSection.style.display = 'none';
            // }}
            // const initialGridSection = document.getElementById('initial-grid-section');
            // if (initialGridSection) {{
            //     initialGridSection.style.display = 'block';
            // }}
        }}
        
        function toggleAnagramMode() {{
            const initialCluesContainer = document.getElementById('initial-clues-container');
            const anagramCluesContainer = document.getElementById('anagram-clues-container');
            const toggleButton = document.getElementById('dev-toggle-anagram');
            
            if (initialCluesContainer && anagramCluesContainer) {{
                const isAnagramMode = anagramCluesContainer.style.display === 'block';
                
                if (isAnagramMode) {{
                    // Switch to initial mode
                    initialCluesContainer.style.display = 'block';
                    anagramCluesContainer.style.display = 'none';
                    toggleButton.textContent = 'Toggle Anagram Mode';
                    toggleButton.style.backgroundColor = '#17a2b8';
                    // Hide anagram fill button
                    document.getElementById('dev-fill-anagram').style.display = 'none';
                    // Switched to Initial Grid Mode
                    // Update progress for initial grid
                    updateProgress();
                }} else {{
                    // Switch to anagram mode
                    initialCluesContainer.style.display = 'none';
                    anagramCluesContainer.style.display = 'block';
                    toggleButton.textContent = 'Toggle Initial Mode';
                    toggleButton.style.backgroundColor = '#28a745';
                    // Show anagram fill button
                    document.getElementById('dev-fill-anagram').style.display = 'inline-block';
                    // Switched to Anagram Grid Mode
                    // Reset progress bar to zero for anagram grid
                    document.querySelector('.progress-fill').style.width = '0%';
                    document.querySelector('.progress-stats').innerHTML = 
                        `<div>Cells filled: 0/64 (0.0%)</div>
                         <div>Clues solved: 0/24</div>`;
                }}
            }}
        }}
        
        function toggleConstraints() {{
            anagramConstraintsEnabled = !anagramConstraintsEnabled;
            const toggleButton = document.getElementById('dev-toggle-constraints');
            
            if (anagramConstraintsEnabled) {{
                toggleButton.textContent = 'Constraints: ON';
                toggleButton.style.backgroundColor = '#6f42c1';
                // Anagram constraints enabled
            }} else {{
                toggleButton.textContent = 'Constraints: OFF';
                toggleButton.style.backgroundColor = '#dc3545';
                // Anagram constraints disabled
            }}
            
            // Regenerate anagram clues with new constraint setting
            if (Object.keys(anagramClueObjects).length > 0) {{
                applyAnagramConstraints();
                generateAnagramCluesHTMLFromObjects();
            }}
        }}
        
        function getFilteredCandidatesForClue(clueId) {{
            const clue = clueObjects[clueId];
            if (!clue || !clue.is_unclued) {{
                return [];
            }}
            
            // Use the embedded unclued candidates list (305 numbers that satisfy anagram/multiple constraint)
            const uncluedCandidates = [100035, 100089, 100350, 100449, 100890, 100899, 100989, 102249, 102375, 102564, 103428, 103500, 103845, 104490, 104499, 104769, 104895, 105264, 106254, 106749, 106848, 107235, 107583, 107793, 107892, 108726, 108900, 108990, 108999, 109890, 109899, 109989, 111873, 113724, 113967, 114237, 114528, 116397, 116688, 116880, 116988, 118731, 118830, 118833, 119883, 120267, 123507, 123714, 123750, 123876, 123975, 124137, 124875, 125406, 125604, 125874, 126054, 126702, 126873, 126888, 127389, 128034, 128052, 128205, 128574, 129003, 129030, 129033, 129903, 130029, 130149, 130290, 130299, 130329, 130869, 132159, 132903, 133029, 133359, 133449, 133590, 133599, 133659, 134490, 134499, 134505, 134739, 135045, 135900, 135990, 135999, 136590, 136599, 136659, 137124, 137241, 137286, 138402, 138456, 138546, 138600, 138627, 139860, 139986, 140085, 140184, 140247, 140256, 140526, 140850, 140985, 141237, 141858, 142371, 142470, 142497, 142587, 142857, 143505, 143793, 143856, 145035, 145281, 145386, 147024, 147240, 148257, 148509, 148590, 148599, 149085, 149724, 149859, 150192, 150345, 150435, 151893, 151920, 151992, 153846, 154269, 154386, 154896, 156282, 156942, 157284, 158427, 158598, 159786, 166782, 167604, 167802, 167820, 167832, 167982, 168027, 169728, 169782, 170268, 172575, 172968, 174285, 174825, 175257, 175725, 176004, 176034, 176040, 176049, 176604, 178002, 178020, 178200, 178302, 178320, 178332, 178437, 179487, 179802, 179820, 179832, 179982, 180027, 180267, 180270, 180327, 182703, 182973, 183027, 188547, 189657, 190476, 194787, 196587, 196728, 197280, 197283, 197298, 197328, 197604, 197802, 197820, 197832, 197982, 198027, 199728, 199782, 200178, 201678, 201780, 201783, 201798, 201978, 205128, 206793, 206856, 207693, 212805, 215628, 216678, 216780, 216783, 216798, 216978, 217800, 217830, 217833, 217980, 217983, 217998, 219780, 219783, 219798, 219978, 230679, 230769, 230895, 233958, 235071, 235107, 237114, 237141, 237501, 237510, 238095, 238761, 239508, 239580, 239583, 239598, 239658, 239751, 239958, 240147, 241137, 241371, 241470, 241497, 242748, 247014, 247140, 247428, 247500, 248274, 248760, 248976, 249714, 249750, 249876, 249975, 251757, 257175, 257517, 258714, 258741, 271584, 274248, 274824, 275850, 275886, 275985, 276489, 280341, 281034, 282474, 284157, 285714, 285741, 285750, 285876, 285975, 287586, 287649, 288576, 297585, 298575, 306792, 307692, 314379, 320679, 320769, 412587, 412857, 425871, 428571];
            const filteredCandidates = [];
            
            for (const candidate of uncluedCandidates) {{
                if (candidate.toString().length === clue.length) {{
                    // Check if this candidate conflicts with already solved cells
                    let conflicts = false;
                    const candidateStr = candidate.toString().padStart(clue.length, '0');
                    
                    for (let i = 0; i < clue.cell_indices.length; i++) {{
                        const cellIndex = clue.cell_indices[i];
                        if (cellIndex in solvedCells) {{
                            if (solvedCells[cellIndex] !== parseInt(candidateStr[i])) {{
                                conflicts = true;
                                break;
                            }}
                        }}
                    }}
                    
                    if (!conflicts) {{
                        filteredCandidates.push(candidate);
                    }}
                }}
            }}
            
            return filteredCandidates;
        }}
        

        
        function updateUncluedClueDisplays() {{
            // Update each unclued clue to show candidate count
            for (const [clueId, clue] of Object.entries(clueObjects)) {{
                if (clue.is_unclued) {{
                    const clueElement = document.querySelector(`[data-clue="${{clueId}}"]`);
                    const inputDiv = document.getElementById(`input-${{clueId}}`);
                    const dropdownDiv = document.getElementById(`dropdown-${{clueId}}`);
                    const countElement = document.getElementById(`unclued-count-${{clueId}}`);
                    
                    if (clueElement) {{
                        const candidates = getFilteredCandidatesForClue(clueId);
                        const candidateCount = candidates.length;
                        
                        // Update the count element (right-aligned, no parentheses, no italics)
                        if (countElement) {{
                            if (userSelectedSolutions.has(clueId)) {{
                                countElement.textContent = `Solved: ${{clue.possible_solutions[0]}}`;
                            }} else {{
                                countElement.textContent = `${{candidateCount}} ${{candidateCount === 1 ? 'candidate' : 'candidates'}}`;
                            }}
                        }}
                        
                        // Check if this clue has a user-selected solution
                        if (userSelectedSolutions.has(clueId)) {{
                            // Clue is solved - hide both input and dropdown
                            if (dropdownDiv) dropdownDiv.style.display = 'none';
                            if (inputDiv) inputDiv.style.display = 'none';
                        }} else {{
                            // Hide both input and dropdown - they'll show when clicked
                            if (dropdownDiv) dropdownDiv.style.display = 'none';
                            if (inputDiv) inputDiv.style.display = 'none';
                        }}
                    }}
                }}
            }}
        }}

        function showNotification(message, type) {{
            // Remove existing notifications
            const existing = document.querySelector('.notification');
            if (existing) {{
                existing.remove();
            }}
            
            // Create new notification
            const notification = document.createElement('div');
            notification.className = `notification ${{type}}`;
            notification.textContent = message;
            
            // Append to main-content instead of body
            const mainContent = document.querySelector('.main-content');
            if (mainContent) {{
                mainContent.appendChild(notification);
            }} else {{
                document.body.appendChild(notification);
            }}
            
            // Show notification
            setTimeout(() => {{
                notification.style.opacity = '1';
            }}, 10);
            
            // Hide notification after 3 seconds
            setTimeout(() => {{
                notification.style.opacity = '0';
                setTimeout(() => {{
                    if (notification.parentNode) {{
                        notification.remove();
                    }}
                }}, 300);
            }}, 3000);
        }}

        function showDeselectDialog(clueId) {{
            // Hide any existing dialogs
            document.querySelectorAll('.solution-dropdown, .solution-input, .deselect-dialog').forEach(d => {{
                d.style.display = 'none';
            }});
            
            const clue = clueObjects[clueId];
            const currentSolution = clue.possible_solutions[0];
            const solutionStr = currentSolution.toString().padStart(clue.length, '0');
            
            // Create deselect dialog
            const dialog = document.createElement('div');
            dialog.className = 'deselect-dialog';
            dialog.id = `deselect-${{clueId}}`;
            dialog.style.cssText = `
                margin-top: 8px;
                padding: 12px;
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                border-left: 4px solid #f39c12;
            `;
            
            dialog.innerHTML = `
                <div style="margin-bottom: 8px; font-weight: bold; color: #856404;">
                    Current solution: <span style="font-family: monospace;">${{solutionStr}}</span>
                </div>
                <div style="margin-bottom: 12px; color: #856404;">
                    Click "Deselect" to remove this solution and restore all possible solutions for this clue.
                </div>
                <button class="deselect-solution" data-clue="${{clueId}}" style="
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                    margin-right: 8px;
                ">Deselect Solution</button>
                <button class="cancel-deselect" style="
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                ">Cancel</button>
            `;
            
            // Find the clue element and append the dialog
            const clueElement = document.querySelector(`[data-clue="${{clueId}}"]`);
            if (clueElement) {{
                clueElement.appendChild(dialog);
                
                // Add event listeners
                dialog.querySelector('.deselect-solution').addEventListener('click', function(e) {{
                    e.stopPropagation();
                    deselectSolution(clueId);
                }});
                
                dialog.querySelector('.cancel-deselect').addEventListener('click', function(e) {{
                    e.stopPropagation();
                    dialog.style.display = 'none';
                }});
            }}
        }}

        function deselectSolution(clueId) {{
            console.log(`Deselecting solution for clue ${{clueId}}`);
            
            // Save current state before deselecting
            saveState(clueId, 'DESELECT');
            
            // Check if this is an anagram clue
            const isAnagramClue = clueId.startsWith('anagram_');
            
            if (isAnagramClue) {{
                // Handle anagram clue deselection
                const anagramClue = anagramClueObjects[clueId];
                if (!anagramClue) {{
                    showNotification('Anagram clue not found', 'error');
                    return;
                }}
                
                const currentSolution = anagramClue.possible_solutions[0];
                const solutionStr = currentSolution.toString().padStart(anagramClue.length, '0');
                
                // Remove the solution from the anagram grid cells
                for (let i = 0; i < anagramClue.cell_indices.length; i++) {{
                    const cellIndex = anagramClue.cell_indices[i];
                    
                    // Check if this cell is used by other user-selected anagram clues
                    let canRemoveCell = true;
                    for (const [otherClueId, otherClue] of Object.entries(anagramClueObjects)) {{
                        if (otherClueId !== clueId && anagramUserSelectedSolutions.has(otherClueId)) {{
                            if (otherClue.cell_indices.includes(cellIndex)) {{
                                canRemoveCell = false;
                                break;
                            }}
                        }}
                    }}
                    
                    if (canRemoveCell) {{
                        delete anagramSolvedCells[cellIndex];
                        
                        // Clear the anagram cell display
                        const cell = document.querySelector(`[data-cell="${{cellIndex}}"][data-anagram="true"]`);
                        if (cell) {{
                            const valueElement = cell.querySelector('.cell-value');
                            if (valueElement) {{
                                valueElement.remove();
                            }}
                        }}
                    }}
                }}
                
                // Remove from anagram user-selected solutions
                anagramUserSelectedSolutions.delete(clueId);
                
                // Restore original anagram solutions for the deselected clue
                const originalAnagramSolutions = anagramClue.anagram_solutions || [];
                anagramClue.possible_solutions = [...originalAnagramSolutions];
                
                // Update anagram clue displays
                updateAnagramClueDisplays();
                
                // Show success message
                const restoredCount = anagramClue.possible_solutions.length;
                showNotification(`Deselected anagram solution for clue ${{clueId}}. Restored ${{restoredCount}} possible anagrams.`, 'success');
                
            }} else {{
                // Handle initial clue deselection (existing logic)
                const clue = clueObjects[clueId];
                const currentSolution = clue.possible_solutions[0];
                
                // Remove the solution from the grid cells
                const solutionStr = currentSolution.toString().padStart(clue.length, '0');
                for (let i = 0; i < clue.cell_indices.length; i++) {{
                    const cellIndex = clue.cell_indices[i];
                    
                    // Check if this cell is used by other user-selected clues
                    let canRemoveCell = true;
                    for (const [otherClueId, otherClue] of Object.entries(clueObjects)) {{
                        if (otherClueId !== clueId && userSelectedSolutions.has(otherClueId)) {{
                            if (otherClue.cell_indices.includes(cellIndex)) {{
                                canRemoveCell = false;
                                break;
                            }}
                        }}
                    }}
                    
                    if (canRemoveCell) {{
                        delete solvedCells[cellIndex];
                        
                        // Clear the cell display
                        const cell = document.querySelector(`[data-cell="${{cellIndex}}"]`);
                        if (cell) {{
                            const valueElement = cell.querySelector('.cell-value');
                            if (valueElement) {{
                                valueElement.remove();
                            }}
                        }}
                    }}
                }}
                
                // Remove from user-selected solutions BEFORE recalculating constraints
                userSelectedSolutions.delete(clueId);
                
                // Explicitly restore original solutions for the deselected clue
                const originalCount = clue.original_solution_count || 0;
                console.log(`Restoring original solutions for ${{clueId}}: original count = ${{originalCount}}`);
                
                // Restore from stored original solutions
                if (originalSolutions[clueId]) {{
                    clue.possible_solutions = [...originalSolutions[clueId]]; // Deep copy
                    console.log(`Restored original solutions for ${{clueId}}:`, originalSolutions[clueId]);
                }} else {{
                    console.log(`No original solutions found for ${{clueId}}`);
                    clue.possible_solutions = [];
                }}
                
                // Recalculate constraints for all OTHER clues (not the deselected one)
                recalculateAllConstraintsExcept(clueId);
                
                // Update all clue displays
                updateAllClueDisplays();
                
                // Show success message
                const restoredCount = clue.possible_solutions.length;
                showNotification(`Deselected solution for clue ${{clueId}}. Restored ${{restoredCount}} possible solutions.`, 'success');
            }}
            
            // Update progress
            updateProgress();
            
            // Hide the deselect dialog
            const dialog = document.getElementById(`deselect-${{clueId}}`);
            if (dialog) {{
                dialog.style.display = 'none';
            }}
        }}

        function recalculateAllConstraintsExcept(excludeClueId) {{
            // Recalculate constraints based on current solved cells, excluding the specified clue
            for (const [clueId, clue] of Object.entries(clueObjects)) {{
                // Skip the excluded clue and clues that have user-selected solutions
                if (clueId === excludeClueId || userSelectedSolutions.has(clueId)) continue;
                
                // Get original solutions for this clue from our stored original solutions
                const clueOriginalSolutions = originalSolutions[clueId] || [];
                const validSolutions = [];
                
                // Check each original solution against current grid state
                for (const solution of clueOriginalSolutions) {{
                    const solutionInt = parseInt(solution);
                    const solutionStr = solutionInt.toString().padStart(clue.length, '0');
                    let isValid = true;
                    
                    // Check each cell position
                    for (let i = 0; i < clue.cell_indices.length; i++) {{
                        const cellIndex = clue.cell_indices[i];
                        const digit = parseInt(solutionStr[i]);
                        
                        // If this cell is already solved, check compatibility
                        if (cellIndex in solvedCells) {{
                            if (solvedCells[cellIndex] !== digit) {{
                                isValid = false;
                                break;
                            }}
                        }}
                    }}
                    
                    if (isValid) {{
                        validSolutions.push(solutionInt);
                    }}
                }}
                
                // Update the clue's possible solutions
                clue.possible_solutions = validSolutions;
            }}
        }}

        function recalculateAllConstraints() {{
            // Recalculate constraints for all clues (used for undo operations)
            for (const [clueId, clue] of Object.entries(clueObjects)) {{
                // Skip clues that have user-selected solutions
                if (userSelectedSolutions.has(clueId)) continue;
                
                // Get original solutions for this clue from our stored original solutions
                const clueOriginalSolutions = originalSolutions[clueId] || [];
                const validSolutions = [];
                
                // Check each original solution against current grid state
                for (const solution of clueOriginalSolutions) {{
                    const solutionInt = parseInt(solution);
                    const solutionStr = solutionInt.toString().padStart(clue.length, '0');
                    let isValid = true;
                    
                    // Check each cell position
                    for (let i = 0; i < clue.cell_indices.length; i++) {{
                        const cellIndex = clue.cell_indices[i];
                        const digit = parseInt(solutionStr[i]);
                        
                        // If this cell is already solved, check compatibility
                        if (cellIndex in solvedCells) {{
                            if (solvedCells[cellIndex] !== digit) {{
                                isValid = false;
                                break;
                            }}
                        }}
                    }}
                    
                    if (isValid) {{
                        validSolutions.push(solutionInt);
                    }}
                }}
                
                // Update the clue's possible solutions
                clue.possible_solutions = validSolutions;
            }}
        }}
        
        // Developer functions for quick testing
        function fill14A() {{
            // Fill in clue 14A (unclued) with the known solution
            const solution = '142857';
            applySolutionToGrid('14_ACROSS', solution);
                            showNotification('Filled 14A with solution 142857', 'success');
        }}
        
        function fillCompleteGrid() {{
            // Fill the complete grid with actual known solutions for testing
            const knownSolutions = {{
                '1_ACROSS': '3375', // Known solution
                '1_DOWN': '3249', // Known solution
                '2_DOWN': '35', // Known solution
                '3_DOWN': '7776',    // From test file - 10:1 constraint
                '4_ACROSS': '5254',  // From solution_sets.json
                '5_DOWN': '2048',    // From solution_sets.json - 11:0 constraint
                '6_DOWN': '4207',    // From solution_sets.json
                '7_DOWN': '137241',  // From test file - actual unclued solution
                '8_DOWN': '119883', // Known solution
                '9_ACROSS': '72', // Known solution
                '10_ACROSS': '4173', // Known solution
                '11_ACROSS': '1430', // Known solution
                '12_ACROSS': '167982', // Known solution
                '13_DOWN': '5132', // Known solution
                '14_ACROSS': '142857', // Known solution
                '15_DOWN': '4225', // Known solution
                '16_DOWN': '5642', // Known solution
                '17_DOWN': '2401',   // From solution_sets.json
                '18_ACROSS': '1024', // From solution_sets.json
                '19_ACROSS': '8624', // Known solution
                '20_ACROSS': '32',   // From solution_sets.json
                '21_DOWN': '16', // Known solution
                '22_ACROSS': '2858', // Known solution
                '23_ACROSS': '9261', // Known solution
            }};
            
            // Apply each solution
            for (const [clueId, solution] of Object.entries(knownSolutions)) {{
                const clue = clueObjects[clueId];
                if (clue && solution.length === clue.length) {{
                    console.log(`Applying solution ${{solution}} to clue ${{clueId}}`);
                    applySolutionToGrid(clueId, solution);
                }} else {{
                    console.log(`Skipping clue ${{clueId}} - not found or length mismatch`);
                }}
            }}
            
                            showNotification('Filled grid with actual known solutions only', 'success');
        }}
        
        function fillAnagramGrid() {{
            // Fill the anagram grid with known anagram solutions for testing
            const knownAnagramSolutions = {{
                'anagram_1_ACROSS': '3573', // Anagram of 3375
                'anagram_1_DOWN': '3942', // Anagram of 3249
                'anagram_2_DOWN': '53', // Anagram of 35
                'anagram_3_DOWN': '7677', // Anagram of 7776
                'anagram_4_ACROSS': '5452', // Anagram of 5254
                'anagram_5_DOWN': '4802', // Anagram of 2048
                'anagram_6_DOWN': '2740', // Anagram of 4207
                'anagram_7_DOWN': '411723', // Anagram of 137241 (multiple of original)
                'anagram_8_DOWN': '839181', // Anagram of 119883
                'anagram_9_ACROSS': '27', // Anagram of 72
                'anagram_10_ACROSS': '4371', // Anagram of 4173
                'anagram_11_ACROSS': '3014', // Anagram of 1430
                'anagram_12_ACROSS': '671928', // Anagram of 167982
                'anagram_13_DOWN': '3125', // Anagram of 5132
                'anagram_14_ACROSS': '857142', // Anagram of 142857 (multiple of original)
                'anagram_15_DOWN': '5422', // Anagram of 4225
                'anagram_16_DOWN': '4256', // Anagram of 5642
                'anagram_17_DOWN': '1402', // Anagram of 2401 (same)
                'anagram_18_ACROSS': '1042', // Anagram of 1024 (same)
                'anagram_19_ACROSS': '8264', // Anagram of 8624
                'anagram_20_ACROSS': '23', // Anagram of 32
                'anagram_21_DOWN': '61', // Anagram of 16
                'anagram_22_ACROSS': '5828', // Anagram of 2858 (same)
                'anagram_23_ACROSS': '9612', // Anagram of 9261
            }};
            
            // First, make sure we have anagram clues generated
            if (Object.keys(anagramClueObjects).length === 0) {{
                generateAnagramClues();
            }}
            
            // Apply each anagram solution
            for (const [clueId, solution] of Object.entries(knownAnagramSolutions)) {{
                const anagramClue = anagramClueObjects[clueId];
                if (anagramClue && solution.length === anagramClue.length) {{
                    console.log(`Applying anagram solution ${{solution}} to clue ${{clueId}}`);
                    applySolutionToGrid(clueId, solution);
                }} else {{
                    console.log(`Skipping anagram clue ${{clueId}} - not found or length mismatch`);
                }}
            }}
            
                            showNotification('Filled anagram grid with known anagram solutions', 'success');
        }}

        // Add this function after updateAllClueDisplays
        function updateAnagramClueDisplays() {{
            // Update each anagram clue's display based on current state
            for (const [clueId, clue] of Object.entries(anagramClueObjects)) {{
                const clueElement = document.querySelector(`[data-clue="${{clueId}}"]`);
                if (!clueElement) continue;
                
                // Update the clue text to show selected solution or original
                const textElement = clueElement.querySelector('.clue-text');
                if (textElement) {{
                    if (anagramUserSelectedSolutions.has(clueId)) {{
                        // Show the selected anagram solution
                        const selectedSolution = clue.possible_solutions[0];
                        textElement.textContent = selectedSolution;
                    }} else {{
                        // Show the original solution
                        textElement.textContent = clue.original_solution;
                    }}
                }}
                
                        // Update the count text
        const countElement = clueElement.querySelector('.solution-count');
        if (countElement) {{
            if (anagramUserSelectedSolutions.has(clueId)) {{
                countElement.textContent = 'Selected';
            }} else {{
                // Show count of anagrams (singular when only one)
                const anagramText = clue.anagram_solutions.length === 1 ? 'anagram' : 'anagrams';
                countElement.textContent = `${{clue.anagram_solutions.length}} ${{anagramText}}`;
            }}
        }}
                
                // Remove all status classes and apply correct one
                clueElement.className = 'clue anagram-clue';
                if (anagramUserSelectedSolutions.has(clueId)) {{
                    clueElement.classList.add('user-selected');
                }} else if (clue.anagram_solutions && clue.anagram_solutions.length > 1) {{
                    clueElement.classList.add('multiple');
                }} else if (clue.anagram_solutions && clue.anagram_solutions.length === 0) {{
                    clueElement.classList.add('unclued');
                }}
                
                // Update dropdown options if it exists
                const dropdownDiv = document.getElementById(`dropdown-${{clueId}}`);
                if (dropdownDiv) {{
                    const select = dropdownDiv.querySelector('.solution-select');
                    if (select) {{
                        // Keep the first option (placeholder) and update only the solution options
                        const placeholderOption = select.querySelector('option[value=""]');
                        select.innerHTML = '';
                        
                        // Restore the placeholder option
                        if (placeholderOption) {{
                            select.appendChild(placeholderOption);
                        }} else {{
                            const newPlaceholder = document.createElement('option');
                            newPlaceholder.value = '';
                            newPlaceholder.textContent = '-- Select an anagram --';
                            select.appendChild(newPlaceholder);
                        }}
                        
                        // Add the anagram solution options
                        for (const solution of clue.anagram_solutions) {{
                            const option = document.createElement('option');
                            option.value = solution;
                            option.textContent = solution.toString().padStart(clue.length, '0');
                            select.appendChild(option);
                        }}
                        
                        console.log(`Updated anagram dropdown for ${{clueId}} with ${{clue.anagram_solutions.length}} solutions`);
                    }}
                }}
            }}
        }}

        // Modal system
        function createModal(id, title, content, buttons) {{
            const existingModal = document.getElementById(id);
            if (existingModal) {{
                existingModal.remove();
            }}
            const modal = document.createElement('div');
            modal.id = id;
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 10000;
                animation: fadeIn 0.5s ease-in;
            `;
            if (!document.getElementById('modal-animations')) {{
                const style = document.createElement('style');
                style.id = 'modal-animations';
                style.textContent = `
                    @keyframes fadeIn {{
                        from {{ opacity: 0; }}
                        to {{ opacity: 1; }}
                    }}
                    @keyframes slideIn {{
                        from {{ transform: translateY(-50px); opacity: 0; }}
                        to {{ transform: translateY(0); opacity: 1; }}
                    }}
                    @keyframes subtleGlow {{
                        0% {{ box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
                        50% {{ box-shadow: 0 20px 40px rgba(0,0,0,0.3), 0 0 30px rgba(40, 167, 69, 0.3); }}
                        100% {{ box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
                    }}
                    
                    /* Mobile-specific modal styles */
                    @media (max-width: 768px) {{
                        .modal-content {{
                            max-height: 85vh !important;
                            margin: 10px !important;
                            padding: 20px !important;
                        }}
                    }}
                    
                    @media (max-width: 480px) {{
                        .modal-content {{
                            max-height: 90vh !important;
                            margin: 5px !important;
                            padding: 15px !important;
                        }}
                    }}
                `;
                document.head.appendChild(style);
            }}
            modal.innerHTML = `
                <div class="modal-content" style="
                    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                    color: white;
                    padding: 40px;
                    border-radius: 12px;
                    text-align: center;
                    max-width: 600px;
                    max-height: 80vh;
                    margin: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                    animation: slideIn 0.6s ease-out;
                    position: relative;
                    overflow-y: auto;
                    overflow-x: hidden;
                    border: 1px solid #495057;
                    box-sizing: border-box;
                    -webkit-overflow-scrolling: touch;
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        height: 4px;
                        background: linear-gradient(90deg, #28a745, #17a2b8, #007bff);
                        z-index: 1;
                    "></div>
                    <h1 style="font-size: 2.2em; margin: 0 0 20px 0; color: #e9ecef; font-weight: 300; letter-spacing: 1px;">
                        ${{title}}
                    </h1>
                    ${{content}}
                    <div style="margin-top: 30px;">
                        ${{buttons}}
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            if (id.includes('celebration')) {{
                // Add subtle glow animation for celebrations
                const modalContent = modal.querySelector('div');
                modalContent.style.animation = 'slideIn 0.6s ease-out, subtleGlow 3s ease-in-out infinite';
            }}
        }}

        function hideModal(modalId) {{
            const modal = document.getElementById(modalId);
            if (modal) {{
                modal.style.animation = 'fadeIn 0.5s ease-in reverse';
                setTimeout(() => {{
                    if (modal.parentNode) {{
                        modal.remove();
                    }}
                    // Scroll to top after intro modal is dismissed
                    if (modalId === 'intro-modal') {{
                        window.scrollTo(0, 0);
                    }}
                }}, 500);
            }}
        }}

        function showIntroModal() {{
            const title = '🧩 Welcome to the Listener Crossword Solver 🧩';
            const content = `
                <div style="background: rgba(255,255,255,0.08);padding: 20px;border-radius: 8px;margin: 20px 0;border: 1px solid rgba(255,255,255,0.1);">
                    <h3 style="margin: 0 0 15px 0; color: #28a745; font-weight: 500; font-size: 1.3em;">The Prime Factor Challenge</h3>
                    <p style="margin: 0 0 15px 0; line-height: 1.6; color: #e9ecef;">
                        Welcome to the first stage of this mathematical crossword puzzle. 
                        Your goal is to fill in the grid with numbers that satisfy specific mathematical constraints.
                    </p>
                    <div style="background: rgba(40, 167, 69, 0.15);padding: 15px;border-radius: 8px;border-left: 4px solid #28a745;text-align: center;font-style: normal;color: #e9ecef;">
                        <strong style="color: #28a745;">How to Play:</strong><br>
                        • <strong>Clued entries</strong> in "a:b" format where a= no. of prime factors of solution and b= difference between largest and smallest factor<br>
                        • <strong>Unclued entries</strong> form an anagram of themselves in the final grid when multiplied by an integer<br>
                        • <strong>Mathematical Key:</strong> Look a key among the unclued entries - there's a special cyclic number that could be key to solving the puzzle
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.08);padding: 20px;border-radius: 8px;margin: 20px 0;border: 1px solid rgba(255,255,255,0.1);">
                    <h3 style="margin: 0 0 15px 0; color: #17a2b8; font-weight: 500; font-size: 1.3em;">Playing Tips</h3>
                    <ul style="margin: 0; padding-left: 0; list-style: none;">
                        <li style="text-align: center; margin-bottom: 8px; color: #e9ecef;">• Start with the clued entries to establish some constraints</li>
                        <li style="text-align: center; margin-bottom: 8px; color: #e9ecef;">• 'Think ahead' for the unclued entries</li>
                        <li style="text-align: center; margin-bottom: 8px; color: #e9ecef;">• Look for the mathematical key - a number with unique properties</li>
                        <li style="text-align: center; margin-bottom: 8px; color: #e9ecef;">• Use the factoring notepad (and the undo feature for mistakes...</li>
                    </ul>
                </div>
            `;
            const buttons = `
                <button onclick="hideModal('intro-modal')" style="background: linear-gradient(135deg, #28a745, #20c997);color: white;border: none;padding: 15px 30px;border-radius: 8px;font-size: 1.1em;font-weight: 500;cursor: pointer;transition: all 0.3s ease;box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 16px rgba(40, 167, 69, 0.4)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 12px rgba(40, 167, 69, 0.3)'">🚀 Start Solving</button>
            `;
            createModal('intro-modal', title, content, buttons);
        }}

        function showAnagramCompletionCelebration() {{
            const title = '🏆 Listener 4869 Completed 🏆';
            const content = `
                <div style="background: rgba(255,255,255,0.08);padding: 20px;border-radius: 8px;margin: 20px 0;border: 1px solid rgba(255,255,255,0.1);">
                    <h3 style="margin: 0 0 15px 0; color: #28a745; font-weight: 500; font-size: 1.3em;">Congratulations!</h3>
                    <p style="margin: 0 0 15px 0; line-height: 1.6; color: #e9ecef;">
                        You have successfully completed both stages of this ingenious mathematical puzzle. 
                        This is no small feat - it takes mathematical and logical insight to solve.
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.08);padding: 20px;border-radius: 8px;margin: 20px 0;border: 1px solid rgba(255,255,255,0.1);">
                    <h3 style="margin: 0 0 15px 0; color: #17a2b8; font-weight: 500; font-size: 1.3em;">The Mathematical Key...</h3>
                    <p style="margin: 0 0 15px 0; line-height: 1.6; color: #e9ecef;">
                        Did you discover the special cyclic number <strong style="color: #28a745;">142857</strong>? This remarkable number is a helpful key to the puzzle:
                    </p>
                    <div style="background: rgba(23, 162, 184, 0.15);padding: 15px;border-radius: 8px;border-left: 4px solid #17a2b8;text-align: center;font-style: normal;color: #e9ecef;">
                        <strong style="color: #17a2b8;">The Magic of 142857:</strong><br>
                        • 142857 × 1 = 142857<br>
                        • 142857 × 2 = 285714<br>
                        • 142857 × 3 = 428571<br>
                        • 142857 × 5 = 714285<br>
                        • 142857 × 6 = 857142<br>
                        • 142857 × 4 = 571428<br>
                        <br>
                        This cyclic property makes it perfect for the initial puzzle and the anagram grid.
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.08);padding: 20px;border-radius: 8px;margin: 20px 0;border: 1px solid rgba(255,255,255,0.1);">
                    <h3 style="margin: 0 0 15px 0; color: #6c757d; font-weight: 500; font-size: 1.3em;">Your Solving Journey</h3>
                    <p style="margin: 0 0 15px 0; line-height: 1.6; color: #e9ecef;">
                        Whether you found this through mathematical insight, systematic trial and error, or a bit of luck, 
                        you've demonstrated tenacity and strong problem-solving skills.
                    </p>
                    <p style="margin: 0 0 15px 0; line-height: 1.6; font-style: italic; color: #adb5bd;">
                        "The value of a problem is not so much coming up with the answer as in the ideas it forces on the solver." - Andrew Wiles
                    </p>
                </div>
            `;
            const buttons = `
                <button onclick="hideModal('anagram-completion-celebration')" style="background: linear-gradient(135deg, #6c757d, #495057);color: white;border: none;padding: 15px 30px;border-radius: 8px;font-size: 1.1em;font-weight: 500;cursor: pointer;transition: all 0.3s ease;box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 16px rgba(108, 117, 125, 0.4)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 12px rgba(108, 117, 125, 0.3)'">🎉 Now take a well-earned break! 🎉</button>
            `;
            createModal('anagram-completion-celebration', title, content, buttons);
        }}

        function createConfetti() {{
            // Removed confetti for sophisticated design
            // The subtle glow animation provides sufficient celebration effect
        }}
        
        // Iframe communication for Flask app integration
        window.addEventListener('message', function(event) {{
            console.log('Received message from parent:', event.data);
            
            if (event.data.action === 'save_state') {{
                console.log('Save state requested by parent');
                
                // Send state back to parent (including anagram state)
                window.parent.postMessage({{
                    action: 'save_state_request',
                    state: {{
                        solved_cells: solvedCells,
                        user_selected_solutions: Array.from(userSelectedSolutions),
                        solution_history: solutionHistory,
                        anagram_solved_cells: anagramSolvedCells,
                        anagram_user_selected_solutions: Array.from(anagramUserSelectedSolutions),
                        anagram_clue_objects: anagramClueObjects
                    }}
                }}, '*');
            }}
            else if (event.data.action === 'load_state') {{
                console.log('Load state requested by parent');
                
                // Request state from parent
                window.parent.postMessage({{
                    action: 'load_state_request'
                }}, '*');
            }}
            else if (event.data.action === 'load_state_response') {{
                console.log('Load state response received:', event.data.state);
                
                // Apply loaded state (including anagram state)
                const state = event.data.state;
                solvedCells = state.solved_cells || {{}};
                userSelectedSolutions = new Set(state.user_selected_solutions || []);
                solutionHistory = state.solution_history || [];
                
                // Load anagram state
                anagramSolvedCells = state.anagram_solved_cells || {{}};
                anagramUserSelectedSolutions = new Set(state.anagram_user_selected_solutions || []);
                anagramClueObjects = state.anagram_clue_objects || {{}};
                
                // Update UI
                updateGridDisplay();
                updateAllClueDisplays();
                updateProgress();
                updateUndoButton();
                
                // Update anagram grid if anagram state exists
                if (Object.keys(anagramSolvedCells).length > 0 || Object.keys(anagramClueObjects).length > 0) {{
                    // Update anagram grid display
                    for (const [cellIndex, digit] of Object.entries(anagramSolvedCells)) {{
                        updateAnagramCellDisplay(parseInt(cellIndex), digit);
                    }}
                    
                    // Update anagram clue displays
                    updateAnagramClueDisplays();
                    
                    // Show anagram grid section
                    const anagramGridSection = document.getElementById('anagram-grid-section');
                    if (anagramGridSection) {{
                        anagramGridSection.style.display = 'block';
                    }}
                    
                    // Show anagram clues if they exist
                    if (Object.keys(anagramClueObjects).length > 0) {{
                        generateAnagramCluesHTMLFromObjects();
                        
                        const initialCluesContainer = document.getElementById('initial-clues-container');
                        const anagramCluesContainer = document.getElementById('anagram-clues-container');
                        if (initialCluesContainer) {{
                            initialCluesContainer.style.display = 'none';
                        }}
                        if (anagramCluesContainer) {{
                            anagramCluesContainer.style.display = 'block';
                        }}
                    }}
                }}
                
                // State loaded successfully
            }}
            else if (event.data.action === 'test_communication') {{
                // Send test response back (no notification needed)
                window.parent.postMessage({{
                    action: 'test_response',
                    message: 'Iframe communication working!'
                }}, '*');
            }}
        }});

        function factorizeNumber() {{
            const input = document.getElementById('workpad-number');
            const resultDiv = document.getElementById('factorization-result');
            const statsDiv = document.getElementById('factorization-stats');
            const number = parseInt(input.value);
            if (!number || number <= 0) {{
                resultDiv.innerHTML = '<div style="color: #dc3545;">Please enter a positive number</div>';
                statsDiv.style.display = 'none';
                return;
            }}
            const factorization = getPrimeFactorization(number);
            const stats = getPrimeFactorStats(number);
            resultDiv.innerHTML = `<div style="font-weight: bold; margin-bottom: 8px;">${{factorization}}</div>`;
            statsDiv.innerHTML = `
                <strong>Factors:</strong><br>
                • Number of factors: ${{stats.count}}<br>
                • Smallest factor: ${{stats.min_factor}}<br>
                • Largest factor: ${{stats.max_factor}}<br>
                • Difference: ${{stats.difference}}<br>
                <br>
                <strong>Clue:</strong> <strong>${{stats.count}}:${{stats.difference}}</strong>
            `;
            statsDiv.style.display = 'block';
        }}

        function clearWorkpad() {{
            document.getElementById('workpad-number').value = '';
            document.getElementById('factorization-result').innerHTML = '<div style="color: #6c757d; font-style: italic;">Enter a number above to see its prime factorization</div>';
            document.getElementById('factorization-stats').style.display = 'none';
        }}

        function getPrimeFactorization(number) {{
            if (number <= 1) return `${{number}} (no prime factors)`;
            const factors = [];
            let n = number;
            while (n % 2 === 0) {{
                factors.push(2);
                n = n / 2;
            }}
            for (let i = 3; i <= Math.sqrt(n); i += 2) {{
                while (n % i === 0) {{
                    factors.push(i);
                    n = n / i;
                }}
            }}
            if (n > 2) {{
                factors.push(n);
            }}
            if (factors.length === 0) {{
                return `${{number}} (prime)`;
            }}
            const factorCounts = {{}};
            for (const factor of factors) {{
                factorCounts[factor] = (factorCounts[factor] || 0) + 1;
            }}
            const factorParts = [];
            for (const [factor, count] of Object.entries(factorCounts).sort((a, b) => parseInt(a[0]) - parseInt(b[0]))) {{
                if (count === 1) {{
                    factorParts.push(factor);
                }} else {{
                    factorParts.push(`${{factor}}^${{count}}`);
                }}
            }}
            return `${{number}} = ${{factorParts.join(' × ')}}`;
        }}

        function getPrimeFactorStats(number) {{
            if (number <= 1) {{
                return {{
                    count: 0,
                    min_factor: null,
                    max_factor: null,
                    difference: null,
                    is_prime: number > 1
                }};
            }}
            const factors = [];
            let n = number;
            while (n % 2 === 0) {{
                factors.push(2);
                n = n / 2;
            }}
            for (let i = 3; i <= Math.sqrt(n); i += 2) {{
                while (n % i === 0) {{
                    factors.push(i);
                    n = n / i;
                }}
            }}
            if (n > 2) {{
                factors.push(n);
            }}
            if (factors.length === 0) {{
                return {{
                    count: 0,
                    min_factor: number,
                    max_factor: number,
                    difference: 0,
                    is_prime: true
                }};
            }}
            return {{
                count: factors.length,
                min_factor: Math.min(...factors),
                max_factor: Math.max(...factors),
                difference: Math.max(...factors) - Math.min(...factors),
                is_prime: false
            }};
        }}
    </script>
</body>
</html>"""
    
    return html_content

def save_html_to_static(html_content: str, filename: str = "interactive_solver.html"):
    """Save generated HTML to static folder for Flask app deployment."""
    static_dir = "static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    filepath = os.path.join(static_dir, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[SUCCESS] HTML saved to {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Error saving HTML: {e}")
        return False

def main():
    """Main function to generate interactive solver."""
    print("=== INTERACTIVE CROSSWORD SOLVER ===")
    
    # Load clue objects using systematic grid parser and clue classes
    grid_clues, clue_objects, clue_manager = load_clue_objects()
    
    print(f"Loaded {len(grid_clues)} grid clues")
    print(f"Loaded {len(clue_objects)} clue objects")
    
    # Debug: Print the clue objects to see what's loaded
    print("\nDebug - Clue objects loaded:")
    for number, clue in sorted(clue_objects.items()):
        print(f"  {clue}")
    
    # Generate interactive HTML
    html_content = generate_interactive_html(clue_objects)
    
    # Save for local development
    filename = "interactive_solver.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Also save to static folder for Flask app deployment
    save_html_to_static(html_content)
    
    print(f"Generated interactive solver: {filename}")
    print("[SUCCESS] HTML automatically saved to static/ folder for Flask deployment")
    print("Open this file in a web browser to use the interactive solver")
    
    # Try to open in browser
    try:
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        print("Opened in default web browser")
    except:
        print("Please open the HTML file manually in your web browser")

if __name__ == "__main__":
    main() 