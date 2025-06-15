from typing import Dict, List, Set, Tuple
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

class CrosswordGrid:
    def __init__(self, size: int = 8):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.clues: Dict[str, List[Clue]] = {
            'ACROSS': [],
            'DOWN': []
        }
        self.undefined_positions: Set[Tuple[int, int]] = set()

    def add_clue(self, clue: Clue) -> None:
        """Add a clue to the grid."""
        self.clues[clue.direction].append(clue)
        # Generate possible solutions for this clue
        clue.possible_solutions = list(find_solutions(*clue.parameters))

    def add_undefined_position(self, row: int, col: int) -> None:
        """Mark a position as undefined (no clue)."""
        self.undefined_positions.add((row, col))

    def get_cell_value(self, row: int, col: int) -> int:
        """Get the value at a specific cell."""
        return self.grid[row][col]

    def set_cell_value(self, row: int, col: int, value: int) -> None:
        """Set the value at a specific cell."""
        self.grid[row][col] = value

    def is_valid_placement(self, row: int, col: int, value: int) -> bool:
        """Check if a value can be placed at the given position."""
        # Convert value to string for digit-by-digit checking
        value_str = str(value)
        
        # Check if the value fits in the grid
        if col + len(value_str) > self.size:
            return False

        # Check if the value conflicts with existing numbers
        for i, digit in enumerate(value_str):
            current = self.grid[row][col + i]
            if current != 0 and current != int(digit):
                return False

        return True

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
        row, col = clue.position

        for solution in clue.possible_solutions:
            if self.is_valid_placement(row, col, solution):
                # Try placing the solution
                self._place_solution(clue, solution)
                
                if self._solve_recursive(clues, index + 1):
                    return True
                
                # Backtrack
                self._remove_solution(clue)

        return False

    def _place_solution(self, clue: Clue, solution: int) -> None:
        """Place a solution in the grid."""
        row, col = clue.position
        solution_str = str(solution)
        
        if clue.direction == 'ACROSS':
            for i, digit in enumerate(solution_str):
                self.grid[row][col + i] = int(digit)
        else:  # DOWN
            for i, digit in enumerate(solution_str):
                self.grid[row + i][col] = int(digit)

    def _remove_solution(self, clue: Clue) -> None:
        """Remove a solution from the grid."""
        row, col = clue.position
        length = clue.length
        
        if clue.direction == 'ACROSS':
            for i in range(length):
                self.grid[row][col + i] = 0
        else:  # DOWN
            for i in range(length):
                self.grid[row + i][col] = 0

    def print_grid(self) -> None:
        """Print the current state of the grid."""
        for row in self.grid:
            print(' '.join(str(x) for x in row))

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
        parameters=(4, 3, 2)        # (a, b, c) for find_solutions
    ))
    grid.add_clue(Clue(4, 'ACROSS', 5, (1, 0), (5, 4, 3)))
    # ... Add all other clues ...

    # Add undefined positions
    grid.add_undefined_position(3, 3)
    grid.add_undefined_position(3, 4)
    grid.add_undefined_position(4, 3)
    grid.add_undefined_position(4, 4)

    # Solve the puzzle
    if grid.solve():
        print("Solution found!")
        grid.print_grid()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main() 