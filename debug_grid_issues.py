"""
Debug script to investigate grid structure issues
"""

from puzzle_integration import create_puzzle_from_files
from puzzle_presenter import PuzzlePresenter

def debug_grid_issues():
    """Debug the grid structure issues"""
    print("DEBUGGING GRID STRUCTURE ISSUES")
    print("="*60)
    
    # Create puzzle
    puzzle = create_puzzle_from_files()
    
    print("\nStep 1: Initial puzzle state before solving")
    print("-" * 40)
    presenter = PuzzlePresenter(puzzle)
    print(presenter.display_solution_summary())
    
    # Check specific clues that seem wrong
    print("\nStep 2: Checking specific clues")
    print("-" * 40)
    
    # Check Clue 1 ACROSS (should be 4 digits)
    clue_1_across = puzzle.get_clue(1)
    if clue_1_across:
        print(f"Clue 1 ACROSS: {clue_1_across}")
        print(f"  Cell indices: {clue_1_across.cell_indices}")
        print(f"  Length: {clue_1_across.length}")
        print(f"  Parameters: b={clue_1_across.b}, c={clue_1_across.c}")
        print(f"  Valid solutions: {clue_1_across.get_valid_solutions()}")
    
    # Check Clue 1 DOWN (should be 4 digits)
    clue_1_down = None
    for clue in puzzle.clues.values():
        if clue.number == 1 and clue.direction == "DOWN":
            clue_1_down = clue
            break
    
    if clue_1_down:
        print(f"\nClue 1 DOWN: {clue_1_down}")
        print(f"  Cell indices: {clue_1_down.cell_indices}")
        print(f"  Length: {clue_1_down.length}")
        print(f"  Parameters: b={clue_1_down.b}, c={clue_1_down.c}")
        print(f"  Valid solutions: {clue_1_down.get_valid_solutions()}")
    
    # Check what happens during constraint propagation
    print("\nStep 3: Running constraint propagation step by step")
    print("-" * 40)
    
    # Find clues that can be solved immediately
    solvable_clues = [clue for clue in puzzle.clues.values() if clue.is_solved()]
    print(f"Initially solvable clues: {len(solvable_clues)}")
    
    for clue in solvable_clues:
        print(f"  Clue {clue.number} {clue.direction}: {clue.get_solution()}")
    
    # Apply first solution and see what happens
    if solvable_clues:
        first_clue = solvable_clues[0]
        print(f"\nApplying first solution: Clue {first_clue.number} {first_clue.direction} = {first_clue.get_solution()}")
        
        # Show grid before
        print("\nGrid BEFORE applying solution:")
        print(presenter.display_solved_grid(show_clue_numbers=False))
        
        # Apply solution
        eliminated = puzzle.apply_constraint(first_clue.number, first_clue.get_solution())
        print(f"Eliminated {len(eliminated)} incompatible solutions")
        
        # Show grid after
        print("\nGrid AFTER applying solution:")
        print(presenter.display_solved_grid(show_clue_numbers=False))
        
        # Show what cells were filled
        print("\nCells filled by this solution:")
        solution_str = str(first_clue.get_solution()).zfill(first_clue.length)
        for i, cell_index in enumerate(first_clue.cell_indices):
            digit = int(solution_str[i])
            print(f"  Cell {cell_index}: {digit}")
    
    print("\n" + "="*60)
    print("DEBUG COMPLETE")
    print("="*60)

if __name__ == "__main__":
    debug_grid_issues() 