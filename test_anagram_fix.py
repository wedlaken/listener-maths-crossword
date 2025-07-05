#!/usr/bin/env python3
"""
Test script to verify anagram generation fix for duplicate permutations.
"""

from interactive_solver import generate_anagram_solutions_for_clue

def test_anagram_generation():
    """Test anagram generation for various cases."""
    
    print("=== Testing Anagram Generation Fix ===")
    
    # Test case 1: 3D = 7776 (should have 4 anagrams, not 18)
    print("\n1. Testing 3D = 7776:")
    anagrams_7776 = generate_anagram_solutions_for_clue(7776, 4, False)
    print(f"   Original: 7776")
    print(f"   Expected: 4 anagrams (4! / 3! = 4, since 3 identical 7s)")
    print(f"   Actual: {len(anagrams_7776)} anagrams")
    print(f"   Anagrams: {anagrams_7776}")
    
    # Test case 2: 2-digit number
    print("\n2. Testing 2-digit number (35):")
    anagrams_35 = generate_anagram_solutions_for_clue(35, 2, False)
    print(f"   Original: 35")
    print(f"   Expected: 1 anagram (53)")
    print(f"   Actual: {len(anagrams_35)} anagrams")
    print(f"   Anagrams: {anagrams_35}")
    
    # Test case 3: Number with no duplicates (1234)
    print("\n3. Testing 4-digit number with no duplicates (1234):")
    anagrams_1234 = generate_anagram_solutions_for_clue(1234, 4, False)
    print(f"   Original: 1234")
    print(f"   Expected: 23 anagrams (4! - 1 = 23, excluding original)")
    print(f"   Actual: {len(anagrams_1234)} anagrams")
    print(f"   First 5 anagrams: {anagrams_1234[:5]}")
    
    # Test case 4: Number with some duplicates (1123)
    print("\n4. Testing 4-digit number with some duplicates (1123):")
    anagrams_1123 = generate_anagram_solutions_for_clue(1123, 4, False)
    print(f"   Original: 1123")
    print(f"   Expected: 11 anagrams (4! / 2! - 1 = 11, since 2 identical 1s)")
    print(f"   Actual: {len(anagrams_1123)} anagrams")
    print(f"   Anagrams: {anagrams_1123}")
    
    # Test case 5: Unclued 6-digit number (142857)
    print("\n5. Testing unclued 6-digit number (142857):")
    anagrams_142857 = generate_anagram_solutions_for_clue(142857, 6, True)
    print(f"   Original: 142857")
    print(f"   Expected: Multiples that are anagrams")
    print(f"   Actual: {len(anagrams_142857)} anagrams")
    print(f"   First 5 anagrams: {anagrams_142857[:5]}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_anagram_generation() 