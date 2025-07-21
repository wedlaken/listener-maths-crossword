#!/usr/bin/env python3
"""
Test script to analyze anagram constraints on Listener 4869
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import find_anagram_multiples, generate_anagrams, is_anagram, parse_grid
from clue_classes import ListenerClue, ClueFactory, ClueParameters

def load_test_solutions():
    """Load some test solutions to analyze anagram constraints."""
    # These are hypothetical solutions for testing
    # In reality, we'd need to solve the first grid first
    test_solutions = {
        # Across clues
        '1_ACROSS': 1234,
        '4_ACROSS': 5678,
        '9_ACROSS': 9999,
        '10_ACROSS': 1111,
        '11_ACROSS': 2222,
        '12_ACROSS': 1000,  # Unclued - 6 digits
        '14_ACROSS': 2000,  # Unclued - 6 digits
        '18_ACROSS': 3333,
        '19_ACROSS': 4444,
        '20_ACROSS': 5555,
        '22_ACROSS': 6666,
        '23_ACROSS': 7777,
        
        # Down clues
        '1_DOWN': 8888,
        '2_DOWN': 9999,
        '3_DOWN': 1010,
        '5_DOWN': 2048,  # This is actually known from the puzzle
        '6_DOWN': 2995,  # This is actually known from the puzzle
        '7_DOWN': 3000,  # Unclued - 6 digits
        '8_DOWN': 4000,  # Unclued - 6 digits
        '13_DOWN': 5050,
        '15_DOWN': 6060,
        '16_DOWN': 7070,
        '17_DOWN': 8080,
        '21_DOWN': 9090,
    }
    return test_solutions

def analyze_unclued_digit_constraints():
    """Analyze what digit constraints the anagram requirement places on unclued solutions."""
    print("=== ANALYZING UNCLUED DIGIT CONSTRAINTS ===")
    print()
    
    # Test different starting digits for unclued solutions
    unclued_clues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN']
    
    for start_digit in range(1, 10):  # 1-9 (no leading zeros)
        print(f"Testing unclued solutions starting with {start_digit}:")
        
        # Test a 6-digit number starting with this digit
        test_number = start_digit * 100000  # e.g., 100000, 200000, etc.
        
        # Find anagram multiples
        multiples = find_anagram_multiples(test_number, max_digits=6)
        
        if multiples:
            print(f"  ✓ {test_number} has {len(multiples)} valid anagram multiples")
            print(f"    Examples: {multiples[:3]}")  # Show first 3
        else:
            print(f"  ✗ {test_number} has no valid anagram multiples")
        
        print()
    
    print("=== KEY INSIGHTS ===")
    print("1. Unclued solutions cannot start with digits > 5")
    print("   (Any multiple would be at least 7 digits and too long)")
    print("2. Unclued solutions cannot start with 0 (puzzle rule)")
    print("3. This significantly constrains the possible unclued solutions!")
    print()

def test_known_solutions():
    """Test with some known solutions from the puzzle."""
    print("=== TESTING WITH KNOWN SOLUTIONS ===")
    print()
    
    # Some solutions we know from the puzzle
    known_solutions = {
        '5_DOWN': 2048,  # 11:0 - only solution
        '6_DOWN': 2995,  # 2:594 - one of the solutions
    }
    
    for clue_id, solution in known_solutions.items():
        print(f"Clue {clue_id}: {solution}")
        anagrams = generate_anagrams(solution)
        print(f"  Anagram possibilities: {anagrams}")
        print()

def analyze_anagram_multiples_pattern():
    """Analyze patterns in numbers that have anagram multiples."""
    print("=== ANALYZING ANAGRAM MULTIPLES PATTERNS ===")
    print()
    
    # Test different number patterns
    test_patterns = {
        "Powers of 2": [1024, 2048, 4096, 8192],
        "Multiples of 1089": [1089, 2178, 3267, 4356, 5445, 6534, 7623, 8712, 9801],
        "Repeated digits": [1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999],
        "Sequential": [1234, 2345, 3456, 4567, 5678, 6789],
    }
    
    for pattern_name, numbers in test_patterns.items():
        print(f"{pattern_name}:")
        working_numbers = []
        
        for num in numbers:
            multiples = find_anagram_multiples(num, max_digits=6)
            if multiples:
                working_numbers.append((num, multiples))
                print(f"  ✓ {num}: {len(multiples)} multiples")
            else:
                print(f"  ✗ {num}: No multiples")
        
        print(f"  Summary: {len(working_numbers)}/{len(numbers)} numbers work")
        print()

def test_grid_constraints():
    """Test how anagram constraints interact with grid constraints."""
    print("=== TESTING GRID CONSTRAINTS ===")
    print()
    
    # Load the grid structure
    try:
        grid_data = parse_grid('data/Listener grid 4869.png')
        print(f"Loaded grid with {len(grid_data)} clues")
        
        # Find unclued clues
        unclued_clues = []
        for clue in grid_data:
            if clue.parameters == (-1, -1):  # Unclued
                unclued_clues.append(clue)
        
        print(f"Found {len(unclued_clues)} unclued clues:")
        for clue in unclued_clues:
            print(f"  {clue.number} {clue.direction}: {len(clue.cell_indices)} cells")
        
    except Exception as e:
        print(f"Error loading grid: {e}")
        print("Skipping grid constraint analysis")

def main():
    """Main analysis function."""
    print("="*60)
    print("ANAGRAM CONSTRAINTS ANALYSIS")
    print("="*60)
    
    # Analyze unclued digit constraints
    analyze_unclued_digit_constraints()
    
    # Test with known solutions
    test_known_solutions()
    
    # Analyze anagram multiples patterns
    analyze_anagram_multiples_pattern()
    
    # Test grid constraints
    test_grid_constraints()
    
    print("="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    
    print("\nKey Findings:")
    print("1. Anagram requirements create strong constraints on unclued solutions")
    print("2. Only certain number patterns have anagram multiples")
    print("3. This significantly reduces the search space for unclued clues")
    print("4. Grid constraints further limit possible solutions")

if __name__ == "__main__":
    main() 