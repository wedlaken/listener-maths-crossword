#!/usr/bin/env python3
"""Forward search for unclued solutions with anagram multiples"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from archive.anagram_grid_solver import is_anagram
import json
from collections import defaultdict

def find_anagram_multiples_forward(number, max_digits=6, max_factor=9):
    """Find all anagram multiples of a number up to max_digits."""
    multiples = []
    
    # Check multiples from 1 to max_factor
    for factor in range(1, max_factor + 1):
        multiple = number * factor
        if len(str(multiple)) <= max_digits:
            if is_anagram(number, multiple):
                multiples.append((factor, multiple))
    
    return multiples

def forward_search_unclued_candidates():
    """Forward search for all 6-digit numbers with anagram multiples."""
    print("=== FORWARD SEARCH FOR UNCLUED CANDIDATES ===")
    print()
    
    candidates = []
    factor_stats = defaultdict(int)
    
    print("Searching all 6-digit numbers for anagram multiples...")
    
    # Search through all 6-digit numbers
    for num in range(100000, 1000000):
        multiples = find_anagram_multiples_forward(num)
        if multiples:
            candidates.append({
                'number': num,
                'multiples': multiples
            })
            
            # Track factor statistics
            for factor, _ in multiples:
                factor_stats[factor] += 1
    
    print(f"Found {len(candidates)} candidates with anagram multiples")
    print()
    
    print("Factor statistics:")
    for factor in sorted(factor_stats.keys()):
        print(f"  Factor {factor}: {factor_stats[factor]} candidates")
    print()
    
    # Show some examples
    print("Sample candidates:")
    for i, candidate in enumerate(candidates[:10]):
        print(f"{i+1}. {candidate['number']}: {candidate['multiples']}")
    
    # Note: Large candidate files removed - using embedded 305-candidate list instead
    print(f"\nGenerated {len(candidates)} candidates (not saved - using embedded list)")
    
    return candidates

def verify_known_solutions_forward():
    """Verify that our forward search finds the known solutions."""
    print("=== VERIFYING KNOWN SOLUTIONS ===")
    print()
    
    known_solutions = [
        (167982, 4),  # 12A
        (428571, 2),  # 14A  
        (137241, 3),  # 7D
        (119883, 7)   # 8D
    ]
    
    found_count = 0
    for number, expected_factor in known_solutions:
        multiples = find_anagram_multiples_forward(number)
        print(f"{number}:")
        print(f"  Expected factor: {expected_factor}")
        print(f"  Found multiples: {multiples}")
        
        # Check if expected factor is found
        found_factors = [factor for factor, _ in multiples]
        if expected_factor in found_factors:
            print(f"  ✓ Expected factor {expected_factor} found")
            found_count += 1
        else:
            print(f"  ✗ Expected factor {expected_factor} NOT found")
        print()
    
    print(f"Found {found_count}/{len(known_solutions)} known solutions")
    return found_count == len(known_solutions)

def analyze_candidate_distribution():
    """Analyze the distribution of candidates by factor."""
    print("=== CANDIDATE DISTRIBUTION ANALYSIS ===")
    print()
    
    candidates = forward_search_unclued_candidates()
    
    # Group candidates by their factors
    factor_groups = defaultdict(list)
    for candidate in candidates:
        for factor, _ in candidate['multiples']:
            factor_groups[factor].append(candidate['number'])
    
    print("Candidates by factor:")
    for factor in sorted(factor_groups.keys()):
        candidates_for_factor = factor_groups[factor]
        print(f"  Factor {factor}: {len(candidates_for_factor)} candidates")
        
        # Show first few examples
        examples = candidates_for_factor[:5]
        print(f"    Examples: {examples}")
        print()

def find_candidates_with_specific_factors(target_factors):
    """Find candidates that have specific factors."""
    print(f"=== CANDIDATES WITH FACTORS {target_factors} ===")
    print()
    
    candidates = []
    for num in range(100000, 1000000):
        multiples = find_anagram_multiples_forward(num)
        if multiples:
            found_factors = [factor for factor, _ in multiples]
            # Check if any target factors are present
            if any(factor in found_factors for factor in target_factors):
                candidates.append({
                    'number': num,
                    'multiples': multiples,
                    'target_factors': [f for f in found_factors if f in target_factors]
                })
    
    print(f"Found {len(candidates)} candidates with factors {target_factors}")
    print()
    
    # Show examples
    print("Sample candidates:")
    for i, candidate in enumerate(candidates[:10]):
        print(f"{i+1}. {candidate['number']}: {candidate['multiples']}")
        print(f"    Target factors: {candidate['target_factors']}")
    
    return candidates

def create_enhanced_candidate_sets():
    """Create enhanced candidate sets for the interactive solver."""
    print("=== CREATING ENHANCED CANDIDATE SETS ===")
    print()
    
    # Get all candidates
    all_candidates = forward_search_unclued_candidates()
    
    # Create factor-specific sets
    factor_sets = defaultdict(set)
    for candidate in all_candidates:
        for factor, _ in candidate['multiples']:
            factor_sets[factor].add(candidate['number'])
    
    # Create comprehensive set
    all_numbers = set()
    for candidate in all_candidates:
        all_numbers.add(candidate['number'])
    
    # Note: Large candidate files removed - using embedded 305-candidate list instead
    print(f"Generated enhanced candidate sets:")
    print(f"  Total candidates: {len(all_numbers)}")
    for factor in sorted(factor_sets.keys()):
        print(f"  Factor {factor}: {len(factor_sets[factor])} candidates")
    
    print(f"\nNot saved - using embedded 305-candidate list instead")
    
    return enhanced_sets

if __name__ == "__main__":
    print("Starting forward search for unclued solutions...")
    print()
    
    # Verify our search finds known solutions
    success = verify_known_solutions_forward()
    if success:
        print("✓ All known solutions found by forward search!")
    else:
        print("✗ Some known solutions not found by forward search")
    
    print()
    
    # Analyze distribution
    analyze_candidate_distribution()
    
    # Find candidates with specific factors
    target_factors = [1, 2, 3, 4, 7]
    find_candidates_with_specific_factors(target_factors)
    
    # Create enhanced candidate sets
    create_enhanced_candidate_sets()
    
    print("\nForward search complete!") 