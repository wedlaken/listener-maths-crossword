"""
Test script to demonstrate the new backtracking capabilities
"""

from puzzle_integration import create_puzzle_from_files
from crossword_solver import ListenerPuzzle

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

def test_rejected_solutions():
    """Test the rejected solutions tracking"""
    print("\n" + "="*60)
    print("TESTING REJECTED SOLUTIONS")
    print("="*60)
    
    puzzle = create_puzzle_from_files()
    
    # Get a clue with multiple solutions
    clue_2 = puzzle.get_clue(2)
    if clue_2 and not clue_2.is_solved():
        print(f"Clue 2 initial state: {len(clue_2.valid_solutions)} valid solutions")
        print(f"Valid solutions: {clue_2.get_valid_solutions()}")
        
        # Eliminate a solution
        solutions = clue_2.get_valid_solutions()
        if solutions:
            solution_to_eliminate = solutions[0]
            print(f"Eliminating solution: {solution_to_eliminate}")
            clue_2.eliminate_solution(solution_to_eliminate, "test")
            
            print(f"After elimination: {len(clue_2.valid_solutions)} valid solutions")
            print(f"Rejected solutions: {clue_2.get_rejected_solutions()}")
            
            # Restore the solution
            print(f"Restoring solution: {solution_to_eliminate}")
            clue_2.restore_solution(solution_to_eliminate)
            
            print(f"After restoration: {len(clue_2.valid_solutions)} valid solutions")
            print(f"Rejected solutions: {clue_2.get_rejected_solutions()}")
    
    print("✓ Rejected solutions test completed")

def main():
    """Main test function"""
    print("LISTENER MATHS CROSSWORD - BACKTRACKING TEST")
    print("="*60)
    
    try:
        # Test backtracking capabilities
        puzzle, success = test_backtracking_capabilities()
        
        # Test state management
        test_state_management()
        
        # Test rejected solutions
        test_rejected_solutions()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETE")
        print("="*60)
        
        if success:
            print("✓ Puzzle solved successfully with backtracking!")
        else:
            print("✗ Puzzle not fully solved")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 