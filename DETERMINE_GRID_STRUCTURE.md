# Grid Structure Determination Algorithm

## Requirements and Assumptions

### Input Requirements
- **Image file**: Tightly cropped grid (functionality to auto-crop insufficiently cropped images can be added later)
- **Grid size**: 8 × 8 cells (configurable constant for other puzzle types)
- **Clue numbers**: Present in grid cells, recognized and assigned cell numbers via OCR
- **Cell indexing**: Left to right, top to bottom, from 0 to 63 (consistent with computer indexing)

### Grid Structure Rules
- Each clue/solution has a unique tuple marking its position in the grid
- **ACROSS example**: `(0,1,2,3)` = 4-digit solution starting in top-left corner
- **DOWN example**: `(0,8,16)` = 3-digit solution starting in top-left corner
- **Constraint**: Each cell belongs to exactly 1 ACROSS clue and 1 DOWN clue
- **Storage**: Tuples stored in two separate lists (ACROSS and DOWN)

### Challenge
- **Clue boundaries**: Marked by thicker lines between cells in the grid image
- **Detection**: Need to identify these thicker boundaries programmatically

## Approach and Methodology

### Core Assumptions
1. **Cell 0**: Starting point for both clues 1 ACROSS and 1 DOWN
2. **Boundary detection**: 
   - **ACROSS clues**: Check right-side border thickness
   - **DOWN clues**: Check bottom border thickness
3. **Baseline establishment**: Use cell 0 as reference for "normal" border thickness

### Baseline Thickness Detection

#### Reference Point: Cell 0
- **Known fact**: Cell 0 will not have thick boundaries to the right or bottom
- **Sampling method**: 
  - Sample pixels within ±3% of the dividing line (x-coordinate) between cell 0 and cell 1
  - Extend sampling for 90% of cell height (avoid top/bottom border influence)
  - Compare characteristics with cell center
  - **Result**: Baseline description of simple, thin cell border

#### Threshold Determination
- Apply similar sampling to other cell borders
- Compare results with baseline
- Set threshold to best capture clue/solution boundaries
- **Validation**: Check visually during development and adjust threshold as needed

## Search Algorithm

### Row-by-Row Processing

#### ACROSS Clue Detection
1. **Starting points**: Begin at cells 0, 8, 16, etc. (leftmost cells of each row)
2. **Progression**: Move cell-by-cell to the right
3. **Boundary check**: Look for thick right border (end of clue/solution space)
4. **Tuple building**: Add each cell index to the current ACROSS tuple
5. **Termination**: Stop when thick border is reached or end of row (cells 7, 15, etc.)

#### DOWN Clue Detection
1. **Trigger**: When ACROSS clue ends, check next cell containing a clue number
2. **Validation**: Verify cell is not already in an ACROSS tuple (prevent overlaps)
3. **Assumption**: If not in ACROSS tuple, assume it's the start of a DOWN clue
4. **Processing**: Build DOWN tuple using similar boundary detection (bottom borders)

#### Iteration Logic
- **Return point**: After each clue ends, return to next cell containing a clue number
- **Direction**: Begin ACROSS search again from that cell
- **Continuation**: Repeat until all cells with clue numbers are processed

## Implementation Considerations

### Cell Indexing Standardization
- **Current code**: Uses 1-64 indexing
- **Proposed approach**: Uses 0-63 indexing
- **Action needed**: Standardize on one indexing system throughout

### Border Sampling Parameters
- **Sample width**: ±3% of dividing line
- **Sample height**: 90% of cell height
- **Threshold**: Dynamic adjustment based on visual validation

### Error Handling
- **OCR failures**: Plan for cases where clue numbers aren't detected
- **Boundary ambiguity**: Handle cases where border thickness is unclear
- **Overlap detection**: Robust checking to prevent invalid clue assignments

### Performance Optimization
- **Efficient sampling**: Optimize pixel sampling for speed
- **Caching**: Cache baseline measurements to avoid recalculation
- **Early termination**: Stop processing when all clues are found

## Expected Benefits

1. **Reliability**: Systematic approach reduces guesswork and errors
2. **Accuracy**: Direct boundary detection more reliable than pattern matching
3. **Maintainability**: Clear, step-by-step algorithm easier to debug and modify
4. **Scalability**: Framework can be adapted for different grid sizes and puzzle types
5. **Validation**: Built-in overlap prevention ensures grid consistency
