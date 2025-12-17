"""
HTML Renderers Module

Generates HTML for crossword grids and clue lists.
This module handles all HTML generation for the interactive solver.
"""

from typing import Dict, List, Tuple, Optional
from solver.grid import get_grid_structure, calculate_grid_borders


def get_clue_number_at_cell(cell_index: int, grid_clues: List[Tuple[int, str, Tuple[int, ...]]]) -> Optional[int]:
    """
    Get the clue number at a specific cell, if any.
    
    Args:
        cell_index: The cell index to check
        grid_clues: List of (number, direction, cell_indices) tuples
        
    Returns:
        Clue number if this is the first cell of a clue, None otherwise
    """
    for number, direction, cell_indices in grid_clues:
        if cell_indices[0] == cell_index:  # First cell of the clue
            return number
    return None


def generate_base_grid_html(
    solved_cells: Dict[int, str] = None,
    grid_clues: List[Tuple[int, str, Tuple[int, ...]]] = None,
    additional_classes: str = "",
    additional_attributes: str = "",
    cell_additional_classes: str = "",
    cell_additional_attributes: str = ""
) -> str:
    """
    Generate base HTML for the crossword grid with shared logic.
    
    Args:
        solved_cells: Dictionary mapping cell indices to digit strings
        grid_clues: Grid structure (defaults to get_grid_structure())
        additional_classes: Additional CSS classes for the grid container
        additional_attributes: Additional HTML attributes for the grid container
        cell_additional_classes: Additional CSS classes for each cell
        cell_additional_attributes: Additional HTML attributes for each cell
        
    Returns:
        HTML string for the grid
    """
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


def generate_grid_html(solved_cells: Dict[int, str] = None) -> str:
    """
    Generate HTML for the initial crossword grid.
    
    Args:
        solved_cells: Dictionary mapping cell indices to digit strings
        
    Returns:
        HTML string for the grid with wrapper
    """
    base_grid = generate_base_grid_html(solved_cells)
    return f'<div class="grid-wrapper">\n{base_grid}\n</div>'


def generate_anagram_grid_html(solved_cells: Dict[int, str] = None) -> str:
    """
    Generate HTML for the anagram crossword grid.
    
    Args:
        solved_cells: Dictionary mapping cell indices to digit strings
        
    Returns:
        HTML string for the anagram grid
    """
    return generate_base_grid_html(
        solved_cells=solved_cells,
        additional_classes=" anagram-grid",
        additional_attributes=' id="anagram-grid"',
        cell_additional_classes=" anagram-cell",
        cell_additional_attributes=' data-anagram="true"'
    )


def create_clue_id(number: int, direction: str) -> str:
    """
    Create a unique identifier for a clue.
    
    Args:
        number: Clue number
        direction: Direction (ACROSS or DOWN)
        
    Returns:
        Unique clue ID like "1_ACROSS" or "2_DOWN"
    """
    return f"{number}_{direction}"


def generate_clue_column_html(
    clues: List,
    direction: str,
    title: str,
    clue_id_prefix: str = "",
    additional_classes: str = "",
    grid_type: str = "initial"
) -> str:
    """
    Generate HTML for a column of clues (Across or Down) with shared logic.
    
    Args:
        clues: List of clue objects (ListenerClue or AnagramClue)
        direction: Direction (ACROSS or DOWN)
        title: Column title
        clue_id_prefix: Optional prefix for clue IDs (e.g., "anagram_")
        additional_classes: Additional CSS classes for clues
        grid_type: Type of grid ("initial" or "anagram")
        
    Returns:
        HTML string for the clue column
    """
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


def generate_clues_html(clue_objects: Dict[Tuple[int, str], any]) -> str:
    """
    Generate HTML for the clues section using clue objects.
    
    Args:
        clue_objects: Dictionary mapping (number, direction) to ListenerClue objects
        
    Returns:
        HTML string for the clues section
    """
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


def generate_anagram_clues_html(anagram_clue_objects: Dict[Tuple[int, str], any]) -> str:
    """
    Generate HTML for the anagram clues section using AnagramClue objects.
    
    Args:
        anagram_clue_objects: Dictionary mapping (number, direction) to AnagramClue objects
        
    Returns:
        HTML string for the anagram clues section
    """
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
