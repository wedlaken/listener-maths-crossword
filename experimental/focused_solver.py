#!/usr/bin/env python3
"""
Focused solver that starts with clues having fewest solutions and works outward
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Tuple, List, Optional, Set
from collections import defaultdict

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
    clue_params = load_clue_parameters("data/Listener 4869 clues.txt")
    
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

def find_clue_groups(puzzle: ListenerPuzzle) -> List[List[ListenerClue]]:
    """Find groups of clues that share cells (are connected)."""
    # Build adjacency graph
    cell_to_clues = defaultdict(list)
    for clue in puzzle.clues.values():
        for cell in clue.cell_indices:
            cell_to_clues[cell].append(clue)
    
    # Find connected components using DFS
    visited = set()
    groups = []
    
    for clue in puzzle.clues.values():
        if clue.clue_id in visited:
            continue
        
        # Start new group
        group = []
        stack = [clue]
        
        while stack:
            current = stack.pop()
            if current.clue_id in visited:
                continue
            
            visited.add(current.clue_id)
            group.append(current)
            
            # Add all connected clues
            for cell in current.cell_indices:
                for connected_clue in cell_to_clues[cell]:
                    if connected_clue.clue_id not in visited:
                        stack.append(connected_clue)
        
        if group:
            groups.append(group)
    
    return groups

def solve_clue_group(group: List[ListenerClue], puzzle: ListenerPuzzle) -> bool:
    """Try to solve a group of connected clues."""
    print(f"\nAttempting to solve group with {len(group)} clues:")
    for clue in group:
        print(f"  {clue.clue_id}: {len(clue.valid_solutions)} solutions")
    
    # Sort clues by number of solutions (fewest first)
    sorted_clues = sorted(group, key=lambda c: len(c.valid_solutions))
    
    # Try to solve each clue in order
    for clue in sorted_clues:
        if clue.is_solved():
            print(f"  {clue.clue_id} already solved: {clue.get_solution()}")
            continue
        
        if len(clue.valid_solutions) == 1:
            solution = clue.get_solution()
            print(f"  Solving {clue.clue_id} with single solution: {solution}")
            
            # Apply solution
            if not puzzle.solve_clue(clue):
                print(f"  FAILED to solve {clue.clue_id}")
                return False
            
            # Update unclued clues in this group
            puzzle.update_unclued_clues()
            
        elif len(clue.valid_solutions) <= 5:
            print(f"  {clue.clue_id} has {len(clue.valid_solutions)} solutions: {clue.get_valid_solutions()}")
        else:
            print(f"  {clue.clue_id} has {len(clue.valid_solutions)} solutions")
    
    return True

def analyze_smallest_groups(puzzle: ListenerPuzzle) -> None:
    """Analyze and solve the smallest connected groups first."""
    print("=== ANALYZING CLUE GROUPS ===")
    
    groups = find_clue_groups(puzzle)
    print(f"Found {len(groups)} connected groups:")
    
    # Sort groups by size
    groups.sort(key=len)
    
    for i, group in enumerate(groups):
        print(f"\nGroup {i+1} ({len(group)} clues):")
        for clue in group:
            status = "SOLVED" if clue.is_solved() else f"{len(clue.valid_solutions)} solutions"
            print(f"  {clue.clue_id}: {status}")
    
    # Try to solve smallest groups first
    print(f"\n=== SOLVING SMALLEST GROUPS ===")
    
    for i, group in enumerate(groups):
        if len(group) <= 3:  # Focus on small groups first
            print(f"\n--- Group {i+1} ({len(group)} clues) ---")
            if solve_clue_group(group, puzzle):
                print(f"  Group {i+1} solved successfully!")
            else:
                print(f"  Group {i+1} failed to solve completely")
        else:
            print(f"\n--- Group {i+1} ({len(group)} clues) - SKIPPING (too large) ---")

def main():
    """Main focused solving function."""
    print("=== FOCUSED SOLVER ===")
    
    # Create puzzle
    puzzle = create_puzzle()
    print(f"Created puzzle with {len(puzzle.clues)} clues")
    
    # Show initial state
    print("\nInitial clue status:")
    for clue_id in sorted(puzzle.clues.keys()):
        clue = puzzle.clues[clue_id]
        if clue.is_solved():
            print(f"  {clue_id}: SOLVED = {clue.get_solution()}")
        else:
            print(f"  {clue_id}: {len(clue.valid_solutions)} solutions")
    
    # Analyze and solve smallest groups
    analyze_smallest_groups(puzzle)
    
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
    
    # Show grid
    puzzle.print_solution()

if __name__ == "__main__":
    main() 