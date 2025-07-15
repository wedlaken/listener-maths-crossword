# Deployment Guide for CS50 Final Project

## Overview
This guide covers deploying the Interactive Crossword Solver web application for CS50 Final Project demonstration.

## Virtual Environment Management

### Checking Virtual Environment Status
Before activating a virtual environment, check if you're already in one:

```bash
echo $VIRTUAL_ENV
```

**Output meanings:**
- **If in a virtual environment**: Shows path like `/workspaces/111866764/project/.venv`
- **If not in a virtual environment**: Empty output (nothing printed)

### Environment Status Commands
```bash
# Check if you're in a virtual environment
echo $VIRTUAL_ENV

# Check which Python interpreter you're using
which python

# Check Python version
python --version

# Check if specific packages are installed
pip list | grep flask
```

### Avoiding Nested Virtual Environments
To prevent double activation (showing `((.venv))`):
1. **Check first**: `echo $VIRTUAL_ENV`
2. **Only activate if needed**: `source .venv/bin/activate`
3. **Deactivate if nested**: `deactivate`

## Local Development Setup

### 1. Install Dependencies
```bash
# Check if virtual environment exists
ls -la .venv/

# Activate virtual environment (if not already active)
source .venv/bin/activate  # Mac/Linux
# or
.\venv\Scripts\activate   # Windows

# Install Flask dependencies
pip install -r requirements.txt
```

### 2. Run Locally
```bash
python app.py
```
The application will be available at `http://localhost:5001`

## CS50 Codespace Setup

### Environment Compatibility
- **Python Version**: 3.12.10 (in Codespace)
- **Local Python**: 3.13.3 (may have different package compatibility)
- **Requirements**: Updated for Python 3.12 compatibility

### Codespace Setup Steps
```bash
# Navigate to project directory
cd /workspaces/111866764/project

# Check if virtual environment exists
ls -la .venv/

# Activate virtual environment
source .venv/bin/activate

# Verify activation
echo $VIRTUAL_ENV
which python

# Install dependencies (if needed)
pip install -r requirements.txt

# Start Flask application
python app.py
```

### Port Forwarding
- **Local URL**: `http://127.0.0.1:5001`
- **Access Method**: Use VS Code port forwarding feature
- **Browser Access**: Click port forwarding notification or check "Ports" tab

## Deployment Options

### Option 1: Heroku (Recommended for CS50)

#### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

#### Steps
1. **Create Heroku App**
   ```bash
   heroku create your-crossword-solver
   ```

2. **Add Buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Add Flask web application"
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

### Option 2: Railway

#### Steps
1. Connect GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

### Option 3: Render

#### Steps
1. Connect GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`
4. Deploy

## Database Setup

### Local Development
The SQLite database is created automatically when you first run the application:
```bash
python app.py
```

### Production Deployment
For production, consider using PostgreSQL:
1. Add `psycopg2-binary` to requirements.txt
2. Update database URI in app.py
3. Set up PostgreSQL database in your hosting platform

## Environment Variables

### Required
- `SECRET_KEY`: Secret key for Flask sessions (set automatically in production)

### Optional
- `DATABASE_URL`: Database connection string (for production)

## CS50 Project Demonstration

### Features to Highlight
1. **Database Management**: SQLite with SQLAlchemy ORM
2. **User Authentication**: Email/password registration and login
3. **State Persistence**: Save/load puzzle solving progress
4. **Full-Stack Development**: Flask backend + HTML/CSS/JavaScript frontend
5. **Real-time Interaction**: Interactive crossword solving with constraint propagation
6. **Modern Web Technologies**: Bootstrap, AJAX, JSON APIs

### Code Structure
```
├── app.py                 # Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── register.html     # Registration
│   ├── login.html        # Login
│   └── solver.html       # Main solver interface
├── static/               # Static files
│   └── interactive_solver.html  # Interactive solver
├── interactive_solver.py # Core solver logic
├── clue_classes.py       # Clue management
└── requirements.txt      # Python dependencies
```

### Database Schema
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Puzzle sessions table
CREATE TABLE puzzle_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    puzzle_id TEXT NOT NULL,
    solved_cells TEXT,        -- JSON
    user_selected_solutions TEXT, -- JSON
    solution_history TEXT,    -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Testing the Deployment

### 1. Registration
- Visit the deployed URL
- Click "Register" and create an account
- Verify email/password authentication

### 2. Puzzle Solving
- Login to your account
- Start solving the crossword
- Test save/load functionality
- Try the deselect feature

### 3. Cross-Device Testing
- Access from different browsers
- Test on mobile devices
- Verify state persistence across sessions

## Troubleshooting

### Common Issues
1. **Database not found**: Ensure `db.create_all()` runs on first startup
2. **Static files not loading**: Check if files are in the `static/` directory
3. **CORS issues**: Ensure proper iframe communication setup
4. **Environment variables**: Verify all required variables are set

### Logs
- **Heroku**: `heroku logs --tail`
- **Railway**: Check logs in dashboard
- **Render**: View logs in dashboard

## Security Considerations

### For Production
1. Use strong SECRET_KEY
2. Enable HTTPS
3. Implement rate limiting
4. Add input validation
5. Use environment variables for sensitive data

### For CS50 Demonstration
- Focus on demonstrating understanding of web development concepts
- Show database operations and user management
- Highlight full-stack integration 