"""
Clue Classes for Listener Maths Crossword
Combines tuple structure with listener parameters and handles unclued clues
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from listener import find_solutions
import math

@dataclass
class ClueTuple:
    """Basic clue tuple with cell positions"""
    number: int
    direction: str  # 'ACROSS' or 'DOWN'
    cell_indices: Tuple[int, ...]  # 0-63 indices
    length: int

@dataclass
class ClueParameters:
    """Listener clue parameters (a, b, c)"""
    a: int  # Number of digits (length)
    b: int  # Number of prime factors (with multiplicity)
    c: int  # Difference between largest and smallest prime factor
    is_unclued: bool = False
    
    def __post_init__(self):
        """Validate parameters after initialization"""
        if self.a <= 0:
            raise ValueError(f"Parameter 'a' must be positive, got {self.a}")
        if not self.is_unclued:
            if self.b <= 0:
                raise ValueError(f"Parameter 'b' must be positive for clued entries, got {self.b}")
            if self.c < 0:
                raise ValueError(f"Parameter 'c' must be non-negative, got {self.c}")

class ListenerClue:
    """
    Complete Listener clue class combining tuple structure with parameters
    Handles both clued and unclued entries
    """
    
    def __init__(self, number: int, direction: str, cell_indices: Tuple[int, ...], 
                 parameters: ClueParameters):
        self.number = number
        self.direction = direction
        self.cell_indices = cell_indices
        self.parameters = parameters
        self.length = len(cell_indices)
        
        # Validate that length matches parameter 'a'
        if self.length != parameters.a:
            raise ValueError(f"Clue length {self.length} doesn't match parameter 'a' {parameters.a}")
        
        # Initialize solution tracking
        self._initialize_solutions()
    
    def _initialize_solutions(self):
        """Initialize possible solutions based on clue type"""
        if self.parameters.is_unclued:
            # Unclued clues start with empty solution sets
            # They will be populated as constraints are applied from crossing clues
            self.possible_solutions = set()
            self.original_solution_count = 0  # Will be set when constraints are first applied
        else:
            # Clued clues use listener.py find_solutions function
            solutions = find_solutions(self.parameters.a, self.parameters.b, self.parameters.c)
            self.possible_solutions = set(solutions)
            self.original_solution_count = len(self.possible_solutions)
    
    def __repr__(self):
        status = "UNCLUED" if self.parameters.is_unclued else f"({self.parameters.b}:{self.parameters.c})"
        return f"Clue {self.number} {self.direction}: {self.cell_indices} {status} - {len(self.possible_solutions)}/{self.original_solution_count} solutions"
    
    def __str__(self):
        return self.__repr__()
    
    def eliminate_solution(self, solution: int) -> bool:
        """Remove a solution from the valid set. Returns True if solution was removed."""
        if solution in self.possible_solutions:
            self.possible_solutions.remove(solution)
            return True
        return False
    
    def get_valid_solutions(self) -> List[int]:
        """Get list of currently valid solutions."""
        return list(self.possible_solutions)
    
    def is_solved(self) -> bool:
        """Check if this clue has only one valid solution."""
        return len(self.possible_solutions) == 1
    
    def get_solution(self) -> Optional[int]:
        """Get the solution if this clue is solved, otherwise None."""
        if self.is_solved():
            return list(self.possible_solutions)[0]
        return None
    
    def update_from_constraints(self, solved_cells: Dict[int, int]) -> bool:
        """
        Update valid solutions based on current grid state.
        Returns True if solutions were eliminated.
        """
        # For unclued clues, initialize with all possible numbers if this is the first time
        if self.parameters.is_unclued and self.original_solution_count == 0:
            start = 10**(self.length - 1)
            end = 10**self.length
            self.possible_solutions = set(range(start, end))
            self.original_solution_count = len(self.possible_solutions)
        
        solutions_to_remove = []
        
        for solution in self.possible_solutions:
            solution_str = str(solution).zfill(self.length)
            
            # Check if this solution is compatible with current grid state
            for i, cell_index in enumerate(self.cell_indices):
                if cell_index in solved_cells:
                    expected_digit = solved_cells[cell_index]
                    actual_digit = int(solution_str[i])
                    if expected_digit != actual_digit:
                        solutions_to_remove.append(solution)
                        break
        
        # Remove incompatible solutions
        for solution in solutions_to_remove:
            self.eliminate_solution(solution)
        
        return len(solutions_to_remove) > 0
    
    def get_crossing_clues(self, all_clues: Dict[int, 'ListenerClue']) -> List['ListenerClue']:
        """Get all clues that cross this clue (share cells)."""
        crossing = []
        for other_clue in all_clues.values():
            if other_clue.number != self.number:
                # Check if any cells overlap
                if set(self.cell_indices) & set(other_clue.cell_indices):
                    crossing.append(other_clue)
        return crossing

class ClueFactory:
    """
    Factory class for creating ListenerClue objects from various input formats
    """
    
    @staticmethod
    def from_tuple_and_parameters(clue_tuple: ClueTuple, b: int, c: int) -> ListenerClue:
        """Create a ListenerClue from a ClueTuple and b, c parameters"""
        if b == -1 or c == -1:
            # Unclued clue
            parameters = ClueParameters(
                a=clue_tuple.length,
                b=-1,
                c=-1,
                is_unclued=True
            )
        else:
            # Clued clue
            parameters = ClueParameters(
                a=clue_tuple.length,
                b=b,
                c=c,
                is_unclued=False
            )
        
        return ListenerClue(
            number=clue_tuple.number,
            direction=clue_tuple.direction,
            cell_indices=clue_tuple.cell_indices,
            parameters=parameters
        )
    
    @staticmethod
    def from_text_line(line: str, direction: str, cell_indices: Tuple[int, ...]) -> Optional[ListenerClue]:
        """
        Create a ListenerClue from a text line like "1 6:2" or "12 Unclued"
        """
        parts = line.strip().split()
        if len(parts) < 2:
            return None
        
        try:
            number = int(parts[0])
            
            if parts[1].lower() == 'unclued':
                # Unclued clue
                parameters = ClueParameters(
                    a=len(cell_indices),
                    b=-1,
                    c=-1,
                    is_unclued=True
                )
            else:
                # Parse "b:c" format
                b_c_parts = parts[1].split(':')
                if len(b_c_parts) != 2:
                    return None
                
                b = int(b_c_parts[0])
                c = int(b_c_parts[1])
                
                parameters = ClueParameters(
                    a=len(cell_indices),
                    b=b,
                    c=c,
                    is_unclued=False
                )
            
            return ListenerClue(
                number=number,
                direction=direction,
                cell_indices=cell_indices,
                parameters=parameters
            )
            
        except (ValueError, IndexError):
            return None

class ClueManager:
    """
    Manages all clues in a puzzle and their interactions
    """
    
    def __init__(self):
        self.clues: Dict[int, ListenerClue] = {}  # clue_number -> ListenerClue
        self.cell_to_clues: Dict[int, List[int]] = {}  # cell_index -> [clue_numbers]
        self.solved_cells: Dict[int, int] = {}  # cell_index -> digit_value
        self.solution_history: List[Tuple[int, int]] = []  # [(clue_number, solution), ...]
    
    def add_clue(self, clue: ListenerClue) -> None:
        """Add a clue to the manager."""
        self.clues[clue.number] = clue
        
        # Update cell-to-clues mapping
        for cell_index in clue.cell_indices:
            if cell_index not in self.cell_to_clues:
                self.cell_to_clues[cell_index] = []
            self.cell_to_clues[cell_index].append(clue.number)
    
    def get_clue(self, clue_number: int) -> Optional[ListenerClue]:
        """Get a clue by its number."""
        return self.clues.get(clue_number)
    
    def get_clues_for_cell(self, cell_index: int) -> List[ListenerClue]:
        """Get all clues that use a specific cell."""
        clue_numbers = self.cell_to_clues.get(cell_index, [])
        return [self.clues[num] for num in clue_numbers]
    
    def get_overlapping_clues(self, clue_number: int) -> List[ListenerClue]:
        """Get all clues that overlap with the given clue."""
        clue = self.clues[clue_number]
        overlapping = set()
        
        for cell_index in clue.cell_indices:
            for other_clue_num in self.cell_to_clues.get(cell_index, []):
                if other_clue_num != clue_number:
                    overlapping.add(other_clue_num)
        
        return [self.clues[num] for num in overlapping]
    
    def apply_solution(self, clue_number: int, solution: int) -> List[Tuple[int, int]]:
        """
        Apply a solution to a clue and propagate constraints to overlapping clues.
        Returns list of eliminated solutions: [(clue_number, eliminated_solution), ...]
        """
        clue = self.clues[clue_number]
        eliminated = []
        
        # Convert solution to digits
        solution_str = str(solution).zfill(clue.length)
        
        # Apply this solution to the grid
        for i, cell_index in enumerate(clue.cell_indices):
            digit = int(solution_str[i])
            self.solved_cells[cell_index] = digit
        
        # Check overlapping clues and eliminate incompatible solutions
        for overlapping_clue in self.get_overlapping_clues(clue_number):
            eliminated_from_clue = self._eliminate_incompatible_solutions(overlapping_clue)
            eliminated.extend(eliminated_from_clue)
        
        # Update unclued clues based on new grid state
        for unclued_clue in self._get_unclued_clues():
            if unclued_clue.update_from_constraints(self.solved_cells):
                eliminated.append((unclued_clue.number, -1))  # -1 indicates constraint update
        
        # Record this solution
        self.solution_history.append((clue_number, solution))
        
        return eliminated
    
    def _get_unclued_clues(self) -> List[ListenerClue]:
        """Get all unclued clues."""
        return [clue for clue in self.clues.values() if clue.parameters.is_unclued]
    
    def _eliminate_incompatible_solutions(self, clue: ListenerClue) -> List[Tuple[int, int]]:
        """
        Eliminate solutions from a clue that are incompatible with current grid state.
        Returns list of eliminated solutions: [(clue_number, eliminated_solution), ...]
        """
        eliminated = []
        solutions_to_remove = []
        
        for solution in clue.possible_solutions:
            if not self._is_solution_compatible(clue, solution):
                solutions_to_remove.append(solution)
        
        for solution in solutions_to_remove:
            if clue.eliminate_solution(solution):
                eliminated.append((clue.number, solution))
        
        return eliminated
    
    def _is_solution_compatible(self, clue: ListenerClue, solution: int) -> bool:
        """Check if a solution is compatible with the current grid state."""
        solution_str = str(solution).zfill(clue.length)
        
        for i, cell_index in enumerate(clue.cell_indices):
            if cell_index in self.solved_cells:
                expected_digit = self.solved_cells[cell_index]
                actual_digit = int(solution_str[i])
                if expected_digit != actual_digit:
                    return False
        
        return True
    
    def print_state(self) -> None:
        """Print the current state of all clues."""
        print("\nClue Manager State:")
        print("=" * 50)
        
        for clue_number in sorted(self.clues.keys()):
            clue = self.clues[clue_number]
            print(f"{clue}")
        
        print(f"\nSolved cells: {len(self.solved_cells)}")
        if self.solved_cells:
            print("Cell values:", dict(sorted(self.solved_cells.items())))
        
        print(f"Solution history: {len(self.solution_history)} steps")
    
    def get_solved_clues(self) -> List[ListenerClue]:
        """Get all clues that have been solved (only one solution remaining)."""
        return [clue for clue in self.clues.values() if clue.is_solved()]
    
    def get_unsolved_clues(self) -> List[ListenerClue]:
        """Get all clues that haven't been solved yet."""
        return [clue for clue in self.clues.values() if not clue.is_solved()]
    
    def is_puzzle_solved(self) -> bool:
        """Check if all clues have been solved."""
        return all(clue.is_solved() for clue in self.clues.values()) 