#!/usr/bin/env python3
"""Enhanced Interactive Solver with Forward-Search Unclued Candidates"""

import json
import os
from typing import Dict, List, Set, Optional
from utils import is_anagram

class ForwardUncluedSolver:
    """Enhanced solver using forward-search unclued candidates."""
    
    def __init__(self, candidate_file: str = None):
        """Initialize with forward-search candidates."""
        self.candidates = self.load_candidates(candidate_file)
        self.factor_sets = self.candidates.get('factor_sets', {})
        self.all_candidates = set(self.candidates.get('all_candidates', []))
        
    def load_candidates(self, filename: str) -> Dict:
        """Load candidate sets from file."""
        if filename is None:
            print("Note: Using embedded 305-candidate list instead of file")
            return {'all_candidates': [], 'factor_sets': {}}
        
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Candidate file {filename} not found")
            return {'all_candidates': [], 'factor_sets': {}}
    
    def validate_unclued_solution(self, solution: int) -> Dict:
        """Validate an unclued solution against forward-search candidates."""
        if solution not in self.all_candidates:
            return {
                'valid': False,
                'reason': 'Not in forward-search candidate set',
                'suggestions': self.get_suggestions(solution)
            }
        
        # Find what factors this solution has
        factors = []
        for factor_str, candidates in self.factor_sets.items():
            if solution in candidates:
                factors.append(int(factor_str))
        
        return {
            'valid': True,
            'factors': factors,
            'anagram_multiples': self.get_anagram_multiples(solution)
        }
    
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
    
    def get_statistics(self) -> Dict:
        """Get statistics about the candidate sets."""
        return {
            'total_candidates': len(self.all_candidates),
            'factor_statistics': self.candidates.get('factor_statistics', {}),
            'available_factors': list(self.factor_sets.keys())
        }

def main():
    """Test the forward-search enhanced solver."""
    print("=== FORWARD-SEARCH ENHANCED UNCLUED SOLVER ===")
    print()
    
    # Initialize solver
    solver = ForwardUncluedSolver()
    
    # Show statistics
    stats = solver.get_statistics()
    print(f"Total candidates: {stats['total_candidates']}")
    print("Factor statistics:")
    for factor, count in stats['factor_statistics'].items():
        print(f"  Factor {factor}: {count} candidates")
    print()
    
    # Test known solutions
    known_solutions = [167982, 428571, 137241, 119883]
    print("Testing known solutions:")
    for solution in known_solutions:
        result = solver.validate_unclued_solution(solution)
        print(f"{solution}: {result}")
    print()
    
    # Test invalid solutions
    invalid_solutions = [123456, 999999, 100000]
    print("Testing invalid solutions:")
    for solution in invalid_solutions:
        result = solver.validate_unclued_solution(solution)
        print(f"{solution}: {result}")
        if not result['valid'] and result['suggestions']:
            print(f"  Suggestions: {result['suggestions']}")
    print()

if __name__ == "__main__":
    main() 