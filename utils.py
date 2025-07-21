#!/usr/bin/env python3
"""
Utility functions and centralized import hub for the Listener Maths Crossword Solver project.
This module serves as a single point of access for all shared functions and modules.
"""

import os
import sys
import itertools
import logging
from typing import Dict, List, Tuple, Set, Optional, Any

# Configure logging for the import hub
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImportHub:
    """
    Centralized import hub with enhanced error handling and logging.
    
    This class provides a clean interface for managing imports across different
    project folders (archive, experimental, scripts) with graceful fallbacks
    and comprehensive logging.
    """
    
    def __init__(self):
        self._imports: Dict[str, Any] = {}
        self._import_paths: Dict[str, str] = {}
        self._fallbacks: Dict[str, Any] = {}
        self._setup_paths()
    
    def _setup_paths(self):
        """Setup Python path to include all project folders."""
        project_root = os.path.dirname(os.path.abspath(__file__))
        current_dir = os.getcwd()
        
        # Add project paths
        paths_to_add = [
            project_root,
            current_dir,
            os.path.join(project_root, 'archive'),
            os.path.join(project_root, 'experimental'),
            os.path.join(project_root, 'scripts')
        ]
        
        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)
                logger.debug(f"Added path to sys.path: {path}")
    
    def register_import(self, name: str, import_path: str, fallback: Optional[Any] = None, 
                       description: str = "") -> bool:
        """
        Register an import with optional fallback.
        
        Args:
            name: The name to use when accessing this import
            import_path: The full import path (e.g., 'archive.systematic_grid_parser')
            fallback: Optional fallback implementation if import fails
            description: Optional description of what this import provides
            
        Returns:
            bool: True if import succeeded, False if using fallback
        """
        try:
            # Handle different import patterns
            if '.' in import_path:
                module_name, attr_name = import_path.rsplit('.', 1)
                module = __import__(module_name, fromlist=[attr_name])
                imported_obj = getattr(module, attr_name)
            else:
                imported_obj = __import__(import_path)
            
            self._imports[name] = imported_obj
            self._import_paths[name] = import_path
            
            if description:
                logger.info(f"✅ Successfully imported {name} from {import_path} - {description}")
            else:
                logger.info(f"✅ Successfully imported {name} from {import_path}")
            
            return True
            
        except ImportError as e:
            if fallback is not None:
                self._imports[name] = fallback
                self._fallbacks[name] = fallback
                self._import_paths[name] = f"{import_path} (FALLBACK)"
                
                if description:
                    logger.warning(f"⚠️ Using fallback for {name} from {import_path} - {description}")
                else:
                    logger.warning(f"⚠️ Using fallback for {name} from {import_path}")
                logger.debug(f"Import error: {e}")
                
                return False
            else:
                logger.error(f"❌ Failed to import {name} from {import_path}: {e}")
                if description:
                    logger.error(f"   Description: {description}")
                raise
    
    def get(self, name: str) -> Any:
        """Get an imported object by name."""
        if name not in self._imports:
            raise KeyError(f"Import '{name}' not found. Available imports: {list(self._imports.keys())}")
        return self._imports[name]
    
    def has(self, name: str) -> bool:
        """Check if an import is available."""
        return name in self._imports
    
    def is_fallback(self, name: str) -> bool:
        """Check if an import is using a fallback implementation."""
        return name in self._fallbacks
    
    def get_import_path(self, name: str) -> str:
        """Get the import path for a registered import."""
        return self._import_paths.get(name, "Not registered")
    
    def list_imports(self) -> Dict[str, Dict[str, Any]]:
        """Get a detailed list of all registered imports."""
        result = {}
        for name in self._imports:
            result[name] = {
                'path': self._import_paths[name],
                'is_fallback': self.is_fallback(name),
                'available': True
            }
        return result
    
    def get_status_report(self) -> str:
        """Generate a human-readable status report of all imports."""
        lines = ["Import Hub Status Report", "=" * 30]
        
        for name, info in self.list_imports().items():
            status = "🔄 FALLBACK" if info['is_fallback'] else "✅ ACTIVE"
            lines.append(f"{name}: {status} ({info['path']})")
        
        return "\n".join(lines)

# Create the global import hub instance
hub = ImportHub()

# Register all the project imports with descriptions
hub.register_import(
    'parse_grid', 
    'archive.systematic_grid_parser.parse_grid',
    description="Grid parsing functionality"
)

hub.register_import(
    'SystematicGridParser', 
    'archive.systematic_grid_parser.SystematicGridParser',
    description="Systematic grid parser class"
)

hub.register_import(
    'ClueTuple', 
    'archive.systematic_grid_parser.ClueTuple',
    description="Clue tuple data structure"
)

hub.register_import(
    'ListenerPuzzle', 
    'experimental.crossword_solver.ListenerPuzzle',
    description="Main puzzle solver class"
)

hub.register_import(
    'ListenerClue', 
    'experimental.crossword_solver.ListenerClue',
    description="Listener clue class"
)

hub.register_import(
    'Clue', 
    'experimental.crossword_solver.Clue',
    description="Base clue class"
)

hub.register_import(
    'CrosswordGrid', 
    'experimental.crossword_solver.CrosswordGrid',
    description="Crossword grid class"
)

# Register anagram-related imports
hub.register_import(
    'find_anagram_multiples', 
    'archive.anagram_grid_solver.find_anagram_multiples',
    description="Find anagram multiples function"
)

hub.register_import(
    'generate_anagrams', 
    'archive.anagram_grid_solver.generate_anagrams',
    description="Generate anagrams function"
)

hub.register_import(
    'generate_anagrams_including_original', 
    'archive.anagram_grid_solver.generate_anagrams_including_original',
    description="Generate anagrams including original function"
)

hub.register_import(
    'validate_anagram_constraints', 
    'archive.anagram_grid_solver.validate_anagram_constraints',
    description="Validate anagram constraints function"
)

# Register listener-related imports
hub.register_import(
    'find_solutions', 
    'listener.find_solutions',
    description="Find solutions function"
)

hub.register_import(
    'get_prime_factors_with_multiplicity', 
    'listener.get_prime_factors_with_multiplicity',
    description="Get prime factors with multiplicity function"
)



# Core utility functions (local implementations)
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

# Set up fallbacks for anagram functions
if not hub.has('find_anagram_multiples'):
    hub.register_import('find_anagram_multiples', 'local', fallback=find_anagram_multiples_local)

if not hub.has('generate_anagrams'):
    hub.register_import('generate_anagrams', 'local', fallback=generate_anagrams_local)

if not hub.has('generate_anagrams_including_original'):
    hub.register_import('generate_anagrams_including_original', 'local', fallback=generate_anagrams_including_original_local)

if not hub.has('validate_anagram_constraints'):
    hub.register_import('validate_anagram_constraints', 'local', fallback=validate_anagram_constraints_local)

# Convenience functions for backward compatibility
def get_available_modules() -> Dict[str, bool]:
    """Return a dictionary showing which modules are available."""
    return {
        'systematic_grid_parser': hub.has('SystematicGridParser'),
        'crossword_solver': hub.has('ListenerPuzzle'),
        'anagram_grid_solver': hub.has('find_anagram_multiples'),
    }

def is_running_from_folder(folder_name: str) -> bool:
    """Check if the current script is running from a specific folder."""
    current_dir = os.path.basename(os.getcwd())
    return current_dir == folder_name

# Create convenient aliases for commonly used imports
parse_grid = hub.get('parse_grid')
SystematicGridParser = hub.get('SystematicGridParser')
ClueTuple = hub.get('ClueTuple')
ListenerPuzzle = hub.get('ListenerPuzzle')
ListenerClue = hub.get('ListenerClue')
Clue = hub.get('Clue')
CrosswordGrid = hub.get('CrosswordGrid')
find_anagram_multiples = hub.get('find_anagram_multiples')
generate_anagrams = hub.get('generate_anagrams')
generate_anagrams_including_original = hub.get('generate_anagrams_including_original')
validate_anagram_constraints = hub.get('validate_anagram_constraints')
find_solutions = hub.get('find_solutions')
get_prime_factors_with_multiplicity = hub.get('get_prime_factors_with_multiplicity')


# Print status report on module load (only in development)
if __name__ != "__main__":
    logger.info("Import Hub initialized successfully")
    logger.debug(hub.get_status_report())
