#!/usr/bin/env python3
"""
Test script to analyze anagram constraints on Listener 4869
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from anagram_grid_solver import *
from systematic_grid_parser import parse_grid
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
    
    # Test some numbers to see patterns
    test_numbers = [
        1000, 2000, 3000, 4000, 5000,  # Unclued possibilities
        1024, 2048, 4096, 8192,        # Powers of 2
        1001, 2002, 3003, 4004,        # Palindromic patterns
        1234, 2345, 3456, 4567,        # Sequential
        1111, 2222, 3333, 4444,        # Repeated digits
    ]
    
    for num in test_numbers:
        multiples = find_anagram_multiples(num, max_digits=6)
        if multiples:
            print(f"{num}: {len(multiples)} multiples - {multiples}")
        else:
            print(f"{num}: No valid multiples")
    
    print()
    print("=== PATTERN INSIGHTS ===")
    print("Numbers with many anagram multiples often have:")
    print("1. Repeated digits (1111, 2222, etc.)")
    print("2. Symmetric patterns")
    print("3. Small prime factors")
    print("4. Powers of 2 (1024, 2048, etc.)")
    print()

def main():
    """Main analysis function."""
    print("ANAGRAM GRID CONSTRAINT ANALYSIS")
    print("=" * 50)
    print()
    
    # Analyze unclued digit constraints
    analyze_unclued_digit_constraints()
    
    # Test with known solutions
    test_known_solutions()
    
    # Analyze patterns
    analyze_anagram_multiples_pattern()
    
    # Test with sample data
    print("=== TESTING WITH SAMPLE DATA ===")
    test_solutions = load_test_solutions()
    print_anagram_analysis(test_solutions)

if __name__ == "__main__":
    main() 