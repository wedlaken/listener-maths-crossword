#!/usr/bin/env python3
"""
Test script for AnagramClue class
"""

from clue_classes import ListenerClue, ClueParameters, AnagramClue

def test_anagram_clue():
    """Test the AnagramClue class with various scenarios."""
    
    print("=== Testing AnagramClue Class ===\n")
    
    # Test 1: Length 2 clued clue (should have 1 anagram)
    print("Test 1: Length 2 clued clue")
    clue_params = ClueParameters(a=2, b=2, c=1, is_unclued=False)
    original_clue = ListenerClue(number=1, direction="ACROSS", cell_indices=(0, 1), parameters=clue_params)
    original_clue.possible_solutions = {12}  # Simulate solved clue
    
    anagram_clue = AnagramClue(original_clue)
    print(f"Original: {anagram_clue.get_original_solution()}")
    print(f"Anagrams: {anagram_clue.get_anagram_solutions()}")
    print(f"Count: {len(anagram_clue.get_anagram_solutions())}")
    print()
    
    # Test 2: Length 4 clued clue (should have up to 23 anagrams)
    print("Test 2: Length 4 clued clue")
    clue_params = ClueParameters(a=4, b=3, c=2, is_unclued=False)
    original_clue = ListenerClue(number=2, direction="DOWN", cell_indices=(0, 8, 16, 24), parameters=clue_params)
    original_clue.possible_solutions = {1234}  # Simulate solved clue
    
    anagram_clue = AnagramClue(original_clue)
    print(f"Original: {anagram_clue.get_original_solution()}")
    anagrams = anagram_clue.get_anagram_solutions()
    print(f"Anagrams: {anagrams[:5]}{'...' if len(anagrams) > 5 else ''}")
    print(f"Count: {len(anagrams)}")
    print()
    
    # Test 3: Length 6 unclued clue (should have multiples only)
    print("Test 3: Length 6 unclued clue")
    clue_params = ClueParameters(a=6, b=-1, c=-1, is_unclued=True)
    original_clue = ListenerClue(number=7, direction="DOWN", cell_indices=(11, 19, 27, 35, 43, 51), parameters=clue_params)
    original_clue.possible_solutions = {142857}  # Famous cyclic number
    
    anagram_clue = AnagramClue(original_clue)
    print(f"Original: {anagram_clue.get_original_solution()}")
    anagrams = anagram_clue.get_anagram_solutions()
    print(f"Anagrams (multiples only): {anagrams}")
    print(f"Count: {len(anagrams)}")
    print()
    
    # Test 4: Another unclued clue with different number
    print("Test 4: Another unclued clue")
    original_clue.possible_solutions = {100000}  # Simple number
    
    anagram_clue = AnagramClue(original_clue)
    print(f"Original: {anagram_clue.get_original_solution()}")
    anagrams = anagram_clue.get_anagram_solutions()
    print(f"Anagrams (multiples only): {anagrams}")
    print(f"Count: {len(anagrams)}")
    print()

if __name__ == "__main__":
    test_anagram_clue() 