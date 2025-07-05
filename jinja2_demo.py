#!/usr/bin/env python3
"""
Jinja2 Demo for Crossword Solver
Shows how the current f-string approach could be refactored using Jinja2 templating.
"""

import json
import os
import sys
from typing import Dict, List, Tuple
from jinja2 import Environment, Template

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from systematic_grid_parser import parse_grid, ClueTuple
from clue_classes import ListenerClue, ClueFactory, ClueManager, ClueParameters, AnagramClue

def load_clue_parameters(filename: str) -> Dict[Tuple[int, str], Tuple[int, int, int]]:
    """Load clue parameters from file."""
    clue_params = {}
    try:
        data_path = os.path.join('data', filename)
        with open(data_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or not line[0].isdigit():
                    continue
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
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        number = int(parts[0])
                        clue_text = parts[1]
                        clues[(number, current_direction)] = clue_text
    except FileNotFoundError:
        print(f"Warning: Could not find clues file {filename}")
    
    return clues

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
                new_clue = ClueFactory.from_tuple_and_parameters(
                    ClueTuple(number=number, direction=direction, cell_indices=clue.cell_indices, length=clue.length, parameters=(clue.length, -1, -1)),
                    -1, -1
                )
            else:
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
                        new_clue = clue
                except ValueError:
                    new_clue = clue
            
            # Update the clue object
            clue_objects[(number, direction)] = new_clue
            clue_manager.clues[number] = new_clue
    
    return grid_clues, clue_objects, clue_manager

def get_grid_clue_numbers() -> Dict[int, int]:
    """Get clue numbers for each cell position."""
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
    
    clue_numbers = {}
    for number, direction, cell_indices in grid_clues:
        if cell_indices:  # First cell of the clue
            clue_numbers[cell_indices[0]] = number
    
    return clue_numbers

def get_grid_borders() -> Dict[int, List[str]]:
    """Get border classes for each cell position."""
    # Initialize border sets
    thick_right_cells = set()
    thick_bottom_cells = set()
    thick_left_cells = set()
    thick_top_cells = set()
    
    # Define grid structure
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
    
    # Handle isolated cells and specific borders
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
    thick_top_cells.update([11, 12, 30, 25, 54])
    thick_left_cells.update([11, 51, 25, 54])
    thick_right_cells.update([11, 12, 30, 38, 51, 52, 54])
    thick_bottom_cells.update([30, 38, 51, 52, 25, 33])
    
    # Create border classes dictionary
    borders = {}
    for cell_index in range(64):
        border_classes = []
        if cell_index in thick_right_cells:
            border_classes.append('thick-right')
        if cell_index in thick_bottom_cells:
            border_classes.append('thick-bottom')
        if cell_index in thick_left_cells:
            border_classes.append('thick-left')
        if cell_index in thick_top_cells:
            border_classes.append('thick-top')
        borders[cell_index] = border_classes
    
    return borders

def prepare_clues_data(clue_objects: Dict[Tuple[int, str], ListenerClue], direction: str) -> List[Dict]:
    """Prepare clue data for template rendering."""
    clues = []
    for (number, dir), clue in clue_objects.items():
        if dir == direction:
            clue_id = f"{number}_{direction}"
            current_solutions = clue.get_valid_solutions()
            solution_count = len(current_solutions)
            clue_text = "Unclued" if clue.parameters.is_unclued else f"{clue.parameters.b}:{clue.parameters.c}"
            
            # Determine status class
            status_class = ""
            if solution_count > 1:
                status_class = "multiple"
            elif clue.parameters.is_unclued:
                status_class = "unclued"
            
            clues.append({
                'id': clue_id,
                'number': number,
                'direction': direction,
                'text': clue_text,
                'length': clue.length,
                'is_unclued': clue.parameters.is_unclued,
                'solution_count': solution_count,
                'solutions': current_solutions,
                'status_class': status_class
            })
    
    return sorted(clues, key=lambda x: x['number'])

def prepare_clue_objects_for_js(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> Dict:
    """Prepare clue objects for JavaScript consumption."""
    js_data = {}
    for (number, direction), clue in clue_objects.items():
        clue_id = f"{number}_{direction}"
        js_data[clue_id] = {
            'number': clue.number,
            'direction': clue.direction,
            'cell_indices': list(clue.cell_indices),
            'length': clue.length,
            'is_unclued': clue.parameters.is_unclued,
            'possible_solutions': list(clue.possible_solutions),
            'original_solution_count': clue.original_solution_count
        }
    return js_data

def generate_jinja2_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate HTML using Jinja2 templates."""
    
    # Prepare data for templates
    template_data = {
        'title': 'Jinja2 Crossword Solver Demo',
        'timestamp': 'Listener 4869, 24 May 2025',
        'grid_clue_numbers': get_grid_clue_numbers(),
        'grid_borders': get_grid_borders(),
        'solved_cells': {},  # Empty for demo
        'across_clues': prepare_clues_data(clue_objects, 'ACROSS'),
        'down_clues': prepare_clues_data(clue_objects, 'DOWN'),
        'clue_objects_json': json.dumps(prepare_clue_objects_for_js(clue_objects))
    }
    
    # Jinja2 template (embedded as string for demo)
    template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
        }
        
        .header h1 {
            color: #333;
            margin: 0;
        }
        
        .main-content {
            display: flex;
            gap: 30px;
            align-items: flex-start;
        }
        
        .grid-section {
            flex: 1;
        }
        
        .info-section {
            flex: 1;
            min-width: 400px;
        }
        
        .crossword-grid {
            display: inline-block;
            border: 3px solid #333;
            background-color: #333;
        }
        
        .grid-row {
            display: flex;
        }
        
        .grid-cell {
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
        }
        
        .grid-clue-number {
            position: absolute;
            top: 2px;
            left: 2px;
            font-size: 10px;
            color: #666;
            font-weight: normal;
        }
        
        .cell-value {
            font-size: 20px;
            color: #333;
        }
        
        .thick-right {
            border-right: 3px solid #333 !important;
        }
        
        .thick-bottom {
            border-bottom: 3px solid #333 !important;
        }
        
        .thick-left {
            border-left: 3px solid #333 !important;
        }
        
        .thick-top {
            border-top: 3px solid #333 !important;
        }
        
        .clues-section {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .clues-column {
            flex: 1;
        }
        
        .clues-column h3 {
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        
        .clue {
            margin-bottom: 8px;
            padding: 8px;
            border-radius: 4px;
            background-color: #f9f9f9;
            cursor: pointer;
            transition: background-color 0.2s;
            border: 2px solid transparent;
        }
        
        .clue:hover {
            background-color: #e9e9e9;
        }
        
        .clue.multiple {
            background-color: #fff3cd !important;
            color: #856404 !important;
        }
        
        .clue.unclued {
            background-color: #f8d7da !important;
            color: #721c24 !important;
            font-style: italic !important;
        }
        
        .clue-header {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .clue-number {
            font-weight: normal;
            min-width: 20px;
            color: #888;
            font-size: 13px;
            flex-shrink: 0;
        }
        
        .clue-text {
            flex: 1;
            margin-left: 8px;
            font-weight: bold;
            font-size: 16px;
            color: #222;
        }
        
        .solution-count {
            font-size: 12px;
            color: #666;
            text-align: right;
            flex-shrink: 0;
            min-width: 90px;
        }
        
        .demo-info {
            background-color: #e3f2fd;
            border: 1px solid #2196f3;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .demo-info h3 {
            color: #1976d2;
            margin-top: 0;
        }
        
        .demo-info ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .demo-info li {
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <div class="timestamp">{{ timestamp }}</div>
        </div>

        <div class="demo-info">
            <h3>🎯 Jinja2 Template Demo</h3>
            <p>This demonstrates how the crossword solver could be implemented using Jinja2 templating instead of f-strings.</p>
            <ul>
                <li><strong>No Escaping Issues:</strong> Jinja2 handles all curly brace escaping automatically</li>
                <li><strong>Cleaner Code:</strong> HTML structure is separate from Python logic</li>
                <li><strong>Better Maintainability:</strong> Templates can be edited with proper HTML tooling</li>
                <li><strong>Reusable:</strong> Templates can be extended and reused</li>
            </ul>
            <p><strong>Note:</strong> This is a static demo - the interactive functionality would need to be added separately.</p>
        </div>

        <div class="main-content">
            <div class="grid-section">
                <h3>Puzzle Grid (Jinja2 Generated)</h3>
                <div class="crossword-grid">
                    {% for row in range(8) %}
                    <div class="grid-row">
                        {% for col in range(8) %}
                            {% set cell_index = row * 8 + col %}
                            {% set clue_number = grid_clue_numbers.get(cell_index) %}
                            {% set cell_value = solved_cells.get(cell_index, '') %}
                            {% set border_classes = grid_borders.get(cell_index, []) %}
                            
                            <div class="grid-cell {{ ' '.join(border_classes) }}" data-cell="{{ cell_index }}">
                                {% if clue_number %}
                                    <div class="grid-clue-number">{{ clue_number }}</div>
                                {% endif %}
                                {% if cell_value %}
                                    <div class="cell-value">{{ cell_value }}</div>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="info-section">
                <div class="clues-section">
                    <div class="clues-column">
                        <h3>Across</h3>
                        {% for clue in across_clues %}
                        <div class="clue {{ clue.status_class }}" data-clue="{{ clue.id }}" data-grid-type="initial">
                            <div class="clue-header">
                                <span class="clue-number">{{ clue.number }}.</span>
                                <span class="clue-text">{{ clue.text }}</span>
                                {% if not clue.is_unclued %}
                                    <span class="solution-count">{{ clue.solution_count }} solutions</span>
                                {% else %}
                                    <span class="solution-count" id="unclued-count-{{ clue.id }}"></span>
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    
                    <div class="clues-column">
                        <h3>Down</h3>
                        {% for clue in down_clues %}
                        <div class="clue {{ clue.status_class }}" data-clue="{{ clue.id }}" data-grid-type="initial">
                            <div class="clue-header">
                                <span class="clue-number">{{ clue.number }}.</span>
                                <span class="clue-text">{{ clue.text }}</span>
                                {% if not clue.is_unclued %}
                                    <span class="solution-count">{{ clue.solution_count }} solutions</span>
                                {% else %}
                                    <span class="solution-count" id="unclued-count-{{ clue.id }}"></span>
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; margin-top: 20px;">
                    <h3>Template Data</h3>
                    <p><strong>Total Clues:</strong> {{ across_clues|length + down_clues|length }}</p>
                    <p><strong>Across Clues:</strong> {{ across_clues|length }}</p>
                    <p><strong>Down Clues:</strong> {{ down_clues|length }}</p>
                    <p><strong>Unclued Clues:</strong> {{ (across_clues + down_clues) | selectattr('is_unclued') | list | length }}</p>
                    <p><strong>Multiple Solutions:</strong> {{ (across_clues + down_clues) | selectattr('status_class', 'equalto', 'multiple') | list | length }}</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Demo JavaScript - shows how data is passed from Python to JS
        const clueObjects = {{ clue_objects_json | safe }};
        
        console.log('Jinja2 Demo - Clue Objects loaded:', Object.keys(clueObjects).length, 'clues');
        console.log('Sample clue data:', Object.values(clueObjects)[0]);
        
        // Add click handlers to show template functionality
        document.querySelectorAll('.clue').forEach(clueElement => {
            clueElement.addEventListener('click', function() {
                const clueId = this.getAttribute('data-clue');
                const clue = clueObjects[clueId];
                if (clue) {
                    alert(`Clue ${clueId}: ${clue.possible_solutions.length} possible solutions`);
                }
            });
        });
        
        // Add hover effect to grid cells
        document.querySelectorAll('.grid-cell').forEach(cell => {
            cell.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#e3f2fd';
            });
            cell.addEventListener('mouseleave', function() {
                this.style.backgroundColor = 'white';
            });
        });
    </script>
</body>
</html>
"""
    
    # Create Jinja2 template and render
    template = Template(template_str)
    return template.render(**template_data)

def main():
    """Main function to generate Jinja2 demo."""
    print("=== JINJA2 CROSSWORD SOLVER DEMO ===")
    
    # Load clue objects using existing logic
    grid_clues, clue_objects, clue_manager = load_clue_objects()
    
    print(f"Loaded {len(grid_clues)} grid clues")
    print(f"Loaded {len(clue_objects)} clue objects")
    
    # Generate HTML using Jinja2
    html_content = generate_jinja2_html(clue_objects)
    
    # Save to file
    filename = "jinja2_demo.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated Jinja2 demo: {filename}")
    print("Open this file in a web browser to see the Jinja2 templating approach")
    print("\nKey differences from f-string approach:")
    print("- No manual escaping of curly braces")
    print("- HTML structure is clearly visible in template")
    print("- Python logic is separate from presentation")
    print("- Easier to maintain and debug")
    
    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        print("Opened in default web browser")
    except:
        print("Please open the HTML file manually in your web browser")

if __name__ == "__main__":
    main() 