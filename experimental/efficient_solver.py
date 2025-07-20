#!/usr/bin/env python3
"""
Efficient solver that handles unclued clues differently and leverages grid symmetry
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Tuple, List, Optional, Set

from utils import parse_grid
from utils import ListenerPuzzle, ListenerClue

def load_clue_parameters(filename: str) -> Dict[Tuple[int, str], Tuple[int, int, int]]:
    """Load clue parameters from file."""
    parameters = {}
    
    with open(filename, 'r') as f:
        current_direction = None
        for line in f:
            line = line.strip()
            if line == "Across":
                current_direction = "ACROSS"
            elif line == "Down":
                current_direction = "DOWN"
            elif line and current_direction:
                parts = line.split()
                if len(parts) >= 2:
                    number = int(parts[0])
                    if parts[1] == "Unclued":
                        parameters[(number, current_direction)] = (0, 0, 0)
                    else:
                        b_c = parts[1].split(':')
                        if len(b_c) == 2:
                            b = int(b_c[0])
                            c = int(b_c[1])
                            parameters[(number, current_direction)] = (0, b, c)
    
    return parameters

def create_clue_id(number: int, direction: str) -> str:
    """Create unique clue ID like 'A1', 'D1'"""
    prefix = "A" if direction == "ACROSS" else "D"
    return f"{prefix}{number}"

class EfficientListenerClue(ListenerClue):
    """Efficient clue class that handles unclued clues differently"""
    
    def __init__(self, clue_id: str, direction: str, cell_indices: Tuple[int, ...], 
                 parameters: Tuple[int, int, int]):
        self.clue_id = clue_id
        self.direction = direction
        self.cell_indices = cell_indices
        self.length = len(cell_indices)
        self.b = parameters[1]
        self.c = parameters[2]
        
        # Check if this is an unclued clue
        self.is_undefined = (self.b == 0 and self.c == 0)
        
        if self.is_undefined:
            # For unclued clues, don't store all possible solutions
            # Just track that it's unclued and will be constrained by crossing clues
            self.valid_solutions = set()  # Empty set - will be populated as constraints are applied
            self.original_solution_count = float('inf')  # Infinite possibilities
            self.is_constrained = False  # Track if constraints have been applied
        else:
            # Generate solutions for clued clues as normal
            from listener import find_solutions
            self.valid_solutions = set(find_solutions(self.length, self.b, self.c))
            self.original_solution_count = len(self.valid_solutions)
            self.is_constrained = True
        
        # Backtracking support
        self.rejected_solutions = set()
        self.elimination_history = []
        self.tried_solutions = set()
    
    def update_from_constraints(self, solved_cells: Dict[int, int]) -> bool:
        """Update unclued clues based on current grid state."""
        if not self.is_undefined:
            return False
        
        # For unclued clues, generate valid solutions based on current constraints
        if not self.is_constrained:
            # First time applying constraints - generate all possible numbers of correct length
            start = 10**(self.length - 1)
            end = 10**self.length
            self.valid_solutions = set(range(start, end))
            self.is_constrained = True
        
        # Filter solutions based on current grid state
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

def analyze_grid_symmetry():
    """Analyze the grid symmetry pattern."""
    print("=== GRID SYMMETRY ANALYSIS ===")
    
    # Define the 8x8 grid with cell indices 0-63
    grid = [[i + j*8 for j in range(8)] for i in range(8)]
    
    print("Grid layout (cell indices):")
    for row in grid:
        print(f"  {row}")
    
    # Identify constraint cells in each quadrant
    # Based on your observation about thick borders and symmetry
    
    # Top-left quadrant (cells 0-7, 8-15, 16-23, 24-31)
    top_left_constraints = {0, 2, 16, 18}
    
    # Top-right quadrant (cells 32-39, 40-47, 48-55, 56-63)
    # Rotated 90 degrees from top-left
    top_right_constraints = {5, 7, 21, 25}
    
    # Bottom-left quadrant (cells 32-39, 40-47, 48-55, 56-63)
    # Rotated 180 degrees from top-left
    bottom_left_constraints = {45, 47, 61, 63}
    
    # Bottom-right quadrant (cells 32-39, 40-47, 48-55, 56-63)
    # Rotated 270 degrees from top-left
    bottom_right_constraints = {40, 42, 56, 58}
    
    print(f"\nConstraint cells by quadrant:")
    print(f"  Top-left: {sorted(top_left_constraints)}")
    print(f"  Top-right: {sorted(top_right_constraints)}")
    print(f"  Bottom-left: {sorted(bottom_left_constraints)}")
    print(f"  Bottom-right: {sorted(bottom_right_constraints)}")
    
    return {
        'top_left': top_left_constraints,
        'top_right': top_right_constraints,
        'bottom_left': bottom_left_constraints,
        'bottom_right': bottom_right_constraints
    }

def create_efficient_puzzle():
    """Create puzzle with efficient clue handling."""
    # Parse grid and load parameters
    grid_clues = parse_grid()
    clue_params = load_clue_parameters("data/Listener 4869 clues.txt")
    
    # Create puzzle
    puzzle = ListenerPuzzle()
    
    for number, direction, cell_indices in grid_clues:
        clue_id = create_clue_id(number, direction)
        param_key = (number, direction)
        
        if param_key in clue_params:
            a, b, c = clue_params[param_key]
            a = len(cell_indices)
            parameters = (a, b, c)
        else:
            a = len(cell_indices)
            parameters = (a, 0, 0)
        
        # Use efficient clue class
        clue = EfficientListenerClue(clue_id, direction, cell_indices, parameters)
        puzzle.add_clue(clue)
    
    return puzzle

def solve_with_symmetry(puzzle: ListenerPuzzle):
    """Solve using symmetry insights."""
    print("\n=== SOLVING WITH SYMMETRY INSIGHTS ===")
    
    # Analyze symmetry
    symmetry = analyze_grid_symmetry()
    
    # Apply solved clues first
    print("\n--- Phase 1: Apply solved clues ---")
    applied_count = 0
    for clue in puzzle.clues.values():
        if clue.is_solved():
            solution = clue.get_solution()
            print(f"Applying {clue.clue_id}: {solution}")
            
            if puzzle.solve_clue(clue):
                applied_count += 1
                print(f"  Successfully applied {clue.clue_id}")
            else:
                print(f"  FAILED to apply {clue.clue_id}")
    
    print(f"Applied {applied_count} solved clues")
    
    # Show grid after applying solved clues
    print(f"\nGrid after applying solved clues:")
    puzzle.print_solution()
    
    # Focus on clues with fewest solutions
    print(f"\n--- Phase 2: Solve clues with fewest solutions ---")
    
    # Get clues sorted by solution count (excluding unclued)
    clued_clues = [c for c in puzzle.clues.values() if not c.is_undefined and not c.is_solved()]
    clued_clues.sort(key=lambda c: len(c.valid_solutions))
    
    print(f"Clued clues sorted by solution count:")
    for clue in clued_clues[:10]:  # Show top 10
        print(f"  {clue.clue_id}: {len(clue.valid_solutions)} solutions")
    
    # Try to solve clues with 2-3 solutions first
    for clue in clued_clues:
        if len(clue.valid_solutions) <= 3:
            print(f"\nTrying to solve {clue.clue_id} with {len(clue.valid_solutions)} solutions")
            
            if len(clue.valid_solutions) == 1:
                # Single solution - apply it
                solution = clue.get_solution()
                if puzzle.solve_clue(clue):
                    print(f"  Successfully applied {clue.clue_id} = {solution}")
                    puzzle.update_unclued_clues()
                else:
                    print(f"  FAILED to apply {clue.clue_id}")
            else:
                # Multiple solutions - show them
                solutions = clue.get_valid_solutions()
                print(f"  Solutions: {solutions}")
                print(f"  Need to choose one - skipping for now")

def main():
    """Main efficient solving function."""
    print("=== EFFICIENT SOLVER WITH SYMMETRY ===")
    
    # Create efficient puzzle
    puzzle = create_efficient_puzzle()
    print(f"Created puzzle with {len(puzzle.clues)} clues")
    
    # Show initial state
    print("\nInitial clue status:")
    solved_clues = []
    unsolved_clues = []
    unclued_clues = []
    
    for clue_id in sorted(puzzle.clues.keys()):
        clue = puzzle.clues[clue_id]
        if clue.is_solved():
            solved_clues.append(clue)
            print(f"  {clue_id}: SOLVED = {clue.get_solution()}")
        elif clue.is_undefined:
            unclued_clues.append(clue)
            print(f"  {clue_id}: UNCLUED (efficient handling)")
        else:
            unsolved_clues.append(clue)
            print(f"  {clue_id}: {len(clue.valid_solutions)} solutions")
    
    print(f"\nInitial state: {len(solved_clues)} solved, {len(unsolved_clues)} unsolved, {len(unclued_clues)} unclued")
    
    # Solve with symmetry insights
    solve_with_symmetry(puzzle)
    
    # Final state
    print(f"\n=== FINAL STATE ===")
    print(f"Solved clues: {len(puzzle.get_solved_clues())}/{len(puzzle.clues)}")
    print(f"Solved cells: {len(puzzle.solved_cells)}")
    print(f"Completion: {puzzle.get_completion_percentage():.1f}%")
    
    # Show remaining unsolved clues
    unsolved = puzzle.get_unsolved_clues()
    if unsolved:
        print(f"\nRemaining unsolved clues:")
        for clue in sorted(unsolved, key=lambda c: len(c.valid_solutions) if not c.is_undefined else float('inf')):
            if clue.is_undefined:
                print(f"  {clue.clue_id}: UNCLUED")
            else:
                print(f"  {clue.clue_id}: {len(clue.valid_solutions)} solutions")
    
    # Show final grid
    puzzle.print_solution()

if __name__ == "__main__":
    main() 