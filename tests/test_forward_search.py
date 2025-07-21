#!/usr/bin/env python3
"""Test forward search algorithm"""

from utils import is_anagram

def test_forward_search():
    """Test that forward search finds known solutions."""
    print("=== TESTING FORWARD SEARCH ===")
    print()
    
    # Known solutions and their factors
    known_solutions = [
        (167982, 4),  # 12A
        (428571, 2),  # 14A  
        (137241, 3),  # 7D
        (119883, 7)   # 8D
    ]
    
    def find_anagram_multiples(number):
        """Find all anagram multiples of a number."""
        multiples = []
        for factor in range(1, 10):
            multiple = number * factor
            if len(str(multiple)) <= 6 and is_anagram(number, multiple):
                multiples.append((factor, multiple))
        return multiples
    
    print("Testing known solutions:")
    for number, expected_factor in known_solutions:
        multiples = find_anagram_multiples(number)
        found_factors = [factor for factor, _ in multiples]
        
        print(f"{number}:")
        print(f"  Expected factor: {expected_factor}")
        print(f"  Found multiples: {multiples}")
        
        if expected_factor in found_factors:
            print(f"  ✓ Factor {expected_factor} found")
        else:
            print(f"  ✗ Factor {expected_factor} NOT found")
        print()
    
    print("Forward search test complete!")

if __name__ == "__main__":
    test_forward_search() 