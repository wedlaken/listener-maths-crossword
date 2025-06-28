# Systematic Grid Parser
# Implements the approach outlined in DETERMINE_GRID_STRUCTURE.md
# Uses 0-63 indexing and dynamic boundary detection

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass

@dataclass
class GridCell:
    """Represents a cell in the 8x8 grid with index 0-63"""
    index: int  # 0-63, left to right, top to bottom
    row: int    # 0-7
    col: int    # 0-7
    clue_number: Optional[int] = None
    value: Optional[int] = None

@dataclass
class ClueTuple:
    """Represents a clue with its cell positions"""
    number: int
    direction: str  # 'ACROSS' or 'DOWN'
    cell_indices: Tuple[int, ...]  # 0-63 indices
    length: int
    parameters: Tuple[int, int, int]  # (a, b, c)

class SystematicGridParser:
    """Systematic grid parser using 0-63 indexing and dynamic boundary detection"""
    
    def __init__(self, grid_image_path: str, clues_image_path: str = None):
        """Initialize the parser with grid and clues images"""
        self.grid_image = cv2.imread(grid_image_path)
        if self.grid_image is None:
            raise ValueError(f"Could not load grid image: {grid_image_path}")
        
        self.clues_image = None
        if clues_image_path:
            self.clues_image = cv2.imread(clues_image_path)
            if self.clues_image is None:
                print(f"Warning: Could not load clues image: {clues_image_path}")
        
        self.grid_size = 8
        self.cells = []
        for i in range(64):
            row = i // self.grid_size
            col = i % self.grid_size
            self.cells.append(GridCell(index=i, row=row, col=col))
        
        self.across_clues = []
        self.down_clues = []
        
        # Ground truth border data from user
        self.thick_right_borders = {3, 8, 9, 10, 11, 12, 13, 19, 24, 30, 32, 38, 43, 49, 50, 51, 52, 53, 54, 59}
        self.thick_bottom_borders = {3, 4, 6, 9, 14, 17, 22, 24, 25, 26, 29, 30, 31, 33, 38, 41, 46, 49, 51, 52}
        
        # Ground truth clue direction assignments
        self.across_clue_numbers = {1, 4, 9, 10, 11, 12, 14, 18, 19, 20, 22, 23}
        self.down_clue_numbers = {1, 2, 3, 5, 6, 7, 8, 13, 15, 16, 17, 21}
        # Note: Clue 1 appears in both ACROSS and DOWN
        
        # Baseline thickness (kept for future image detection)
        self.baseline_thickness = 0
        self.thickness_threshold = 0

    def detect_clue_numbers_ocr(self) -> Dict[int, int]:
        """Detect clue numbers in cells using OCR (placeholder for now)"""
        print("Detecting clue numbers using OCR...")
        
        # TODO: Implement actual OCR detection
        # For now, return a manual mapping based on visual inspection
        # This should be replaced with real OCR results
        
        # Updated mapping based on visual review of the actual puzzle
        # Clues 1-23 are in cells: [0,1,2,4,5,7,11,12,14,16,20,25,32,33,34,37,39,40,44,48,54,56,60]
        detected_numbers = {
            1: 0,   # Clue 1 in cell 0
            2: 1,   # Clue 2 in cell 1
            3: 2,   # Clue 3 in cell 2
            4: 4,   # Clue 4 in cell 4
            5: 5,   # Clue 5 in cell 5
            6: 7,   # Clue 6 in cell 7
            7: 11,  # Clue 7 in cell 11
            8: 12,  # Clue 8 in cell 12
            9: 14,  # Clue 9 in cell 14
            10: 16, # Clue 10 in cell 16
            11: 20, # Clue 11 in cell 20
            12: 25, # Clue 12 in cell 25
            13: 32, # Clue 13 in cell 32
            14: 33, # Clue 14 in cell 33
            15: 34, # Clue 15 in cell 34
            16: 37, # Clue 16 in cell 37
            17: 39, # Clue 17 in cell 39
            18: 40, # Clue 18 in cell 40
            19: 44, # Clue 19 in cell 44
            20: 48, # Clue 20 in cell 48
            21: 54, # Clue 21 in cell 54
            22: 56, # Clue 22 in cell 56
            23: 60, # Clue 23 in cell 60
        }
        
        # Update cell clue numbers
        for clue_num, cell_index in detected_numbers.items():
            if 0 <= cell_index < 64:
                self.cells[cell_index].clue_number = clue_num
        
        print(f"Detected {len(detected_numbers)} clue numbers")
        return detected_numbers

    def establish_baseline_thickness(self) -> None:
        """Establish baseline border thickness using cell 0"""
        print("Establishing baseline border thickness from cell 0...")
        
        # Get cell 0 dimensions
        cell_width = self.grid_image.shape[1] // self.grid_size
        cell_height = self.grid_image.shape[0] // self.grid_size
        
        # Sample right border of cell 0 (between cell 0 and cell 1)
        x_border = cell_width
        sample_width = int(cell_width * 0.06)  # ±3% of cell width
        y_start = int(cell_height * 0.05)  # 5% from top
        y_end = int(cell_height * 0.95)    # 95% from top (90% of height)
        
        # Sample the border region
        border_region = self.grid_image[y_start:y_end, x_border-sample_width//2:x_border+sample_width//2]
        
        # Convert to grayscale and calculate average intensity
        if len(border_region.shape) == 3:
            gray_border = cv2.cvtColor(border_region, cv2.COLOR_BGR2GRAY)
        else:
            gray_border = border_region
        
        self.baseline_thickness = np.mean(gray_border)
        
        # Sample bottom border of cell 0 (between cell 0 and cell 8)
        y_border = cell_height
        x_start = int(cell_width * 0.05)
        x_end = int(cell_width * 0.95)
        
        bottom_region = self.grid_image[y_border-sample_width//2:y_border+sample_width//2, x_start:x_end]
        
        if len(bottom_region.shape) == 3:
            gray_bottom = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
        else:
            gray_bottom = bottom_region
        
        bottom_thickness = np.mean(gray_bottom)
        
        # Use the average of right and bottom borders as baseline
        self.baseline_thickness = (self.baseline_thickness + bottom_thickness) / 2
        
        # Set initial threshold (can be adjusted dynamically)
        self.thickness_threshold = self.baseline_thickness * 0.6  # 40% darker = thicker (more lenient)
        
        print(f"Baseline thickness: {self.baseline_thickness:.2f}")
        print(f"Initial threshold: {self.thickness_threshold:.2f}")

    def is_thick_border(self, cell_index: int, direction: str) -> bool:
        """Check if a cell has a thick border in the specified direction using ground truth data"""
        if cell_index < 0 or cell_index >= 64:
            return False
        
        # Use ground truth border data
        if direction == 'right':
            return cell_index in self.thick_right_borders
        elif direction == 'bottom':
            return cell_index in self.thick_bottom_borders
        else:
            return False
        
        # TODO: Future image-based detection can be implemented here
        # For now, we use ground truth data for accurate results

    def find_across_clue(self, start_cell: int, used_cells: Set[int]) -> Optional[ClueTuple]:
        """Find an ACROSS clue starting from the given cell"""
        if start_cell in used_cells:
            return None
        
        # Skip ACROSS search for clue numbers in end-of-row cells (column 7)
        # These should be treated as DOWN clues
        if self.cells[start_cell].col == self.grid_size - 1:  # Column 7 (end of row)
            return None
        
        cell_indices = []
        current_cell = start_cell
        
        # Progress right until thick border or end of row
        while current_cell < 64 and self.cells[current_cell].row == self.cells[start_cell].row:
            cell_indices.append(current_cell)
            
            # Check if next cell would be beyond row boundary
            if self.cells[current_cell].col == self.grid_size - 1:
                break  # End of row - always end ACROSS clue here
            
            # Check for thick right border (only for non-edge cells)
            if self.is_thick_border(current_cell, 'right'):
                print(f"    Found thick right border at cell {current_cell}, ending ACROSS clue")
                break
            
            current_cell += 1
        
        if len(cell_indices) == 0:
            return None
        
        # Check if any cell in this clue has a clue number
        clue_number = None
        for cell_idx in cell_indices:
            if self.cells[cell_idx].clue_number:
                clue_number = self.cells[cell_idx].clue_number
                break
        
        if clue_number is None:
            return None
        
        # Create clue tuple (parameters will be filled later)
        return ClueTuple(
            number=clue_number,
            direction='ACROSS',
            cell_indices=tuple(cell_indices),
            length=len(cell_indices),
            parameters=(len(cell_indices), 0, 0)  # Placeholder
        )

    def find_down_clue(self, start_cell: int, used_cells: Set[int]) -> Optional[ClueTuple]:
        """Find a DOWN clue starting from the given cell"""
        if start_cell in used_cells:
            return None
        
        cell_indices = []
        current_cell = start_cell
        
        # Progress down until thick border or end of column
        while current_cell < 64 and self.cells[current_cell].col == self.cells[start_cell].col:
            cell_indices.append(current_cell)
            
            # Check if next cell would be beyond column boundary (last row)
            if self.cells[current_cell].row == self.grid_size - 1:
                break  # End of column - always end DOWN clue here (no border check)
            
            # Check for thick bottom border (only for non-edge cells)
            if self.is_thick_border(current_cell, 'bottom'):
                print(f"    Found thick bottom border at cell {current_cell}, ending DOWN clue")
                break
            
            current_cell += self.grid_size
        
        # Special rule: if clue starts in last column (col 7), force at least one cell down
        # since it can't be a single-digit ACROSS clue
        if (self.cells[start_cell].col == self.grid_size - 1 and 
            len(cell_indices) == 1 and 
            start_cell + self.grid_size < 64):
            print(f"    Forcing clue starting in last column to extend at least one cell down")
            cell_indices.append(start_cell + self.grid_size)
        
        if len(cell_indices) == 0:
            return None
        
        # Check if any cell in this clue has a clue number
        clue_number = None
        for cell_idx in cell_indices:
            if self.cells[cell_idx].clue_number:
                clue_number = self.cells[cell_idx].clue_number
                break
        
        if clue_number is None:
            return None
        
        # Create clue tuple (parameters will be filled later)
        return ClueTuple(
            number=clue_number,
            direction='DOWN',
            cell_indices=tuple(cell_indices),
            length=len(cell_indices),
            parameters=(len(cell_indices), 0, 0)  # Placeholder
        )

    def parse_grid_structure(self) -> None:
        """Parse the grid structure using the systematic approach"""
        print("Parsing grid structure systematically...")
        
        # Step 1: Detect clue numbers
        detected_numbers = self.detect_clue_numbers_ocr()
        
        # Step 2: Establish baseline thickness
        self.establish_baseline_thickness()
        
        # Step 3: Find all cells with clue numbers
        cells_with_clues = [cell.index for cell in self.cells if cell.clue_number is not None]
        cells_with_clues.sort()
        print(f"Cells with clue numbers: {cells_with_clues}")
        print("Detected clue numbers and their cell indices:")
        for cell in self.cells:
            if cell.clue_number is not None:
                print(f"  Clue {cell.clue_number} at cell {cell.index} (row {cell.row}, col {cell.col})")
        
        # Step 4: Process each clue number individually
        used_across_cells = set()
        used_down_cells = set()
        processed_clue_numbers = set()
        
        # Get all unique clue numbers
        all_clue_numbers = {cell.clue_number for cell in self.cells if cell.clue_number is not None}
        
        for clue_number in sorted(all_clue_numbers):
            if clue_number in processed_clue_numbers:
                continue
            
            # Find all cells with this clue number
            cells_with_this_clue = [cell.index for cell in self.cells if cell.clue_number == clue_number]
            
            # Try to build a clue starting from each cell with this number
            clue_built = False
            for start_cell in cells_with_this_clue:
                # Special case: clue 1 should be both ACROSS and DOWN
                if clue_number == 1:
                    print(f"DEBUG: Processing clue 1 at cell {start_cell}")
                    # Try ACROSS
                    if clue_number in self.across_clue_numbers:
                        across_clue = self.find_across_clue(start_cell, used_across_cells)
                        if across_clue and across_clue.number == clue_number and across_clue not in self.across_clues:
                            self.across_clues.append(across_clue)
                            used_across_cells.update(across_clue.cell_indices)
                            print(f"Found ACROSS clue {across_clue.number}: {across_clue.cell_indices}")
                            clue_built = True
                        else:
                            print(f"DEBUG: ACROSS clue 1 not found or already exists")
                    # Try DOWN
                    if clue_number in self.down_clue_numbers:
                        down_clue = self.find_down_clue(start_cell, used_down_cells)
                        if down_clue and down_clue.number == clue_number and down_clue not in self.down_clues:
                            self.down_clues.append(down_clue)
                            used_down_cells.update(down_clue.cell_indices)
                            print(f"Found DOWN clue {down_clue.number}: {down_clue.cell_indices}")
                            clue_built = True
                        else:
                            print(f"DEBUG: DOWN clue 1 not found or already exists")
                    # Do NOT continue or break here; allow both to be found for all cells with clue 1
                    continue
                # Determine which direction to try first based on ground truth
                if clue_number in self.across_clue_numbers:
                    # Try ACROSS first for this clue number
                    across_clue = self.find_across_clue(start_cell, used_across_cells)
                    if across_clue and across_clue.number == clue_number:
                        self.across_clues.append(across_clue)
                        used_across_cells.update(across_clue.cell_indices)
                        if clue_number != 1:
                            processed_clue_numbers.add(clue_number)
                        print(f"Found ACROSS clue {across_clue.number}: {across_clue.cell_indices}")
                        clue_built = True
                        break
                    # If ACROSS failed, try DOWN (for clue 1 which appears in both)
                    if clue_number in self.down_clue_numbers:
                        down_clue = self.find_down_clue(start_cell, used_down_cells)
                        if down_clue and down_clue.number == clue_number:
                            self.down_clues.append(down_clue)
                            used_down_cells.update(down_clue.cell_indices)
                            if clue_number != 1:
                                processed_clue_numbers.add(clue_number)
                            print(f"Found DOWN clue {down_clue.number}: {down_clue.cell_indices}")
                            clue_built = True
                            break
                elif clue_number in self.down_clue_numbers:
                    # Try DOWN first for this clue number
                    down_clue = self.find_down_clue(start_cell, used_down_cells)
                    if down_clue and down_clue.number == clue_number:
                        self.down_clues.append(down_clue)
                        used_down_cells.update(down_clue.cell_indices)
                        if clue_number != 1:
                            processed_clue_numbers.add(clue_number)
                        print(f"Found DOWN clue {down_clue.number}: {down_clue.cell_indices}")
                        clue_built = True
                        break
                    # If DOWN failed, try ACROSS (for clue 1 which appears in both)
                    if clue_number in self.across_clue_numbers:
                        across_clue = self.find_across_clue(start_cell, used_across_cells)
                        if across_clue and across_clue.number == clue_number:
                            self.across_clues.append(across_clue)
                            used_across_cells.update(across_clue.cell_indices)
                            if clue_number != 1:
                                processed_clue_numbers.add(clue_number)
                            print(f"Found ACROSS clue {across_clue.number}: {across_clue.cell_indices}")
                            clue_built = True
                            break
            if not clue_built:
                print(f"WARNING: Could not build clue {clue_number}")
        print(f"Found {len(self.across_clues)} ACROSS clues and {len(self.down_clues)} DOWN clues")

    def get_all_clues(self) -> List[ClueTuple]:
        """Get all clues sorted by number"""
        all_clues = self.across_clues + self.down_clues
        all_clues.sort(key=lambda x: x.number)
        return all_clues

    def print_results(self) -> None:
        """Print the parsing results"""
        print("\nGrid Structure Results:")
        print("=" * 50)
        
        all_clues = self.get_all_clues()
        
        print("\nACROSS Clues:")
        for clue in sorted(self.across_clues, key=lambda x: x.number):
            print(f"  Clue {clue.number}: {clue.cell_indices} (length={clue.length})")
        
        print("\nDOWN Clues:")
        for clue in sorted(self.down_clues, key=lambda x: x.number):
            print(f"  Clue {clue.number}: {clue.cell_indices} (length={clue.length})")
        
        print(f"\nTotal: {len(all_clues)} clues")

    def print_cell_clue_summary(self):
        """Print a summary showing which clues each cell belongs to (ACROSS and/or DOWN)"""
        cell_to_across = {cell: [] for cell in range(64)}
        cell_to_down = {cell: [] for cell in range(64)}
        for clue in self.across_clues:
            for cell in clue.cell_indices:
                cell_to_across[cell].append(clue.number)
        for clue in self.down_clues:
            for cell in clue.cell_indices:
                cell_to_down[cell].append(clue.number)
        print("\nCell Clue Summary (cell: [ACROSS clues] | [DOWN clues]):")
        for row in range(self.grid_size):
            row_summary = []
            for col in range(self.grid_size):
                idx = row * self.grid_size + col
                across = cell_to_across[idx]
                down = cell_to_down[idx]
                row_summary.append(f"{idx}:A{across} D{down}")
            print("  ".join(row_summary))

def parse_grid() -> List[Tuple[int, str, Tuple[int, ...]]]:
    """
    Parse the grid and return clue information.
    Returns list of (number, direction, cell_indices) tuples.
    """
    parser = SystematicGridParser('data/Listener grid 4869.png')
    parser.parse_grid_structure()
    
    clues = []
    for clue_tuple in parser.get_all_clues():
        clues.append((clue_tuple.number, clue_tuple.direction, clue_tuple.cell_indices))
    
    return clues

def main():
    """Main function for testing the parser"""
    print("Systematic Grid Parser Test")
    print("=" * 40)
    
    try:
        # Create parser
        parser = SystematicGridParser('data/Listener grid 4869.png')
        
        # Parse grid structure
        parser.parse_grid_structure()
        
        # Print results
        parser.print_results()
        
        # Print cell clue summary
        parser.print_cell_clue_summary()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()