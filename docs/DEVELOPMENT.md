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
3. `systematic_grid_parser.py`: Grid structure parsing (now uses ground truth data)
4. `app.py`: Flask web application (MAIN ENTRY POINT)
5. `interactive_solver.py`: Interactive solving interface
6. `dev_server.py`: Development server with auto-reload

### Architecture: Web Application Components

#### `app.py` - Flask Web Application
**Purpose**: Main web application with user authentication and database persistence
- **Features**: User registration/login, session management, API endpoints
- **Database**: SQLite with SQLAlchemy ORM (stored in `instance/crossword_solver.db`)
- **API Endpoints**: Save/load puzzle state, user authentication
- **Templates**: HTML templates for web interface

#### `interactive_solver.py` - Interactive Solving Engine
**Purpose**: Core interactive puzzle solving with constraint propagation
- **Features**: Real-time constraint propagation, solution selection, undo/deselect
- **Interface**: HTML generation with JavaScript interactivity
- **State Management**: Tracks solving history and user selections

#### `dev_server.py` - Development Server
**Purpose**: Auto-reloading development server (similar to nodemon)
- **Features**: File watching, automatic restart on changes
- **Usage**: `python dev_server.py` for development

### Architecture Flow
```
User Request → Flask (app.py) → Interactive Solver → Database
                    ↓
            HTML Templates + JavaScript
                    ↓
            Real-time Constraint Propagation
```

## Strategic Decision: From OCR to Ground Truth Data

### Initial Approach: OCR and Image Processing
The project began with an ambitious approach using **OpenCV and Tesseract OCR** for automated puzzle parsing:

- **Image Processing**: OpenCV for grid detection and cell boundary identification
- **OCR Detection**: Tesseract for reading clue numbers from grid cells
- **Dynamic Border Detection**: Algorithmic identification of thick borders between clues
- **Automated Parsing**: Computer vision techniques to extract puzzle structure

### OCR Challenges Encountered
During development, several significant challenges emerged:

1. **OCR Accuracy Issues**: Tesseract struggled with small, printed numbers in grid cells
2. **Image Quality Dependencies**: Results varied significantly based on image resolution and lighting
3. **Border Detection Complexity**: Algorithmic detection of thick borders was inconsistent
4. **Development Bottleneck**: Debugging OCR issues consumed significant development time
5. **Cross-Platform Issues**: OCR setup and dependencies varied across development environments
6. **Learning Focus**: OCR debugging was taking time away from core programming concepts

### Strategic Transition: Ground Truth Data
To maintain project momentum and focus on core algorithmic development, the decision was made to **transition to ground truth data**:

#### What Changed
- **Manual Clue Parsing**: Clue parameters manually extracted from puzzle images using online tools
- **Hard-coded Grid Structure**: Border positions and clue numbers manually determined and hard-coded
- **Text-based Input**: Clue data stored in simple text files (`data/Listener 4869 clues.txt`)
- **Reliable Foundation**: Eliminated OCR dependencies for consistent, predictable behavior

#### Benefits Achieved
1. **Reliability**: 100% accurate data input, eliminating OCR errors
2. **Development Speed**: Focus shifted from debugging OCR to core algorithm development
3. **Cross-Platform Consistency**: No dependency on system-specific OCR installations
4. **Maintainability**: Simple text files easier to modify and version control
5. **Learning Focus**: More time available for advanced programming concepts and web development

#### Current Data Sources
- **`data/Listener 4869 clues.txt`**: Manually parsed clue parameters in b:c format
- **`systematic_grid_parser.py`**: Hard-coded border positions and clue number locations
- **Ground truth validation**: All puzzle data verified manually for accuracy

### Future OCR Development
While the current implementation uses ground truth data, the framework remains in place for future OCR integration:

- **OCR Infrastructure**: OpenCV and Tesseract setup maintained for future use
- **Image Processing**: Grid detection algorithms preserved
- **Hybrid Approach**: Potential to combine OCR with ground truth validation
- **Machine Learning**: Future possibility of ML-enhanced number recognition

## Development Tips
1. **Always activate virtual environment** before running the application
2. **Use development server** (`python dev_server.py`) for auto-reload during development
3. **Database location**: `instance/crossword_solver.db` (Flask default)
4. **Test user registration** and login flow regularly
5. **Check browser console** for JavaScript errors and API communication
6. **Ground truth data**: Verify clue parameters in `data/Listener 4869 clues.txt` for accuracy

## Daily Progress Log

### 2025-06-27: Documentation Update - OCR to Ground Truth Transition

#### Key Achievements
- **✅ DOCUMENTED**: Strategic transition from OCR to ground truth data approach
- **✅ UPDATED**: Development notes to reflect current implementation
- **✅ CLARIFIED**: Project architecture and data flow
- **✅ PRESERVED**: OCR infrastructure for future development

#### Technical Details
- **Ground Truth Data**: Manual parsing of clue parameters from puzzle images
- **Hard-coded Structure**: Border positions and clue numbers in systematic_grid_parser.py
- **Text-based Input**: Simple, reliable data sources in data/ directory
- **OCR Framework**: Maintained for potential future reintegration

#### Files Modified
- `docs/DETERMINE_GRID_STRUCTURE.md` - Updated to reflect ground truth approach
- `docs/DEVELOPMENT.md` - Added strategic decision documentation
- `docs/PROJECT_STATUS.md` - Updated to reflect current implementation

#### Current Status
✅ **Ground truth data** approach working reliably  
✅ **Development speed** significantly improved  
✅ **Learning focus** shifted to advanced programming concepts  
✅ **OCR infrastructure** preserved for future development  
🔄 **Next phase**: Continue with web application enhancements  

#### Lessons Learned
- **Strategic Decision Making**: Sometimes simpler solutions enable faster progress
- **Development Bottlenecks**: Identify and mitigate technical challenges early
- **Learning Priorities**: Focus on core programming concepts over peripheral technologies
- **Future Planning**: Maintain infrastructure for potential future enhancements
- **Documentation**: Clear documentation of decisions and their rationale

### 2025-06-26: Web Application Completion & Database Integration

#### Key Achievements
- **✅ COMPLETED**: Full-stack web application with Flask backend
- **✅ COMPLETED**: User authentication system (registration/login)
- **✅ COMPLETED**: SQLite database with SQLAlchemy ORM
- **✅ COMPLETED**: Interactive solver with real-time constraint propagation
- **✅ COMPLETED**: Save/load functionality with automatic progress persistence
- **✅ COMPLETED**: Undo/deselect features for backtracking
- **✅ COMPLETED**: Development server with auto-reload
- **✅ COMPLETED**: Deployment configuration (Heroku, Railway, Render)

#### Technical Details
- **Database Schema**: Users table + PuzzleSessions table for state persistence
- **API Communication**: Parent page ↔ iframe ↔ Flask backend
- **State Management**: JSON serialization for database storage
- **User Sessions**: Flask-Login for secure session management
- **Auto-reload**: Watchdog-based file monitoring for development

#### Files Created/Modified
- `app.py` - Complete Flask web application
- `dev_server.py` - Development server with auto-reload
- `templates/` - HTML templates for web interface
- `static/interactive_solver.html` - Interactive solver interface
- `requirements.txt` - Updated with Flask dependencies
- `Procfile` - Heroku deployment configuration

#### Current Status
✅ **PRODUCTION READY** - Full web application with all features  
✅ **Database persistence** working correctly  
✅ **User authentication** fully functional  
✅ **Interactive solving** with constraint propagation  
✅ **Save/load functionality** automatic and reliable  
✅ **Deployment ready** for multiple platforms  

#### Next Steps
1. **Deploy to production** (Heroku recommended for CS50)
2. **Add more puzzles** for variety
3. **User management features** (password reset, profiles)
4. **Analytics and statistics** for solving patterns

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

## Future Enhancements
1. **Mobile optimization** - Better touch interface
2. **Social features** - Share solutions, leaderboards
3. **Advanced solving** - AI hints, difficulty levels
4. **Puzzle creation** - Tools for creating new puzzles
5. **Export features** - PDF solutions, progress reports

## Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract)
- [SymPy Documentation](https://docs.sympy.org/) 