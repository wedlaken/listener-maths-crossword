#!/usr/bin/env python3
"""Analyze the actual solutions from the prize-winning puzzle"""

from anagram_grid_solver import find_anagram_multiples, generate_anagrams_including_original, is_anagram

def analyze_actual_solutions():
    """Analyze the actual unclued solutions from the prize-winning puzzle."""
    print("=== ACTUAL SOLUTIONS FROM PRIZE-WINNING PUZZLE ===")
    print()
    
    # Actual solutions from the prize-winning puzzle
    # Format: (initial_grid_solution, final_grid_solution, multiple_factor)
    actual_solutions = {
        '12_ACROSS': {
            'initial': 167982,
            'final': 671928,
            'multiple_factor': 671928 / 167982
        },
        '14_ACROSS': {
            'initial': 428571,  # This is what we need to find in initial grid
            'final': 857142,    # This is what we see in final grid
            'multiple_factor': 857142 / 428571
        },
        '7_DOWN': {
            'initial': 137241,  # This is what we need to find in initial grid
            'final': 411723,    # This is what we see in final grid
            'multiple_factor': 411723 / 137241
        },
        '8_DOWN': {
            'initial': 119883,  # This is what we need to find in initial grid
            'final': 839181,    # This is what we see in final grid
            'multiple_factor': 839181 / 119883
        }
    }
    
    for clue_id, data in actual_solutions.items():
        print(f"{clue_id}:")
        print(f"  Initial Grid: {data['initial']}")
        print(f"  Final Grid: {data['final']}")
        print(f"  Multiple factor: {data['multiple_factor']}")
        
        # Check if final is an anagram of initial
        if is_anagram(data['initial'], data['final']):
            print(f"  ✓ Final is an anagram of initial")
        else:
            print(f"  ✗ Final is NOT an anagram of initial")
        
        # Check if final is a multiple of initial
        if data['final'] % data['initial'] == 0:
            print(f"  ✓ Final is a multiple of initial")
        else:
            print(f"  ✗ Final is NOT a multiple of initial")
        
        # Check if initial has anagram multiples
        multiples = find_anagram_multiples(data['initial'], max_digits=6)
        print(f"  Anagram multiples of initial: {multiples}")
        
        print()

def analyze_7d_solution():
    """Analyze the 7D solution specifically."""
    print("=== 7D SOLUTION ANALYSIS ===")
    print()
    
    initial_7d = 137241
    final_7d = 411723
    multiple_factor = 3
    
    print(f"7D Initial: {initial_7d}")
    print(f"7D Final: {final_7d}")
    print(f"Multiple factor: {multiple_factor}")
    print(f"Verification: {initial_7d} × {multiple_factor} = {initial_7d * multiple_factor}")
    print(f"Matches final: {initial_7d * multiple_factor == final_7d}")
    
    # Check if final is an anagram of initial
    if is_anagram(initial_7d, final_7d):
        print("✓ Final is an anagram of initial")
    else:
        print("✗ Final is NOT an anagram of initial")
    
    # Check all anagrams of initial
    anagrams = generate_anagrams_including_original(initial_7d)
    print(f"All anagrams of {initial_7d}: {anagrams}")
    
    # Check if final appears in anagrams
    if final_7d in anagrams:
        print(f"✓ {final_7d} is an anagram of {initial_7d}")
    else:
        print(f"✗ {final_7d} is NOT an anagram of {initial_7d}")
    
    print()

def analyze_special_properties():
    """Analyze special properties of the actual solutions."""
    print("=== SPECIAL PROPERTIES ANALYSIS ===")
    print()
    
    solutions = [167982, 857142, 411723, 839181]
    
    for solution in solutions:
        print(f"Solution: {solution}")
        
        # Check for palindromic properties
        solution_str = str(solution)
        is_palindrome = solution_str == solution_str[::-1]
        print(f"  Palindrome: {is_palindrome}")
        
        # Check for repeated patterns
        unique_digits = len(set(solution_str))
        print(f"  Unique digits: {unique_digits}/6")
        
        # Check for symmetric patterns
        first_half = solution_str[:3]
        second_half = solution_str[3:]
        is_symmetric = first_half == second_half[::-1]
        print(f"  Symmetric halves: {is_symmetric}")
        
        # Check for mathematical properties
        print(f"  Divisible by 9: {solution % 9 == 0}")
        print(f"  Divisible by 11: {solution % 11 == 0}")
        
        # Check all anagrams
        anagrams = generate_anagrams_including_original(solution)
        print(f"  Total anagrams: {len(anagrams)}")
        
        print()

def analyze_14a_solution():
    """Analyze the 14A solution specifically."""
    print("=== 14A SOLUTION ANALYSIS ===")
    print()
    
    initial_14a = 428571
    final_14a = 857142
    multiple_factor = 2
    
    print(f"14A Initial: {initial_14a}")
    print(f"14A Final: {final_14a}")
    print(f"Multiple factor: {multiple_factor}")
    print(f"Verification: {initial_14a} × {multiple_factor} = {initial_14a * multiple_factor}")
    print(f"Matches final: {initial_14a * multiple_factor == final_14a}")
    
    # Check if final is an anagram of initial
    if is_anagram(initial_14a, final_14a):
        print("✓ Final is an anagram of initial")
    else:
        print("✗ Final is NOT an anagram of initial")
    
    # Check all anagrams of initial
    anagrams = generate_anagrams_including_original(initial_14a)
    print(f"All anagrams of {initial_14a}: {anagrams}")
    
    # Check if final appears in anagrams
    if final_14a in anagrams:
        print(f"✓ {final_14a} is an anagram of {initial_14a}")
    else:
        print(f"✗ {final_14a} is NOT an anagram of {initial_14a}")
    
    print()

def analyze_8d_solution():
    """Analyze the 8D solution specifically."""
    print("=== 8D SOLUTION ANALYSIS ===")
    print()
    
    initial_8d = 119883
    final_8d = 839181
    multiple_factor = 7
    
    print(f"8D Initial: {initial_8d}")
    print(f"8D Final: {final_8d}")
    print(f"Multiple factor: {multiple_factor}")
    print(f"Verification: {initial_8d} × {multiple_factor} = {initial_8d * multiple_factor}")
    print(f"Matches final: {initial_8d * multiple_factor == final_8d}")
    
    # Check if final is an anagram of initial
    if is_anagram(initial_8d, final_8d):
        print("✓ Final is an anagram of initial")
    else:
        print("✗ Final is NOT an anagram of initial")
    
    # Check all anagrams of initial
    anagrams = generate_anagrams_including_original(initial_8d)
    print(f"All anagrams of {initial_8d}: {anagrams}")
    
    # Check if final appears in anagrams
    if final_8d in anagrams:
        print(f"✓ {final_8d} is an anagram of {initial_8d}")
    else:
        print(f"✗ {final_8d} is NOT an anagram of {initial_8d}")
    
    print()

def revise_understanding():
    """Revise our understanding of the anagram grid requirements."""
    print("=== CORRECTED UNDERSTANDING ===")
    print()
    
    print("CORRECT understanding:")
    print("1. Initial Grid: Solve the 8x8 grid with prime factor constraints")
    print("2. Final Grid: Transform to anagram grid where:")
    print("   - All solutions become anagrams of themselves")
    print("   - Unclued solutions in FINAL grid are multiples of unclued solutions in INITIAL grid")
    print()
    
    print("Actual solutions show:")
    print("1. 12A: 167982 (initial) → 671928 (final, ×4)")
    print("2. 14A: 428571 (initial) → 857142 (final, ×2)")
    print("3. 7D: 137241 (initial) → 411723 (final, ×3)")
    print("4. 8D: 119883 (initial) → 839181 (final, ×7)")
    print()
    
    print("Key insights:")
    print("- We need to find unclued solutions for the INITIAL grid")
    print("- These solutions must have anagram multiples (for the final grid)")
    print("- The multiple factors are: 1, 2, 3, 4, 7, and possibly others")
    print("- This means our search space is still constrained but larger than we thought")

def generate_corrected_candidates():
    """Generate candidates based on the corrected understanding."""
    print("=== CORRECTED CANDIDATE GENERATION ===")
    print()
    
    print("New criteria for unclued solutions in INITIAL grid:")
    print("1. Must be 6 digits")
    print("2. Cannot start with 0")
    print("3. Must have anagram multiples (for final grid)")
    print("4. Multiple factors we know exist: 1, 2, 3, 4, 7")
    print("5. The anagram multiple must be ≤ 6 digits")
    print()
    
    print("This means we need to find 6-digit numbers that have anagram multiples")
    print("with factors like 1, 2, 3, 4, 7, etc., where the multiple is also ≤ 6 digits.")

if __name__ == "__main__":
    analyze_actual_solutions()
    analyze_7d_solution()
    analyze_14a_solution()
    analyze_8d_solution()
    analyze_special_properties()
    revise_understanding()
    generate_corrected_candidates() 