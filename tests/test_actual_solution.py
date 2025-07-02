#!/usr/bin/env python3
"""Test the actual solution from the prize-winning puzzle"""

from anagram_grid_solver import find_anagram_multiples, generate_anagrams_including_original

def test_actual_solution():
    """Test the actual solution 167982."""
    print("=== TESTING ACTUAL SOLUTION ===")
    
    # The actual solution from the prize-winning puzzle
    actual_solution = 167982
    anagram_multiple = 671928
    
    print(f"Actual solution: {actual_solution}")
    print(f"Anagram multiple: {anagram_multiple}")
    print(f"Multiple factor: {anagram_multiple / actual_solution}")
    
    # Test our anagram functions
    print(f"\nAll anagrams of {actual_solution}:")
    anagrams = generate_anagrams_including_original(actual_solution)
    print(f"Found {len(anagrams)} anagrams: {anagrams}")
    
    print(f"\nAnagram multiples of {actual_solution}:")
    multiples = find_anagram_multiples(actual_solution, max_digits=6)
    print(f"Found {len(multiples)} multiples: {multiples}")
    
    # Check if 671928 is in the anagrams
    if anagram_multiple in anagrams:
        print(f"✓ {anagram_multiple} is an anagram of {actual_solution}")
    else:
        print(f"✗ {anagram_multiple} is NOT an anagram of {actual_solution}")
    
    # Check if it's a multiple
    if anagram_multiple % actual_solution == 0:
        print(f"✓ {anagram_multiple} is a multiple of {actual_solution}")
    else:
        print(f"✗ {anagram_multiple} is NOT a multiple of {actual_solution}")

def test_constraints():
    """Test the constraints you mentioned."""
    print("\n=== TESTING CONSTRAINTS ===")
    
    # Known solutions
    clue_5d = 2048  # 11:0 constraint
    clue_3d = 7776  # 10:1 constraint
    
    print(f"5D = {clue_5d}")
    print(f"3D = {clue_3d}")
    
    # 12A constraints based on crossing clues
    # 12A is 6 digits: _ _ _ _ _ _
    # 5D crosses at position 1 (second digit): 6
    # 3D crosses at position 4 (fifth digit): 8
    
    print(f"12A constraints: _ 6 _ _ 8 _")
    
    # Test if 167982 fits these constraints
    solution_12a = 167982
    solution_str = str(solution_12a)
    
    print(f"12A solution: {solution_str}")
    print(f"Second digit (from 5D): {solution_str[1]} (should be 6)")
    print(f"Fifth digit (from 3D): {solution_str[4]} (should be 8)")
    
    if solution_str[1] == '6' and solution_str[4] == '8':
        print("✓ 167982 fits the grid constraints!")
    else:
        print("✗ 167982 does NOT fit the grid constraints")

def analyze_why_we_missed_it():
    """Analyze why our search missed this solution."""
    print("\n=== ANALYZING WHY WE MISSED IT ===")
    
    actual_solution = 167982
    
    # Check our search criteria
    print(f"Actual solution: {actual_solution}")
    print(f"Starts with digit: {str(actual_solution)[0]} (should be ≤ 5)")
    print(f"Length: {len(str(actual_solution))} digits")
    
    # Check if it has anagram multiples
    multiples = find_anagram_multiples(actual_solution, max_digits=6)
    print(f"Anagram multiples: {multiples}")
    
    # Check our search strategy
    print("\nOur search strategy:")
    print("1. Repeated digits (111111, 222222, etc.)")
    print("2. Powers of 2 (102400, 204800, etc.)")
    print("3. Multiples of 1089")
    print("4. Palindromic numbers")
    print("5. Systematic search (every 100th number)")
    
    print(f"\n167982 analysis:")
    print(f"- Repeated digits: {len(set(str(actual_solution))) == 1}")
    print(f"- Power of 2: {actual_solution in [102400, 204800, 409600, 819200]}")
    print(f"- Multiple of 1089: {actual_solution % 1089 == 0}")
    print(f"- Palindromic: {str(actual_solution) == str(actual_solution)[::-1]}")
    print(f"- In systematic search: {actual_solution % 100 == 0}")
    
    print("\nThe issue: Our systematic search only checked every 100th number!")
    print("167982 is not divisible by 100, so we missed it.")

if __name__ == "__main__":
    test_actual_solution()
    test_constraints()
    analyze_why_we_missed_it() 