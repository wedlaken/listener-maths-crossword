# Technical Documentation: Image Processing and Solution Testing

## Overview
This document explains how the Listener Maths Crossword solver processes images and converts them into manipulatable objects for solution testing. The process involves several stages of image processing, data structure creation, and solution validation.

## Image Processing Pipeline

### 1. Initial Image Processing
```python
def preprocess_image(self):
    # Convert to grayscale
    gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to get binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Find the grid contour
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
- **Purpose**: Prepares the image for grid detection
- **Steps**:
  1. Converts color image to grayscale
  2. Applies thresholding to create binary (black/white) image
  3. Uses OpenCV to find the grid's outline
- **Key Components**:
  - OpenCV (cv2) for image processing
  - Thresholding for binary conversion
  - Contour detection for grid identification

### 2. Grid Structure Detection
```python
def detect_grid_structure(self):
    # Create cells
    for row in range(self.grid_size):
        for col in range(self.grid_size):
            # Calculate cell boundaries
            x1 = col * self.cell_width
            y1 = row * self.cell_height
            # Check if cell is black
            cell_gray = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
            is_black = np.mean(cell_gray) < 128
```
- **Purpose**: Identifies individual cells and their properties
- **Steps**:
  1. Divides grid into 8x8 cells
  2. Calculates boundaries for each cell
  3. Determines if each cell is black (undefined) or white (for numbers)
- **Key Components**:
  - Cell size calculation
  - Color analysis for cell state
  - Grid structure preservation

## Data Structure Creation

### 1. CrosswordGrid Class
```python
class CrosswordGrid:
    def __init__(self, size: int = 8):
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.clues = {'ACROSS': [], 'DOWN': []}
        self.undefined_positions = set()
```
- **Purpose**: Creates a manipulatable representation of the crossword
- **Components**:
  1. 2D array for grid representation
  2. Separate lists for across and down clues
  3. Set of undefined (black) positions
- **Key Features**:
  - Easy access to grid positions
  - Organized clue storage
  - Efficient position tracking

## Solution Testing

### 1. Placement Validation
```python
def is_valid_placement(self, row: int, col: int, value: int) -> bool:
    # Convert value to string for digit-by-digit checking
    value_str = str(value)
    
    # Check if the value fits in the grid
    if col + len(value_str) > self.size:
        return False

    # Check if the value conflicts with existing numbers
    for i, digit in enumerate(value_str):
        current = self.grid[row][col + i]
        if current != 0 and current != int(digit):
            return False
```
- **Purpose**: Validates potential solutions
- **Steps**:
  1. Converts number to string for digit-by-digit checking
  2. Verifies the number fits within grid boundaries
  3. Checks for conflicts with existing numbers
- **Key Features**:
  - Boundary checking
  - Conflict detection
  - Digit-by-digit validation

## Process Flow
1. **Image → Binary Grid**
   - Color image converted to black and white
   - Grid outline detected
   - Cell boundaries identified

2. **Binary Grid → Cell Structure**
   - Each cell analyzed for state (black/white)
   - Cell positions and properties recorded
   - Grid structure preserved

3. **Cell Structure → CrosswordGrid Object**
   - 2D array created for grid representation
   - Clues organized by direction
   - Undefined positions tracked

4. **CrosswordGrid → Solution Testing**
   - Numbers checked for fit
   - Conflicts with existing numbers verified
   - Intersecting words validated

## Future Enhancements

### 1. Image Processing
- Improved grid detection for skewed images
- Better handling of poor lighting conditions
- Enhanced OCR accuracy

### 2. Data Structure
- More efficient clue storage
- Better handling of intersecting words
- Improved position tracking

### 3. Solution Testing
- Faster validation algorithms
- Better conflict detection
- More efficient backtracking

### 4. Anagram Transformation System
The final version of the puzzle requires an additional transformation layer:

#### Requirements
1. **Anagram Transformation**
   - Each clue solution must be rearranged into an anagram of itself
   - All digits from the original solution must be used
   - No new digits can be added
   - The anagram must still satisfy all crossword constraints

2. **Unclued Entries**
   - Four special entries in the middle of the grid:
     - 2 across entries
     - 2 down entries
   - These entries are not directly clued
   - They must be multiples of their original solutions
   - Must maintain anagram consistency with intersecting entries

#### Implementation Challenges
1. **Anagram Generation**
   - Need to generate all possible anagrams of each solution
   - Must maintain digit frequency
   - Must satisfy crossword constraints
   - Need efficient storage of anagram possibilities

2. **Unclued Entry Processing**
   - Need to identify unclued positions
   - Must calculate possible multiples
   - Must verify anagram consistency
   - Need to maintain grid constraints

3. **Validation System**
   - Need to verify anagram properties
   - Must check multiple relationships
   - Must maintain crossword consistency
   - Need to validate final solution

#### Proposed Solution Approach
1. **Anagram Generation**
   ```python
   def generate_anagrams(number: int) -> List[int]:
       # Convert number to list of digits
       # Generate all possible permutations
       # Filter valid anagrams
       # Return list of valid anagrams
   ```

2. **Unclued Entry Processing**
   ```python
   def process_unclued_entries(grid: CrosswordGrid) -> List[Tuple[int, int]]:
       # Identify unclued positions
       # Calculate possible multiples
       # Verify anagram consistency
       # Return valid solutions
   ```

3. **Final Solution Validation**
   ```python
   def validate_final_solution(grid: CrosswordGrid) -> bool:
       # Check anagram properties
       # Verify multiple relationships
       # Validate crossword consistency
       # Return validation result
   ```

## Notes
- This documentation should be updated as the code evolves
- New features and bug fixes should be documented here
- Performance improvements should be noted
- Any changes to the processing pipeline should be reflected in this document
- The anagram transformation system will require significant additional development 