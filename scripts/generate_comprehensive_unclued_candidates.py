#!/usr/bin/env python3
"""Generate comprehensive list of unclued solution candidates"""

from utils import find_anagram_multiples, is_anagram
import json
from collections import defaultdict

def find_all_anagram_multiples(number, max_digits=6):
    """Find all anagram multiples of a number up to max_digits."""
    multiples = []
    number_str = str(number)
    
    # Check multiples from 1 to 9 (reasonable factors)
    for factor in range(1, 10):
        multiple = number * factor
        if len(str(multiple)) <= max_digits:
            if is_anagram(number, multiple):
                multiples.append((factor, multiple))
    
    return multiples

def generate_comprehensive_candidates():
    """Generate comprehensive list of candidates with anagram multiples."""
    print("=== COMPREHENSIVE UNCLUED CANDIDATE SEARCH ===")
    print()
    
    candidates = []
    factor_stats = defaultdict(int)
    
    # Search through all 6-digit numbers
    for num in range(100000, 1000000):
        multiples = find_all_anagram_multiples(num)
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
    
    # Save to file
    output_data = {
        'total_candidates': len(candidates),
        'factor_statistics': dict(factor_stats),
        'candidates': candidates
    }
    
    with open('data/comprehensive_unclued_candidates.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nSaved {len(candidates)} candidates to data/comprehensive_unclued_candidates.json")
    
    return candidates

def analyze_known_solutions():
    """Analyze the known solutions to verify our search."""
    print("=== KNOWN SOLUTIONS VERIFICATION ===")
    print()
    
    known_solutions = [
        (167982, 4),  # 12A
        (428571, 2),  # 14A  
        (137241, 3),  # 7D
        (119883, 7)   # 8D
    ]
    
    for number, expected_factor in known_solutions:
        multiples = find_all_anagram_multiples(number)
        print(f"{number}:")
        print(f"  Expected factor: {expected_factor}")
        print(f"  Found multiples: {multiples}")
        
        # Check if expected factor is found
        found_factors = [factor for factor, _ in multiples]
        if expected_factor in found_factors:
            print(f"  ✓ Expected factor {expected_factor} found")
        else:
            print(f"  ✗ Expected factor {expected_factor} NOT found")
        print()

def generate_factor_specific_candidates():
    """Generate candidates for specific factors we know exist."""
    print("=== FACTOR-SPECIFIC CANDIDATES ===")
    print()
    
    # Factors we know exist: 1, 2, 3, 4, 7
    target_factors = [1, 2, 3, 4, 7]
    
    for factor in target_factors:
        print(f"Factor {factor} candidates:")
        count = 0
        examples = []
        
        for num in range(100000, 1000000):
            multiple = num * factor
            if len(str(multiple)) <= 6 and is_anagram(num, multiple):
                count += 1
                if len(examples) < 5:
                    examples.append((num, multiple))
        
        print(f"  Total: {count}")
        print(f"  Examples: {examples}")
        print()

if __name__ == "__main__":
    generate_comprehensive_candidates()
    analyze_known_solutions()
    generate_factor_specific_candidates() 