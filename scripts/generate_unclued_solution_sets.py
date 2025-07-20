#!/usr/bin/env python3
"""
Generate unclued solution sets for Listener 4869
Integrates with existing solution set structure and provides validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import find_anagram_multiples
from typing import List, Dict, Set
import json

def find_unclued_candidates_efficient() -> Dict[int, List[int]]:
    """
    Efficiently find 6-digit numbers with anagram multiples.
    Uses mathematical insights to reduce search space.
    """
    print("=== FINDING UNCLUED CANDIDATES (EFFICIENT METHOD) ===")
    
    valid_candidates = {}
    
    # Strategy: Focus on numbers with properties that often have anagram multiples
    # 1. Numbers with repeated digits
    # 2. Powers of 2
    # 3. Multiples of 1089
    # 4. Palindromic numbers
    # 5. Numbers with symmetric digit patterns
    
    # 1. Repeated digits (111111, 222222, etc.)
    print("Checking repeated digits...")
    for digit in range(1, 6):  # Only 1-5 to keep multiples ≤ 6 digits
        num = int(str(digit) * 6)
        multiples = find_anagram_multiples(num, max_digits=6)
        if multiples:
            valid_candidates[num] = multiples
    
    # 2. Powers of 2
    print("Checking powers of 2...")
    powers_of_2 = [102400, 204800, 409600, 819200]
    for num in powers_of_2:
        if num <= 500000:  # Only if ≤ 500000 to keep multiples ≤ 6 digits
            multiples = find_anagram_multiples(num, max_digits=6)
            if multiples:
                valid_candidates[num] = multiples
    
    # 3. Multiples of 1089
    print("Checking multiples of 1089...")
    for i in range(1, 1000):
        num = 1089 * i
        if 100000 <= num <= 500000:  # 6-digit and ≤ 500000
            multiples = find_anagram_multiples(num, max_digits=6)
            if multiples:
                valid_candidates[num] = multiples
    
    # 4. Palindromic numbers
    print("Checking palindromic numbers...")
    for i in range(100, 1000):
        # Create 6-digit palindrome
        num = int(str(i) + str(i)[::-1])
        if num <= 500000:
            multiples = find_anagram_multiples(num, max_digits=6)
            if multiples:
                valid_candidates[num] = multiples
    
    # 5. Systematic search for remaining patterns
    print("Systematic search for other patterns...")
    for start_digit in range(1, 6):
        for middle in range(10000):
            num = start_digit * 100000 + middle
            if 100000 <= num <= 500000:
                # Only check every 100th number to speed up
                if num % 100 == 0:
                    multiples = find_anagram_multiples(num, max_digits=6)
                    if multiples:
                        valid_candidates[num] = multiples
    
    print(f"Found {len(valid_candidates)} valid candidates")
    return valid_candidates

def create_unclued_solution_sets(candidates: Dict[int, List[int]]) -> Dict[str, List[int]]:
    """
    Create solution sets for unclued clues.
    
    Returns:
        Dict mapping clue_id to list of valid solutions
    """
    unclued_clues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN']
    solution_sets = {}
    
    # For now, all candidates are valid for all unclued clues
    # In practice, we'd filter based on grid constraints
    candidate_list = sorted(list(candidates.keys()))
    
    for clue_id in unclued_clues:
        solution_sets[clue_id] = candidate_list
    
    return solution_sets

def create_validation_data(candidates: Dict[int, List[int]]) -> Dict[str, any]:
    """
    Create validation data for the interactive solver.
    
    Returns:
        Dict with validation lookup and metadata
    """
    validation_data = {
        'valid_candidates': list(candidates.keys()),
        'candidate_multiples': candidates,
        'total_candidates': len(candidates),
        'average_multiples': sum(len(m) for m in candidates.values()) / len(candidates) if candidates else 0
    }
    
    return validation_data

def save_unclued_data(solution_sets: Dict[str, List[int]], 
                     validation_data: Dict[str, any]):
    """Save unclued solution data to files."""
    
    # Save solution sets (similar to existing solution_sets.json structure)
    with open('data/unclued_solution_sets.json', 'w') as f:
        json.dump(solution_sets, f, indent=2)
    
    # Save validation data
    with open('data/unclued_validation.json', 'w') as f:
        json.dump(validation_data, f, indent=2)
    
    print("\n=== SAVED UNCLUED DATA ===")
    print("data/unclued_solution_sets.json - Solution sets for unclued clues")
    print("data/unclued_validation.json - Validation data for interactive solver")

def main():
    """Main function to generate unclued solution sets."""
    print("GENERATING UNCLUED SOLUTION SETS")
    print("=" * 40)
    print()
    
    # Find valid candidates
    candidates = find_unclued_candidates_efficient()
    
    # Create solution sets
    solution_sets = create_unclued_solution_sets(candidates)
    
    # Create validation data
    validation_data = create_validation_data(candidates)
    
    # Save data
    save_unclued_data(solution_sets, validation_data)
    
    print("\n=== SUMMARY ===")
    print(f"Total valid unclued candidates: {len(candidates)}")
    print(f"Average anagram multiples per candidate: {validation_data['average_multiples']:.1f}")
    print()
    print("Integration with interactive solver:")
    print("1. Load unclued_validation.json for fast validation")
    print("2. Use unclued_solution_sets.json for solution suggestions")
    print("3. Filter candidates based on grid constraints")
    print("4. Provide real-time feedback on anagram validity")

if __name__ == "__main__":
    main() 