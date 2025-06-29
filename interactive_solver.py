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

from systematic_grid_parser import parse_grid, ClueTuple
from clue_classes import ListenerClue, ClueFactory, ClueManager, ClueParameters

def load_clue_parameters(filename: str) -> Dict[Tuple[int, str], Tuple[int, int, int]]:
    """Load clue parameters from file."""
    clue_params = {}
    try:
        # Update path to data directory
        data_path = os.path.join('data', filename)
        with open(data_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or not line[0].isdigit():
                    continue  # Skip headers, comments, or blank lines
                parts = line.split()
                if len(parts) >= 4:
                    number = int(parts[0])
                    direction = parts[1]
                    a = int(parts[2])
                    b = int(parts[3])
                    c = int(parts[4]) if len(parts) > 4 else 0
                    clue_params[(number, direction)] = (a, b, c)
    except FileNotFoundError:
        print(f"Warning: Could not find clue parameters file {filename}")
    return clue_params

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
    """Load clue objects using the systematic grid parser and clue classes."""
    print("Loading grid structure and clue objects...")
    
    # Parse grid structure
    grid_clues = parse_grid()
    
    # Create clue manager
    clue_manager = ClueManager()
    
    # Load clue parameters
    clue_params = load_clue_parameters("clue_parameters_4869.txt")
    
    # Create ListenerClue objects
    clue_objects = {}
    
    for number, direction, cell_indices in grid_clues:
        # Get parameters for this clue
        if (number, direction) in clue_params:
            a, b, c = clue_params[(number, direction)]
            is_unclued = False
        else:
            # Try to get from clue text
            clues_text = load_clues_from_file()
            clue_key = (number, direction)
            if clue_key in clues_text:
                text = clues_text[clue_key]
                if text.lower() == 'unclued':
                    b = None
                    c = None
                    is_unclued = True
                else:
                    try:
                        b_c_parts = text.split(':')
                        if len(b_c_parts) == 2:
                            b = int(b_c_parts[0])
                            c = int(b_c_parts[1])
                            is_unclued = False
                        else:
                            b = 1
                            c = 0
                            is_unclued = False
                    except ValueError:
                        b = 1
                        c = 0
                        is_unclued = False
            else:
                b = 1
                c = 0
                is_unclued = False
            a = len(cell_indices)
        # Create clue object
        if is_unclued:
            clue = ListenerClue(
                number=number,
                direction=direction,
                cell_indices=cell_indices,
                parameters=ClueParameters(a=len(cell_indices), b=1, c=0, is_unclued=True)
            )
        else:
            clue = ClueFactory.from_tuple_and_parameters(
                ClueTuple(number=number, direction=direction, cell_indices=cell_indices, length=len(cell_indices), parameters=(len(cell_indices), b, c)),
                b, c
            )
        clue_objects[(number, direction)] = clue
        clue_manager.add_clue(clue)
    
    # Load clue text and update parameters
    clues_text = load_clues_from_file()
    
    for (number, direction), text in clues_text.items():
        if (number, direction) in clue_objects:
            clue = clue_objects[(number, direction)]
            
            # Update clue parameters based on text
            if text.lower() == 'unclued':
                # Create unclued clue
                new_clue = ClueFactory.from_tuple_and_parameters(
                    ClueTuple(number=number, direction=direction, cell_indices=clue.cell_indices, length=clue.length, parameters=(clue.length, -1, -1)),
                    -1, -1  # Unclued parameters
                )
            else:
                # Parse "b:c" format
                try:
                    b_c_parts = text.split(':')
                    if len(b_c_parts) == 2:
                        b = int(b_c_parts[0])
                        c = int(b_c_parts[1])
                        new_clue = ClueFactory.from_tuple_and_parameters(
                            ClueTuple(number=number, direction=direction, cell_indices=clue.cell_indices, length=clue.length, parameters=(clue.length, b, c)),
                            b, c
                        )
                    else:
                        new_clue = clue  # Keep original if parsing fails
                except ValueError:
                    new_clue = clue  # Keep original if parsing fails
            
            # Update the clue object
            clue_objects[(number, direction)] = new_clue
            clue_manager.clues[number] = new_clue
    
    return grid_clues, clue_objects, clue_manager

def generate_grid_html(solved_cells: Dict[int, str] = None) -> str:
    """Generate HTML for the crossword grid."""
    if solved_cells is None:
        solved_cells = {}
    
    # Define grid structure (same as puzzle_visualizer.py)
    grid_clues = [
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
    
    # Initialize border sets (same logic as puzzle_visualizer.py)
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
    
    # Add specific borders for cell pair separations (same as puzzle_visualizer.py)
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
    
    # Generate grid HTML
    grid_html = ['<div class="crossword-grid">']
    
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
            if cell_index in thick_right_cells:
                border_classes.append('thick-right')
            if cell_index in thick_bottom_cells:
                border_classes.append('thick-bottom')
            if cell_index in thick_left_cells:
                border_classes.append('thick-left')
            if cell_index in thick_top_cells:
                border_classes.append('thick-top')
            
            border_class = ' '.join(border_classes)
            
            # Create interactive cell
            cell_html = f'    <div class="grid-cell {border_class}" data-cell="{cell_index}">'
            if clue_number:
                cell_html += f'<div class="grid-clue-number">{clue_number}</div>'
            if cell_value:
                cell_html += f'<div class="cell-value">{cell_value}</div>'
            cell_html += '</div>'
            
            grid_html.append(cell_html)
        
        grid_html.append('  </div>')
    
    grid_html.append('</div>')
    
    return '\n'.join(grid_html)

def generate_clues_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate HTML for the clues section using clue objects."""
    html = ['<div class="clues-section">']

    # Across clues
    html.append('  <div class="clues-column">')
    html.append('    <h3>Across</h3>')

    across_clues = [clue for clue in clue_objects.values() if clue.direction == "ACROSS"]
    across_clues.sort(key=lambda x: x.number)

    for clue in across_clues:
        clue_id = create_clue_id(clue.number, clue.direction)
        current_solutions = clue.get_valid_solutions()
        solution_count = len(current_solutions)
        clue_text = "Unclued" if clue.parameters.is_unclued else f"{clue.parameters.b}:{clue.parameters.c}"
        status_class = "multiple" if solution_count > 1 else "unclued" if clue.parameters.is_unclued else ""
        html.append(f'    <div class="clue {status_class}" data-clue="{clue_id}">')
        html.append('      <div class="clue-header">')
        html.append(f'        <span class="clue-number">{clue.number}.</span>')
        html.append(f'        <span class="clue-text">{clue_text}</span>')
        if not clue.parameters.is_unclued:
            html.append(f'        <span class="solution-count">({solution_count} solutions)</span>')
        html.append('      </div>')
        if clue.parameters.is_unclued:
            html.append(f'      <div class="solution-input" id="input-{clue_id}" style="display: none;">')
            html.append(f'        <input type="text" class="solution-text-input" data-clue="{clue_id}" placeholder="Enter {clue.length}-digit solution" maxlength="{clue.length}">')
            html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
            html.append(f'        <span class="unclued-error" id="error-{clue_id}" style="color: #b00; margin-left: 8px; display: none;"></span>')
            html.append(f'      </div>')
        else:
            if current_solutions:
                html.append(f'      <div class="solution-dropdown" id="dropdown-{clue_id}" style="display: none;">')
                html.append(f'        <select class="solution-select" data-clue="{clue_id}">')
                html.append(f'          <option value="">-- Select a solution --</option>')
                for solution in current_solutions:
                    html.append(f'          <option value="{solution}">{solution}</option>')
                html.append(f'        </select>')
                html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
                html.append(f'      </div>')
        html.append(f'    </div>')

    html.append('  </div>')

    # Down clues
    html.append('  <div class="clues-column">')
    html.append('    <h3>Down</h3>')

    down_clues = [clue for clue in clue_objects.values() if clue.direction == "DOWN"]
    down_clues.sort(key=lambda x: x.number)

    for clue in down_clues:
        clue_id = create_clue_id(clue.number, clue.direction)
        current_solutions = clue.get_valid_solutions()
        solution_count = len(current_solutions)
        clue_text = "Unclued" if clue.parameters.is_unclued else f"{clue.parameters.b}:{clue.parameters.c}"
        status_class = "multiple" if solution_count > 1 else "unclued" if clue.parameters.is_unclued else ""
        html.append(f'    <div class="clue {status_class}" data-clue="{clue_id}">')
        html.append('      <div class="clue-header">')
        html.append(f'        <span class="clue-number">{clue.number}.</span>')
        html.append(f'        <span class="clue-text">{clue_text}</span>')
        if not clue.parameters.is_unclued:
            html.append(f'        <span class="solution-count">({solution_count} solutions)</span>')
        html.append('      </div>')
        if clue.parameters.is_unclued:
            html.append(f'      <div class="solution-input" id="input-{clue_id}" style="display: none;">')
            html.append(f'        <input type="text" class="solution-text-input" data-clue="{clue_id}" placeholder="Enter {clue.length}-digit solution" maxlength="{clue.length}">')
            html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
            html.append(f'        <span class="unclued-error" id="error-{clue_id}" style="color: #b00; margin-left: 8px; display: none;"></span>')
            html.append(f'      </div>')
        else:
            if current_solutions:
                html.append(f'      <div class="solution-dropdown" id="dropdown-{clue_id}" style="display: none;">')
                html.append(f'        <select class="solution-select" data-clue="{clue_id}">')
                html.append(f'          <option value="">-- Select a solution --</option>')
                for solution in current_solutions:
                    html.append(f'          <option value="{solution}">{solution}</option>')
                html.append(f'        </select>')
                html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
                html.append(f'      </div>')
        html.append(f'    </div>')

    html.append('  </div>')
    html.append('</div>')
    return '\n'.join(html)

def generate_interactive_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate the complete interactive HTML interface."""
    
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
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Crossword Solver</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
        }}
        
        .header h1 {{
            color: #333;
            margin: 0;
        }}
        
        .main-content {{
            display: flex;
            gap: 30px;
            align-items: flex-start;
        }}
        
        .grid-section {{
            flex: 1;
        }}
        
        .info-section {{
            flex: 1;
            min-width: 400px;
        }}
        
        .crossword-grid {{
            display: inline-block;
            border: 3px solid #333;
            background-color: #333;
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
        
        .clue.solved {{
            background-color: #d4edda;
            color: #155724;
            font-weight: bold;
        }}
        
        .clue.user-selected {{
            background-color: #cce5ff;
            color: #004085;
            font-weight: bold;
            border-left: 4px solid #007bff;
        }}
        
        .clue.algorithm-solved {{
            background-color: #d1ecf1;
            color: #0c5460;
            font-weight: bold;
            border-left: 4px solid #17a2b8;
        }}
        
        .clue.multiple {{
            background-color: #fff3cd;
            color: #856404;
        }}
        
        .clue.unclued {{
            background-color: #f8d7da;
            color: #721c24;
            font-style: italic;
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
            position: fixed;
            top: 850px;
            left: 20px;
            width: 600px;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Interactive Crossword Solver</h1>
            <div class="timestamp">Listener 4869, 24 May 2025</div>
        </div>

        <div class="main-content">
            <div class="grid-section">
                <h3>Puzzle Grid</h3>
                {generate_grid_html()}
            </div>
            
            <div class="info-section">
                {generate_clues_html(clue_objects)}
                
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
            </div>
        </div>
    </div>

    <script>
        // Interactive functionality
        let solvedCells = {{}};
        let clueObjects = {json.dumps(clue_data)};
        
        // Track user-selected solutions vs algorithm-determined solutions
        let userSelectedSolutions = new Set();
        let originalSolutionCounts = {{}};
        let originalSolutions = {{}};
        
        // Initialize original solution counts and store original solutions
        for (const [clueId, clue] of Object.entries(clueObjects)) {{
            originalSolutionCounts[clueId] = clue.possible_solutions.length;
            originalSolutions[clueId] = [...clue.possible_solutions]; // Store original solutions
        }}
        
        // Undo system
        let solutionHistory = [];
        let undoButton = null;
        let historyInfo = null;
        
        // Function to save current state
        function saveState(clueId, solution) {{
            const state = {{
                timestamp: new Date().toLocaleTimeString(),
                clueId: clueId,
                solution: solution,
                solvedCells: {{...solvedCells}},
                clueObjects: JSON.parse(JSON.stringify(clueObjects)), // Deep copy
                userSelectedSolutions: new Set(userSelectedSolutions) // Copy the set
            }};
            solutionHistory.push(state);
            updateUndoButton();
            console.log('Saved state:', state);
        }}
        
        // Function to restore previous state
        function undoLastSolution() {{
            if (solutionHistory.length === 0) return;
            
            const lastState = solutionHistory.pop();
            console.log('Undoing solution:', lastState);
            
            // Restore solved cells
            solvedCells = {{...lastState.solvedCells}};
            
            // Restore clue objects
            clueObjects = JSON.parse(JSON.stringify(lastState.clueObjects));
            
            // Restore user-selected solutions
            userSelectedSolutions = new Set(lastState.userSelectedSolutions);
            
            // Update grid display
            updateGridDisplay();
            
            // Update all clue displays
            updateAllClueDisplays();
            
            // Update progress
            updateProgress();
            
            // Update undo button
            updateUndoButton();
            
            // Show notification based on action type
            if (lastState.solution === 'DESELECT') {{
                showNotification(`Undid deselect for clue ${{lastState.clueId}}`, 'info');
            }} else {{
                showNotification(`Undid solution "${{lastState.solution}}" for clue ${{lastState.clueId}}`, 'info');
            }}
        }}
        
        // Function to update undo button state
        function updateUndoButton() {{
            if (!undoButton) return;
            
            const canUndo = solutionHistory.length > 0;
            undoButton.disabled = !canUndo;
            
            if (canUndo) {{
                const lastState = solutionHistory[solutionHistory.length - 1];
                if (lastState.solution === 'DESELECT') {{
                    historyInfo.textContent = `Last action: Deselected clue ${{lastState.clueId}} at ${{lastState.timestamp}}`;
                }} else {{
                    historyInfo.textContent = `Last solution: ${{lastState.solution}} for ${{lastState.clueId}} at ${{lastState.timestamp}}`;
                }}
            }} else {{
                historyInfo.textContent = 'No solutions applied yet';
            }}
        }}
        
        // Function to update grid display from solvedCells
        function updateGridDisplay() {{
            // Clear all cell values first
            document.querySelectorAll('.cell-value').forEach(el => {{
                el.remove();
            }});
            
            // Update cells that have values
            for (const [cellIndex, digit] of Object.entries(solvedCells)) {{
                updateCellDisplay(parseInt(cellIndex), digit);
            }}
        }}

        // Attach event listeners after DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, setting up event listeners');
            
            // Initialize undo system
            undoButton = document.getElementById('undo-button');
            historyInfo = document.getElementById('history-info');
            updateUndoButton();
            
            // Add undo button event listener
            undoButton.addEventListener('click', undoLastSolution);
            
            // Event delegation for clue clicks
            document.querySelector('.clues-section').addEventListener('click', function(e) {{
                const clueDiv = e.target.closest('.clue');
                if (!clueDiv) return;
                
                // Don't toggle if clicking on the dropdown or input itself
                if (e.target.closest('.solution-dropdown') || e.target.closest('.solution-input') || e.target.closest('.deselect-dialog') || e.target.classList.contains('apply-solution') || e.target.classList.contains('deselect-solution')) {{
                    return;
                }}
                
                const clueId = clueDiv.getAttribute('data-clue');
                console.log('Clue clicked:', clueId);
                
                // Check if this clue has a user-selected solution
                if (userSelectedSolutions.has(clueId)) {{
                    // Show deselect dialog instead of dropdown
                    showDeselectDialog(clueId);
                    return;
                }}
                
                const dropdown = document.getElementById(`dropdown-${{clueId}}`);
                const input = document.getElementById(`input-${{clueId}}`);
                
                // Hide all other dropdowns and inputs
                document.querySelectorAll('.solution-dropdown, .solution-input, .deselect-dialog').forEach(d => {{
                    if (d !== dropdown && d !== input) d.style.display = 'none';
                }});
                
                // Toggle this dropdown/input
                if (dropdown) {{
                    const isHidden = dropdown.style.display === 'none' || dropdown.style.display === '';
                    dropdown.style.display = isHidden ? 'block' : 'none';
                    console.log('Toggled dropdown for', clueId, 'to', isHidden ? 'visible' : 'hidden');
                }} else if (input) {{
                    const isHidden = input.style.display === 'none' || input.style.display === '';
                    input.style.display = isHidden ? 'block' : 'none';
                    console.log('Toggled input for', clueId, 'to', isHidden ? 'visible' : 'hidden');
                }}
            }});

            // Handle solution selection and application using event delegation
            document.querySelector('.clues-section').addEventListener('click', function(e) {{
                if (e.target.classList.contains('apply-solution')) {{
                    e.stopPropagation(); // Prevent bubbling to clue click
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

        function applySolutionToGrid(clueId, solution) {{
            console.log(`Applying solution "${{solution}}" to clue ${{clueId}}`);
            
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
            
            // Get clue object
            const clue = clueObjects[clueId];
            if (!clue) {{
                showNotification('Clue not found', 'error');
                return;
            }}
            
            // Validate solution length
            if (solution.length !== clue.length) {{
                showNotification(`Solution must be ${{clue.length}} digits long`, 'error');
                return;
            }}
            
            // For unclued clues, check if the solution conflicts with already solved crossing clues
            if (clue.is_unclued) {{
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
                solvedCells[cellIndex] = digit;
                
                // Update grid display
                updateCellDisplay(cellIndex, digit);
            }}
            
            // Mark clue as solved
            clue.possible_solutions = [parseInt(solution)];
            
            // Mark this as a user-selected solution
            userSelectedSolutions.add(clueId);
            
            // Propagate constraints to crossing clues
            const eliminatedSolutions = propagateConstraints(clueId, solution);
            
            // Update all clue displays
            updateAllClueDisplays();
            
            // Update progress
            updateProgress();
            
            // Show success message
            const eliminatedCount = eliminatedSolutions.length;
            if (eliminatedCount > 0) {{
                showNotification(`Solution applied! Eliminated ${{eliminatedCount}} incompatible solutions from crossing clues.`, 'success');
            }} else {{
                showNotification('Solution applied successfully!', 'success');
            }}
            
            // Hide the dropdown/input
            const dropdown = document.getElementById(`dropdown-${{clueId}}`);
            const input = document.getElementById(`input-${{clueId}}`);
            if (dropdown) dropdown.style.display = 'none';
            if (input) input.style.display = 'none';
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
            
            // Update solution count - show actual remaining solutions, not just "1" if user selected
            const countElement = clueElement.querySelector('.solution-count');
            if (countElement) {{
                countElement.textContent = `${{clue.possible_solutions.length}} solutions`;
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
            const dropdown = document.getElementById(`dropdown-${{clueId}}`);
            if (dropdown) {{
                const select = dropdown.querySelector('.solution-select');
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
            document.body.appendChild(notification);
            
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
            
            // Update progress
            updateProgress();
            
            // Hide the deselect dialog
            const dialog = document.getElementById(`deselect-${{clueId}}`);
            if (dialog) {{
                dialog.style.display = 'none';
            }}
            
            // Show success message
            const restoredCount = clue.possible_solutions.length;
            showNotification(`Deselected solution for clue ${{clueId}}. Restored ${{restoredCount}} possible solutions.`, 'success');
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
    </script>
</body>
</html>"""
    
    return html_content

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
    
    # Save and open
    filename = "interactive_solver.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated interactive solver: {filename}")
    print("Open this file in a web browser to use the interactive solver")
    
    # Try to open in browser
    try:
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        print("Opened in default web browser")
    except:
        print("Please open the HTML file manually in your web browser")

if __name__ == "__main__":
    main() 