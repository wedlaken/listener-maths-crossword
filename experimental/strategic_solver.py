#!/usr/bin/env python3
"""
Strategic solver that works in phases like a human would
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from systematic_grid_parser import parse_grid
from crossword_solver import ListenerPuzzle, ListenerClue
from typing import Dict, Tuple, List, Optional, NamedTuple

class Checkpoint(NamedTuple):
    """Represents a decision point for backtracking"""
    clue_id: str
    solutions: List[int]
    shared_clues: List[str]  # Clues that share cells with this one
    potential_impact: int    # How many other clues this might help solve

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
    grid_clues = parse_grid()
    clue_params = load_clue_parameters("Listener 4869 clues.txt")
    
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
        
        clue = ListenerClue(clue_id, direction, cell_indices, parameters)
        puzzle.add_clue(clue)
    
    return puzzle

def phase1_apply_solved_clues(puzzle: ListenerPuzzle) -> int:
    """Phase 1: Apply all already-solved clues."""
    print("=== PHASE 1: APPLYING SOLVED CLUES ===")
    
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
    
    print(f"Phase 1 complete: Applied {applied_count} solved clues")
    return applied_count

def phase2_constraint_propagation(puzzle: ListenerPuzzle) -> int:
    """Phase 2: Apply constraint propagation to solve single-solution clues."""
    print("\n=== PHASE 2: CONSTRAINT PROPAGATION ===")
    
    solved_count = 0
    max_iterations = 10
    
    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        
        # Find clues with single solutions
        single_solution_clues = []
        for clue in puzzle.clues.values():
            if not clue.is_solved() and len(clue.valid_solutions) == 1:
                single_solution_clues.append(clue)
        
        if not single_solution_clues:
            print("No single-solution clues found")
            break
        
        print(f"Found {len(single_solution_clues)} single-solution clues")
        
        # Apply each single-solution clue
        for clue in single_solution_clues:
            solution = clue.get_solution()
            print(f"  Applying {clue.clue_id}: {solution}")
            
            if puzzle.solve_clue(clue):
                solved_count += 1
                print(f"    Successfully applied {clue.clue_id}")
            else:
                print(f"    FAILED to apply {clue.clue_id}")
        
        # Update unclued clues
        puzzle.update_unclued_clues()
        
        # Show progress
        total_solved = len(puzzle.get_solved_clues())
        print(f"  Progress: {total_solved}/{len(puzzle.clues)} clues solved")
    
    print(f"Phase 2 complete: Solved {solved_count} additional clues")
    return solved_count

def find_best_checkpoint(puzzle: ListenerPuzzle) -> Optional[Checkpoint]:
    """Find the best checkpoint for backtracking."""
    print("\n=== ANALYZING CHECKPOINT CANDIDATES ===")
    
    # Build cell-to-clues mapping
    cell_to_clues = {}
    for clue in puzzle.clues.values():
        for cell in clue.cell_indices:
            if cell not in cell_to_clues:
                cell_to_clues[cell] = []
            cell_to_clues[cell].append(clue.clue_id)
    
    # Find clues with 2-5 solutions
    candidates = []
    for clue in puzzle.clues.values():
        if not clue.is_solved() and 2 <= len(clue.valid_solutions) <= 5:
            # Find clues that share cells with this one
            shared_clues = set()
            for cell in clue.cell_indices:
                for shared_clue_id in cell_to_clues.get(cell, []):
                    if shared_clue_id != clue.clue_id:
                        shared_clue = puzzle.clues[shared_clue_id]
                        if not shared_clue.is_solved():
                            shared_clues.add(shared_clue_id)
            
            # Calculate potential impact
            potential_impact = len(shared_clues)
            
            checkpoint = Checkpoint(
                clue_id=clue.clue_id,
                solutions=clue.get_valid_solutions(),
                shared_clues=list(shared_clues),
                potential_impact=potential_impact
            )
            candidates.append(checkpoint)
    
    # Sort by potential impact (highest first), then by number of solutions (lowest first)
    candidates.sort(key=lambda c: (-c.potential_impact, len(c.solutions)))
    
    print("Checkpoint candidates:")
    for i, candidate in enumerate(candidates[:5]):  # Show top 5
        print(f"  {i+1}. {candidate.clue_id}: {len(candidate.solutions)} solutions, "
              f"impact: {candidate.potential_impact}, shared: {candidate.shared_clues}")
    
    return candidates[0] if candidates else None

def phase3_backtrack_at_checkpoint(puzzle: ListenerPuzzle, checkpoint: Checkpoint) -> bool:
    """Phase 3: Try backtracking at the identified checkpoint."""
    print(f"\n=== PHASE 3: BACKTRACKING AT {checkpoint.clue_id} ===")
    print(f"Trying {len(checkpoint.solutions)} solutions: {checkpoint.solutions}")
    print(f"Shared clues: {checkpoint.shared_clues}")
    
    # Save current state
    puzzle.save_state()
    
    for i, solution in enumerate(checkpoint.solutions):
        print(f"\n--- Trying solution {i+1}: {solution} ---")
        
        # Restore state
        puzzle.restore_state()
        
        # Apply this solution
        clue = puzzle.clues[checkpoint.clue_id]
        original_solutions = set(clue.valid_solutions)
        clue.valid_solutions = {solution}
        
        if puzzle.solve_clue(clue):
            print(f"  Successfully applied {checkpoint.clue_id} = {solution}")
            
            # Try to solve more clues
            additional_solved = phase2_constraint_propagation(puzzle)
            
            if additional_solved > 0:
                print(f"  This path led to {additional_solved} additional solved clues!")
                print(f"  Total solved: {len(puzzle.get_solved_clues())}/{len(puzzle.clues)}")
                return True
            else:
                print(f"  This path didn't lead to additional solved clues")
        else:
            print(f"  Failed to apply {checkpoint.clue_id} = {solution}")
    
    # Restore original state if no path worked
    puzzle.restore_state()
    print(f"  No path from {checkpoint.clue_id} led to progress")
    return False

def main():
    """Main strategic solving function."""
    print("=== STRATEGIC SOLVER ===")
    
    # Create puzzle
    puzzle = create_puzzle()
    print(f"Created puzzle with {len(puzzle.clues)} clues")
    
    # Phase 1: Apply solved clues
    phase1_solved = phase1_apply_solved_clues(puzzle)
    
    # Show grid after phase 1
    print(f"\nGrid after Phase 1:")
    puzzle.print_solution()
    
    # Phase 2: Constraint propagation
    phase2_solved = phase2_constraint_propagation(puzzle)
    
    # Show grid after phase 2
    print(f"\nGrid after Phase 2:")
    puzzle.print_solution()
    
    # Find best checkpoint
    checkpoint = find_best_checkpoint(puzzle)
    
    if checkpoint:
        # Phase 3: Backtracking at checkpoint
        success = phase3_backtrack_at_checkpoint(puzzle, checkpoint)
        
        if success:
            print(f"\nGrid after Phase 3:")
            puzzle.print_solution()
        else:
            print(f"\nPhase 3 didn't lead to progress")
    else:
        print(f"\nNo suitable checkpoint found")
    
    # Final state
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

if __name__ == "__main__":
    main() 