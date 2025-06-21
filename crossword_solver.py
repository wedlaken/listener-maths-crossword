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
    """Enhanced clue class for Listener puzzles with tuple-based identification"""
    
    def __init__(self, number: int, direction: str, cell_indices: Tuple[int, ...], 
                 parameters: Tuple[int, int, int]):
        self.number = number
        self.direction = direction
        self.cell_indices = cell_indices
        self.length = len(cell_indices)  # 'a' parameter from tuple length
        self.b = parameters[1]  # Number of prime factors
        self.c = parameters[2]  # Difference between largest and smallest prime factors
        
        # Check if this is an undefined clue (b or c is -1)
        self.is_undefined = (self.b == -1 or self.c == -1)
        
        if self.is_undefined:
            # For undefined clues, we'll start with all possible numbers of the given length
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
        
    def __repr__(self):
        if self.is_undefined:
            return f"Clue {self.number} {self.direction}: {self.cell_indices} (UNDEFINED - {len(self.valid_solutions)}/{self.original_solution_count} solutions)"
        else:
            return f"Clue {self.number} {self.direction}: {self.cell_indices} ({len(self.valid_solutions)}/{self.original_solution_count} solutions)"
    
    def eliminate_solution(self, solution: int) -> bool:
        """Remove a solution from the valid set. Returns True if solution was removed."""
        if solution in self.valid_solutions:
            self.valid_solutions.remove(solution)
            return True
        return False
    
    def get_valid_solutions(self) -> List[int]:
        """Get list of currently valid solutions."""
        return list(self.valid_solutions)
    
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
            return False  # Only undefined clues need this
        
        solutions_to_remove = []
        
        for solution in self.valid_solutions:
            solution_str = str(solution)
            
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
            self.eliminate_solution(solution)
        
        return len(solutions_to_remove) > 0

class ListenerPuzzle:
    """Main puzzle class that manages all clues and their interactions"""
    
    def __init__(self):
        self.clues: Dict[int, ListenerClue] = {}  # clue_number -> ListenerClue
        self.cell_to_clues: Dict[int, List[int]] = {}  # cell_index -> [clue_numbers]
        self.solved_cells: Dict[int, int] = {}  # cell_index -> digit_value
        self.solution_history: List[Tuple[int, int]] = []  # [(clue_number, solution), ...]
        
    def add_clue(self, clue: ListenerClue) -> None:
        """Add a clue to the puzzle."""
        self.clues[clue.number] = clue
        
        # Update cell-to-clues mapping
        for cell_index in clue.cell_indices:
            if cell_index not in self.cell_to_clues:
                self.cell_to_clues[cell_index] = []
            self.cell_to_clues[cell_index].append(clue.number)
    
    def get_clue(self, clue_number: int) -> Optional[ListenerClue]:
        """Get a clue by its number."""
        return self.clues.get(clue_number)
    
    def get_clues_for_cell(self, cell_index: int) -> List[ListenerClue]:
        """Get all clues that use a specific cell."""
        clue_numbers = self.cell_to_clues.get(cell_index, [])
        return [self.clues[num] for num in clue_numbers]
    
    def get_overlapping_clues(self, clue_number: int) -> List[ListenerClue]:
        """Get all clues that overlap with the given clue."""
        clue = self.clues[clue_number]
        overlapping = set()
        
        for cell_index in clue.cell_indices:
            for other_clue_num in self.cell_to_clues.get(cell_index, []):
                if other_clue_num != clue_number:
                    overlapping.add(other_clue_num)
        
        return [self.clues[num] for num in overlapping]
    
    def apply_constraint(self, clue_number: int, solution: int) -> List[Tuple[int, int]]:
        """Apply a solution to a clue and propagate constraints to overlapping clues.
        Returns list of eliminated solutions: [(clue_number, eliminated_solution), ...]"""
        
        clue = self.clues[clue_number]
        eliminated = []
        
        # Convert solution to digits
        solution_str = str(solution)
        
        # Apply this solution to the grid
        for i, cell_index in enumerate(clue.cell_indices):
            digit = int(solution_str[i])
            self.solved_cells[cell_index] = digit
        
        # Check overlapping clues and eliminate incompatible solutions
        for overlapping_clue in self.get_overlapping_clues(clue_number):
            eliminated_from_clue = self._eliminate_incompatible_solutions(overlapping_clue)
            eliminated.extend(eliminated_from_clue)
        
        # Update undefined clues based on new grid state
        for undefined_clue in self._get_undefined_clues():
            if undefined_clue.update_from_constraints(self.solved_cells):
                eliminated.append((undefined_clue.number, -1))  # -1 indicates constraint update
        
        # Record this solution
        self.solution_history.append((clue_number, solution))
        
        return eliminated
    
    def _get_undefined_clues(self) -> List[ListenerClue]:
        """Get all undefined clues."""
        return [clue for clue in self.clues.values() if clue.is_undefined]
    
    def _eliminate_incompatible_solutions(self, clue: ListenerClue) -> List[Tuple[int, int]]:
        """Eliminate solutions from a clue that are incompatible with current grid state.
        Returns list of eliminated solutions: [(clue_number, eliminated_solution), ...]"""
        
        eliminated = []
        solutions_to_remove = []
        
        for solution in clue.valid_solutions:
            if not self._is_solution_compatible(clue, solution):
                solutions_to_remove.append(solution)
        
        for solution in solutions_to_remove:
            if clue.eliminate_solution(solution):
                eliminated.append((clue.number, solution))
        
        return eliminated
    
    def _is_solution_compatible(self, clue: ListenerClue, solution: int) -> bool:
        """Check if a solution is compatible with the current grid state."""
        solution_str = str(solution)
        
        for i, cell_index in enumerate(clue.cell_indices):
            if cell_index in self.solved_cells:
                expected_digit = self.solved_cells[cell_index]
                actual_digit = int(solution_str[i])
                if expected_digit != actual_digit:
                    return False
        
        return True
    
    def solve(self) -> bool:
        """Solve the puzzle using constraint propagation."""
        print("Starting puzzle solution...")
        print(f"Initial state: {len(self.clues)} clues")
        
        # Count undefined clues
        undefined_count = len(self._get_undefined_clues())
        print(f"Defined clues: {len(self.clues) - undefined_count}")
        print(f"Undefined clues: {undefined_count}")
        
        # Print initial state
        self.print_puzzle_state()
        
        # Main solving loop
        iteration = 0
        max_iterations = 50  # Prevent infinite loops
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Find clues with only one valid solution
            solved_clues = [clue for clue in self.clues.values() if clue.is_solved()]
            
            if not solved_clues:
                print("No more clues can be solved automatically.")
                break
            
            # Apply solutions for solved clues
            for clue in solved_clues:
                solution = clue.get_solution()
                if clue.is_undefined:
                    print(f"Solving undefined Clue {clue.number} {clue.direction}: {solution}")
                else:
                    print(f"Applying solution for Clue {clue.number} {clue.direction}: {solution}")
                
                eliminated = self.apply_constraint(clue.number, solution)
                if eliminated:
                    print(f"  Eliminated {len(eliminated)} incompatible solutions")
                
                self.print_puzzle_state()
        
        # Check if puzzle is complete
        total_cells = len(self.cell_to_clues)
        solved_cells = len(self.solved_cells)
        
        print(f"\nPuzzle solution complete: {solved_cells}/{total_cells} cells solved")
        
        return solved_cells == total_cells
    
    def print_puzzle_state(self) -> None:
        """Print the current state of the puzzle."""
        print("\n" + "="*60)
        print("PUZZLE STATE")
        print("="*60)
        
        # Print clue status
        for clue_num in sorted(self.clues.keys()):
            clue = self.clues[clue_num]
            status = "SOLVED" if clue.is_solved() else f"{len(clue.valid_solutions)} solutions"
            print(f"Clue {clue_num} {clue.direction}: {clue.cell_indices} - {status}")
        
        # Print grid state
        print("\nGrid State:")
        print("-" * 30)
        for row in range(8):
            for col in range(8):
                cell_index = row * 8 + col + 1
                if cell_index in self.solved_cells:
                    print(f"{self.solved_cells[cell_index]}", end=" ")
                else:
                    print(".", end=" ")
            print()
        print("="*60)
    
    def print_solution(self) -> None:
        """Print the final solution."""
        print("\nFINAL SOLUTION:")
        print("="*30)
        
        for row in range(8):
            for col in range(8):
                cell_index = row * 8 + col + 1
                if cell_index in self.solved_cells:
                    print(f"{self.solved_cells[cell_index]}", end=" ")
                else:
                    print("?", end=" ")
            print()
        
        print("\nSolution History:")
        for clue_num, solution in self.solution_history:
            print(f"Clue {clue_num}: {solution}")

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