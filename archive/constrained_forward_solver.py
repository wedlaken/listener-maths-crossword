#!/usr/bin/env python3
"""Constrained Forward Solver with Minimum Cell Requirements"""

import json
import os
from typing import Dict, List, Set, Optional, Tuple
from anagram_grid_solver import is_anagram

class ConstrainedForwardSolver:
    """Enhanced solver with constraints for unclued solutions."""
    
    def __init__(self, candidate_file: str = 'data/unclued_candidates.json', 
                 min_solved_cells: int = 1):
        """Initialize with constraints."""
        self.candidates = self.load_candidates(candidate_file)
        
        # Handle different file formats
        if 'all_candidates' in self.candidates:
            # Enhanced format with all_candidates and factor_sets
            self.factor_sets = self.candidates.get('factor_sets', {})
            self.all_candidates = set(self.candidates.get('all_candidates', []))
        else:
            # Simple format with {number: [multiples]}
            self.all_candidates = set(int(k) for k in self.candidates.keys())
            # Create factor_sets from the multiples data
            self.factor_sets = {}
            for number, multiples in self.candidates.items():
                for multiple in multiples:
                    factor = multiple // int(number)
                    if str(factor) not in self.factor_sets:
                        self.factor_sets[str(factor)] = []
                    self.factor_sets[str(factor)].append(int(number))
        
        self.min_solved_cells = min_solved_cells
        
        # Track solved cells and their values
        self.solved_cells = {}  # {cell_index: digit}
        self.solved_clues = {}  # {clue_id: solution}
        
    def load_candidates(self, filename: str) -> Dict:
        """Load candidate sets from file."""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Candidate file {filename} not found")
            return {'all_candidates': [], 'factor_sets': {}}
    
    def add_solved_cell(self, cell_index: int, digit: int) -> None:
        """Add a solved cell to track constraints."""
        self.solved_cells[cell_index] = digit
    
    def add_solved_clue(self, clue_id: str, solution: int) -> None:
        """Add a solved clue."""
        self.solved_clues[clue_id] = solution
    
    def remove_solved_clue(self, clue_id: str) -> None:
        """Remove a solved clue."""
        if clue_id in self.solved_clues:
            del self.solved_clues[clue_id]
    
    def get_solved_cell_count(self) -> int:
        """Get the number of solved cells."""
        return len(self.solved_cells)
    
    def can_enter_unclued_solution(self) -> Dict:
        """Check if user can enter an unclued solution based on constraints."""
        solved_count = self.get_solved_cell_count()
        
        if solved_count < self.min_solved_cells:
            return {
                'allowed': False,
                'reason': f'Need at least {self.min_solved_cells} solved cells, but only have {solved_count}',
                'solved_count': solved_count,
                'required_count': self.min_solved_cells
            }
        
        return {
            'allowed': True,
            'solved_count': solved_count,
            'required_count': self.min_solved_cells
        }
    
    def validate_unclued_solution(self, solution: int, clue_cells: List[int]) -> Dict:
        """Validate an unclued solution with current constraints."""
        # First check if we can enter unclued solutions at all
        constraint_check = self.can_enter_unclued_solution()
        if not constraint_check['allowed']:
            return {
                'valid': False,
                'reason': constraint_check['reason'],
                'constraint_violation': True
            }
        
        # Check if solution is in our candidate set
        if solution not in self.all_candidates:
            return {
                'valid': False,
                'reason': 'Not in forward-search candidate set',
                'suggestions': self.get_suggestions(solution),
                'constraint_violation': False
            }
        
        # Check for conflicts with already solved cells
        conflicts = self.check_cell_conflicts(solution, clue_cells)
        if conflicts:
            return {
                'valid': False,
                'reason': f'Conflicts with solved cells: {conflicts}',
                'constraint_violation': False
            }
        
        # Find what factors this solution has
        factors = []
        for factor_str, candidates in self.factor_sets.items():
            if solution in candidates:
                factors.append(int(factor_str))
        
        return {
            'valid': True,
            'factors': factors,
            'anagram_multiples': self.get_anagram_multiples(solution),
            'constraint_violation': False
        }
    
    def check_cell_conflicts(self, solution: int, clue_cells: List[int]) -> List[str]:
        """Check if solution conflicts with already solved cells."""
        conflicts = []
        solution_str = str(solution).zfill(len(clue_cells))
        
        for i, cell_index in enumerate(clue_cells):
            if cell_index in self.solved_cells:
                expected_digit = self.solved_cells[cell_index]
                actual_digit = int(solution_str[i])
                if expected_digit != actual_digit:
                    conflicts.append(f"Cell {cell_index}: expected {expected_digit}, got {actual_digit}")
        
        return conflicts
    
    def get_suggestions(self, invalid_solution: int) -> List[int]:
        """Get suggestions for invalid solutions."""
        suggestions = []
        
        # Find similar numbers (same digits, different order)
        invalid_str = str(invalid_solution)
        for candidate in self.all_candidates:
            candidate_str = str(candidate)
            if len(candidate_str) == len(invalid_str) and sorted(candidate_str) == sorted(invalid_str):
                suggestions.append(candidate)
                if len(suggestions) >= 5:  # Limit suggestions
                    break
        
        return suggestions
    
    def get_anagram_multiples(self, solution: int) -> List[tuple]:
        """Get anagram multiples for a solution."""
        multiples = []
        for factor in range(1, 10):
            multiple = solution * factor
            if len(str(multiple)) <= 6 and is_anagram(solution, multiple):
                multiples.append((factor, multiple))
        return multiples
    
    def get_candidates_by_factor(self, factor: int) -> List[int]:
        """Get all candidates for a specific factor."""
        return self.factor_sets.get(str(factor), [])
    
    def get_filtered_candidates(self, clue_cells: List[int]) -> List[int]:
        """Get candidates that don't conflict with current solved cells."""
        if not self.can_enter_unclued_solution()['allowed']:
            return []
        
        filtered_candidates = []
        for candidate in self.all_candidates:
            if len(str(candidate)) == len(clue_cells):
                conflicts = self.check_cell_conflicts(candidate, clue_cells)
                if not conflicts:
                    filtered_candidates.append(candidate)
        
        return filtered_candidates
    
    def get_statistics(self) -> Dict:
        """Get statistics about the solver state."""
        return {
            'total_candidates': len(self.all_candidates),
            'factor_statistics': self.candidates.get('factor_statistics', {}),
            'available_factors': list(self.factor_sets.keys()),
            'solved_cells': len(self.solved_cells),
            'solved_clues': len(self.solved_clues),
            'min_required_cells': self.min_solved_cells,
            'can_enter_unclued': self.can_enter_unclued_solution()['allowed']
        }

def main():
    """Test the constrained forward solver."""
    print("=== CONSTRAINED FORWARD-SEARCH SOLVER ===")
    print()
    
    # Initialize solver with minimum 2 cells requirement
    solver = ConstrainedForwardSolver(min_solved_cells=2)
    
    # Show initial state
    stats = solver.get_statistics()
    print(f"Initial state:")
    print(f"  Solved cells: {stats['solved_cells']}/{stats['min_required_cells']}")
    print(f"  Can enter unclued: {stats['can_enter_unclued']}")
    print()
    
    # Test constraint checking
    print("Testing constraint checking:")
    constraint_check = solver.can_enter_unclued_solution()
    print(f"Can enter unclued: {constraint_check}")
    print()
    
    # Add some solved cells
    print("Adding solved cells...")
    solver.add_solved_cell(0, 1)  # Cell 0 = 1
    solver.add_solved_cell(8, 6)  # Cell 8 = 6
    
    stats = solver.get_statistics()
    print(f"After adding cells:")
    print(f"  Solved cells: {stats['solved_cells']}/{stats['min_required_cells']}")
    print(f"  Can enter unclued: {stats['can_enter_unclued']}")
    print()
    
    # Test validation with constraints
    print("Testing validation with constraints:")
    test_solution = 167982
    test_cells = [0, 1, 2, 3]  # 4-cell clue
    
    result = solver.validate_unclued_solution(test_solution, test_cells)
    print(f"Solution {test_solution}: {result}")
    print()
    
    # Test filtered candidates
    print("Testing filtered candidates:")
    filtered = solver.get_filtered_candidates(test_cells)
    print(f"Filtered candidates for cells {test_cells}: {len(filtered)} candidates")
    if filtered:
        print(f"First 5: {filtered[:5]}")

if __name__ == "__main__":
    main() 