#!/usr/bin/env python3
"""
Anagram Grid Solver for Listener 4869
Handles the second stage of the puzzle where all solutions become anagrams
and unclued solutions must be multiples of their original values.
"""

import itertools
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict

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

def find_valid_anagram_combinations(original_solutions: Dict[str, int]) -> List[Dict[str, int]]:
    """
    Find all valid combinations of anagram solutions.
    
    Args:
        original_solutions: Dict mapping clue_id to original solution
    
    Returns:
        List of valid anagram solution dictionaries
    """
    valid_combinations = []
    
    # Separate clued and unclued clues
    clued_clues = []
    unclued_clues = []
    
    for clue_id, original in original_solutions.items():
        if clue_id in ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN']:
            unclued_clues.append((clue_id, original))
        else:
            clued_clues.append((clue_id, original))
    
    # Generate all possible anagrams for clued clues
    clued_anagram_options = {}
    for clue_id, original in clued_clues:
        anagrams = generate_anagrams(original)
        clued_anagram_options[clue_id] = anagrams
    
    # Generate all possible anagrams for unclued clues (must be multiples)
    unclued_anagram_options = {}
    for clue_id, original in unclued_clues:
        multiples = find_anagram_multiples(original, max_digits=6)
        unclued_anagram_options[clue_id] = multiples
    
    # Generate all combinations
    def generate_combinations(clued_assignments, unclued_assignments):
        """Recursively generate valid combinations."""
        if len(clued_assignments) == len(clued_clues) and len(unclued_assignments) == len(unclued_clues):
            # Complete assignment - check for uniqueness
            all_numbers = set(original_solutions.values())
            all_numbers.update(clued_assignments.values())
            all_numbers.update(unclued_assignments.values())
            
            if len(all_numbers) == len(original_solutions) + len(clued_assignments) + len(unclued_assignments):
                # All numbers are unique
                complete_assignment = {**clued_assignments, **unclued_assignments}
                valid_combinations.append(complete_assignment)
            return
        
        # Try next clued clue
        if len(clued_assignments) < len(clued_clues):
            clue_id, original = clued_clues[len(clued_assignments)]
            for anagram in clued_anagram_options[clue_id]:
                # Check if this anagram conflicts with current assignments
                conflicts = False
                for assigned_anagram in list(clued_assignments.values()) + list(unclued_assignments.values()):
                    if anagram == assigned_anagram:
                        conflicts = True
                        break
                
                if not conflicts:
                    new_clued = {**clued_assignments, clue_id: anagram}
                    generate_combinations(new_clued, unclued_assignments)
        
        # Try next unclued clue
        elif len(unclued_assignments) < len(unclued_clues):
            clue_id, original = unclued_clues[len(unclued_assignments)]
            for anagram in unclued_anagram_options[clue_id]:
                # Check if this anagram conflicts with current assignments
                conflicts = False
                for assigned_anagram in list(clued_assignments.values()) + list(unclued_assignments.values()):
                    if anagram == assigned_anagram:
                        conflicts = True
                        break
                
                if not conflicts:
                    new_unclued = {**unclued_assignments, clue_id: anagram}
                    generate_combinations(clued_assignments, new_unclued)
    
    generate_combinations({}, {})
    return valid_combinations

def analyze_unclued_constraints(original_solutions: Dict[str, int]) -> Dict[str, List[int]]:
    """
    Analyze what constraints the anagram requirement places on unclued solutions.
    
    Args:
        original_solutions: Dict mapping clue_id to original solution (including unclued)
    
    Returns:
        Dict mapping unclued clue_id to list of valid original solutions
    """
    unclued_clues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN']
    constraints = {}
    
    for clue_id in unclued_clues:
        if clue_id in original_solutions:
            original = original_solutions[clue_id]
            multiples = find_anagram_multiples(original, max_digits=6)
            
            if multiples:
                constraints[clue_id] = [original]  # This original value works
            else:
                constraints[clue_id] = []  # This original value doesn't work
    
    return constraints

def find_anagram_grid_solutions(original_grid: Dict[str, int]) -> Tuple[List[Dict[str, int]], Dict[str, List[int]]]:
    """
    Find all valid anagram grid solutions and analyze constraints.
    
    Args:
        original_grid: Complete original grid solutions
    
    Returns:
        Tuple of (valid_anagram_combinations, unclued_constraints)
    """
    # Find all valid anagram combinations
    valid_combinations = find_valid_anagram_combinations(original_grid)
    
    # Analyze constraints on unclued solutions
    unclued_constraints = analyze_unclued_constraints(original_grid)
    
    return valid_combinations, unclued_constraints

def print_anagram_analysis(original_solutions: Dict[str, int]):
    """Print detailed analysis of anagram possibilities."""
    print("=== ANAGRAM GRID ANALYSIS ===")
    print()
    
    # Analyze each clue
    for clue_id, original in sorted(original_solutions.items()):
        print(f"Clue {clue_id}: {original}")
        
        if clue_id in ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN']:
            # Unclued clue
            multiples = find_anagram_multiples(original, max_digits=6)
            if multiples:
                print(f"  ✓ Valid anagram multiples: {multiples}")
            else:
                print(f"  ✗ No valid anagram multiples found!")
        else:
            # Clued clue
            anagrams = generate_anagrams(original)
            print(f"  Anagram possibilities: {anagrams}")
        
        print()
    
    # Find all valid combinations
    print("=== FINDING VALID COMBINATIONS ===")
    valid_combinations, unclued_constraints = find_anagram_grid_solutions(original_solutions)
    
    print(f"Found {len(valid_combinations)} valid anagram grid combinations")
    print()
    
    if valid_combinations:
        print("Sample valid combination:")
        sample = valid_combinations[0]
        for clue_id, anagram in sorted(sample.items()):
            original = original_solutions[clue_id]
            print(f"  {clue_id}: {original} → {anagram}")
    
    print()
    print("=== UNCLUED CONSTRAINT ANALYSIS ===")
    for clue_id, valid_originals in unclued_constraints.items():
        if valid_originals:
            print(f"{clue_id}: ✓ Original value {valid_originals[0]} works")
        else:
            print(f"{clue_id}: ✗ Original value {original_solutions[clue_id]} has no valid anagram multiples")

if __name__ == "__main__":
    # Test with some sample data
    test_solutions = {
        '1_ACROSS': 1234,
        '4_ACROSS': 5678,
        '12_ACROSS': 1000,  # Unclued
        '14_ACROSS': 2000,  # Unclued
        '1_DOWN': 1111,
        '7_DOWN': 3000,     # Unclued
        '8_DOWN': 4000,     # Unclued
    }
    
    print_anagram_analysis(test_solutions) 