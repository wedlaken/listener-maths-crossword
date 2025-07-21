#!/usr/bin/env python3
"""
Simple test script for anagram functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import find_anagram_multiples, generate_anagrams

def test_anagram_functions():
    """Test basic anagram functionality."""
    print("Testing anagram functions...")
    
    # Test find_anagram_multiples
    test_number = 142857
    multiples = find_anagram_multiples(test_number)
    print(f"Anagram multiples of {test_number}: {multiples}")
    
    # Test generate_anagrams
    test_number = 123
    anagrams = generate_anagrams(test_number)
    print(f"Anagrams of {test_number}: {anagrams}")

if __name__ == "__main__":
    test_anagram_functions() 