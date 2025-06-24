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
        with open(filename, 'r') as f:
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
        with open(filename, 'r') as f:
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

def load_solution_sets(filename: str = "solution_sets.json") -> Dict[str, List[str]]:
    """Load pre-computed solution sets from JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find solution sets file {filename}")
        return {}

def create_clue_id(number: int, direction: str) -> str:
    """Create a unique identifier for a clue."""
    return f"{number}_{direction}"

def get_clue_number_at_cell(cell_index: int, grid_clues: List[Tuple[int, str, Tuple[int, ...]]]) -> Optional[int]:
    """Get the clue number at a specific cell, if any."""
    for number, direction, cell_indices in grid_clues:
        if cell_indices[0] == cell_index:  # First cell of the clue
            return number
    return None

def load_clue_objects() -> Tuple[List[Tuple[int, str, Tuple[int, ...]]], Dict[int, ListenerClue], ClueManager]:
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
        clue_objects[number] = clue
        clue_manager.add_clue(clue)
    
    # Load clue text and update parameters
    clues_text = load_clues_from_file()
    
    for (number, direction), text in clues_text.items():
        if number in clue_objects:
            clue = clue_objects[number]
            
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
            clue_objects[number] = new_clue
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
                cell_html += f'<div class="clue-number">{clue_number}</div>'
            if cell_value:
                cell_html += f'<div class="cell-value">{cell_value}</div>'
            cell_html += '</div>'
            
            grid_html.append(cell_html)
        
        grid_html.append('  </div>')
    
    grid_html.append('</div>')
    
    return '\n'.join(grid_html)

def generate_clues_html(clue_objects: Dict[int, ListenerClue], solution_sets: Dict[str, List[str]]) -> str:
    """Generate HTML for the clues section using clue objects."""
    html = ['<div class="clues-section">']
    
    # Across clues
    html.append('  <div class="clues-column">')
    html.append('    <h3>Across</h3>')
    
    across_clues = [clue for clue in clue_objects.values() if clue.direction == "ACROSS"]
    across_clues.sort(key=lambda x: x.number)
    
    for clue in across_clues:
        clue_id = create_clue_id(clue.number, clue.direction)
        
        # Get current valid solutions from the clue object
        current_solutions = clue.get_valid_solutions()
        solution_count = len(current_solutions)
        
        # Get clue text
        if clue.parameters.is_unclued:
            clue_text = "Unclued"
        else:
            clue_text = f"{clue.parameters.b}:{clue.parameters.c}"
        
        status_class = "solved" if solution_count == 1 else "multiple" if solution_count > 1 else "unclued" if clue.parameters.is_unclued else ""
        
        # Render as a single string, e.g. '1. 6:2'
        html.append(f'    <div class="clue {status_class}" data-clue="{clue_id}">')
        
        # For unclued clues, show "Unclued" without solution count
        if clue.parameters.is_unclued:
            html.append(f'      <div class="clue-header">{clue.number}. {clue_text}</div>')
            # Add input box for unclued clues
            html.append(f'      <div class="solution-input" id="input-{clue_id}" style="display: none;">')
            html.append(f'        <input type="text" class="solution-text-input" data-clue="{clue_id}" placeholder="Enter {clue.length}-digit solution" maxlength="{clue.length}">')
            html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
            html.append(f'      </div>')
        else:
            html.append(f'      <div class="clue-header">{clue.number}. {clue_text} <span class="solution-count">({solution_count} solutions)</span></div>')
            
            # Show solution dropdown only if there are solutions
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
        
        # Get current valid solutions from the clue object
        current_solutions = clue.get_valid_solutions()
        solution_count = len(current_solutions)
        
        # Get clue text
        if clue.parameters.is_unclued:
            clue_text = "Unclued"
        else:
            clue_text = f"{clue.parameters.b}:{clue.parameters.c}"
        
        status_class = "solved" if solution_count == 1 else "multiple" if solution_count > 1 else "unclued" if clue.parameters.is_unclued else ""
        
        html.append(f'    <div class="clue {status_class}" data-clue="{clue_id}">')
        
        # For unclued clues, show "Unclued" without solution count
        if clue.parameters.is_unclued:
            html.append(f'      <div class="clue-header">{clue.number}. {clue_text}</div>')
            # Add input box for unclued clues
            html.append(f'      <div class="solution-input" id="input-{clue_id}" style="display: none;">')
            html.append(f'        <input type="text" class="solution-text-input" data-clue="{clue_id}" placeholder="Enter {clue.length}-digit solution" maxlength="{clue.length}">')
            html.append(f'        <button class="apply-solution" data-clue="{clue_id}">Apply</button>')
            html.append(f'      </div>')
        else:
            html.append(f'      <div class="clue-header">{clue.number}. {clue_text} <span class="solution-count">({solution_count} solutions)</span></div>')
            
            # Show solution dropdown only if there are solutions
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

def main():
    """Main function to generate interactive solver."""
    print("=== INTERACTIVE CROSSWORD SOLVER ===")
    
    # Load clue objects using systematic grid parser and clue classes
    grid_clues, clue_objects, clue_manager = load_clue_objects()
    solution_sets = load_solution_sets()
    
    print(f"Loaded {len(grid_clues)} grid clues")
    print(f"Loaded {len(clue_objects)} clue objects")
    print(f"Loaded {len(solution_sets)} solution sets")
    
    # Debug: Print the clue objects to see what's loaded
    print("\nDebug - Clue objects loaded:")
    for number, clue in sorted(clue_objects.items()):
        print(f"  {clue}")
    
    # Generate interactive HTML
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
        
        .clue-number {{
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
        
        .clue-number {{
            font-weight: bold;
            min-width: 20px;
            color: #333;
            font-size: 14px;
        }}
        
        .clue-text {{
            flex: 1;
            margin-left: 8px;
        }}
        
        .solution-count {{
            font-size: 12px;
            color: #666;
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
            font-family: monospace;
            font-size: 14px;
        }}
        
        .solution-input {{
            margin-top: 8px;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }}
        
        .apply-solution {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 4px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}
        
        .apply-solution:hover {{
            background-color: #0056b3;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Interactive Crossword Solver</h1>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>

        <div class="main-content">
            <div class="grid-section">
                <h3>Puzzle Grid</h3>
                {generate_grid_html()}
            </div>
            
            <div class="info-section">
                {generate_clues_html(clue_objects, solution_sets)}
                
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
            </div>
        </div>
    </div>

    <script>
        // Interactive functionality
        let solvedCells = {{}};
        let clueObjects = {{}}; // Will be populated with clue data
        
        // Initialize clue objects from the server data
        function initializeClueObjects() {{
            // This would be populated from the server-side clue objects
            // For now, we'll use a simplified approach
            console.log("Initializing clue objects...");
        }}
        
        // Handle clue clicks to show/hide solution dropdowns
        document.querySelectorAll('.clue').forEach(clue => {{
            clue.addEventListener('click', function(e) {{
                // Don't toggle if clicking on the dropdown or input itself
                if (e.target.closest('.solution-dropdown') || e.target.closest('.solution-input')) {{
                    return;
                }}
                
                const clueId = this.getAttribute('data-clue');
                const dropdown = document.getElementById(`dropdown-${{clueId}}`);
                const input = document.getElementById(`input-${{clueId}}`);
                
                if (dropdown) {{
                    // Hide all other dropdowns and inputs
                    document.querySelectorAll('.solution-dropdown, .solution-input').forEach(d => {{
                        if (d !== dropdown) d.style.display = 'none';
                    }});
                    
                    // Toggle this dropdown
                    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
                }} else if (input) {{
                    // Hide all other dropdowns and inputs
                    document.querySelectorAll('.solution-dropdown, .solution-input').forEach(d => {{
                        if (d !== input) d.style.display = 'none';
                    }});
                    
                    // Toggle this input
                    input.style.display = input.style.display === 'none' ? 'block' : 'none';
                }}
            }});
        }});
        
        // Handle solution selection and application
        document.querySelectorAll('.apply-solution').forEach(button => {{
            button.addEventListener('click', function(e) {{
                e.stopPropagation(); // Prevent bubbling to clue click
                const clueId = this.getAttribute('data-clue');
                const select = this.parentNode.querySelector('.solution-select');
                const input = this.parentNode.querySelector('.solution-text-input');
                
                let solution = '';
                if (select) {{
                    solution = select.value;
                }} else if (input) {{
                    solution = input.value;
                }}
                
                if (solution) {{
                    applySolutionToGrid(clueId, solution);
                }}
            }});
        }});
        
        // Prevent dropdown and input clicks from bubbling up
        document.querySelectorAll('.solution-dropdown, .solution-input').forEach(element => {{
            element.addEventListener('click', function(e) {{
                e.stopPropagation();
            }});
        }});
        
        // Prevent select and input clicks from bubbling up
        document.querySelectorAll('.solution-select, .solution-text-input').forEach(element => {{
            element.addEventListener('click', function(e) {{
                e.stopPropagation();
            }});
        }});
        
        function applySolutionToGrid(clueId, solution) {{
            console.log(`Applying solution "${{solution}}" to clue ${{clueId}}`);
            
            // Parse clue ID to get number and direction
            const [number, direction] = clueId.split('_');
            const clueNumber = parseInt(number);
            
            // For now, just show an alert - in a full implementation,
            // this would update the grid and propagate constraints
            alert(`Would apply solution "${{solution}}" to clue ${{clueId}}\\n\\nThis would:\\n1. Place the solution in the grid\\n2. Update all crossing clues\\n3. Remove incompatible solutions\\n4. Refresh the display`);
            
            // TODO: Implement full solution application:
            // 1. Get clue object by number
            // 2. Apply solution to grid cells
            // 3. Update all contingent clues
            // 4. Refresh the display
            
            // Update progress
            updateProgress();
        }}
        
        function updateProgress() {{
            const filledCells = Object.keys(solvedCells).length;
            const percentage = (filledCells / 64) * 100;
            
            document.querySelector('.progress-fill').style.width = percentage + '%';
            document.querySelector('.progress-stats').innerHTML = 
                `<div>Cells filled: ${{filledCells}}/64 (${{percentage.toFixed(1)}}%)</div>
                 <div>Clues solved: ${{filledCells}}/24</div>`;
        }}
        
        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', function() {{
            initializeClueObjects();
        }});
    </script>
</body>
</html>"""
    
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