# Listener Maths Crossword Solver
#### Video Demo: [URL HERE - To be added after video recording]
#### Description:

## Project Overview

The Listener Maths Crossword Solver is a sophisticated, production-ready web application that solves mathematical crossword puzzles using constraint satisfaction algorithms and real-time interactivity. What began as a command-line puzzle solver evolved into a full-stack web application demonstrating advanced programming concepts.

I've spoken about the benefits of working with AI tools in the video recorded for this submission and please read the VIDEO_SCRIPT.md in the root of this project in conjunction with this required file. I've allowed Cursor to put the bulk of this README together so as not to overlook some of the programming paradigms and frameworks we've used and many of the advanced programmatic techniques – especially in Pyhton and JavaScript – that I've wanted to explore and implement. I was keen that the fundamental structure of the programming had class objects at its heart and used multiple techniques to manipulate those objects and their states to meet the challenge of a quite sophisiticated puzzle posed by a human (Listener Crossword no.4869).

You will find a lot more detail about the challenges, changes to development direction and TODOs for future enhancements in the mutiple .md files in the document folders. 

## Key Features

### 🧩 Interactive Puzzle Solving
- **Real-time Constraint Propagation**: When you select a solution for one clue, the system automatically filters out incompatible solutions for intersecting clues
- **Visual Feedback**: Color-coded clues distinguish between user-selected solutions and algorithm-determined solutions
- **Undo/Redo System**: Complete solution history with selective restoration capabilities
- **Deselect Functionality**: Remove individual solutions and restore all possible options
- **Two-Stage Puzzle Experience**: Complete the initial mathematical puzzle, then tackle an anagram challenge where every entry must be an anagram of the original
- **Prime Factorization Workpad**: Interactive tool for exploring mathematical properties and understanding clue constraints

### 🔐 User Management & Persistence
- **User Registration & Authentication**: Email-based registration with secure password hashing
- **Automatic Progress Saving**: Real-time state persistence to SQLite database
- **Session Management**: Secure login/logout with session tracking
- **Cross-device Synchronization**: Access your progress from any device

### 🎯 Mathematical Problem Solving
- **Prime Factorization Algorithms**: Efficient algorithms for finding numbers with specific prime factor properties
- **Constraint Satisfaction**: Complex puzzle logic handling multiple intersecting mathematical constraints
- **Solution Optimization**: Smart filtering to reduce computational complexity

## Technical Architecture

### Backend (Python/Flask)
- **Flask Web Framework**: Complete web application with RESTful API endpoints
- **SQLAlchemy ORM**: Database abstraction layer for user accounts and puzzle state
- **SQLite Database**: Lightweight, file-based database for user data and progress tracking
- **Session Management**: Secure authentication with password hashing and session cookies

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Bootstrap framework ensuring compatibility across devices
- **Real-time Interactivity**: JavaScript-based constraint propagation and state management
- **AJAX Communication**: Asynchronous updates without page refreshes
- **Progressive State Management**: Automatic save/load functionality with user progress tracking
- **Unified Grid Interface**: Seamless transition between initial and anagram puzzle stages with consistent UI/UX
- **Mathematical Tools**: Interactive prime factorization workpad for educational exploration

### Mathematical Engine
- **Prime Number Algorithms**: Efficient prime factorization and property checking
- **Constraint Propagation**: Real-time filtering of valid solutions based on intersecting clues
- **Backtracking with State Management**: Sophisticated undo/redo system with state snapshots

## Strategic Development Approach

### Initial Vision vs. Practical Implementation
The project began with an ambitious vision of **automated puzzle parsing using OCR and computer vision**:
- **Original Goal**: Use OpenCV and Tesseract OCR to automatically detect grid structure and clue numbers
- **Technical Challenges**: OCR accuracy issues, image quality dependencies, cross-platform setup problems
- **Development Bottleneck**: Debugging OCR issues consumed significant development time

### Strategic Pivot to Ground Truth Data
The decision to transition to **ground truth data approach** proved to be a strategic success:
- **Manual Clue Parsing**: Clue parameters extracted from puzzle images using online tools
- **Hard-coded Grid Structure**: Border positions and clue numbers manually determined
- **Text-based Input**: Clue data stored in simple text files (`data/Listener 4869 clues.txt`)
- **Reliable Foundation**: Eliminated OCR dependencies for consistent, predictable behavior

### Benefits of Strategic Pivot
This transition enabled significant progress:
1. **Development Speed**: Focus shifted from OCR debugging to core algorithm development
2. **Learning Focus**: More time available for advanced programming concepts and web development
3. **Reliability**: 100% accurate data input, eliminating OCR errors
4. **Cross-Platform Consistency**: No dependency on system-specific OCR installations
5. **Maintainability**: Simple text files easier to modify and version control

## File Structure & Key Components

### Core Application Files
- **`app.py`**: Main Flask application with user authentication, database models, and API endpoints
- **`interactive_solver.py`**: Generates the interactive HTML interface with real-time constraint propagation and two-stage puzzle experience
- **`listener.py`**: Core mathematical algorithms for prime factorization and number property checking
- **`systematic_grid_parser.py`**: Ground truth data parser for grid structure and clue positions
- **`clue_classes.py`**: Advanced data structures for clue management and state tracking, including AnagramClue class for second-stage puzzle

### Data & Configuration
- **`data/Listener 4869 clues.txt`**: Ground truth clue parameters and puzzle data
- **`data/clue_parameters_4869.txt`**: Mathematical parameters for each clue
- **`instance/crossword_solver.db`**: SQLite database for user accounts and progress
- **`requirements.txt`**: Python dependencies for the project

### Development & Deployment
- **`dev_server.py`**: Development server with auto-reload and file watching
- **`config/Procfile`**: Production deployment configuration
- **`templates/`**: HTML templates for the web interface
- **`static/`**: CSS, JavaScript, and static assets

## Advanced Programming Concepts Implemented

### 1. Complex Algorithm Design
- **Constraint Propagation Algorithms**: Real-time filtering of valid solutions based on intersecting clues
- **Backtracking with State Management**: Sophisticated undo/redo system with state snapshots
- **Prime Factorization Logic**: Mathematical algorithms for finding numbers with specific prime factor properties
- **Real-time Solution Filtering**: Dynamic updating of valid solutions as the puzzle progresses
- **Anagram Generation Algorithms**: Permutation-based anagram generation with mathematical constraints for second-stage puzzle
- **Cross-Stage State Management**: Seamless transition between initial and anagram puzzle stages with progress tracking

### 2. Sophisticated Data Structures
- **Custom Clue Classes**: Advanced state tracking with original vs. current solution management
- **AnagramClue Class**: Specialized data structure for second-stage puzzle with anagram solution generation
- **Complex Grid Management**: Multi-dimensional grid systems with cell indexing and validation
- **JSON Serialization**: Efficient state persistence for database storage and restoration
- **Solution Set Management**: Optimized handling of large solution sets (up to 32 solutions per clue)
- **Cross-Stage Data Synchronization**: Separate state management for initial and anagram puzzle stages

### 3. Full-Stack Web Development
- **Flask Backend**: Complete web framework with SQLAlchemy ORM and user authentication
- **Interactive JavaScript Frontend**: Real-time communication between iframe and parent window
- **Database Integration**: SQLite with proper schema design for user accounts and puzzle state
- **Session Management**: Secure user authentication with password hashing and session tracking

## Learning Outcomes & CS50 Skills Demonstrated

### Technical Skills
✅ **Database Management** - SQLite with proper schema design and SQLAlchemy ORM  
✅ **User Authentication** - Secure password hashing, session management, and user registration  
✅ **Web Development** - Complete Flask application with HTML templates and static files  
✅ **JavaScript Programming** - Interactive frontend with real-time updates and state management  
✅ **Problem Solving** - Complex algorithmic thinking with mathematical constraints  
✅ **Code Organization** - Well-structured, maintainable code with proper separation of concerns  

### Strategic Decision Making
✅ **Adaptive Development** - Demonstrated ability to pivot when initial approaches prove challenging  
✅ **Risk Assessment** - Identifying and mitigating development bottlenecks early  
✅ **Iterative Development** - Starting simple and adding complexity as needed  
✅ **Documentation** - Clear documentation of decisions and their rationale  

## Interactive Solver

The main interactive solver can be run with:
```bash
python interactive_solver.py
```

**Note for Remote Environments (CS50 Codespace, etc.):**
- The solver will generate an HTML file and attempt to open it in a browser
- In remote environments, the browser may not open automatically due to environment limitations
- The HTML file (`interactive_solver.html`) will be created in the project directory
- You can manually open this file in your browser or use the Flask server version (see below)

### Flask Server Version (Recommended for CS50)
For better compatibility with remote environments, use the Flask server:
```bash
python app.py
```

**Access in CS50 Codespace:**
- The server runs on `http://127.0.0.1:5001`
- Use the **port forwarding** feature in VS Code to access the web interface
- Click on the port forwarding notification or check the "Ports" tab
- The application will open in your browser with full functionality

**Features:**
- User authentication (register/login)
- Interactive crossword solver
- Database persistence (SQLite/PostgreSQL)
- Anagram grid functionality
- Prime factor workpad
- Solution history and undo functionality

## Installation & Usage

### Local Development
1. Clone the repository: `git clone [repository-url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the development server: `python dev_server.py`
4. Open `http://localhost:5001` in your browser

### Production Deployment
The application is configured for deployment on platforms like Heroku, Railway, or Render:
- Database automatically created on first run
- Environment variables for configuration
- Static file serving configured
- Production-ready WSGI server

## Recent Enhancements & Future Development

### Recent Additions (Latest Development Session)
- **Two-Stage Puzzle Experience**: Complete anagram challenge after solving the initial mathematical puzzle
- **Prime Factorization Workpad**: Interactive mathematical exploration tool
- **Unified UI/UX**: Consistent interface across both puzzle stages with seamless transitions
- **Enhanced Progress Tracking**: Reset progress bar when transitioning to anagram stage
- **Improved Grammar**: Singular/plural display for solution counts ("1 solution" vs "2 solutions")

### Future Enhancements
While the current implementation uses ground truth data for reliability, the OCR infrastructure has been preserved for potential future enhancements:
- **Automated Puzzle Parsing**: Reintegration of OCR for automatic puzzle input
- **Multiple Puzzle Support**: Database schema supports multiple puzzle types
- **Advanced Analytics**: User solving patterns and statistics
- **Mobile Optimization**: Enhanced responsive design for mobile devices
- **Server Deployment**: Learning web hosting and deployment processes

## Conclusion

This project demonstrates not just basic web development skills, but the ability to build complex, real-world applications that combine multiple programming paradigms, mathematical problem-solving, and modern web technologies. It also shows **strategic thinking and adaptability** - the ability to recognize when initial approaches aren't working and pivot to more effective solutions.

The decision to input grid structure and clue data instead of OCR was a major change to the original concept but it allowed me to focus on core programming concepts and advanced features, resulting in an application that shows understanding of both theoretical concepts and practical implementation, and with greater attention to UX and game play.

**AI-Assisted Development Impact**: Working with Cursor on this project fundamentally changed my development approach and resulted in me thinking extensively about how I am likely to program 'in the wild' and therefore on how I want this graduation project to reflect realities that have changed dramatically even over the time since I started CS50 in 2023. I am not a dedicated programmer; I started an Edx course for some education in computer science while working on a startup venture)with the idea that I should at least understand what is possible, and have a better idea if someone I might hire knew what they were doing! I've seen how LLMs changed a lot in how people work and write from 2022's launch of ChatGPT and through the last year or so began to see the integration of those tools in programming. Arguably, the impact is even greater in programming than in natural human language, as its so much more about syntax and less about semantics and the available, contextual codebase is enormous. So, I scrapped my earlier attempts at my final project and started this. Instead of getting bogged down in syntax details and repetitive coding tasks, I saw that I could focus on architectural decisions, user experience design, and learning new technologies and programming techniques. I could explore advanced concepts like SQLAlchemy ORM, session management, and complex algorithmic thinking that I might not have attempted otherwise. Please look at the VIDEO_SCRIPT.md for some more thoughts on this.

The result of my time over the last couple of weeks is a sophisticated application that goes far beyond my initial intention, demonstrating both technical proficiency and strategic thinking in the 'new paradigm' of software development. I've learnt a huge amount and am glad that I prompted my development partner (Cursor) to document everything as we went along and update my learning points, so that I'll continue to learn from this project for weeks and months to come and to be inspired for even longer.

---