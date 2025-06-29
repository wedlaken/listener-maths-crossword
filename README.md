# Listener Maths Crossword Solver

A sophisticated web application for solving mathematical crossword puzzles, built as a CS50 Final Project.

## 🚀 Quick Start

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python -c "from app import app; app.run(debug=True, port=5001)"

# Access at http://localhost:5001
```

## 📁 Project Structure

```
listener-maths-crossword/
├── 🎯 CORE APPLICATION (Root Level)
│   ├── app.py                     # Main Flask web application
│   ├── dev_server.py              # Development server
│   ├── interactive_solver.py      # Core interactive solver logic
│   ├── crossword_solver.py        # Backtracking solver
│   ├── systematic_grid_parser.py  # Grid structure parsing
│   ├── clue_classes.py            # Clue management
│   ├── listener.py                # Mathematical solving
│   ├── requirements.txt           # Dependencies
│   └── README.md                  # Main project overview
│
├── 📁 docs/                       # Detailed documentation
├── 📁 scripts/                    # Utility scripts
├── 📁 tests/                      # Test suite
├── 📁 data/                       # Puzzle data files
├── 📁 experimental/               # Alternative solver approaches & development artifacts
├── 📁 web/                        # Web interface (templates/ & static/)
└── 📁 config/                     # Configuration files
```

## 🎮 Features

- **Interactive Web Interface** - Solve puzzles in your browser
- **User Authentication** - Register and save progress
- **Real-time Constraint Propagation** - See how your choices affect other clues
- **Undo/Redo Functionality** - Explore different solving paths
- **Database Persistence** - Progress saved automatically
- **Mathematical Puzzle Solving** - Advanced algorithms for number theory problems

## 📚 Documentation

- **[Project Overview](docs/README.md)** - Comprehensive project documentation
- **[Current Status](docs/PROJECT_STATUS.md)** - Development status and features
- **[Deployment Guide](docs/DEPLOYMENT.md)** - How to deploy to production
- **[Development Setup](docs/DEVELOPMENT.md)** - Development environment setup
- **[Technical Details](docs/TECHNICAL_DOCUMENTATION.md)** - Architecture and algorithms

## 🎓 CS50 Project Requirements

This project demonstrates:
- **Python** - Backend logic and mathematical solving
- **JavaScript** - Frontend interactivity
- **HTML/CSS** - Web interface with Bootstrap
- **SQL** - Database management with SQLAlchemy
- **Advanced Concepts** - User authentication, real-time updates, constraint satisfaction algorithms

## 🔧 Development

For detailed development information, see the [Development Guide](docs/DEVELOPMENT.md).

## 📄 License

This project was created for CS50 Final Project submission.

## Project Structure Notes

- The main application is now fully interactive and human-guided.
- **Legacy code:** The original automatic solver (`crossword_solver.py`) has been moved to the `experimental/` folder for reference only. It is not part of the main application and is no longer maintained.
- All current logic and clue management is handled by `clue_classes.py` and the interactive solver. 