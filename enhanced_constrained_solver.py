#!/usr/bin/env python3
"""Enhanced Interactive Solver with Constrained Forward Search"""

import json
import os
from typing import Dict, List, Set, Optional
from constrained_forward_solver import ConstrainedForwardSolver

class EnhancedConstrainedSolver:
    """Enhanced interactive solver with constraint checking."""
    
    def __init__(self, min_solved_cells: int = 2):
        """Initialize the enhanced solver."""
        self.solver = ConstrainedForwardSolver(min_solved_cells=min_solved_cells)
        self.min_solved_cells = min_solved_cells
        
        # Track the current state
        self.solved_cells = {}  # {cell_index: digit}
        self.solved_clues = {}  # {clue_id: solution}
        self.clue_cells = {}    # {clue_id: [cell_indices]}
        
    def add_clue_cells(self, clue_id: str, cell_indices: List[int]) -> None:
        """Add clue cell mapping."""
        self.clue_cells[clue_id] = cell_indices
    
    def apply_solution(self, clue_id: str, solution: int) -> Dict:
        """Apply a solution to a clue."""
        if clue_id not in self.clue_cells:
            return {
                'success': False,
                'reason': f'Clue {clue_id} not found'
            }
        
        cell_indices = self.clue_cells[clue_id]
        solution_str = str(solution).zfill(len(cell_indices))
        
        # Check for conflicts with existing cells
        conflicts = []
        for i, cell_index in enumerate(cell_indices):
            if cell_index in self.solved_cells:
                if self.solved_cells[cell_index] != int(solution_str[i]):
                    conflicts.append(f"Cell {cell_index}: {self.solved_cells[cell_index]} vs {solution_str[i]}")
        
        if conflicts:
            return {
                'success': False,
                'reason': f'Conflicts with existing cells: {conflicts}'
            }
        
        # Apply the solution
        for i, cell_index in enumerate(cell_indices):
            self.solved_cells[cell_index] = int(solution_str[i])
            self.solver.add_solved_cell(cell_index, int(solution_str[i]))
        
        self.solved_clues[clue_id] = solution
        self.solver.add_solved_clue(clue_id, solution)
        
        return {
            'success': True,
            'cells_updated': len(cell_indices),
            'total_solved_cells': len(self.solved_cells)
        }
    
    def remove_solution(self, clue_id: str) -> Dict:
        """Remove a solution from a clue."""
        if clue_id not in self.solved_clues:
            return {
                'success': False,
                'reason': f'Clue {clue_id} not solved'
            }
        
        cell_indices = self.clue_cells[clue_id]
        
        # Remove cells that aren't used by other solved clues
        cells_to_remove = []
        for cell_index in cell_indices:
            # Check if this cell is used by other solved clues
            used_by_others = False
            for other_clue_id, other_cells in self.clue_cells.items():
                if other_clue_id != clue_id and other_clue_id in self.solved_clues:
                    if cell_index in other_cells:
                        used_by_others = True
                        break
            
            if not used_by_others:
                cells_to_remove.append(cell_index)
        
        # Remove the cells
        for cell_index in cells_to_remove:
            if cell_index in self.solved_cells:
                del self.solved_cells[cell_index]
                # Note: We'd need to update the solver's solved_cells too
        
        # Remove the clue solution
        del self.solved_clues[clue_id]
        self.solver.remove_solved_clue(clue_id)
        
        return {
            'success': True,
            'cells_removed': len(cells_to_remove),
            'total_solved_cells': len(self.solved_cells)
        }
    
    def validate_unclued_solution(self, clue_id: str, solution: int) -> Dict:
        """Validate an unclued solution."""
        if clue_id not in self.clue_cells:
            return {
                'valid': False,
                'reason': f'Clue {clue_id} not found'
            }
        
        cell_indices = self.clue_cells[clue_id]
        return self.solver.validate_unclued_solution(solution, cell_indices)
    
    def get_unclued_candidates(self, clue_id: str) -> Dict:
        """Get filtered candidates for an unclued clue."""
        if clue_id not in self.clue_cells:
            return {
                'candidates': [],
                'reason': f'Clue {clue_id} not found'
            }
        
        cell_indices = self.clue_cells[clue_id]
        constraint_check = self.solver.can_enter_unclued_solution()
        
        if not constraint_check['allowed']:
            return {
                'candidates': [],
                'reason': constraint_check['reason'],
                'constraint_violation': True
            }
        
        candidates = self.solver.get_filtered_candidates(cell_indices)
        return {
            'candidates': candidates,
            'count': len(candidates),
            'constraint_violation': False
        }
    
    def get_solver_status(self) -> Dict:
        """Get current solver status."""
        stats = self.solver.get_statistics()
        constraint_check = self.solver.can_enter_unclued_solution()
        
        return {
            'solved_cells': len(self.solved_cells),
            'solved_clues': len(self.solved_clues),
            'min_required_cells': self.min_solved_cells,
            'can_enter_unclued': constraint_check['allowed'],
            'constraint_message': constraint_check.get('reason', ''),
            'total_candidates': stats['total_candidates'],
            'available_factors': stats['available_factors']
        }
    
    def get_solved_cells_display(self) -> Dict:
        """Get solved cells for display."""
        return self.solved_cells.copy()

def main():
    """Test the enhanced constrained solver."""
    print("=== ENHANCED CONSTRAINED SOLVER TEST ===")
    print()
    
    # Initialize solver
    solver = EnhancedConstrainedSolver(min_solved_cells=2)
    
    # Add some clue mappings
    solver.add_clue_cells("12_ACROSS", [0, 1, 2, 3])
    solver.add_clue_cells("14_ACROSS", [33, 34, 35, 36, 37, 38])
    solver.add_clue_cells("7_DOWN", [11, 19, 27, 35, 43, 51])
    solver.add_clue_cells("8_DOWN", [12, 20, 28, 36, 44, 52])
    
    # Show initial status
    status = solver.get_solver_status()
    print(f"Initial status: {status}")
    print()
    
    # Test constraint checking
    print("Testing unclued validation (should fail):")
    result = solver.validate_unclued_solution("12_ACROSS", 167982)
    print(f"12A 167982: {result}")
    print()
    
    # Apply some regular solutions first
    print("Applying regular solutions...")
    solver.apply_solution("10_ACROSS", 1234)  # Add a regular clue
    solver.apply_solution("11_ACROSS", 5678)  # Add another regular clue
    
    status = solver.get_solver_status()
    print(f"After regular solutions: {status}")
    print()
    
    # Now test unclued validation
    print("Testing unclued validation (should work):")
    result = solver.validate_unclued_solution("12_ACROSS", 167982)
    print(f"12A 167982: {result}")
    print()
    
    # Test getting candidates
    print("Testing candidate generation:")
    candidates = solver.get_unclued_candidates("12_ACROSS")
    print(f"12A candidates: {candidates}")
    print()
    
    # Test applying unclued solution
    print("Testing unclued solution application:")
    result = solver.apply_solution("12_ACROSS", 167982)
    print(f"Apply 12A 167982: {result}")
    print()
    
    # Show final status
    status = solver.get_solver_status()
    print(f"Final status: {status}")
    print(f"Solved cells: {solver.get_solved_cells_display()}")

if __name__ == "__main__":
    main() 