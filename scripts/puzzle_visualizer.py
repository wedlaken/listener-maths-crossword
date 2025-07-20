#!/usr/bin/env python3
"""
Puzzle visualizer that generates HTML output for grid display
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Tuple, List, Optional

from utils import parse_grid

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
        print(f"Error: File '{filename}' not found.")
    
    return clue_params

def create_clue_id(number: int, direction: str) -> str:
    """Create unique clue ID like 'A1', 'D1'"""
    prefix = "A" if direction == "ACROSS" else "D"
    return f"{prefix}{number}"

def get_clue_number_at_cell(cell_index: int, grid_clues: List[Tuple[int, str, Tuple[int, ...]]]) -> Optional[int]:
    """Get the clue number at a specific cell, if any."""
    for number, direction, cell_indices in grid_clues:
        if cell_indices[0] == cell_index:  # First cell of the clue
            return number
    return None

def generate_html_grid(grid_clues: List[Tuple[int, str, Tuple[int, ...]]], 
                      solved_cells: Dict[int, int] = None,
                      solved_clues: Dict[str, int] = None,
                      title: str = "Listener Maths Crossword") -> str:
    """Generate HTML for the puzzle grid."""
    
    if solved_cells is None:
        solved_cells = {}
    if solved_clues is None:
        solved_clues = {}
    
    # Create 8x8 grid
    grid_html = []
    grid_html.append('<div class="crossword-grid">')
    
    # Create sets of cells that should have thick borders
    # For barred crossword: thick borders mark the END of clues/solutions
    thick_right_cells = set()
    thick_bottom_cells = set()
    thick_left_cells = set()
    thick_top_cells = set()
    
    # Process ACROSS clues to find thick right borders
    across_clues = [clue for clue in grid_clues if clue[1] == 'ACROSS']
    for number, direction, cell_indices in across_clues:
        if len(cell_indices) > 0:
            # The last cell of each ACROSS clue gets a thick right border
            # BUT exclude cells in the rightmost column (column 7) since they already have grid border
            # AND exclude cells 30 and 38 since they have manual border assignments
            last_cell = cell_indices[-1]
            if last_cell % 8 != 7 and last_cell not in {30, 38}:  # Not in rightmost column and not manually assigned
                thick_right_cells.add(last_cell)
    
    # Process DOWN clues to find thick bottom borders
    down_clues = [clue for clue in grid_clues if clue[1] == 'DOWN']
    for number, direction, cell_indices in down_clues:
        if len(cell_indices) > 0:
            # The last cell of each DOWN clue gets a thick bottom border
            # BUT exclude cells in the bottom row (row 7) since they already have grid border
            last_cell = cell_indices[-1]
            if last_cell < 56:  # Not in bottom row (cells 56-63)
                thick_bottom_cells.add(last_cell)
    
    # Find all cells that are part of ACROSS clues
    across_cells = set()
    for number, direction, cell_indices in across_clues:
        across_cells.update(cell_indices)
    
    # Find all cells that are part of DOWN clues
    down_cells = set()
    for number, direction, cell_indices in down_clues:
        down_cells.update(cell_indices)
    
    # Handle isolated cells that need borders on multiple sides
    # These are cells that are not part of ACROSS clues and need isolation
    isolated_cells = {9, 14, 49}  # Based on your analysis - removed cell 21
    
    for cell_index in isolated_cells:
        if cell_index not in across_cells:
            # Cell is not part of any ACROSS clue, so it needs left and right borders
            if cell_index % 8 != 0:  # Not leftmost column
                thick_left_cells.add(cell_index)
            if cell_index % 8 != 7:  # Not rightmost column
                thick_right_cells.add(cell_index)
        
        # Check if cell needs top/bottom borders for isolation
        # This is more complex and depends on the specific grid structure
        # For now, we'll handle the specific cases you mentioned
        
        # Cell 9: needs left, right, bottom borders
        if cell_index == 9:
            thick_left_cells.add(9)
            thick_right_cells.add(9)
            thick_bottom_cells.add(9)
        
        # Cell 14: needs left, top, bottom borders
        elif cell_index == 14:
            thick_left_cells.add(14)
            thick_top_cells.add(14)
            thick_bottom_cells.add(14)
        
        # Cell 49: needs top, bottom, right borders
        elif cell_index == 49:
            thick_top_cells.add(49)
            thick_bottom_cells.add(49)
            thick_right_cells.add(49)
    
    # Add specific borders for cell pair separations
    # These are based on the 90-degree rotation pattern you described
    
    # Cells 11 and 12 separation - thick borders around both cells (except bottom since they're DOWN clues)
    # Cell 11: top, left, right borders
    thick_top_cells.add(11)  # Top border for cell 11
    thick_left_cells.add(11)  # Left border for cell 11
    thick_right_cells.add(11)  # Right border for cell 11 (border between 11 and 12)
    # Cell 12: top, right borders (left border handled by cell 11's right border)
    thick_top_cells.add(12)  # Top border for cell 12
    thick_right_cells.add(12)  # Right border for cell 12
    
    # Cells 30 and 38 separation (90° rotation) - mirrored pattern
    # Cell 30: right, top borders
    thick_right_cells.add(30)  # Right border for cell 30
    thick_top_cells.add(30)    # Top border for cell 30
    # Cell 38: right, bottom borders
    thick_right_cells.add(38)  # Right border for cell 38
    thick_bottom_cells.add(38) # Bottom border for cell 38
    # Thick border between them (bottom of 30)
    thick_bottom_cells.add(30) # Bottom border for cell 30 (border between 30 and 38)
    
    # Cells 51 and 52 separation (180° rotation) - thick border between them
    thick_left_cells.add(51)   # Left border for cell 51
    thick_right_cells.add(51)  # Right border for cell 51 (border between 51 and 52)
    thick_right_cells.add(52)  # Right border for cell 52
    thick_bottom_cells.add(51) # Bottom border for cell 51
    thick_bottom_cells.add(52) # Bottom border for cell 52

    # Cells 25 and 33 separation (270° rotation) - mirrored pattern
    # Cell 25: left, top borders
    thick_left_cells.add(25)   # Left border for cell 25
    thick_top_cells.add(25)    # Top border for cell 25
    # Cell 33: left, bottom borders
    thick_left_cells.add(33)   # Left border for cell 33
    thick_bottom_cells.add(33) # Bottom border for cell 33
    # Thick border between them (bottom of 25)
    thick_bottom_cells.add(25) # Bottom border for cell 25 (border between 25 and 33)
    
    # Cell 54 borders (90° rotation of cell 14's borders)
    # Cell 14 has: thick-bottom, thick-left, thick-top
    # Cell 54 should have: thick-left, thick-top, thick-right (90° rotation)
    thick_left_cells.add(54)   # Left border for cell 54
    thick_top_cells.add(54)    # Top border for cell 54
    thick_right_cells.add(54)  # Right border for cell 54
    
    # Add thick borders for cells that end clues in both directions
    for row in range(8):
        grid_html.append('  <div class="grid-row">')
        for col in range(8):
            cell_index = row * 8 + col
            
            # Get clue number for this cell
            clue_number = get_clue_number_at_cell(cell_index, grid_clues)
            
            # Check if cell is solved
            cell_value = solved_cells.get(cell_index, '')
            
            # Determine border classes
            border_classes = []
            
            # Apply thick right border if this cell ends an ACROSS clue
            if cell_index in thick_right_cells:
                border_classes.append('thick-right')
            
            # Apply thick bottom border if this cell ends a DOWN clue
            if cell_index in thick_bottom_cells:
                border_classes.append('thick-bottom')
            
            # Apply thick left border for isolated cells
            if cell_index in thick_left_cells:
                border_classes.append('thick-left')
            
            # Apply thick top border for isolated cells
            if cell_index in thick_top_cells:
                border_classes.append('thick-top')
            
            border_class = ' '.join(border_classes)
            
            # Create cell
            cell_html = f'    <div class="grid-cell {border_class}">'
            if clue_number:
                cell_html += f'<div class="clue-number">{clue_number}</div>'
            if cell_value:
                cell_html += f'<div class="cell-value">{cell_value}</div>'
            cell_html += '</div>'
            
            grid_html.append(cell_html)
        
        grid_html.append('  </div>')
    
    grid_html.append('</div>')
    
    return '\n'.join(grid_html)

def generate_clues_html(clue_params: Dict[Tuple[int, str], Tuple[int, int, int]], 
                       solved_clues: Dict[str, int] = None) -> str:
    """Generate HTML for the clues section."""
    
    if solved_clues is None:
        solved_clues = {}
    
    clues_html = []
    clues_html.append('<div class="clues-section">')
    
    # Across clues
    clues_html.append('  <div class="clues-column">')
    clues_html.append('    <h3>Across</h3>')
    
    across_clues = []
    for (number, direction), (a, b, c) in clue_params.items():
        if direction == "ACROSS":
            clue_id = create_clue_id(number, direction)
            if clue_id in solved_clues:
                across_clues.append((number, f'      <div class="clue solved">{number}. {solved_clues[clue_id]}</div>'))
            elif b == 0 and c == 0:
                across_clues.append((number, f'      <div class="clue unclued">{number}. Unclued</div>'))
            else:
                across_clues.append((number, f'      <div class="clue">{number}. b={b}, c={c}</div>'))
    
    across_clues.sort(key=lambda x: x[0])
    clues_html.extend([clue_html for _, clue_html in across_clues])
    clues_html.append('  </div>')
    
    # Down clues
    clues_html.append('  <div class="clues-column">')
    clues_html.append('    <h3>Down</h3>')
    
    down_clues = []
    for (number, direction), (a, b, c) in clue_params.items():
        if direction == "DOWN":
            clue_id = create_clue_id(number, direction)
            if clue_id in solved_clues:
                down_clues.append((number, f'      <div class="clue solved">{number}. {solved_clues[clue_id]}</div>'))
            elif b == 0 and c == 0:
                down_clues.append((number, f'      <div class="clue unclued">{number}. Unclued</div>'))
            else:
                down_clues.append((number, f'      <div class="clue">{number}. b={b}, c={c}</div>'))
    
    down_clues.sort(key=lambda x: x[0])
    clues_html.extend([clue_html for _, clue_html in down_clues])
    clues_html.append('  </div>')
    
    clues_html.append('</div>')
    
    return '\n'.join(clues_html)

def generate_progress_html(solved_count: int, total_count: int, solved_cells: int) -> str:
    """Generate HTML for progress information."""
    percentage = (solved_count / total_count * 100) if total_count > 0 else 0
    
    progress_html = f"""
<div class="progress-section">
  <h3>Progress</h3>
  <div class="progress-bar">
    <div class="progress-fill" style="width: {percentage:.1f}%"></div>
  </div>
  <div class="progress-stats">
    <div>Clues solved: {solved_count}/{total_count} ({percentage:.1f}%)</div>
    <div>Cells filled: {solved_cells}/64 ({solved_cells/64*100:.1f}%)</div>
  </div>
</div>
"""
    return progress_html

def generate_full_html(grid_clues: List[Tuple[int, str, Tuple[int, ...]]], 
                      clue_params: Dict[Tuple[int, str], Tuple[int, int, int]],
                      solved_cells: Dict[int, int] = None,
                      solved_clues: Dict[str, int] = None,
                      title: str = "Listener Maths Crossword",
                      iteration: int = None) -> str:
    """Generate complete HTML page."""
    
    if solved_cells is None:
        solved_cells = {}
    if solved_clues is None:
        solved_clues = {}
    
    solved_count = len(solved_clues)
    total_count = len(clue_params)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
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
        
        .header .timestamp {{
            color: #666;
            font-size: 14px;
            margin-top: 5px;
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
            min-width: 300px;
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
            /* Use box-sizing to include borders in width/height */
            box-sizing: border-box;
            /* Default thin borders */
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
        
        /* Remove borders from rightmost column and bottom row */
        .grid-cell:nth-child(8n) {{
            border-right: none;
        }}
        
        .grid-row:last-child .grid-cell {{
            border-bottom: none;
        }}
        
        /* Thick borders for barred crossword effect */
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
            padding: 5px;
            border-radius: 4px;
            background-color: #f9f9f9;
        }}
        
        .clue.solved {{
            background-color: #d4edda;
            color: #155724;
            font-weight: bold;
        }}
        
        .clue.unclued {{
            background-color: #fff3cd;
            color: #856404;
            font-style: italic;
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
        
        .iteration-info {{
            background-color: #e7f3ff;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }}
        
        .iteration-info h3 {{
            margin: 0 0 5px 0;
            color: #007bff;
        }}
        
        .iteration-info p {{
            margin: 0;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
"""
    
    if iteration is not None:
        html += f"""
        <div class="iteration-info">
            <h3>Iteration {iteration}</h3>
            <p>Solving progress at this step</p>
        </div>
"""
    
    html += f"""
        <div class="main-content">
            <div class="grid-section">
                <h3>Puzzle Grid</h3>
                {generate_html_grid(grid_clues, solved_cells, solved_clues)}
            </div>
            
            <div class="info-section">
                {generate_clues_html(clue_params, solved_clues)}
                {generate_progress_html(solved_count, total_count, len(solved_cells))}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html

def save_html_output(html_content: str, filename: str = None) -> str:
    """Save HTML content to file and return the filename."""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"puzzle_output_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def main():
    """Test the visualizer."""
    print("=== PUZZLE VISUALIZER TEST ===")
    
    # Load data
    grid_clues = parse_grid()
    clue_params = load_clue_parameters("data/Listener 4869 clues.txt")
    
    # Create some test solved cells and clues
    solved_cells = {
        0: 1, 1: 2, 2: 1, 3: 5,  # A1 = 1215
        8: 2, 16: 0, 24: 4,      # D1 = 2048
        20: 1, 21: 4, 22: 3, 23: 0,  # A11 = 1430
    }
    
    solved_clues = {
        "A1": 1215,
        "D1": 2048,
        "A11": 1430,
    }
    
    # Generate HTML
    html_content = generate_full_html(
        grid_clues=grid_clues,
        clue_params=clue_params,
        solved_cells=solved_cells,
        solved_clues=solved_clues,
        title="Listener Maths Crossword - Test Output",
        iteration=1
    )
    
    # Save to file
    filename = save_html_output(html_content, "puzzle_visualizer_test.html")
    
    print(f"Generated HTML output: {filename}")
    print(f"Open this file in a web browser to see the puzzle visualization")

if __name__ == "__main__":
    main() 