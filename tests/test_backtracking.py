"""
Test script to demonstrate the new backtracking capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'experimental'))

from utils import ListenerPuzzle
from experimental.puzzle_integration import integrate_puzzle as create_puzzle_from_files

def test_backtracking_capabilities():
    """Test the new backtracking features"""
    print("TESTING BACKTRACKING CAPABILITIES")
    print("="*60)
    
    # Create puzzle
    puzzle = create_puzzle_from_files()
    
    print("\nInitial puzzle state:")
    puzzle.print_puzzle_state()
    
    # Test constraint propagation first
    print("\n" + "="*60)
    print("STEP 1: CONSTRAINT PROPAGATION")
    print("="*60)
    
    success = puzzle.solve_constraint_propagation()
    print(f"Constraint propagation complete. Puzzle solved: {success}")
    
    if not success:
        print("\n" + "="*60)
        print("STEP 2: BACKTRACKING")
        print("="*60)
        
        # Show what clues remain unsolved
        unsolved_clues = [clue for clue in puzzle.clues.values() if not clue.is_solved()]
        print(f"Unsolved clues: {len(unsolved_clues)}")
        
        for clue in unsolved_clues:
            print(f"  Clue {clue.number} {clue.direction}: {len(clue.valid_solutions)} solutions")
            if len(clue.valid_solutions) <= 5:
                print(f"    Solutions: {clue.get_valid_solutions()}")
        
        # Test backtracking
        print("\nStarting backtracking solver...")
        success = puzzle.solve_with_backtracking()
        print(f"Backtracking complete. Puzzle solved: {success}")
    
    # Final state
    print("\n" + "="*60)
    print("FINAL STATE")
    print("="*60)
    
    if success:
        puzzle.print_solution()
    else:
        puzzle.print_puzzle_state()
    
    return puzzle, success

def test_state_management():
    """Test the state snapshot and restoration capabilities"""
    print("\n" + "="*60)
    print("TESTING STATE MANAGEMENT")
    print("="*60)
    
    # Create a simple puzzle for testing
    puzzle = create_puzzle_from_files()
    
    # Apply a few solutions
    print("Applying initial solutions...")
    puzzle.solve_constraint_propagation()
    
    # Create a snapshot
    print("Creating snapshot...")
    snapshot = puzzle.create_snapshot()
    
    # Apply more solutions
    print("Applying more solutions...")
    # Try to solve a specific clue manually
    clue_2 = puzzle.get_clue(2)
    if clue_2 and not clue_2.is_solved():
        solutions = clue_2.get_valid_solutions()
        if solutions:
            print(f"Applying solution {solutions[0]} to Clue 2")
            puzzle.apply_constraint(2, solutions[0])
    
    print("State after additional solutions:")
    puzzle.print_puzzle_state()
    
    # Restore snapshot
    print("Restoring snapshot...")
    puzzle.restore_snapshot(snapshot)
    
    print("State after restoration:")
    puzzle.print_puzzle_state()
    
    print("✓ State management test completed")

def test_backtracking_performance():
    """Test backtracking performance with different strategies"""
    print("\n" + "="*60)
    print("TESTING BACKTRACKING PERFORMANCE")
    print("="*60)
    
    puzzle = create_puzzle_from_files()
    
    # Test different backtracking strategies
    strategies = [
        ("Depth-first", "depth_first"),
        ("Breadth-first", "breadth_first"),
        ("Heuristic", "heuristic")
    ]
    
    for strategy_name, strategy in strategies:
        print(f"\nTesting {strategy_name} strategy:")
        
        # Reset puzzle
        puzzle = create_puzzle_from_files()
        puzzle.solve_constraint_propagation()
        
        # Time the backtracking
        import time
        start_time = time.time()
        
        success = puzzle.solve_with_backtracking(strategy=strategy)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"  Strategy: {strategy_name}")
        print(f"  Success: {success}")
        print(f"  Duration: {duration:.2f} seconds")
        
        if success:
            print(f"  ✓ {strategy_name} solved the puzzle")
        else:
            print(f"  ✗ {strategy_name} could not solve the puzzle")

def main():
    """Main test function"""
    print("LISTENER MATHS CROSSWORD - BACKTRACKING TEST")
    print("="*60)
    
    try:
        # Test basic backtracking
        puzzle, success = test_backtracking_capabilities()
        
        # Test state management
        test_state_management()
        
        # Test performance
        test_backtracking_performance()
        
        print("\n" + "="*60)
        print("ALL BACKTRACKING TESTS COMPLETED")
        print("="*60)
        
        if success:
            print("✓ Backtracking solver successfully solved the puzzle")
        else:
            print("✗ Backtracking solver could not solve the puzzle")
            
    except Exception as e:
        print(f"Error during backtracking tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 