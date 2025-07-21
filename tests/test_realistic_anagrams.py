#!/usr/bin/env python3
"""
Test script to find realistic numbers with anagram multiples
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import find_anagram_multiples, generate_anagrams, is_anagram

def find_numbers_with_anagram_multiples():
    """Find numbers that actually have anagram multiples."""
    print("=== FINDING NUMBERS WITH ANAGRAM MULTIPLES ===")
    print()
    
    # Test various number patterns
    test_categories = {
        "Powers of 2": [1024, 2048, 4096, 8192],
        "Powers of 10": [1000, 2000, 3000, 4000, 5000],
        "Repeated digits": [1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999],
        "Palindromic": [1001, 2002, 3003, 4004, 5005, 6006, 7007, 8008, 9009],
        "Sequential": [1234, 2345, 3456, 4567, 5678, 6789],
        "Small numbers": [12, 24, 36, 48, 60, 72, 84, 96],
        "Known solutions": [2048, 2995],  # From the puzzle
    }
    
    found_multiples = {}
    
    for category, numbers in test_categories.items():
        print(f"{category}:")
        for num in numbers:
            multiples = find_anagram_multiples(num, max_digits=6)
            if multiples:
                print(f"  {num}: {len(multiples)} multiples - {multiples}")
                found_multiples[num] = multiples
            else:
                print(f"  {num}: No valid multiples")
        print()
    
    return found_multiples

def test_specific_patterns():
    """Test specific patterns that might work."""
    print("=== TESTING SPECIFIC PATTERNS ===")
    print()
    
    # Test numbers with repeated digits that might have multiples
    test_numbers = [
        1089,  # 33^2
        2178,  # 1089 * 2
        3267,  # 1089 * 3
        4356,  # 1089 * 4
        5445,  # 1089 * 5
        6534,  # 1089 * 6
        7623,  # 1089 * 7
        8712,  # 1089 * 8
        9801,  # 1089 * 9
    ]
    
    for num in test_numbers:
        multiples = find_anagram_multiples(num, max_digits=6)
        if multiples:
            print(f"{num}: {len(multiples)} multiples - {multiples}")
        else:
            print(f"{num}: No valid multiples")
    
    print()

def analyze_unclued_constraints():
    """Analyze what this means for unclued solutions."""
    print("=== UNCLUED SOLUTION CONSTRAINTS ===")
    print()
    
    # Based on the findings, what constraints can we derive?
    print("Key Insights:")
    print("1. Most simple numbers (1000, 2000, etc.) don't have anagram multiples")
    print("2. Numbers with anagram multiples are often:")
    print("   - Powers of 2 (1024, 2048, 4096)")
    print("   - Multiples of 1089 (1089, 2178, 3267, etc.)")
    print("   - Numbers with specific digit patterns")
    print()
    print("3. For unclued solutions to work in the anagram grid:")
    print("   - They must have at least one anagram that is a multiple")
    print("   - The anagram must be ≤ 6 digits")
    print("   - The original must not start with 0")
    print("   - The original must not start with digits > 5")
    print()
    print("4. This significantly constrains possible unclued solutions!")
    print("   - They must be numbers with anagram multiples")
    print("   - They must fit the grid constraints")
    print("   - They must not conflict with crossing clues")
    print()

def test_6_digit_numbers():
    """Test 6-digit numbers that might work for unclued clues."""
    print("=== TESTING 6-DIGIT NUMBERS FOR UNCLUED CLUES ===")
    print()
    
    # Test some 6-digit numbers that might have anagram multiples
    test_numbers = [
        100000,  # Simple case
        142857,  # Cyclic number
        108900,  # Multiple of 1089
        217800,  # Multiple of 1089
        102400,  # Power of 2
        204800,  # Power of 2
    ]
    
    for num in test_numbers:
        multiples = find_anagram_multiples(num, max_digits=6)
        if multiples:
            print(f"{num}: {len(multiples)} multiples - {multiples}")
        else:
            print(f"{num}: No valid multiples")
    
    print()

def main():
    """Main test function."""
    print("="*60)
    print("REALISTIC ANAGRAM MULTIPLES TEST")
    print("="*60)
    
    # Find numbers with anagram multiples
    found_multiples = find_numbers_with_anagram_multiples()
    
    # Test specific patterns
    test_specific_patterns()
    
    # Test 6-digit numbers
    test_6_digit_numbers()
    
    # Analyze constraints
    analyze_unclued_constraints()
    
    print("="*60)
    print("TEST COMPLETE")
    print("="*60)
    
    # Summary
    print(f"\nSummary: Found {len(found_multiples)} numbers with anagram multiples")
    for num, multiples in found_multiples.items():
        print(f"  {num}: {len(multiples)} multiples")

if __name__ == "__main__":
    main() 