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
🔄 **Next phase**: Integrate clue text and parameters (b, c) from clue list  

#### Lessons Learned
- Image-based border detection is challenging due to cropping irregularities
- Ground truth data provides reliable baseline for development
- Crossword logic requires careful handling of cell reuse (ACROSS + DOWN)
- Clue 1 special case (appears in both directions) requires specific handling

#### Next Steps
1. Integrate clue text and parameters (b, c) from clue list
2. Create complete clue objects with all required data
3. Implement puzzle solver using accurate clue tuples
4. Later: Improve image-based border detection to match ground truth accuracy

#### Folder Organization (2024-12-19)
- **Created `archive/` folder**: Contains old versions of parsers and readers
- **Created `tests/` folder**: Contains all test files for better organization
- **Deleted redundant files**: `detected_clues_tuples.txt`, `generate_clues_file.py`
- **Removed `.DS_Store`**: macOS metadata file now properly ignored
- **Created `clue_parameters_4869.txt`**: Template for storing b, c parameters from online resource

#### Current File Structure
```
listener-maths-crossword/
├── Core files:
│   ├── systematic_grid_parser.py    # Main grid parser
│   ├── puzzle_reader.py             # Updated puzzle reader
│   ├── crossword_solver.py          # Puzzle solver
│   ├── listener.py                  # Core logic
│   └── border_calibration.py        # Border detection tool
├── Images:
│   ├── Listener grid 4869.png       # Puzzle grid
│   └── Listener 4869 clues.png      # Clues image
├── Data:
│   └── clue_parameters_4869.txt     # Template for clue parameters
├── Documentation:
│   ├── DEVELOPMENT.md               # This file
│   ├── DETERMINE_GRID_STRUCTURE.md  # Grid parsing approach
│   └── [other .md files]
├── archive/                         # Old versions
└── tests/                          # Test files
``` 