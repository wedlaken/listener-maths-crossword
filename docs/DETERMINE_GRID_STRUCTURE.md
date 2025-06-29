# Grid Structure Determination Algorithm

## Evolution: From OCR to Ground Truth Data

### Initial Approach: OCR and Image Processing
The project initially attempted to use **OpenCV and Tesseract OCR** to automatically detect grid structure and clue numbers from puzzle images. This approach involved:

- **Image Processing**: OpenCV for grid detection and cell boundary identification
- **OCR Detection**: Tesseract for reading clue numbers from grid cells
- **Dynamic Border Detection**: Algorithmic identification of thick borders between clues
- **Automated Parsing**: Computer vision techniques to extract puzzle structure

### Challenges with OCR Approach
During development, several reliability issues emerged:

1. **OCR Accuracy**: Tesseract struggled with small, printed numbers in grid cells
2. **Image Quality Dependencies**: Results varied significantly based on image resolution and lighting
3. **Border Detection Complexity**: Algorithmic detection of thick borders was inconsistent
4. **Development Bottleneck**: Debugging OCR issues consumed significant development time
5. **Cross-Platform Issues**: OCR setup and dependencies varied across development environments

### Strategic Decision: Ground Truth Data
To maintain project momentum and focus on core algorithmic development, the decision was made to **transition to ground truth data**:

- **Manual Clue Parsing**: Clue parameters manually extracted from puzzle images using online tools
- **Hard-coded Grid Structure**: Border positions and clue numbers manually determined and hard-coded
- **Text-based Input**: Clue data stored in simple text files (`data/Listener 4869 clues.txt`)
- **Reliable Foundation**: Eliminated OCR dependencies for consistent, predictable behavior

### Benefits of Ground Truth Approach
This transition provided significant advantages:

1. **Reliability**: 100% accurate data input, eliminating OCR errors
2. **Development Speed**: Focus shifted from debugging OCR to core algorithm development
3. **Cross-Platform Consistency**: No dependency on system-specific OCR installations
4. **Maintainability**: Simple text files easier to modify and version control
5. **Learning Focus**: More time available for advanced programming concepts and web development

## Current Implementation: Ground Truth Data

### Input Requirements
- **Text file**: `data/Listener 4869 clues.txt` - Manually parsed clue parameters
- **Hard-coded grid structure**: Border positions and clue numbers in `systematic_grid_parser.py`
- **Grid size**: 8 × 8 cells (configurable constant for other puzzle types)
- **Cell indexing**: Left to right, top to bottom, from 0 to 63 (consistent with computer indexing)

### Grid Structure Rules
- Each clue/solution has a unique tuple marking its position in the grid
- **ACROSS example**: `(0,1,2,3)` = 4-digit solution starting in top-left corner
- **DOWN example**: `(0,8,16)` = 3-digit solution starting in top-left corner
- **Constraint**: Each cell belongs to exactly 1 ACROSS clue and 1 DOWN clue
- **Storage**: Tuples stored in two separate lists (ACROSS and DOWN)

### Ground Truth Data Sources

#### 1. Clue Parameters (`data/Listener 4869 clues.txt`)
```
Across
1 6:2
4 3:69
9 5:1
...
Down
1 4:16 
2 2:2
3 10:1
...
```

#### 2. Border Positions (Hard-coded in `systematic_grid_parser.py`)
```python
# Ground truth border data from user
self.thick_right_borders = {3, 8, 9, 10, 11, 12, 13, 19, 24, 30, 32, 38, 43, 49, 50, 51, 52, 53, 54, 59}
self.thick_bottom_borders = {3, 4, 6, 9, 14, 17, 22, 24, 25, 26, 29, 30, 31, 33, 38, 41, 46, 49, 51, 52}
```

#### 3. Clue Number Positions (Hard-coded)
```python
detected_numbers = {
    1: 0,   # Clue 1 in cell 0
    2: 1,   # Clue 2 in cell 1
    3: 2,   # Clue 3 in cell 2
    # ... etc
}
```

## Implementation Approach

### Core Assumptions
1. **Cell 0**: Starting point for both clues 1 ACROSS and 1 DOWN
2. **Ground truth borders**: Pre-determined thick border positions
3. **Manual clue parsing**: Clue parameters extracted manually from puzzle images

### Grid Structure Detection

#### Step 1: Load Ground Truth Data
```python
def __init__(self, grid_image_path: str, clues_image_path: str = None):
    # Ground truth border data from user
    self.thick_right_borders = {3, 8, 9, 10, 11, 12, 13, 19, 24, 30, 32, 38, 43, 49, 50, 51, 52, 53, 54, 59}
    self.thick_bottom_borders = {3, 4, 6, 9, 14, 17, 22, 24, 25, 26, 29, 30, 31, 33, 38, 41, 46, 49, 51, 52}
```

#### Step 2: Hard-coded Clue Number Detection
```python
def detect_clue_numbers_ocr(self) -> Dict[int, int]:
    # Updated mapping based on visual review of the actual puzzle
    detected_numbers = {
        1: 0,   # Clue 1 in cell 0
        2: 1,   # Clue 2 in cell 1
        3: 2,   # Clue 3 in cell 2
        # ... etc
    }
```

#### Step 3: Border Detection Using Ground Truth
```python
def is_thick_border(self, cell_index: int, direction: str) -> bool:
    # Use ground truth border data
    if direction == 'right':
        return cell_index in self.thick_right_borders
    elif direction == 'bottom':
        return cell_index in self.thick_bottom_borders
```

## Search Algorithm

### Row-by-Row Processing

#### ACROSS Clue Detection
1. **Starting points**: Begin at cells 0, 8, 16, etc. (leftmost cells of each row)
2. **Progression**: Move cell-by-cell to the right
3. **Boundary check**: Use ground truth data for thick right borders
4. **Tuple building**: Add each cell index to the current ACROSS tuple
5. **Termination**: Stop when thick border is reached or end of row (cells 7, 15, etc.)

#### DOWN Clue Detection
1. **Trigger**: When ACROSS clue ends, check next cell containing a clue number
2. **Validation**: Verify cell is not already in an ACROSS tuple (prevent overlaps)
3. **Assumption**: If not in ACROSS tuple, assume it's the start of a DOWN clue
4. **Processing**: Build DOWN tuple using ground truth border data (bottom borders)

## Future Development: OCR Reintegration

### Planned OCR Improvements
While the current implementation uses ground truth data, the framework remains in place for future OCR integration:

1. **Enhanced OCR Accuracy**: Improved Tesseract parameters and preprocessing
2. **Better Image Processing**: Advanced OpenCV techniques for grid detection
3. **Machine Learning**: Potential use of ML models for better number recognition
4. **Hybrid Approach**: Combine OCR with ground truth validation

### Current OCR Infrastructure
The following components remain available for future OCR development:

- **Image loading**: OpenCV image processing capabilities
- **Grid detection**: Contour detection and cell boundary identification
- **Border analysis**: Thickness measurement algorithms
- **OCR integration**: Tesseract setup and configuration

## Expected Benefits

1. **Reliability**: Ground truth data provides 100% accuracy
2. **Development Speed**: Focus on core algorithms rather than OCR debugging
3. **Maintainability**: Simple text-based data sources
4. **Learning Value**: More time for advanced programming concepts
5. **Future-Ready**: Framework supports OCR reintegration when needed

## Lessons Learned

### OCR Challenges
- **Accuracy vs. Development Time**: OCR accuracy improvements require significant development investment
- **Cross-Platform Dependencies**: OCR libraries can be problematic across different systems
- **Image Quality Requirements**: OCR performance heavily depends on input image quality

### Strategic Decision Making
- **Pragmatic Approach**: Sometimes simpler solutions enable faster progress
- **Learning Focus**: Ground truth data allowed focus on advanced programming concepts
- **Future Planning**: Maintained OCR infrastructure for potential future use

### Project Management
- **Iterative Development**: Start simple, add complexity as needed
- **Risk Management**: Identify and mitigate development bottlenecks early
- **Documentation**: Clear documentation of decisions and their rationale
