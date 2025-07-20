#!/usr/bin/env python3
"""
Utility functions shared across the Listener Maths Crossword Solver project.
"""

import itertools
from typing import Dict, List, Tuple, Set, Optional

def is_anagram(num1: int, num2: int) -> bool:
    """Check if two numbers are anagrams (same digits, different order)."""
    digits1 = sorted(str(num1))
    digits2 = sorted(str(num2))
    return digits1 == digits2

def generate_anagrams(number: int) -> List[int]:
    """Generate all possible anagrams of a number."""
    digits = list(str(number))
    anagrams = set()
    
    for perm in itertools.permutations(digits):
        if perm[0] != '0':  # No leading zeros
            anagram = int(''.join(perm))
            if anagram != number:  # Exclude the original number
                anagrams.add(anagram)
    
    return sorted(list(anagrams))

def generate_anagrams_including_original(number: int) -> List[int]:
    """Generate all possible anagrams of a number, including the original."""
    digits = list(str(number))
    anagrams = set()
    
    for perm in itertools.permutations(digits):
        if perm[0] != '0':  # No leading zeros
            anagram = int(''.join(perm))
            anagrams.add(anagram)
    
    return sorted(list(anagrams))

def find_anagram_multiples(original: int, max_digits: int = 6) -> List[int]:
    """
    Find all anagrams of a number that are also multiples of it.
    
    Args:
        original: The original number
        max_digits: Maximum number of digits allowed (default 6)
    
    Returns:
        List of anagrams that are multiples of the original number
    """
    anagrams = generate_anagrams_including_original(original)
    multiples = []
    
    for anagram in anagrams:
        if len(str(anagram)) <= max_digits and anagram % original == 0 and anagram != original:
            multiples.append(anagram)
    
    return multiples

def validate_anagram_constraints(original_solutions: Dict[str, int], 
                                anagram_solutions: Dict[str, int]) -> List[str]:
    """
    Validate that anagram solutions meet all constraints.
    
    Args:
        original_solutions: Dict mapping clue_id to original solution
        anagram_solutions: Dict mapping clue_id to anagram solution
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    all_numbers = set()
    
    # Check all original solutions
    for clue_id, solution in original_solutions.items():
        if solution in all_numbers:
            errors.append(f"Duplicate number {solution} in original grid (clue {clue_id})")
        all_numbers.add(solution)
    
    # Check all anagram solutions
    for clue_id, anagram in anagram_solutions.items():
        if anagram in all_numbers:
            errors.append(f"Duplicate number {anagram} in anagram grid (clue {clue_id})")
        all_numbers.add(anagram)
        
        # Check if it's an anagram of the original
        original = original_solutions.get(clue_id)
        if original and not is_anagram(original, anagram):
            errors.append(f"Anagram {anagram} is not an anagram of original {original} (clue {clue_id})")
        
        # Check unclued constraints
        if clue_id in ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN']:  # Unclued clues
            if original and anagram % original != 0:
                errors.append(f"Anagram {anagram} is not a multiple of original {original} (unclued clue {clue_id})")
            if len(str(anagram)) > 6:
                errors.append(f"Anagram {anagram} is too long (unclued clue {clue_id})")
    
    return errors 