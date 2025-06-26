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

### 2024-12-19: Interactive Solver Enhancements - Deselect & Cleanup

#### Key Achievements
- **Implemented deselect functionality** allowing users to remove individual solutions and restore original possibilities
- **Removed JSON dependencies** - solver now uses pure object-based approach with stored original solutions
- **Enhanced visual distinction** between user-selected solutions (blue) and algorithm-determined solutions (teal)
- **Fixed variable naming conflicts** in JavaScript constraint recalculation functions
- **Maintained undo functionality** while adding targeted deselect capability

#### Technical Details
- **Deselect Dialog**: Yellow-themed confirmation dialog with "Deselect Solution" and "Cancel" buttons
- **Smart Cell Handling**: Deselecting only removes cells not used by other user-selected clues
- **Original Solution Storage**: Stores initial solutions at initialization for reliable restoration
- **Visual Feedback**: 
  - User-selected solutions: Blue background with blue left border
  - Algorithm-solved clues: Teal background with teal left border
  - Multiple solutions: Yellow background (unchanged)
- **Accurate Solution Counts**: Shows actual remaining solutions, not just "1" when user has selected something

#### Files Modified
- `interactive_solver.py` - Added deselect functionality, removed JSON dependencies, enhanced styling
- `interactive_solver.html` - Generated updated interface with new features

#### Current Status
✅ **Deselect functionality** working correctly  
✅ **JSON dependencies removed** - pure object-based approach  
✅ **Visual distinction** between solution types implemented  
✅ **Undo system** maintained and enhanced  
✅ **Smart backtracking** allowing selective solution removal  
🔄 **Next phase**: User registration and progress saving  

#### Lessons Learned
- **Variable naming conflicts** in JavaScript can silently break functionality
- **Object-based approach** is more reliable than external file dependencies
- **User experience** benefits from both targeted deselect and full undo capabilities
- **Visual feedback** helps users understand the difference between their choices and algorithmic determinations
- **State management** requires careful tracking of original vs. current solutions

#### Next Steps
1. **User registration system** for personalized solving sessions
2. **Progress saving/loading** to persist solving state across sessions
3. **Puzzle state database** to store user progress and solution history
4. **Multi-user support** for collaborative solving or competition
5. **Analytics and statistics** to track solving patterns and difficulty assessment

### 2024-12-19: Interactive Solver Development

#### Key Achievements
- **Developed interactive crossword solver** (`interactive_solver.py`) for human-guided solving
- **Fixed unclued clue handling** to prevent massive 900,000 solution sets
- **Created hybrid interface** with dropdowns for clued clues and input boxes for unclued clues
- **Implemented real-time solution counting** showing current valid solutions for each clue
- **Built responsive HTML interface** with clickable clues and solution selection

#### Technical Details
- **Unclued Clue Optimization**: Modified `clue_classes.py` to initialize unclued clues with empty solution sets instead of all possible numbers
- **Constraint-Based Population**: Unclued clues only get populated with solutions when constraints are first applied
- **Hybrid UI Design**: 
  - Clued clues: Dropdown menus with pre-computed valid solutions
  - Unclued clues: Text input boxes for manual entry
- **Real-Time Updates**: Solution counts reflect current valid solutions after constraint propagation
- **Event Handling**: JavaScript manages both dropdown and input interactions

#### Files Created/Modified
- `interactive_solver.py` - Complete interactive solver with HTML generation
- `clue_classes.py` - Enhanced with proper unclued clue handling
- `interactive_solver.html` - Generated interactive interface
- Removed redundant files: `puzzle_solution_export.txt`, `debug_grid_issues.py`, etc.

#### Current Status
✅ **Interactive solver** fully functional with modern UI  
✅ **Unclued clue optimization** preventing massive data structures  
✅ **Hybrid interface** supporting both clue types  
✅ **Real-time solution counting** working correctly  
🔄 **Next phase**: Implement constraint propagation and grid updates  

#### Lessons Learned
- **Data Structure Efficiency**: Unclued clues should start empty and populate on-demand
- **User Experience**: Different clue types need different interaction patterns
- **Constraint Propagation**: Real-time updates require careful state management
- **Code Reuse**: Interactive solver benefits from automated solver's clue classes
- **Performance**: Avoiding 900,000 solution sets is crucial for responsiveness

#### Next Steps
1. **Implement constraint propagation** when solutions are applied
2. **Add grid visualization updates** to show placed solutions
3. **Create solution validation** for unclued clue inputs
4. **Add undo/redo functionality** for interactive solving
5. **Implement save/load puzzle state** for session persistence

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

## Project Evolution: Two Parallel Approaches

### Automated Solver (Backtracking-Based)
**Purpose**: Fully automated puzzle solving using constraint propagation and backtracking
**Key Features**:
- Systematic constraint propagation
- Intelligent backtracking with state management
- Complete puzzle solution without human intervention
- Performance optimization for large solution spaces

**Current Status**: Core backtracking implemented, needs integration with systematic parser

### Interactive Solver (Human-Guided)
**Purpose**: Human-guided solving with real-time constraint feedback
**Key Features**:
- Clickable clue interface with solution selection
- Real-time solution counting and validation
- Hybrid UI for different clue types (dropdowns + input boxes)
- Visual grid representation with solution placement

**Current Status**: UI complete, needs constraint propagation implementation

### Cross-Pollination Benefits
- **Shared Clue Classes**: Both approaches use the same `ListenerClue` and `ClueManager` classes
- **Constraint Logic**: Interactive solver can leverage automated solver's constraint propagation
- **State Management**: Both benefit from efficient solution tracking and validation
- **Performance Lessons**: Interactive solver learned from automated solver's data structure optimizations

### Future Integration Opportunities
1. **Hybrid Solving**: Combine automated constraint propagation with human decision-making
2. **Hint System**: Use automated solver to suggest next best moves
3. **Validation**: Use automated solver to verify human solutions
4. **Learning**: Analyze human solving patterns to improve automated algorithms 