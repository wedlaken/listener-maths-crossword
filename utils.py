#!/usr/bin/env python3
"""
Utility functions and centralized import hub for the Listener Maths Crossword Solver project.
This module serves as a single point of access for all shared functions and modules.
"""

import os
import sys
import itertools
from typing import Dict, List, Tuple, Set, Optional

# Add project root to path so imports work from any location
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add archive and experimental folders to path
archive_path = os.path.join(project_root, 'archive')
experimental_path = os.path.join(project_root, 'experimental')
scripts_path = os.path.join(project_root, 'scripts')

for path in [archive_path, experimental_path, scripts_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import commonly used modules
try:
    from archive.systematic_grid_parser import parse_grid, SystematicGridParser, ClueTuple
except ImportError:
    # Fallback if archive module not available
    parse_grid = None
    SystematicGridParser = None
    ClueTuple = None

try:
    from experimental.crossword_solver import ListenerPuzzle, ListenerClue, Clue, CrosswordGrid
except ImportError:
    # Fallback if experimental module not available
    ListenerPuzzle = None
    ListenerClue = None
    Clue = None
    CrosswordGrid = None

try:
    from archive.anagram_grid_solver import (
        find_anagram_multiples, 
        generate_anagrams, 
        generate_anagrams_including_original,
        validate_anagram_constraints
    )
except ImportError:
    # Fallback implementations if archive module not available
    find_anagram_multiples = None
    generate_anagrams = None
    generate_anagrams_including_original = None
    validate_anagram_constraints = None

# Core utility functions
def is_anagram(num1: int, num2: int) -> bool:
    """Check if two numbers are anagrams (same digits, different order)."""
    digits1 = sorted(str(num1))
    digits2 = sorted(str(num2))
    return digits1 == digits2

def generate_anagrams_local(number: int) -> List[int]:
    """Generate all possible anagrams of a number (local implementation)."""
    digits = list(str(number))
    anagrams = set()
    
    for perm in itertools.permutations(digits):
        if perm[0] != '0':  # No leading zeros
            anagram = int(''.join(perm))
            if anagram != number:  # Exclude the original number
                anagrams.add(anagram)
    
    return sorted(list(anagrams))

def generate_anagrams_including_original_local(number: int) -> List[int]:
    """Generate all possible anagrams of a number, including the original (local implementation)."""
    digits = list(str(number))
    anagrams = set()
    
    for perm in itertools.permutations(digits):
        if perm[0] != '0':  # No leading zeros
            anagram = int(''.join(perm))
            anagrams.add(anagram)
    
    return sorted(list(anagrams))

def find_anagram_multiples_local(original: int, max_digits: int = 6) -> List[int]:
    """Find all anagrams of a number that are also multiples of it (local implementation)."""
    anagrams = generate_anagrams_including_original_local(original)
    multiples = []
    
    for anagram in anagrams:
        if len(str(anagram)) <= max_digits and anagram % original == 0 and anagram != original:
            multiples.append(anagram)
    
    return multiples

def validate_anagram_constraints_local(original_solutions: Dict[str, int], 
                                     anagram_solutions: Dict[str, int]) -> List[str]:
    """Validate that anagram solutions meet all constraints (local implementation)."""
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

# Use archive implementations if available, otherwise use local implementations
if find_anagram_multiples is None:
    find_anagram_multiples = find_anagram_multiples_local

if generate_anagrams is None:
    generate_anagrams = generate_anagrams_local

if generate_anagrams_including_original is None:
    generate_anagrams_including_original = generate_anagrams_including_original_local

if validate_anagram_constraints is None:
    validate_anagram_constraints = validate_anagram_constraints_local

# Convenience function to get all available modules
def get_available_modules() -> Dict[str, bool]:
    """Return a dictionary showing which modules are available."""
    return {
        'systematic_grid_parser': SystematicGridParser is not None,
        'crossword_solver': ListenerPuzzle is not None,
        'anagram_grid_solver': find_anagram_multiples is not None,
    }

# Convenience function to check if running from a specific folder
def is_running_from_folder(folder_name: str) -> bool:
    """Check if the current script is running from a specific folder."""
    current_dir = os.path.basename(os.getcwd())
    return current_dir == folder_name 