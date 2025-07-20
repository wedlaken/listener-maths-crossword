#!/usr/bin/env python3
"""
Analyze the unclued solution space for Listener 4869
Find all 6-digit numbers that have anagram multiples ≤ 6 digits
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from archive.anagram_grid_solver import find_anagram_multiples, generate_anagrams_including_original
from typing import List, Dict, Set
import json

def find_all_valid_unclued_candidates() -> Dict[int, List[int]]:
    """
    Find all 6-digit numbers that have anagram multiples ≤ 6 digits.
    
    Returns:
        Dict mapping original number to list of anagram multiples
    """
    print("=== FINDING ALL VALID UNCLUED CANDIDATES ===")
    print("This may take a while...")
    
    valid_candidates = {}
    start_range = 100000  # 6-digit numbers start at 100000
    end_range = 999999    # 6-digit numbers end at 999999
    
    # We can optimize by only checking numbers that start with 1-4
    # (since numbers starting with 5-9 would have multiples > 6 digits)
    valid_starts = [1, 2, 3, 4]
    
    count = 0
    found_count = 0
    
    for start_digit in valid_starts:
        print(f"Checking numbers starting with {start_digit}...")
        
        # Calculate range for this starting digit
        digit_start = start_digit * 100000
        digit_end = (start_digit + 1) * 100000 - 1
        
        for num in range(digit_start, digit_end + 1):
            count += 1
            if count % 10000 == 0:
                print(f"  Processed {count} numbers, found {found_count} valid candidates")
            
            # Check if this number has anagram multiples
            multiples = find_anagram_multiples(num, max_digits=6)
            if multiples:
                valid_candidates[num] = multiples
                found_count += 1
    
    print(f"\nCompleted! Found {found_count} valid candidates out of {count} numbers checked")
    return valid_candidates

def analyze_candidate_patterns(candidates: Dict[int, List[int]]) -> Dict[str, List[int]]:
    """
    Analyze patterns in the valid candidates.
    
    Returns:
        Dict mapping pattern type to list of numbers
    """
    print("\n=== ANALYZING CANDIDATE PATTERNS ===")
    
    patterns = {
        'repeated_digits': [],
        'powers_of_2': [],
        'multiples_of_1089': [],
        'palindromic': [],
        'sequential': [],
        'other': []
    }
    
    for num in candidates.keys():
        num_str = str(num)
        
        # Check for repeated digits
        if len(set(num_str)) == 1:
            patterns['repeated_digits'].append(num)
        # Check for powers of 2
        elif num in [102400, 204800, 409600, 819200]:
            patterns['powers_of_2'].append(num)
        # Check for multiples of 1089
        elif num % 1089 == 0:
            patterns['multiples_of_1089'].append(num)
        # Check for palindromic
        elif num_str == num_str[::-1]:
            patterns['palindromic'].append(num)
        # Check for sequential
        elif len(set(num_str)) == len(num_str) and all(int(num_str[i+1]) == int(num_str[i]) + 1 for i in range(len(num_str)-1)):
            patterns['sequential'].append(num)
        else:
            patterns['other'].append(num)
    
    # Print summary
    for pattern_type, numbers in patterns.items():
        print(f"{pattern_type}: {len(numbers)} candidates")
        if numbers:
            print(f"  Examples: {numbers[:5]}")
        print()
    
    return patterns

def generate_unclued_solution_sets() -> Dict[str, List[int]]:
    """
    Generate solution sets for unclued clues based on anagram constraints.
    
    Returns:
        Dict mapping clue_id to list of valid solutions
    """
    print("=== GENERATING UNCLUED SOLUTION SETS ===")
    
    # Get all valid candidates
    candidates = find_all_valid_unclued_candidates()
    
    # Analyze patterns
    patterns = analyze_candidate_patterns(candidates)
    
    # Create solution sets for each unclued clue
    unclued_clues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN']
    solution_sets = {}
    
    for clue_id in unclued_clues:
        # For now, all candidates are valid for all unclued clues
        # In practice, we'd filter based on grid constraints
        solution_sets[clue_id] = sorted(list(candidates.keys()))
    
    print(f"Generated solution sets for {len(unclued_clues)} unclued clues")
    for clue_id, solutions in solution_sets.items():
        print(f"  {clue_id}: {len(solutions)} solutions")
    
    return solution_sets, candidates

def save_solution_data(solution_sets: Dict[str, List[int]], 
                      candidates: Dict[int, List[int]], 
                      patterns: Dict[str, List[int]]):
    """Save the solution data to JSON files."""
    
    # Save unclued solution sets
    with open('data/unclued_solution_sets.json', 'w') as f:
        json.dump(solution_sets, f, indent=2)
    
    # Save candidate data (with multiples)
    with open('data/unclued_candidates.json', 'w') as f:
        json.dump(candidates, f, indent=2)
    
    # Save pattern analysis
    with open('data/unclued_patterns.json', 'w') as f:
        json.dump(patterns, f, indent=2)
    
    print("\n=== SAVED SOLUTION DATA ===")
    print("data/unclued_solution_sets.json - Solution sets for each unclued clue")
    print("data/unclued_candidates.json - All valid candidates with their anagram multiples")
    print("data/unclued_patterns.json - Pattern analysis of candidates")

def create_validation_lookup(candidates: Dict[int, List[int]]) -> Dict[int, bool]:
    """
    Create a fast lookup table for validation.
    
    Returns:
        Dict mapping number to True if it's a valid unclued candidate
    """
    return {num: True for num in candidates.keys()}

def main():
    """Main analysis function."""
    print("UNCLUED SOLUTION SPACE ANALYSIS")
    print("=" * 50)
    print()
    
    # Generate solution sets
    solution_sets, candidates = generate_unclued_solution_sets()
    
    # Analyze patterns
    patterns = analyze_candidate_patterns(candidates)
    
    # Save data
    save_solution_data(solution_sets, candidates, patterns)
    
    # Create validation lookup
    validation_lookup = create_validation_lookup(candidates)
    
    print("\n=== SUMMARY ===")
    print(f"Total valid unclued candidates: {len(candidates)}")
    print(f"Average anagram multiples per candidate: {sum(len(m) for m in candidates.values()) / len(candidates):.1f}")
    print()
    print("This provides a manageable set of candidates that can be:")
    print("1. Used for validation in the interactive solver")
    print("2. Filtered further based on grid constraints")
    print("3. Presented as suggestions when users input unclued solutions")
    print()
    print("The solution sets are saved and ready for integration!")

if __name__ == "__main__":
    main() 