"""
Show the current puzzle grid state
"""

from puzzle_integration import create_puzzle_from_files
from puzzle_presenter import PuzzlePresenter

def show_current_grid():
    """Display the current puzzle grid state"""
    print("LISTENER MATHS CROSSWORD - CURRENT STATE")
    print("="*60)
    
    # Create puzzle and solve with constraint propagation
    puzzle = create_puzzle_from_files()
    puzzle.solve_constraint_propagation()
    
    # Create presenter
    presenter = PuzzlePresenter(puzzle)
    
    # Show solution summary
    print(presenter.display_solution_summary())
    
    # Show the solved grid
    print(presenter.display_solved_grid(show_clue_numbers=True))
    
    # Show clue status
    print(presenter.display_clue_status(show_solutions=False))
    
    print("\n" + "="*60)
    print("CURRENT STATE DISPLAY COMPLETE")
    print("="*60)

if __name__ == "__main__":
    show_current_grid() 