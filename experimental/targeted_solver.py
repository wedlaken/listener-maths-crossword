#!/usr/bin/env python3
"""
Targeted solver that applies solved clues first, then works with fewest solutions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Tuple, List, Optional

from systematic_grid_parser import parse_grid
from crossword_solver import ListenerPuzzle, ListenerClue

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

def create_puzzle() -> ListenerPuzzle:
    """Create puzzle with all clues."""
    # Parse grid and load parameters
    grid_clues = parse_grid()
    clue_params = load_clue_parameters("Listener 4869 clues.txt")
    
    # Create puzzle
    puzzle = ListenerPuzzle()
    
    for number, direction, cell_indices in grid_clues:
        clue_id = create_clue_id(number, direction)
        param_key = (number, direction)
        
        if param_key in clue_params:
            a, b, c = clue_params[param_key]
            a = len(cell_indices)  # Update from actual length
            parameters = (a, b, c)
        else:
            a = len(cell_indices)
            parameters = (a, 0, 0)
        
        clue = ListenerClue(clue_id, direction, cell_indices, parameters)
        puzzle.add_clue(clue)
    
    return puzzle

def apply_solved_clues(puzzle: ListenerPuzzle) -> int:
    """Apply all already-solved clues to the grid. Returns number applied."""
    print("=== APPLYING SOLVED CLUES ===")
    
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
    return applied_count

def solve_by_fewest_solutions(puzzle: ListenerPuzzle, max_iterations: int = 10) -> None:
    """Solve by repeatedly finding clues with fewest solutions."""
    print(f"\n=== SOLVING BY FEWEST SOLUTIONS ===")
    
    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        
        # Find clue with fewest solutions
        best_clue = None
        min_solutions = float('inf')
        
        for clue in puzzle.clues.values():
            if not clue.is_solved() and len(clue.valid_solutions) < min_solutions:
                min_solutions = len(clue.valid_solutions)
                best_clue = clue
        
        if not best_clue:
            print("No unsolved clues found!")
            break
        
        print(f"Best clue: {best_clue.clue_id} with {min_solutions} solutions")
        
        if min_solutions == 1:
            # Single solution - apply it
            solution = best_clue.get_solution()
            print(f"  Applying single solution: {solution}")
            
            if puzzle.solve_clue(best_clue):
                print(f"  Successfully applied {best_clue.clue_id}")
                # Update unclued clues
                puzzle.update_unclued_clues()
            else:
                print(f"  FAILED to apply {best_clue.clue_id}")
                break
        elif min_solutions <= 5:
            # Show solutions for small sets
            solutions = best_clue.get_valid_solutions()
            print(f"  Solutions: {solutions}")
            print(f"  Need to choose one - skipping for now")
            break
        else:
            print(f"  Too many solutions ({min_solutions}) - stopping")
            break
        
        # Show progress
        solved_count = len(puzzle.get_solved_clues())
        print(f"  Progress: {solved_count}/{len(puzzle.clues)} clues solved")

def analyze_clue_intersections(puzzle: ListenerPuzzle) -> None:
    """Analyze which clues intersect and could help each other."""
    print(f"\n=== ANALYZING CLUE INTERSECTIONS ===")
    
    # Find clues with fewest solutions
    few_solutions = []
    for clue in puzzle.clues.values():
        if not clue.is_solved() and len(clue.valid_solutions) <= 5:
            few_solutions.append(clue)
    
    few_solutions.sort(key=lambda c: len(c.valid_solutions))
    
    print(f"Clues with 5 or fewer solutions:")
    for clue in few_solutions:
        print(f"  {clue.clue_id}: {len(clue.valid_solutions)} solutions")
    
    # Find intersections between these clues
    print(f"\nIntersections between low-solution clues:")
    for i, clue1 in enumerate(few_solutions):
        for clue2 in few_solutions[i+1:]:
            shared_cells = set(clue1.cell_indices) & set(clue2.cell_indices)
            if shared_cells:
                print(f"  {clue1.clue_id} ∩ {clue2.clue_id}: {len(shared_cells)} shared cells at {shared_cells}")

def main():
    """Main targeted solving function."""
    print("=== TARGETED SOLVER ===")
    
    # Create puzzle
    puzzle = create_puzzle()
    print(f"Created puzzle with {len(puzzle.clues)} clues")
    
    # Show initial state
    print("\nInitial clue status:")
    solved_clues = []
    unsolved_clues = []
    
    for clue_id in sorted(puzzle.clues.keys()):
        clue = puzzle.clues[clue_id]
        if clue.is_solved():
            solved_clues.append(clue)
            print(f"  {clue_id}: SOLVED = {clue.get_solution()}")
        else:
            unsolved_clues.append(clue)
            print(f"  {clue_id}: {len(clue.valid_solutions)} solutions")
    
    print(f"\nInitial state: {len(solved_clues)} solved, {len(unsolved_clues)} unsolved")
    
    # Apply already-solved clues
    applied = apply_solved_clues(puzzle)
    
    # Show grid after applying solved clues
    print(f"\nGrid after applying solved clues:")
    puzzle.print_solution()
    
    # Analyze intersections
    analyze_clue_intersections(puzzle)
    
    # Try solving by fewest solutions
    solve_by_fewest_solutions(puzzle)
    
    # Show final state
    print(f"\n=== FINAL STATE ===")
    print(f"Solved clues: {len(puzzle.get_solved_clues())}/{len(puzzle.clues)}")
    print(f"Solved cells: {len(puzzle.solved_cells)}")
    print(f"Completion: {puzzle.get_completion_percentage():.1f}%")
    
    # Show remaining unsolved clues
    unsolved = puzzle.get_unsolved_clues()
    if unsolved:
        print(f"\nRemaining unsolved clues:")
        for clue in sorted(unsolved, key=lambda c: len(c.valid_solutions)):
            print(f"  {clue.clue_id}: {len(clue.valid_solutions)} solutions")
    
    # Show final grid
    puzzle.print_solution()

if __name__ == "__main__":
    main() 