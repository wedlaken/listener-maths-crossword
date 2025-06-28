"""
Test script to demonstrate puzzle solution presentation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'experimental'))
from puzzle_integration import create_puzzle_from_files
from puzzle_presenter import PuzzlePresenter

def test_puzzle_presentation():
    """Test the puzzle presentation functionality"""
    print("PUZZLE PRESENTATION TEST")
    print("="*60)
    
    # Create puzzle and solve it partially
    puzzle = create_puzzle_from_files()
    
    print("\nStep 1: Running constraint propagation...")
    puzzle.solve_constraint_propagation()
    
    # Create presenter
    presenter = PuzzlePresenter(puzzle)
    
    print("\n" + "="*60)
    print("STEP 1: SOLUTION SUMMARY")
    print("="*60)
    print(presenter.display_solution_summary())
    
    print("\n" + "="*60)
    print("STEP 2: SOLVED GRID")
    print("="*60)
    print(presenter.display_solved_grid(show_clue_numbers=True))
    
    print("\n" + "="*60)
    print("STEP 3: CLUE STATUS")
    print("="*60)
    print(presenter.display_clue_status(show_solutions=True))
    
    print("\n" + "="*60)
    print("STEP 4: DETAILED GRID")
    print("="*60)
    print(presenter.display_detailed_grid())
    
    return puzzle, presenter

def test_export_functionality():
    """Test exporting solutions to file"""
    print("\n" + "="*60)
    print("TESTING EXPORT FUNCTIONALITY")
    print("="*60)
    
    # Create puzzle and solve
    puzzle = create_puzzle_from_files()
    puzzle.solve_constraint_propagation()
    
    # Create presenter and export
    presenter = PuzzlePresenter(puzzle)
    
    # Export to file
    filename = "puzzle_solution_export.txt"
    presenter.export_solution_to_file(filename, include_details=True)
    
    print(f"✓ Solution exported to {filename}")
    
    # Show file contents preview
    print("\nFile contents preview:")
    print("-" * 40)
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:20]):  # Show first 20 lines
            print(line.rstrip())
        if len(lines) > 20:
            print("...")
            print(f"(File contains {len(lines)} total lines)")

def test_complete_solution_presentation():
    """Test the complete solution presentation"""
    print("\n" + "="*60)
    print("TESTING COMPLETE SOLUTION PRESENTATION")
    print("="*60)
    
    # Create puzzle and solve
    puzzle = create_puzzle_from_files()
    puzzle.solve_constraint_propagation()
    
    # Create presenter
    presenter = PuzzlePresenter(puzzle)
    
    # Show complete presentation
    presenter.print_complete_solution()

def main():
    """Main test function"""
    print("LISTENER MATHS CROSSWORD - PUZZLE PRESENTATION TEST")
    print("="*60)
    
    try:
        # Test basic presentation
        puzzle, presenter = test_puzzle_presentation()
        
        # Test export functionality
        test_export_functionality()
        
        # Test complete presentation
        test_complete_solution_presentation()
        
        print("\n" + "="*60)
        print("ALL PRESENTATION TESTS COMPLETE")
        print("="*60)
        
        # Show final status
        solved_clues = sum(1 for clue in puzzle.clues.values() if clue.is_solved())
        total_clues = len(puzzle.clues)
        solved_cells = len(puzzle.solved_cells)
        total_cells = 64
        
        print(f"Final Status:")
        print(f"  Clues solved: {solved_clues}/{total_clues} ({solved_clues/total_clues*100:.1f}%)")
        print(f"  Cells solved: {solved_cells}/{total_cells} ({solved_cells/total_cells*100:.1f}%)")
        
        if puzzle.is_puzzle_solved():
            print("✓ Puzzle is completely solved!")
        else:
            print("⚠ Puzzle partially solved - backtracking may be needed")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 