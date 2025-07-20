"""
Puzzle Solution Presenter

This module provides various ways to present and visualize puzzle solutions,
including grid displays, clue status, and solution details.
"""

from typing import Dict, List, Optional, Tuple
from utils import ListenerPuzzle, ListenerClue
import os

class PuzzlePresenter:
    """Handles presentation and visualization of puzzle solutions"""
    
    def __init__(self, puzzle: ListenerPuzzle):
        self.puzzle = puzzle
        self.grid_size = 8  # 8x8 grid
        
    def display_solved_grid(self, show_clue_numbers: bool = True) -> str:
        """Display the solved grid with optional clue numbers"""
        output = []
        output.append("SOLVED PUZZLE GRID")
        output.append("=" * 50)
        output.append("")
        
        # Header row with column numbers
        header = "   "
        for col in range(self.grid_size):
            header += f" {col} "
        output.append(header)
        output.append("   " + "-" * (self.grid_size * 3))
        
        # Grid rows
        for row in range(self.grid_size):
            row_str = f"{row:2d} |"
            for col in range(self.grid_size):
                cell_index = row * self.grid_size + col
                if cell_index in self.puzzle.solved_cells:
                    digit = self.puzzle.solved_cells[cell_index]
                    row_str += f" {digit} "
                else:
                    if show_clue_numbers:
                        # Show clue number if this cell starts a clue
                        clue_num = self._get_clue_number_at_cell(cell_index)
                        if clue_num:
                            row_str += f"{clue_num:2d} "
                        else:
                            row_str += " . "
                    else:
                        row_str += " . "
            row_str += "|"
            output.append(row_str)
        
        output.append("   " + "-" * (self.grid_size * 3))
        output.append("")
        
        return "\n".join(output)
    
    def display_clue_status(self, show_solutions: bool = False) -> str:
        """Display the status of all clues"""
        output = []
        output.append("CLUE STATUS")
        output.append("=" * 50)
        output.append("")
        
        # Separate ACROSS and DOWN clues
        across_clues = []
        down_clues = []
        
        for clue_num in sorted(self.puzzle.clues.keys()):
            clue = self.puzzle.clues[clue_num]
            if clue.direction == "ACROSS":
                across_clues.append(clue)
            else:
                down_clues.append(clue)
        
        # Display ACROSS clues
        output.append("ACROSS:")
        output.append("-" * 20)
        for clue in across_clues:
            status = self._get_clue_status_string(clue, show_solutions)
            output.append(status)
        
        output.append("")
        
        # Display DOWN clues
        output.append("DOWN:")
        output.append("-" * 20)
        for clue in down_clues:
            status = self._get_clue_status_string(clue, show_solutions)
            output.append(status)
        
        output.append("")
        
        return "\n".join(output)
    
    def display_solution_summary(self) -> str:
        """Display a summary of the solution progress"""
        output = []
        output.append("SOLUTION SUMMARY")
        output.append("=" * 50)
        output.append("")
        
        total_clues = len(self.puzzle.clues)
        solved_clues = sum(1 for clue in self.puzzle.clues.values() if clue.is_solved())
        total_cells = self.grid_size * self.grid_size
        solved_cells = len(self.puzzle.solved_cells)
        
        output.append(f"Total clues: {total_clues}")
        output.append(f"Solved clues: {solved_clues}")
        output.append(f"Unsolved clues: {total_clues - solved_clues}")
        output.append(f"Solution progress: {solved_clues}/{total_clues} ({solved_clues/total_clues*100:.1f}%)")
        output.append("")
        
        output.append(f"Total cells: {total_cells}")
        output.append(f"Solved cells: {solved_cells}")
        output.append(f"Unsolved cells: {total_cells - solved_cells}")
        output.append(f"Grid completion: {solved_cells}/{total_cells} ({solved_cells/total_cells*100:.1f}%)")
        output.append("")
        
        # Show solution history
        if self.puzzle.solution_history:
            output.append("SOLUTION HISTORY:")
            output.append("-" * 20)
            for i, (clue_num, solution) in enumerate(self.puzzle.solution_history, 1):
                clue = self.puzzle.clues[clue_num]
                output.append(f"{i:2d}. Clue {clue_num} {clue.direction}: {solution}")
        
        output.append("")
        
        return "\n".join(output)
    
    def display_detailed_grid(self) -> str:
        """Display a detailed grid with clue numbers and cell indices"""
        output = []
        output.append("DETAILED GRID VIEW")
        output.append("=" * 50)
        output.append("")
        
        # Show cell indices
        output.append("Cell Indices (0-63):")
        output.append("-" * 30)
        for row in range(self.grid_size):
            row_str = ""
            for col in range(self.grid_size):
                cell_index = row * self.grid_size + col
                row_str += f"{cell_index:2d} "
            output.append(row_str)
        
        output.append("")
        
        # Show solved grid with cell indices
        output.append("Solved Grid with Cell Indices:")
        output.append("-" * 35)
        for row in range(self.grid_size):
            row_str = ""
            for col in range(self.grid_size):
                cell_index = row * self.grid_size + col
                if cell_index in self.puzzle.solved_cells:
                    digit = self.puzzle.solved_cells[cell_index]
                    row_str += f" {digit} "
                else:
                    row_str += f"{cell_index:2d} "
            output.append(row_str)
        
        output.append("")
        
        return "\n".join(output)
    
    def export_solution_to_file(self, filename: str, include_details: bool = True) -> None:
        """Export the solution to a text file"""
        output = []
        output.append("LISTENER MATHS CROSSWORD - SOLUTION")
        output.append("=" * 50)
        output.append("")
        
        # Add solution summary
        output.append(self.display_solution_summary())
        
        # Add solved grid
        output.append(self.display_solved_grid(show_clue_numbers=True))
        
        # Add clue status
        output.append(self.display_clue_status(show_solutions=True))
        
        if include_details:
            output.append(self.display_detailed_grid())
        
        # Write to file
        with open(filename, 'w') as f:
            f.write("\n".join(output))
        
        print(f"Solution exported to: {filename}")
    
    def _get_clue_number_at_cell(self, cell_index: int) -> Optional[int]:
        """Get the clue number that starts at the given cell"""
        for clue_num, clue in self.puzzle.clues.items():
            if clue.cell_indices[0] == cell_index:
                return clue_num
        return None
    
    def _get_clue_status_string(self, clue: ListenerClue, show_solutions: bool) -> str:
        """Get a formatted string for clue status"""
        if clue.is_solved():
            solution = clue.get_solution()
            status = f"{clue.number:2d}. SOLVED: {solution}"
        else:
            solution_count = len(clue.valid_solutions)
            status = f"{clue.number:2d}. {solution_count} solutions"
            
            if show_solutions and solution_count <= 10:
                solutions = clue.get_valid_solutions()
                status += f" [{', '.join(map(str, solutions))}]"
        
        # Add cell positions
        cell_str = f" ({', '.join(map(str, clue.cell_indices))})"
        status += cell_str
        
        return status
    
    def print_complete_solution(self) -> None:
        """Print a complete solution presentation"""
        print("\n" + "="*60)
        print("COMPLETE PUZZLE SOLUTION")
        print("="*60)
        
        print(self.display_solution_summary())
        print(self.display_solved_grid(show_clue_numbers=True))
        print(self.display_clue_status(show_solutions=True))
        
        print("\n" + "="*60)
        print("SOLUTION COMPLETE")
        print("="*60)

def create_presenter_from_puzzle(puzzle: ListenerPuzzle) -> PuzzlePresenter:
    """Convenience function to create a presenter from a puzzle"""
    return PuzzlePresenter(puzzle) 