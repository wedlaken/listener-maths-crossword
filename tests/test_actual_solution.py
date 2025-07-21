#!/usr/bin/env python3
"""
Test script to verify actual puzzle solutions using anagram functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import find_anagram_multiples, generate_anagrams_including_original, is_anagram

def test_actual_solutions():
    """Test with actual puzzle solutions."""
    print("=== Testing Actual Puzzle Solutions ===")
    
    # Known solutions from the puzzle
    known_solutions = {
        '1A': 1089,
        '2D': 2048,
        '3D': 2178,
        '4A': 142857,
        '5A': 7776,
        '6D': 285714
    }
    
    print("Known solutions:")
    for clue, solution in known_solutions.items():
        print(f"  {clue}: {solution}")
    
    print("\n=== Testing Anagram Relationships ===")
    
    # Test anagram relationships between known solutions
    for clue1, solution1 in known_solutions.items():
        for clue2, solution2 in known_solutions.items():
            if clue1 != clue2 and is_anagram(solution1, solution2):
                print(f"  {clue1} ({solution1}) and {clue2} ({solution2}) are anagrams")
    
    print("\n=== Testing Anagram Multiples ===")
    
    # Test anagram multiples for each solution
    for clue, solution in known_solutions.items():
        multiples = find_anagram_multiples(solution)
        if multiples:
            print(f"  {clue} ({solution}) has {len(multiples)} anagram multiples: {multiples}")
        else:
            print(f"  {clue} ({solution}) has no anagram multiples")
    
    print("\n=== Testing All Anagrams ===")
    
    # Test all anagrams for each solution
    for clue, solution in known_solutions.items():
        all_anagrams = generate_anagrams_including_original(solution)
        print(f"  {clue} ({solution}) has {len(all_anagrams)} total anagrams")
        print(f"    First 5: {all_anagrams[:5]}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_actual_solutions() 