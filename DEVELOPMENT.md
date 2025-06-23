# Development Notes

## Project Setup

### Virtual Environment
- Each machine needs its own virtual environment
- Activate before working on the project:
  - MacBook: `source venv/bin/activate`
  - Windows: `.\venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

### Machine-Specific Notes

#### Windows PC
- Primary development machine
- Uses PowerShell (may need execution policy adjustment)
- If PowerShell restrictions occur:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

#### MacBook
- Secondary development machine
- Uses zsh shell
- No PowerShell restrictions

## Development Workflow

### Git Workflow
1. Always pull before starting work
2. Make changes
3. Commit with descriptive messages
4. Push to GitHub
5. On other machine, pull changes

### Package Management
- When adding new packages:
  1. Install in venv: `pip install <package-name>`
  2. Update requirements: `pip freeze > requirements.txt`
  3. Commit updated requirements.txt
  4. On other machine: `pip install -r requirements.txt`

## Project Context

### Key Components
1. `listener.py`: Core number-finding module
2. `crossword_solver.py`: Grid and solving logic
3. `puzzle_reader.py`: Image processing and OCR

### Architecture: Grid Parsing Components

#### `systematic_grid_parser.py` - Low-Level Grid Parser
**Purpose**: Core grid structure detection and clue boundary analysis
- **Input**: Grid image only
- **Process**: Detects thick borders, finds clue boundaries, maps cell indices
- **Output**: `ClueTuple` objects with cell positions (no clue parameters)
- **Key Features**: 
  - Uses ground truth border data for accuracy
  - 0-63 cell indexing system
  - Handles ACROSS/DOWN clue detection
  - Special case handling (e.g., Clue 1 in both directions)

#### `puzzle_reader.py` - High-Level Puzzle Interface
**Purpose**: Complete puzzle processing and data integration
- **Input**: Grid image + Clues image + Systematic parser results
- **Process**: Combines grid structure with clue parameters (b, c values)
- **Output**: Complete `ListenerClue` objects ready for solving
- **Key Features**:
  - Orchestrates the entire puzzle reading process
  - Integrates clue parameters from separate source
  - Converts to solver-compatible formats
  - Provides user-friendly output and visualization

#### Relationship Flow
```
Grid Image → systematic_grid_parser.py → ClueTuples (cell positions)
Clues Image → puzzle_reader.py → Clue parameters (b, c values)
                    ↓
            Complete ListenerClue objects
                    ↓
            crossword_solver.py
```

**Design Benefits**:
- **Modularity**: Grid parsing can be improved independently
- **Reusability**: Systematic parser can be used by other components
- **Testability**: Each component can be tested separately
- **Future-Proofing**: Easy to swap out grid parsing or clue reading methods

### Important Decisions
- Using OpenCV and Tesseract for OCR
- Using SymPy for prime number operations
- 8x8 grid structure

### Known Issues
- Image quality crucial for OCR accuracy
- Need good lighting for puzzle photos
- Tesseract installation required on both machines

## Development Tips
1. Test OCR with small sections first
2. Keep puzzle images in `images/` directory
3. Use high-resolution images (min 1200x1200)
4. Avoid OneDrive/iCloud sync issues by using GitHub

## Future Enhancements
1. Add support for different grid sizes
2. Implement parallel processing
3. Add graphical user interface
4. Add support for different clue formats
5. Implement solution verification

## Resources
- [OpenCV Documentation](https://docs.opencv.org/)
- [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract)
- [SymPy Documentation](https://docs.sympy.org/) 

## Daily Progress Log

### 2024-12-19: Systematic Grid Parser Development

#### Key Achievements
- **Developed systematic grid parser** (`systematic_grid_parser.py`) with ground truth border data
- **Achieved perfect clue detection**: 12 ACROSS + 12 DOWN clues (24 total)
- **Fixed Clue 1 DOWN detection**: Now correctly spans cells (0, 8, 16, 24)
- **Created border calibration tool** (`border_calibration.py`) for future image detection improvements
- **Maintained structure** for future automated image detection

#### Technical Details
- **Ground truth border data** integrated to bypass image detection issues
- **Cell indexing standardized** to 0-63 (left to right, top to bottom)
- **Separate ACROSS/DOWN tracking** allows cells to be in both directions
- **Special case handling** for Clue 1 (appears in both ACROSS and DOWN)
- **Cell-clue mapping** complete and accurate

#### Files Created/Modified
- `systematic_grid_parser.py` - Main parser with ground truth data
- `border_calibration.py` - Border threshold calibration tool
- `DETERMINE_GRID_STRUCTURE.md` - Detailed approach documentation
- `puzzle_reader.py` - Updated to use systematic parser
- Various archive and test files

#### Current Status
✅ **Grid structure parsing** complete and accurate  
✅ **Clue tuples** generated for all 24 clues  
✅ **Cell-clue relationships** mapped  
✅ **Clue parameters (b, c)** integrated from text file  
✅ **Complete clue objects** with positions, lengths, and parameters  
🔄 **Next phase**: Implement puzzle solver using complete clue data  

#### Lessons Learned
- Image-based border detection is challenging due to cropping irregularities
- Ground truth data provides reliable baseline for development
- Crossword logic requires careful handling of cell reuse (ACROSS + DOWN)
- Clue 1 special case (appears in both directions) requires specific handling
- Text-based clue extraction is more reliable than OCR for development

#### Next Steps
1. ✅ ~~Integrate clue text and parameters (b, c) from clue list~~ **COMPLETED**
2. ✅ ~~Create complete clue objects with all required data~~ **COMPLETED**
3. **Implement puzzle solver** using accurate clue tuples and parameters
4. **Test solver** with complete puzzle data
5. Later: Improve image-based border detection to match ground truth accuracy

### 2024-12-19: Backtracking Implementation

#### Key Achievements
- **Implemented comprehensive backtracking system** for puzzle solving
- **Added rejected solutions tracking** to prevent infinite loops
- **Created state snapshot/restoration** for complete backtracking
- **Developed constraint propagation** with intelligent clue selection
- **Fixed unclued clue handling** using b=0, c=0 special case

#### Technical Details
- **Rejected Solutions List**: `self.rejected_solutions` tracks eliminated solutions for potential restoration
- **State Snapshots**: Complete puzzle state can be saved/restored for backtracking
- **Tried Solutions Tracking**: `self.tried_solutions` prevents infinite loops in backtracking
- **Depth Limiting**: Maximum recursion depth prevents stack overflow
- **Smart Clue Selection**: Picks clues with fewest solutions for efficient backtracking

#### Files Created/Modified
- `crossword_solver.py` - Enhanced with backtracking capabilities
- `puzzle_integration.py` - Integrates systematic parser with solver
- `test_backtracking.py` - Comprehensive backtracking tests
- `test_simple_backtracking.py` - Simple backtracking verification

#### Current Status
✅ **Backtracking system** fully implemented and tested  
✅ **State management** working correctly  
✅ **Constraint propagation** solving many clues automatically  
✅ **Infinite loop prevention** working  
✅ **Unclued clue handling** implemented  
🔄 **Next phase**: Puzzle solution presentation and user interface  

#### Lessons Learned
- Backtracking requires careful state management to prevent infinite loops
- Rejected solutions tracking is essential for effective backtracking
- Constraint propagation can solve many clues without guessing
- Depth limiting is crucial for preventing stack overflow
- State snapshots must capture all relevant data for proper restoration

### 2024-12-19: Clue ID System and Strategic Solver Development

#### Key Achievements
- **Implemented unique clue ID system** (A1, D1, etc.) to prevent conflicts between ACROSS/DOWN clues
- **Fixed clue parameter conflicts** that were causing incorrect clue identification
- **Developed strategic solver approach** with phased solving like human solvers
- **Created comprehensive debugging tools** for clue object analysis
- **Achieved 41.7% puzzle completion** with 10/24 clues solved

#### Technical Details
- **Unique Clue IDs**: Changed from number-based to ID-based system (A1, D1, A4, D2, etc.)
- **Clue Parameter Loading**: Fixed to use (number, direction) tuples as keys
- **Strategic Solver Phases**:
  - Phase 1: Apply already-solved clues
  - Phase 2: Constraint propagation for single-solution clues
  - Phase 3: Backtracking at optimal checkpoints
- **Checkpoint Analysis**: Identifies best clues for backtracking based on solution count and impact
- **JSON Export System**: Complete clue object export for debugging and analysis

#### Files Created/Modified
- `crossword_solver.py` - Updated to use clue IDs instead of numbers
- `puzzle_integration.py` - Fixed clue parameter loading and integration
- `strategic_solver.py` - New phased solving approach
- `targeted_solver.py` - Focused solving with fewest solutions first
- `focused_solver.py` - Group-based solving approach
- `export_clues_json.py` - JSON export for debugging
- `debug_clue_parameters.py` - Clue parameter analysis tool

#### Current Status
✅ **Clue ID system** working correctly, no more conflicts  
✅ **Clue parameter loading** fixed and accurate  
✅ **Strategic solver** implemented with human-like approach  
✅ **Debugging tools** comprehensive and working  
✅ **41.7% completion** achieved (10/24 clues solved)  
🔄 **Next phase**: Improve checkpoint selection and conflict resolution  

#### Progress Summary
- **Solved clues**: A18=1024, A20=32, A22=2858, D5=2048, D17=2401, A11=1430
- **Grid cells filled**: 25/64 cells (39.1%)
- **Remaining challenges**: Several clues with 2-5 solutions need strategic choices
- **Unclued clues**: A12, A14, D7, D8 (900,000+ solutions each)

#### Lessons Learned
- Unique clue IDs are essential for handling ACROSS/DOWN conflicts
- Human-like strategic solving is more effective than brute force
- Checkpoint selection based on impact and solution count works well
- JSON export is invaluable for debugging complex clue relationships
- Constraint conflicts need better detection and resolution

#### Next Steps
1. **Improve conflict detection** in backtracking (A1=1215 created D2 conflict)
2. **Implement better checkpoint selection** prioritizing 2-solution clues
3. **Add conflict resolution** to automatically backtrack from failed paths
4. **Develop solution validation** to verify completed puzzle correctness
5. **Create user interface** for manual solving assistance
6. **Add progress visualization** showing grid state and remaining clues

#### Technical Debt
- Need better error handling for constraint conflicts
- Checkpoint selection algorithm could be more sophisticated
- JSON export could include more debugging information
- Strategic solver could benefit from machine learning approach 