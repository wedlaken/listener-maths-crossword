"""
Simple test to verify backtracking functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'experimental'))

from experimental.puzzle_integration import integrate_puzzle as create_puzzle_from_files

def test_simple_backtracking():
    """Test basic backtracking functionality"""
    print("SIMPLE BACKTRACKING TEST")
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
        print("STEP 2: BACKTRACKING (LIMITED)")
        print("="*60)
        
        # Show what clues remain unsolved
        unsolved_clues = [clue for clue in puzzle.clues.values() if not clue.is_solved()]
        print(f"Unsolved clues: {len(unsolved_clues)}")
        
        for clue in unsolved_clues:
            print(f"  Clue {clue.number} {clue.direction}: {len(clue.valid_solutions)} solutions")
            if len(clue.valid_solutions) <= 5:
                print(f"    Solutions: {clue.get_valid_solutions()}")
        
        # Test backtracking with limited depth
        print("\nStarting backtracking solver (max depth 10)...")
        success = puzzle._solve_backtracking(depth=0, max_depth=10)
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
    """Test state snapshot and restoration"""
    print("\n" + "="*60)
    print("TESTING STATE MANAGEMENT")
    print("="*60)
    
    puzzle = create_puzzle_from_files()
    
    # Apply some solutions
    print("Applying initial solutions...")
    puzzle.solve_constraint_propagation()
    
    # Create snapshot
    print("Creating snapshot...")
    snapshot = puzzle.create_snapshot()
    
    # Apply a solution manually
    clue_2 = puzzle.get_clue(2)
    if clue_2 and not clue_2.is_solved():
        solutions = clue_2.get_valid_solutions()
        if solutions:
            print(f"Applying solution {solutions[0]} to Clue 2")
            puzzle.apply_constraint(2, solutions[0])
    
    print("State after manual solution:")
    puzzle.print_puzzle_state()
    
    # Restore snapshot
    print("Restoring snapshot...")
    puzzle.restore_snapshot(snapshot)
    
    print("State after restoration:")
    puzzle.print_puzzle_state()
    
    print("✓ State management test completed")

def main():
    """Main test function"""
    print("LISTENER MATHS CROSSWORD - SIMPLE BACKTRACKING TEST")
    print("="*60)
    
    try:
        # Test simple backtracking
        puzzle, success = test_simple_backtracking()
        
        # Test state management
        test_state_management()
        
        print("\n" + "="*60)
        print("SIMPLE BACKTRACKING TEST COMPLETE")
        print("="*60)
        
        if success:
            print("✓ Simple backtracking test passed")
        else:
            print("✗ Simple backtracking test failed")
            
    except Exception as e:
        print(f"Error during simple backtracking test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 