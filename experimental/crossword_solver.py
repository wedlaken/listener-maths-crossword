"""
LEGACY CODE - MOVED TO EXPERIMENTAL FOLDER

This file contains the original automatic puzzle solving approach that has been
superseded by the interactive solver approach. This code represents the pre-ground
truth data era when we were still working with OCR and automatic solving.

CURRENT STATUS: LEGACY/EXPERIMENTAL
- Contains automatic puzzle solving algorithms (not interactive)
- Uses legacy ListenerClue class with different interface than clue_classes.py
- Includes backtracking algorithms for complete automation
- Predates the ground truth data approach
- Not used by the current interactive solver

CURRENT APPROACH:
- interactive_solver.py uses clue_classes.py for interactive solving
- Ground truth data approach eliminates OCR dependencies
- Human-guided solving with constraint propagation
- Real-time interactive interface

This file should be moved to the experimental/ folder as it represents an
earlier development phase and is no longer part of the main application.

DEPENDENCIES:
- Used by some experimental solvers and tests
- Contains ListenerClue and ListenerPuzzle classes (legacy versions)
- Contains CrosswordGrid class for automated solving

MIGRATION:
- New interactive approach uses clue_classes.py instead
- ClueFactory and ClueManager provide better separation of concerns
- Ground truth data eliminates OCR dependencies
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from listener import find_solutions

@dataclass
class Clue:
    number: int
    direction: str  # 'ACROSS' or 'DOWN'
    length: int
    position: Tuple[int, int]  # (row, col)
    parameters: Tuple[int, int, int]  # (a, b, c) for find_solutions
    possible_solutions: List[int] = None
    cell_indices: Tuple[int, ...] = None  # Cell indices (1-64) this clue occupies

class ListenerClue:
    """Enhanced clue class for Listener puzzles with unique identifiers"""
    
    def __init__(self, clue_id: str, direction: str, cell_indices: Tuple[int, ...], 
                 parameters: Tuple[int, int, int]):
        self.clue_id = clue_id  # Unique identifier like "A1", "D1"
        self.direction = direction
        self.cell_indices = cell_indices
        self.length = len(cell_indices)  # 'a' parameter from tuple length
        self.b = parameters[1]  # Number of prime factors
        self.c = parameters[2]  # Difference between largest and smallest prime factor
        
        # Check if this is an unclued clue (b=0 and c=0 is our special case for unclued)
        # This avoids using -1 for c since c should never be negative
        self.is_undefined = (self.b == 0 and self.c == 0)
        
        if self.is_undefined:
            # For unclued clues, we'll start with all possible numbers of the given length
            # and narrow them down based on constraints
            start = 10**(self.length - 1)
            end = 10**self.length
            self.possible_solutions = list(range(start, end))
            self.original_solution_count = len(self.possible_solutions)
            self.valid_solutions = set(self.possible_solutions)
        else:
            # Generate all possible solutions for this clue
            self.possible_solutions = list(find_solutions(self.length, self.b, self.c))
            self.original_solution_count = len(self.possible_solutions)
            self.valid_solutions = set(self.possible_solutions)
        
        # Backtracking support
        self.rejected_solutions = set()  # Solutions that were eliminated and can be restored
        self.elimination_history = []  # [(solution, reason), ...] for debugging
        self.tried_solutions = set()  # Solutions that have been tried in backtracking
        
    def __repr__(self):
        if self.is_undefined:
            return f"Clue {self.clue_id} {self.direction}: {self.cell_indices} (UNCLUED - {len(self.valid_solutions)}/{self.original_solution_count} solutions)"
        else:
            return f"Clue {self.clue_id} {self.direction}: {self.cell_indices} ({self.b}:{self.c} - {len(self.valid_solutions)}/{self.original_solution_count} solutions)"
    
    @property
    def number(self) -> int:
        """Extract the numeric part from clue_id for backward compatibility"""
        return int(self.clue_id[1:])
    
    def eliminate_solution(self, solution: int, reason: str = "constraint") -> bool:
        """Remove a solution from the valid set. Returns True if solution was removed."""
        if solution in self.valid_solutions:
            self.valid_solutions.remove(solution)
            self.rejected_solutions.add(solution)
            self.elimination_history.append((solution, reason))
            return True
        return False
    
    def restore_solution(self, solution: int) -> bool:
        """Restore a previously eliminated solution. Returns True if solution was restored."""
        if solution in self.rejected_solutions:
            self.valid_solutions.add(solution)
            self.rejected_solutions.remove(solution)
            # Remove from elimination history (keep most recent entries)
            self.elimination_history = [(s, r) for s, r in self.elimination_history if s != solution]
            return True
        return False
    
    def get_valid_solutions(self) -> List[int]:
        """Get list of currently valid solutions."""
        return list(self.valid_solutions)
    
    def get_rejected_solutions(self) -> List[int]:
        """Get list of rejected solutions that can be restored."""
        return list(self.rejected_solutions)
    
    def is_solved(self) -> bool:
        """Check if this clue has only one valid solution."""
        return len(self.valid_solutions) == 1
    
    def get_solution(self) -> Optional[int]:
        """Get the solution if this clue is solved, otherwise None."""
        if self.is_solved():
            return list(self.valid_solutions)[0]
        return None
    
    def update_from_constraints(self, solved_cells: Dict[int, int]) -> bool:
        """Update valid solutions based on current grid state. Returns True if solutions were eliminated."""
        if not self.is_undefined:
            return False  # Only unclued clues need this
        
        solutions_to_remove = []
        
        for solution in self.valid_solutions:
            solution_str = str(solution).zfill(self.length)
            
            # Check if this solution is compatible with current grid state
            for i, cell_index in enumerate(self.cell_indices):
                if cell_index in solved_cells:
                    expected_digit = solved_cells[cell_index]
                    actual_digit = int(solution_str[i])
                    if expected_digit != actual_digit:
                        solutions_to_remove.append(solution)
                        break
        
        # Remove incompatible solutions
        for solution in solutions_to_remove:
            self.eliminate_solution(solution, "grid_constraint")
        
        return len(solutions_to_remove) > 0
    
    def create_snapshot(self) -> dict:
        """Create a snapshot of the current state for backtracking."""
        return {
            'valid_solutions': set(self.valid_solutions),
            'rejected_solutions': set(self.rejected_solutions),
            'elimination_history': list(self.elimination_history),
            'tried_solutions': set(self.tried_solutions)
        }
    
    def restore_snapshot(self, snapshot: dict) -> None:
        """Restore state from a snapshot."""
        self.valid_solutions = set(snapshot['valid_solutions'])
        self.rejected_solutions = set(snapshot['rejected_solutions'])
        self.elimination_history = list(snapshot['elimination_history'])
        self.tried_solutions = set(snapshot['tried_solutions'])
    
    def mark_solution_tried(self, solution: int) -> None:
        """Mark a solution as tried in backtracking."""
        self.tried_solutions.add(solution)
    
    def clear_tried_solutions(self) -> None:
        """Clear the tried solutions tracking."""
        self.tried_solutions.clear()
    
    def get_untried_solutions(self) -> List[int]:
        """Get solutions that haven't been tried yet."""
        return [s for s in self.valid_solutions if s not in self.tried_solutions]

class ListenerPuzzle:
    """Enhanced puzzle class for Listener puzzles with backtracking support"""
    
    def __init__(self):
        self.clues = {}  # clue_id -> ListenerClue
        self.solved_cells = {}  # cell_index -> digit
        self.solving_order = []  # List of clue_ids in order they were solved
        self.backtrack_stack = []  # Stack of puzzle states for backtracking
        
    def add_clue(self, clue: ListenerClue) -> None:
        """Add a clue to the puzzle."""
        self.clues[clue.clue_id] = clue
    
    def has_clue(self, clue_id: str) -> bool:
        """Check if puzzle has a clue with given ID."""
        return clue_id in self.clues
    
    def get_clue(self, clue_id: str) -> Optional[ListenerClue]:
        """Get a clue by ID."""
        return self.clues.get(clue_id)
    
    def get_clues_by_direction(self, direction: str) -> List[ListenerClue]:
        """Get all clues in a given direction."""
        return [clue for clue in self.clues.values() if clue.direction == direction]
    
    def get_clues_by_number(self, number: int) -> List[ListenerClue]:
        """Get all clues with a given number (both directions)."""
        return [clue for clue in self.clues.values() if clue.number == number]
    
    def get_solved_clues(self) -> List[ListenerClue]:
        """Get all solved clues."""
        return [clue for clue in self.clues.values() if clue.is_solved()]
    
    def get_unsolved_clues(self) -> List[ListenerClue]:
        """Get all unsolved clues."""
        return [clue for clue in self.clues.values() if not clue.is_solved()]
    
    def get_clue_with_one_solution(self) -> Optional[ListenerClue]:
        """Find a clue that has exactly one valid solution."""
        for clue in self.clues.values():
            if len(clue.valid_solutions) == 1:
                return clue
        return None
    
    def get_clue_with_fewest_solutions(self) -> Optional[ListenerClue]:
        """Find the clue with the fewest valid solutions (but more than 1)."""
        min_solutions = float('inf')
        best_clue = None
        
        for clue in self.clues.values():
            if len(clue.valid_solutions) > 1 and len(clue.valid_solutions) < min_solutions:
                min_solutions = len(clue.valid_solutions)
                best_clue = clue
        
        return best_clue
    
    def solve_clue(self, clue: ListenerClue) -> bool:
        """Solve a specific clue and propagate constraints."""
        if not clue.is_solved():
            return False
        
        solution = clue.get_solution()
        if solution is None:
            return False
        
        # Apply the solution to the grid
        solution_str = str(solution).zfill(clue.length)
        
        # Check for conflicts
        for i, cell_index in enumerate(clue.cell_indices):
            if cell_index in self.solved_cells:
                if self.solved_cells[cell_index] != int(solution_str[i]):
                    return False  # Conflict detected
        
        # Apply solution
        for i, cell_index in enumerate(clue.cell_indices):
            self.solved_cells[cell_index] = int(solution_str[i])
        
        # Record solving order
        self.solving_order.append(clue.clue_id)
        
        # Propagate constraints to other clues
        self.propagate_constraints(clue)
        
        return True
    
    def propagate_constraints(self, solved_clue: ListenerClue) -> None:
        """Propagate constraints from a solved clue to other clues."""
        solution = solved_clue.get_solution()
        if solution is None:
            return
        
        solution_str = str(solution).zfill(solved_clue.length)
        
        # Check all other clues that share cells with this clue
        for clue in self.clues.values():
            if clue.clue_id == solved_clue.clue_id:
                continue
            
            # Check if this clue shares any cells with the solved clue
            shared_cells = set(clue.cell_indices) & set(solved_clue.cell_indices)
            if not shared_cells:
                continue
            
            # Eliminate incompatible solutions from this clue
            solutions_to_remove = []
            for potential_solution in clue.valid_solutions:
                potential_str = str(potential_solution).zfill(clue.length)
                
                # Check if this potential solution is compatible with the solved clue
                for shared_cell in shared_cells:
                    # Find the position of this cell in both clues
                    solved_pos = solved_clue.cell_indices.index(shared_cell)
                    clue_pos = clue.cell_indices.index(shared_cell)
                    
                    # Check if the digits match
                    if int(solution_str[solved_pos]) != int(potential_str[clue_pos]):
                        solutions_to_remove.append(potential_solution)
                        break
            
            # Remove incompatible solutions
            for solution_to_remove in solutions_to_remove:
                clue.eliminate_solution(solution_to_remove, f"constraint_from_{solved_clue.clue_id}")
    
    def update_unclued_clues(self) -> bool:
        """Update unclued clues based on current grid state. Returns True if any were updated."""
        updated = False
        
        for clue in self.clues.values():
            if clue.is_undefined:
                if clue.update_from_constraints(self.solved_cells):
                    updated = True
        
        return updated
    
    def solve(self, max_backtrack_depth: int = 10) -> bool:
        """Solve the puzzle using constraint propagation and backtracking."""
        print("Starting puzzle solution...")
        
        # Initial constraint propagation
        self.update_unclued_clues()
        
        # Main solving loop
        while not self.is_puzzle_solved():
            # Try to solve clues with one solution
            clue_to_solve = self.get_clue_with_one_solution()
            
            if clue_to_solve:
                print(f"Solving clue {clue_to_solve.clue_id} with single solution")
                if not self.solve_clue(clue_to_solve):
                    print(f"Failed to solve clue {clue_to_solve.clue_id}")
                    return False
                
                # Update unclued clues after each solve
                self.update_unclued_clues()
                continue
            
            # If no single-solution clues, try backtracking
            print("No single-solution clues found, attempting backtracking...")
            if not self.backtrack_solve(max_backtrack_depth):
                print("Backtracking failed to find solution")
                return False
        
        print("Puzzle solved successfully!")
        return True
    
    def backtrack_solve(self, max_depth: int) -> bool:
        """Solve using backtracking when constraint propagation stalls."""
        return self._backtrack_recursive(0, max_depth)
    
    def _backtrack_recursive(self, depth: int, max_depth: int) -> bool:
        """Recursive backtracking implementation."""
        if depth >= max_depth:
            return False
        
        # Save current state
        self.save_state()
        
        # Find clue with fewest solutions to try
        clue_to_try = self.get_clue_with_fewest_solutions()
        if not clue_to_try:
            return False
        
        print(f"Backtracking: trying clue {clue_to_try.clue_id} at depth {depth}")
        
        # Try each solution for this clue
        for solution in clue_to_try.get_untried_solutions():
            # Mark this solution as tried
            clue_to_try.mark_solution_tried(solution)
            
            # Temporarily set this solution
            original_solutions = set(clue_to_try.valid_solutions)
            clue_to_try.valid_solutions = {solution}
            
            # Try to solve with this assumption
            try:
                # Propagate constraints
                self.propagate_constraints(clue_to_try)
                self.update_unclued_clues()
                
                # Try to solve the rest
                if self.solve_with_backtracking(depth + 1, max_depth):
                    return True
                
            except Exception as e:
                print(f"Error during backtracking: {e}")
            
            finally:
                # Restore original state
                self.restore_state()
                clue_to_try.valid_solutions = original_solutions
        
        return False
    
    def solve_with_backtracking(self, depth: int, max_depth: int) -> bool:
        """Helper method for backtracking that combines constraint propagation and recursion."""
        while not self.is_puzzle_solved():
            # Try constraint propagation first
            clue_to_solve = self.get_clue_with_one_solution()
            
            if clue_to_solve:
                if not self.solve_clue(clue_to_solve):
                    return False
                self.update_unclued_clues()
                continue
            
            # If stuck, recurse
            return self._backtrack_recursive(depth, max_depth)
        
        return True
    
    def save_state(self) -> None:
        """Save current puzzle state for backtracking."""
        state = {
            'solved_cells': dict(self.solved_cells),
            'solving_order': list(self.solving_order),
            'clue_states': {clue_id: clue.create_snapshot() for clue_id, clue in self.clues.items()}
        }
        self.backtrack_stack.append(state)
    
    def restore_state(self) -> None:
        """Restore puzzle state from backtracking stack."""
        if not self.backtrack_stack:
            return
        
        state = self.backtrack_stack.pop()
        self.solved_cells = state['solved_cells']
        self.solving_order = state['solving_order']
        
        for clue_id, clue_state in state['clue_states'].items():
            if clue_id in self.clues:
                self.clues[clue_id].restore_snapshot(clue_state)
    
    def is_puzzle_solved(self) -> bool:
        """Check if the puzzle is completely solved."""
        return all(clue.is_solved() for clue in self.clues.values())
    
    def get_completion_percentage(self) -> float:
        """Get the percentage of clues that are solved."""
        if not self.clues:
            return 0.0
        
        solved_count = len(self.get_solved_clues())
        total_count = len(self.clues)
        return (solved_count / total_count) * 100
    
    def print_puzzle_state(self) -> None:
        """Print the current state of the puzzle."""
        print(f"Puzzle State:")
        print(f"  Total clues: {len(self.clues)}")
        print(f"  Solved clues: {len(self.get_solved_clues())}")
        print(f"  Solved cells: {len(self.solved_cells)}")
        print(f"  Completion: {self.get_completion_percentage():.1f}%")
        
        print("\nClue Status:")
        for clue_id in sorted(self.clues.keys()):
            clue = self.clues[clue_id]
            if clue.is_solved():
                solution = clue.get_solution()
                print(f"  {clue_id}: SOLVED = {solution}")
            else:
                print(f"  {clue_id}: {len(clue.valid_solutions)} solutions")
    
    def print_solution(self) -> None:
        """Print the complete solution grid."""
        print("Solution Grid:")
        print("=" * 50)
        
        # Create 8x8 grid
        grid = [[' ' for _ in range(8)] for _ in range(8)]
        
        # Fill in solved cells
        for cell_index, digit in self.solved_cells.items():
            row = cell_index // 8
            col = cell_index % 8
            grid[row][col] = str(digit)
        
        # Print grid
        for row in range(8):
            print("  " + " ".join(grid[row]))
        
        print("\nSolved Clues:")
        for clue_id in self.solving_order:
            clue = self.clues[clue_id]
            solution = clue.get_solution()
            print(f"  {clue_id}: {solution}")
        
        print(f"\nCompletion: {self.get_completion_percentage():.1f}%")

class CrosswordGrid:
    def __init__(self, size: int = 8):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.clues: Dict[str, List[Clue]] = {
            'ACROSS': [],
            'DOWN': []
        }
        self.clue_cells: Dict[int, Set[int]] = {}  # Maps clue number to set of cell indices

    def add_clue(self, clue: Clue) -> None:
        """Add a clue to the grid."""
        self.clues[clue.direction].append(clue)
        # Generate possible solutions for this clue
        clue.possible_solutions = list(find_solutions(*clue.parameters))
        
        # Store cell indices for this clue
        if clue.cell_indices:
            self.clue_cells[clue.number] = set(clue.cell_indices)

    def get_cell_value(self, row: int, col: int) -> int:
        """Get the value at a specific cell."""
        return self.grid[row][col]

    def set_cell_value(self, row: int, col: int, value: int) -> None:
        """Set the value at a specific cell."""
        self.grid[row][col] = value

    def get_cell_index(self, row: int, col: int) -> int:
        """Convert row, col to cell index (1-64)."""
        return row * self.size + col + 1

    def get_row_col(self, cell_index: int) -> Tuple[int, int]:
        """Convert cell index (1-64) to row, col."""
        cell_index -= 1  # Convert to 0-based
        return cell_index // self.size, cell_index % self.size

    def is_valid_placement(self, clue: Clue, solution: int) -> bool:
        """Check if a solution can be placed for the given clue."""
        solution_str = str(solution)
        
        if clue.direction == 'ACROSS':
            row, col = clue.position
            # Check if the solution fits in the grid
            if col + len(solution_str) > self.size:
                return False
            
            # Check if the solution conflicts with existing numbers
            for i, digit in enumerate(solution_str):
                current = self.grid[row][col + i]
                if current != 0 and current != int(digit):
                    return False
        else:  # DOWN
            row, col = clue.position
            # Check if the solution fits in the grid
            if row + len(solution_str) > self.size:
                return False
            
            # Check if the solution conflicts with existing numbers
            for i, digit in enumerate(solution_str):
                current = self.grid[row + i][col]
                if current != 0 and current != int(digit):
                    return False
        
        return True

    def place_solution(self, clue: Clue, solution: int) -> None:
        """Place a solution in the grid."""
        solution_str = str(solution)
        
        if clue.direction == 'ACROSS':
            row, col = clue.position
            for i, digit in enumerate(solution_str):
                self.grid[row][col + i] = int(digit)
        else:  # DOWN
            row, col = clue.position
            for i, digit in enumerate(solution_str):
                self.grid[row + i][col] = int(digit)

    def remove_solution(self, clue: Clue) -> None:
        """Remove a solution from the grid."""
        if clue.direction == 'ACROSS':
            row, col = clue.position
            for i in range(clue.length):
                self.grid[row][col + i] = 0
        else:  # DOWN
            row, col = clue.position
            for i in range(clue.length):
                self.grid[row + i][col] = 0

    def get_conflicting_clues(self, clue: Clue) -> List[Clue]:
        """Get all clues that share cells with the given clue."""
        if not clue.cell_indices:
            return []
        
        conflicting = []
        clue_cells = set(clue.cell_indices)
        
        for direction in ['ACROSS', 'DOWN']:
            for other_clue in self.clues[direction]:
                if other_clue.number != clue.number and other_clue.cell_indices:
                    other_cells = set(other_clue.cell_indices)
                    if clue_cells.intersection(other_cells):
                        conflicting.append(other_clue)
        
        return conflicting

    def solve(self) -> bool:
        """Solve the crossword puzzle using backtracking."""
        # Sort clues by number of possible solutions (least first)
        all_clues = self.clues['ACROSS'] + self.clues['DOWN']
        all_clues.sort(key=lambda x: len(x.possible_solutions))

        return self._solve_recursive(all_clues, 0)

    def _solve_recursive(self, clues: List[Clue], index: int) -> bool:
        """Recursive helper function for solving."""
        if index == len(clues):
            return True

        clue = clues[index]

        for solution in clue.possible_solutions:
            if self.is_valid_placement(clue, solution):
                # Try placing the solution
                self.place_solution(clue, solution)
                
                if self._solve_recursive(clues, index + 1):
                    return True
                
                # Backtrack
                self.remove_solution(clue)

        return False

    def print_grid(self) -> None:
        """Print the current state of the grid."""
        print("\nSolution Grid:")
        print("=" * 30)
        for row in self.grid:
            print(' '.join(str(x) for x in row))

    def print_grid_with_indices(self) -> None:
        """Print the grid showing cell indices and values."""
        print("\nGrid with Cell Indices and Values:")
        print("=" * 40)
        
        # Print column numbers
        print("   ", end="")
        for col in range(self.size):
            print(f"{col:3} ", end="")
        print("\n")
        
        for row in range(self.size):
            print(f"{row:2} ", end="")
            for col in range(self.size):
                cell_index = self.get_cell_index(row, col)
                value = self.grid[row][col]
                if value != 0:
                    print(f"{value:2} ", end="")
                else:
                    print(f"{cell_index:2} ", end="")
            print()

def main():
    # Create the grid
    grid = CrosswordGrid(8)
    
    # Example of how to add clues (you'll need to fill in the actual parameters)
    # Across clues
    grid.add_clue(Clue(
        number=1,                    # Clue number
        direction='ACROSS',          # Direction
        length=4,                    # Number of digits
        position=(0, 0),            # Starting position (row, col)
        parameters=(4, 3, 2),       # (a, b, c) for find_solutions
        cell_indices=(1, 2, 3, 4)   # Cell indices this clue occupies
    ))
    
    # Down clues
    grid.add_clue(Clue(
        number=2,
        direction='DOWN',
        length=5,
        position=(0, 0),
        parameters=(5, 4, 3),
        cell_indices=(1, 9, 17, 25, 33)
    ))
    
    # Solve the puzzle
    if grid.solve():
        print("Solution found!")
        grid.print_grid()
        grid.print_grid_with_indices()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main() 