"""
Tests for solver.renderers module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.renderers import (
    generate_grid_html,
    generate_anagram_grid_html,
    create_clue_id,
    get_clue_number_at_cell
)
from solver.grid import get_grid_structure


def test_create_clue_id():
    """Test clue ID creation."""
    assert create_clue_id(1, "ACROSS") == "1_ACROSS"
    assert create_clue_id(14, "DOWN") == "14_DOWN"
    assert create_clue_id(23, "ACROSS") == "23_ACROSS"
    print("✅ Clue ID creation tests passed")


def test_get_clue_number_at_cell():
    """Test clue number retrieval."""
    grid_clues = get_grid_structure()
    
    # Cell 0 should have clue 1 (first cell of 1A and 1D)
    assert get_clue_number_at_cell(0, grid_clues) == 1
    
    # Cell 1 should have clue 2 (first cell of 2D)
    assert get_clue_number_at_cell(1, grid_clues) == 2
    
    # Cell 2 should have clue 3 (first cell of 3D)
    assert get_clue_number_at_cell(2, grid_clues) == 3
    
    # Cell 3 should be None (not first cell of any clue)
    assert get_clue_number_at_cell(3, grid_clues) is None
    
    print("✅ Clue number retrieval tests passed")


def test_generate_grid_html():
    """Test basic grid HTML generation."""
    html = generate_grid_html()
    
    # Check for key HTML elements
    assert '<div class="crossword-grid">' in html
    assert 'grid-cell' in html
    assert 'grid-row' in html
    
    # Check grid has correct number of cells (64 cells in 8x8 grid)
    assert html.count('grid-cell') >= 64
    
    # Check for grid wrapper
    assert '<div class="grid-wrapper">' in html
    
    print("✅ Grid HTML generation tests passed")


def test_generate_grid_html_with_cells():
    """Test grid HTML generation with solved cells."""
    solved_cells = {
        0: '1',
        1: '2',
        2: '3',
        3: '4'
    }
    
    html = generate_grid_html(solved_cells)
    
    # Check that cell values are included
    assert '<div class="cell-value">1</div>' in html
    assert '<div class="cell-value">2</div>' in html
    assert '<div class="cell-value">3</div>' in html
    assert '<div class="cell-value">4</div>' in html
    
    print("✅ Grid HTML with cells tests passed")


def test_generate_anagram_grid_html():
    """Test anagram grid HTML generation."""
    html = generate_anagram_grid_html()
    
    # Check for anagram-specific classes
    assert 'anagram-grid' in html
    assert 'anagram-cell' in html
    assert 'data-anagram="true"' in html
    
    # Check basic grid structure still present
    assert 'grid-cell' in html
    assert 'grid-row' in html
    
    print("✅ Anagram grid HTML generation tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Renderers Module Tests")
    print("=" * 60)
    
    test_create_clue_id()
    test_get_clue_number_at_cell()
    test_generate_grid_html()
    test_generate_grid_html_with_cells()
    test_generate_anagram_grid_html()
    
    print("=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
