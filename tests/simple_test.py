#!/usr/bin/env python3
"""Simple test for anagram functions"""

from anagram_grid_solver import find_anagram_multiples, generate_anagrams

print("Testing anagram functions...")

# Test 1089 (known to have anagram multiples)
print(f"1089 anagrams: {generate_anagrams(1089)}")
print(f"1089 anagram multiples: {find_anagram_multiples(1089)}")

# Test 2048 (from the puzzle)
print(f"2048 anagrams: {generate_anagrams(2048)}")
print(f"2048 anagram multiples: {find_anagram_multiples(2048)}")

# Test 2178 (should be a multiple of 1089)
print(f"2178 anagrams: {generate_anagrams(2178)}")
print(f"2178 anagram multiples: {find_anagram_multiples(2178)}")

print("Done!") 