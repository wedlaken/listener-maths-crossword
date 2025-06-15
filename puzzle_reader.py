import cv2
import numpy as np
import pytesseract
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from crossword_solver import Clue, CrosswordGrid
import matplotlib.pyplot as plt
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

@dataclass
class GridCell:
    row: int
    col: int
    value: Optional[int] = None
    clue_number: Optional[int] = None
    is_black: bool = False

class PuzzleReader:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.grid_size = 8
        self.cells: List[GridCell] = []
        self.clues: Dict[str, List[Clue]] = {
            'ACROSS': [],
            'DOWN': []
        }

    def preprocess_image(self) -> None:
        """Preprocess the image for better OCR results."""
        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to get binary image
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest contour (should be the grid)
        grid_contour = max(contours, key=cv2.contourArea)
        
        # Get the bounding rectangle
        x, y, w, h = cv2.boundingRect(grid_contour)
        
        # Crop the image to the grid
        self.grid_image = self.image[y:y+h, x:x+w]
        
        # Calculate cell size
        self.cell_width = w // self.grid_size
        self.cell_height = h // self.grid_size

    def detect_grid_structure(self) -> None:
        """Detect the grid structure and create cells."""
        # Convert to grayscale for processing
        gray = cv2.cvtColor(self.grid_image, cv2.COLOR_BGR2GRAY)
        
        # Detect grid lines
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        
        # Create cells
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Calculate cell boundaries
                x1 = col * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                
                # Extract cell image
                cell_image = self.grid_image[y1:y2, x1:x2]
                
                # Check if cell is black (undefined)
                cell_gray = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
                is_black = np.mean(cell_gray) < 128
                
                # Create cell
                cell = GridCell(row, col, is_black=is_black)
                self.cells.append(cell)

    def read_cell_numbers(self) -> None:
        """Read numbers from each cell using OCR."""
        for cell in self.cells:
            if not cell.is_black:
                # Calculate cell boundaries
                x1 = cell.col * self.cell_width
                y1 = cell.row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                
                # Extract cell image
                cell_image = self.grid_image[y1:y2, x1:x2]
                
                # Preprocess cell image for better OCR
                cell_gray = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
                cell_binary = cv2.threshold(cell_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                
                # Read number using OCR
                number = pytesseract.image_to_string(cell_binary, config='--psm 7 -c tessedit_char_whitelist=0123456789')
                try:
                    cell.value = int(number.strip())
                except ValueError:
                    cell.value = None

    def detect_clue_numbers(self) -> None:
        """Detect clue numbers in the grid."""
        # Look for small numbers in the top-left of each cell
        for cell in self.cells:
            if not cell.is_black:
                # Calculate clue number region (top-left corner of cell)
                x1 = cell.col * self.cell_width
                y1 = cell.row * self.cell_height
                x2 = x1 + self.cell_width // 3
                y2 = y1 + self.cell_height // 3
                
                # Extract clue number region
                clue_region = self.grid_image[y1:y2, x1:x2]
                
                # Read clue number using OCR
                number = pytesseract.image_to_string(clue_region, config='--psm 7 -c tessedit_char_whitelist=0123456789')
                try:
                    cell.clue_number = int(number.strip())
                except ValueError:
                    cell.clue_number = None

    def determine_clue_direction(self, cell: GridCell) -> Optional[str]:
        """Determine if a cell starts an across or down clue."""
        if cell.clue_number is None:
            return None
            
        # Check if this cell starts an across clue
        is_across_start = True
        if cell.col > 0:  # Check cell to the left
            left_cell = next((c for c in self.cells if c.row == cell.row and c.col == cell.col - 1), None)
            if left_cell and not left_cell.is_black:
                is_across_start = False
                
        # Check if this cell starts a down clue
        is_down_start = True
        if cell.row > 0:  # Check cell above
            above_cell = next((c for c in self.cells if c.row == cell.row - 1 and c.col == cell.col), None)
            if above_cell and not above_cell.is_black:
                is_down_start = False
                
        if is_across_start and is_down_start:
            return 'BOTH'
        elif is_across_start:
            return 'ACROSS'
        elif is_down_start:
            return 'DOWN'
        return None

    def get_clue_length(self, cell: GridCell, direction: str) -> int:
        """Calculate the length of a clue starting at the given cell."""
        length = 0
        if direction == 'ACROSS':
            # Count cells to the right until we hit a black cell or grid edge
            for col in range(cell.col, self.grid_size):
                current_cell = next((c for c in self.cells if c.row == cell.row and c.col == col), None)
                if current_cell and not current_cell.is_black:
                    length += 1
                else:
                    break
        else:  # DOWN
            # Count cells down until we hit a black cell or grid edge
            for row in range(cell.row, self.grid_size):
                current_cell = next((c for c in self.cells if c.row == row and c.col == cell.col), None)
                if current_cell and not current_cell.is_black:
                    length += 1
                else:
                    break
        return length

    def extract_clues(self) -> None:
        """Extract clues from the image."""
        # Convert the image to grayscale for better text detection
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Use OCR to find all text in the image
        # We'll look for patterns like "22 2 : 1427"
        text = pytesseract.image_to_string(gray)
        
        # Process each line to find clues
        for line in text.split('\n'):
            # Look for pattern: number space number space colon space number
            parts = line.strip().split()
            if len(parts) >= 4 and parts[2] == ':':
                try:
                    clue_number = int(parts[0])
                    b = int(parts[1])
                    c = int(parts[3])
                    
                    # Find the cell with this clue number
                    cell = next((c for c in self.cells if c.clue_number == clue_number), None)
                    if cell:
                        # Determine if it's across, down, or both
                        direction = self.determine_clue_direction(cell)
                        if direction:
                            # Get the length of the clue
                            length = self.get_clue_length(cell, direction)
                            
                            # Create the clue
                            clue = Clue(
                                number=clue_number,
                                direction=direction,
                                length=length,
                                position=(cell.row, cell.col),
                                parameters=(length, b, c)  # a is the length of the clue
                            )
                            
                            # Add to appropriate direction list
                            if direction == 'BOTH':
                                self.clues['ACROSS'].append(clue)
                                self.clues['DOWN'].append(clue)
                            else:
                                self.clues[direction].append(clue)
                except ValueError:
                    continue  # Skip lines that don't match our pattern

    def create_crossword_grid(self) -> CrosswordGrid:
        """Create a CrosswordGrid object from the detected information."""
        grid = CrosswordGrid(self.grid_size)
        
        # Add undefined positions
        for cell in self.cells:
            if cell.is_black:
                grid.add_undefined_position(cell.row, cell.col)
        
        # Add clues
        for direction in ['ACROSS', 'DOWN']:
            for clue in self.clues[direction]:
                grid.add_clue(clue)
        
        return grid

    def show_detected_grid(self) -> None:
        """Display the detected grid with clue numbers and black cells."""
        # Create a copy of the grid image for visualization
        vis_image = self.grid_image.copy()
        
        # Draw grid lines
        for i in range(self.grid_size + 1):
            # Vertical lines
            cv2.line(vis_image, 
                    (i * self.cell_width, 0),
                    (i * self.cell_width, self.grid_image.shape[0]),
                    (0, 255, 0), 2)
            # Horizontal lines
            cv2.line(vis_image,
                    (0, i * self.cell_height),
                    (self.grid_image.shape[1], i * self.cell_height),
                    (0, 255, 0), 2)
        
        # Draw black cells and clue numbers
        for cell in self.cells:
            x1 = cell.col * self.cell_width
            y1 = cell.row * self.cell_height
            x2 = x1 + self.cell_width
            y2 = y1 + self.cell_height
            
            if cell.is_black:
                cv2.rectangle(vis_image, (x1, y1), (x2, y2), (0, 0, 0), -1)
            
            if cell.clue_number is not None:
                cv2.putText(vis_image,
                          str(cell.clue_number),
                          (x1 + 5, y1 + 20),
                          cv2.FONT_HERSHEY_SIMPLEX,
                          0.5,
                          (255, 0, 0),
                          1)
        
        # Show the image
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB))
        plt.title("Detected Grid Structure")
        plt.axis('off')
        plt.show()

    def show_detected_clues(self) -> None:
        """Display the detected clues in a readable format."""
        print("\nDetected Clues:")
        print("=" * 50)
        
        for direction in ['ACROSS', 'DOWN']:
            print(f"\n{direction} Clues:")
            print("-" * 30)
            
            # Sort clues by number
            sorted_clues = sorted(self.clues[direction], key=lambda x: x.number)
            
            for clue in sorted_clues:
                print(f"{clue.number}. ({clue.length} digits) b={clue.parameters[1]}, c={clue.parameters[2]}")
                print(f"   Position: ({clue.position[0]}, {clue.position[1]})")
                print(f"   Possible solutions: {len(clue.possible_solutions)}")
                print()

    def print_grid_ascii(self) -> None:
        """Print an ASCII representation of the grid."""
        print("\nGrid Structure:")
        print("=" * 50)
        
        # Print column numbers
        print("   ", end="")
        for col in range(self.grid_size):
            print(f"{col:2} ", end="")
        print("\n")
        
        for row in range(self.grid_size):
            print(f"{row:2} ", end="")
            for col in range(self.grid_size):
                cell = next((c for c in self.cells if c.row == row and c.col == col), None)
                if cell.is_black:
                    print(Fore.BLACK + "██ " + Style.RESET_ALL, end="")
                else:
                    clue_num = cell.clue_number if cell.clue_number is not None else " "
                    print(f"{clue_num:2} ", end="")
            print()

    def verify_detection(self) -> bool:
        """Show verification information and get user confirmation."""
        print("\nVerifying Detection Results:")
        print("=" * 50)
        
        # Show ASCII grid
        self.print_grid_ascii()
        
        # Show detected clues
        self.show_detected_clues()
        
        # Show visual grid
        self.show_detected_grid()
        
        # Get user confirmation
        while True:
            response = input("\nIs the detection correct? (y/n): ").lower()
            if response in ['y', 'n']:
                return response == 'y'
            print("Please enter 'y' or 'n'")

    def process_puzzle(self) -> Optional[CrosswordGrid]:
        """Process the puzzle image and return a CrosswordGrid object."""
        self.preprocess_image()
        self.detect_grid_structure()
        self.read_cell_numbers()
        self.detect_clue_numbers()
        self.extract_clues()
        
        # Verify detection
        if not self.verify_detection():
            print("\nPlease adjust the image and try again.")
            return None
        
        return self.create_crossword_grid()

def main():
    # Example usage
    reader = PuzzleReader('path_to_your_puzzle_image.jpg')
    grid = reader.process_puzzle()
    
    if grid:
        print("\nStarting puzzle solution...")
        if grid.solve():
            print("\nSolution found!")
            grid.print_grid()
        else:
            print("\nNo solution found.")

if __name__ == "__main__":
    main() 