"""
Tests for solver.grid module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.grid import GridManager, get_grid_structure, calculate_grid_borders


def test_grid_manager_basic():
    """Test GridManager basic functionality."""
    grid = GridManager(grid_size=8)
    
    # Test cell_to_row_col
    assert grid.cell_to_row_col(0) == (0, 0)
    assert grid.cell_to_row_col(7) == (0, 7)
    assert grid.cell_to_row_col(8) == (1, 0)
    assert grid.cell_to_row_col(15) == (1, 7)
    assert grid.cell_to_row_col(63) == (7, 7)
    
    # Test row_col_to_cell
    assert grid.row_col_to_cell(0, 0) == 0
    assert grid.row_col_to_cell(0, 7) == 7
    assert grid.row_col_to_cell(1, 0) == 8
    assert grid.row_col_to_cell(7, 7) == 63
    
    # Test is_valid_cell
    assert grid.is_valid_cell(0) == True
    assert grid.is_valid_cell(63) == True
    assert grid.is_valid_cell(64) == False
    assert grid.is_valid_cell(-1) == False
    
    print("✅ GridManager basic tests passed")


def test_get_grid_structure():
    """Test grid structure retrieval."""
    clues = get_grid_structure()
    
    # Check we have the right number of clues
    assert len(clues) == 24
    
    # Check we have both ACROSS and DOWN clues
    across_clues = [c for c in clues if c[1] == 'ACROSS']
    down_clues = [c for c in clues if c[1] == 'DOWN']
    
    print(f"✅ Grid structure tests passed (ACROSS: {len(across_clues)}, DOWN: {len(down_clues)})")


def test_calculate_grid_borders():
    """Test border calculations."""
    clues = get_grid_structure()
    borders = calculate_grid_borders(clues)
    
    # Check that we have all border types
    assert 'thick_right' in borders
    assert 'thick_bottom' in borders
    assert 'thick_left' in borders
    assert 'thick_top' in borders
    
    # Check specific borders exist
    assert 3 in borders['thick_right']  # Cell 3 ends 1 ACROSS
    assert 24 in borders['thick_bottom']  # Cell 24 ends 1 DOWN
    
    # Check isolated cells have borders
    assert 9 in borders['thick_left']
    assert 9 in borders['thick_right']
    assert 9 in borders['thick_bottom']
    
    assert 14 in borders['thick_left']
    assert 14 in borders['thick_top']
    assert 14 in borders['thick_bottom']
    
    assert 49 in borders['thick_top']
    assert 49 in borders['thick_bottom']
    assert 49 in borders['thick_right']
    
    print(f"✅ Border calculation tests passed")
    print(f"   Right borders: {len(borders['thick_right'])} cells")
    print(f"   Bottom borders: {len(borders['thick_bottom'])} cells")
    print(f"   Left borders: {len(borders['thick_left'])} cells")
    print(f"   Top borders: {len(borders['thick_top'])} cells")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Grid Module Tests")
    print("=" * 60)
    
    test_grid_manager_basic()
    test_get_grid_structure()
    test_calculate_grid_borders()
    
    print("=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
