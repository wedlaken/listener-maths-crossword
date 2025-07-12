# Interactive Crossword Solver - CS50 Final Project

An intelligent, interactive crossword solver that helps users solve complex mathematical crosswords through constraint propagation and real-time feedback. Built for Harvard CS50 Final Project demonstrating full-stack web development skills.

## 🎯 Project Overview

This project demonstrates advanced web development concepts including:
- **Database Management**: SQLite with SQLAlchemy ORM
- **User Authentication**: Email/password registration and login
- **State Persistence**: Save/load puzzle solving progress
- **Full-Stack Development**: Flask backend + HTML/CSS/JavaScript frontend
- **Real-time Interaction**: Interactive crossword solving with constraint propagation
- **Modern Web Technologies**: Bootstrap, AJAX, JSON APIs

## 🚀 Features

### Core Solver Features
- **Interactive Grid**: Click cells to input values with real-time validation
- **Smart Constraint Propagation**: Automatically updates possible solutions based on crossing clues
- **Solution Selection**: Choose from multiple possible solutions for each clue
- **Undo Functionality**: Step back through your solving history
- **Deselect Feature**: Remove applied solutions and restore original possibilities
- **Visual Feedback**: Different colors for user-selected vs. algorithm-suggested clues

### Web Application Features
- **User Registration & Login**: Email-based authentication system
- **Progress Saving**: Automatically save your solving progress
- **Cross-Device Access**: Access your progress from any device
- **Responsive Design**: Works on desktop and mobile devices
- **Session Management**: Secure user sessions with Flask

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core application logic
- **Flask 2.3.3**: Web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (stored in `instance/crossword_solver.db`)
- **SymPy**: Mathematical expression solving
- **OpenCV**: Image processing for puzzle parsing

### Frontend
- **HTML5/CSS3**: Structure and styling
- **JavaScript (ES6+)**: Interactive functionality
- **Bootstrap 5**: Responsive UI framework
- **AJAX**: Asynchronous communication with backend

### Development Tools
- **Git**: Version control
- **Virtual Environment**: Python dependency management
- **Requirements.txt**: Dependency specification

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/listener-maths-crossword.git
   cd listener-maths-crossword
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   # For development (with auto-reload):
   python dev_server.py
   
   # For production:
   python app.py
   ```

5. **Access the Application**
   - Open your browser and go to `http://localhost:5001`
   - Register a new account or log in
   - Start solving the crossword!

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Puzzle Sessions Table
```sql
CREATE TABLE puzzle_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    puzzle_id TEXT NOT NULL,
    solved_cells TEXT,        -- JSON string
    user_selected_solutions TEXT, -- JSON string
    solution_history TEXT,    -- JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Note**: The database file is automatically created in the `instance/` directory when you first run the application. This is Flask's default location for instance-specific files.

## 🌐 Deployment

### Quick Deployment Options

#### Heroku (Recommended for CS50)
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-crossword-solver

# Add Python buildpack
heroku buildpacks:add heroku/python

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here

# Deploy
git add .
git commit -m "Add Flask web application"
git push heroku main

# Open the app
heroku open
```

#### Railway
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

#### Render
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`
4. Deploy

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🎮 How to Use

### Getting Started
1. **Register/Login**: Create an account or log in to save your progress
2. **Start Solving**: The interactive grid will load with the Listener 4869 puzzle
3. **Select Clues**: Click on clues in the list to see possible solutions
4. **Apply Solutions**: Choose a solution to apply it to the grid
5. **Save Progress**: Your progress is automatically saved as you solve

### Advanced Features
- **Undo**: Click the undo button to step back through your moves
- **Deselect**: Remove applied solutions to explore different paths
- **Constraint Propagation**: Watch as the system automatically updates possible solutions
- **Visual Feedback**: User-selected clues are highlighted differently

## 📁 Project Structure

```
listener-maths-crossword/
├── app.py                     # Flask web application (MAIN ENTRY POINT)
├── dev_server.py              # Development server with auto-reload
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Landing page
│   ├── register.html         # Registration
│   ├── login.html            # Login
│   └── solver.html           # Main solver interface
├── static/                   # Static files
│   └── interactive_solver.html  # Interactive solver
├── interactive_solver.py     # Core solver logic
├── clue_classes.py           # Clue management
├── crossword_solver.py       # Original solver
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment config
├── DEPLOYMENT.md             # Deployment guide
├── PROJECT_STATUS.md         # Current project status
└── README.md                 # This file
```

## 🧪 Testing

### Manual Testing
1. **Registration Flow**: Test user registration and login
2. **Puzzle Solving**: Complete a few clues and verify state persistence
3. **Undo/Deselect**: Test backtracking functionality
4. **Cross-Device**: Access from different browsers/devices

### Automated Testing
```bash
# Run tests (if available)
python -m pytest tests/

# Test database functionality
python test_db.py
```

## 🤝 Contributing

This is a CS50 Final Project, but contributions and feedback are welcome!

## 📄 License

This project is created for educational purposes as part of Harvard CS50.

## 🎓 CS50 Project Requirements

This project demonstrates understanding of:

### Programming Languages
- **Python**: Backend logic, mathematical solving
- **JavaScript**: Frontend interactivity
- **HTML/CSS**: Web interface
- **SQL**: Database queries

### Frameworks & Technologies
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Bootstrap**: UI framework
- **AJAX**: Asynchronous communication

### Concepts
- **Database Management**: SQLite with proper schema design
- **User Authentication**: Secure login system
- **State Persistence**: Save/load functionality
- **Full-Stack Development**: Complete web application
- **Real-time Interaction**: Dynamic puzzle solving
- **Responsive Design**: Mobile-friendly interface

## 📞 Support

For questions about this CS50 project, please refer to the project documentation or contact the developer.

## 📊 Current Status

**✅ PRODUCTION READY** - The application is fully functional with:
- User authentication and database persistence
- Interactive puzzle solving interface
- Automatic progress saving
- Deployment configuration for multiple platforms

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for detailed information about the current state and next steps.

---

**Built with ❤️ for Harvard CS50 Final Project** 