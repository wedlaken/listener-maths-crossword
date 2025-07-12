# Project Environment Setup and Configuration Guide

## Overview
This guide covers the complete setup of the Listener Maths Crossword project environment, including virtual environment management, configuration files, and development tools.

## Why Use a Virtual Environment?
A virtual environment (venv) isolates your Python project's dependencies from your system Python and other projects. This prevents version conflicts and keeps your project self-contained.

## Project Configuration Files Overview

This project uses several configuration files to manage the development environment, dependencies, and code quality. Understanding these files helps you work effectively with the project.

### 1. `pyrightconfig.json` - Type Checking Configuration
**Purpose**: Configures Pyright, a static type checker for Python that provides real-time error detection and IntelliSense in Cursor/VS Code.

**Configuration**:
```json
{
    "venvPath": ".",
    "venv": "venv"
}
```

**What it does**:
- `"venvPath": "."` - Tells Pyright to look for the virtual environment in the current directory
- `"venv": "venv"` - Specifies the virtual environment folder name

**When it runs**: Automatically in Cursor/VS Code during development to provide:
- Real-time type checking
- Error detection before running code
- IntelliSense and autocomplete features

### 2. `pyproject.toml` - Modern Python Project Configuration
**Purpose**: The modern standard for Python project configuration, defining build system, dependencies, and tool configurations.

**Current configuration**:
```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.pylint.messages_control]
disable = ["C0111"]

[tool.pylint.format]
max-line-length = 100

[tool.pylint.basic]
good-names = ["i", "n", "a", "b", "c"]
```

**What it contains**:
- **Build system**: Specifies how to build the project using `setuptools` and `wheel`
- **Pylint configuration**: Code quality and style checking rules
  - Disables missing docstring warnings (`C0111`)
  - Sets maximum line length to 100 characters
  - Allows short variable names for mathematical operations

**When it runs**:
- Build tools read this when packaging the project
- Pylint uses these settings for code quality checks
- Modern Python tools (pip, build) use this for project metadata

### 3. `setup.py` - Package Installation Configuration
**Purpose**: Traditional way to define how the Python package should be installed and what dependencies it needs.

**Current configuration**:
```python
from setuptools import setup, find_packages

setup(
    name="listener_maths_crossword",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sympy>=1.14.0",
    ],
)
```

**What it does**:
- Defines package name (`listener_maths_crossword`)
- Specifies version (`0.1`)
- Lists core required dependencies (`sympy>=1.14.0`)
- Uses `find_packages()` to automatically discover Python modules

**When it runs**:
- When installing the package with `pip install .`
- When building distribution packages (`python setup.py sdist bdist_wheel`)
- When installing in development mode (`pip install -e .`)

### 4. `requirements.txt` - Dependency Management
**Purpose**: Lists all Python packages the project needs to run with specific versions.

**Key dependencies**:
- **Core math libraries**: `sympy`, `numpy`, `mpmath`
- **Image processing**: `opencv-python`, `pillow`, `pytesseract`
- **Plotting**: `matplotlib` and its dependencies
- **Utilities**: `colorama`, `six`, etc.

**When it runs**:
- When setting up a new environment with `pip install -r requirements.txt`
- When deploying the application
- When ensuring consistent dependencies across different machines

## Configuration File Relationships

**Modern vs Legacy Approach**:
- **Modern**: Use `pyproject.toml` for everything (build system, dependencies, tool configuration)
- **Legacy**: Use `setup.py` for package configuration and `requirements.txt` for dependencies

**Current Project Setup**:
This project uses a hybrid approach, which is common during transitions:
- `pyproject.toml` handles build system and code quality tools
- `setup.py` handles package installation and distribution
- `requirements.txt` handles development environment setup
- `pyrightconfig.json` handles development tool configuration

## Understanding PowerShell Script Files (.ps1)
The `.ps1` extension stands for "PowerShell Script" - it's not PowerShell version 1, but rather the standard file extension for PowerShell script files. Here's what you need to know:

- `.ps1` is to PowerShell what `.py` is to Python - it's the standard file extension
- The activation script is named `Activate.ps1` because it's a PowerShell script that sets up your virtual environment
- When you run `.\venv\Scripts\Activate.ps1`, you're telling PowerShell to:
  - `.\` means "run this script from the current directory"
  - `venv\Scripts\` is the path to the script
  - `Activate.ps1` is the script file itself

## Understanding Virtual Environment Persistence
The virtual environment consists of two parts:
1. **The `venv` folder**: This is permanent and contains all your project's Python packages
2. **The activation state**: This is temporary and only exists while your PowerShell window is open

When you close PowerShell:
- ✅ The `venv` folder and all installed packages remain on your computer
- ✅ Your project's dependencies are still there
- ❌ You just need to activate the environment again in your new PowerShell window

Think of it like turning on a light switch:
- The light bulb (venv folder) is always there
- The switch (activation) needs to be turned on each time you enter the room (open a new PowerShell window)

## How to Activate the Virtual Environment
1. **Open PowerShell** and navigate to your project directory:
   ```powershell
   cd C:\Users\neilw\Projects\listener-maths-crossword
   ```

2. **Set the Execution Policy (if needed):**
   PowerShell restricts running scripts for security. You may see an error like:
   > running scripts is disabled on this system

   If you get a permission error when trying to set the execution policy, you have two options:

   **Option 1 (Recommended for most users):** Set the policy for your user account only:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   **Option 2:** Run PowerShell as Administrator and set the policy for all users:
   - Right-click on PowerShell
   - Select "Run as Administrator"
   - Then run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
   ```

   The `-Scope CurrentUser` option is recommended as it's safer and doesn't require administrator privileges.

3. **Activate the Virtual Environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   You should see `(venv)` at the start of your prompt, indicating the environment is active.

4. **Install dependencies (if not already done):**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Deactivate the Virtual Environment:**
   When finished, you can deactivate with:
   ```powershell
   deactivate
   ```

---

## What is the PowerShell Execution Policy?
PowerShell's execution policy is a safety feature that controls whether scripts can run. By default, it may block scripts (like the venv activation script) to protect your system from untrusted code.

- `RemoteSigned` allows scripts created on your computer to run, but requires downloaded scripts to be signed by a trusted publisher.
- The policy can be set at different scopes:
  - `CurrentUser`: Only affects your user account (safer, doesn't require admin rights)
  - `LocalMachine`: Affects all users (requires administrator privileges)

## Can I Permanently Change the Policy?
Yes, and it's recommended to set it permanently for your user account. This way, you won't need to change it each time you open a new PowerShell window. Use:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This is safe because:
1. It only affects your user account
2. It still maintains security by requiring downloaded scripts to be signed
3. It allows you to run local scripts (like your venv activation script)

---

If you have any questions, refer to the [Microsoft documentation on execution policies](https://go.microsoft.com/fwlink/?LinkID=135170).

## Development Server Setup

### Overview
The project includes an advanced development server with auto-reload functionality, similar to nodemon for Node.js applications. This provides a seamless development experience with automatic server restarts when files are modified.

### Auto-Reload Features

#### **What Auto-Reloads:**
- ✅ **Python files** (`app.py`, `interactive_solver.py`, etc.) - Flask debug mode
- ✅ **Template files** (`templates/*.html`) - Flask debug mode  
- ✅ **Static files** (`static/*.html`) - Custom file watcher
- ✅ **Configuration files** - Custom file watcher

#### **What Doesn't Auto-Reload:**
- ❌ **Database changes** - Requires manual restart
- ❌ **Environment variables** - Requires manual restart

### Development Server Options

#### **Option 1: Standard Flask Server (Basic Auto-Reload)**
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run Flask server
python app.py
```
**Features:**
- Auto-reloads Python and template files
- Debug mode enabled
- Simple setup

#### **Option 2: Advanced Development Server (Full Auto-Reload)**
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install development dependencies (if not already done)
pip install watchdog flask-socketio

# Run development server
python dev_server.py
```
**Features:**
- Auto-reloads ALL file types
- File watching with debouncing
- Clean console output
- Automatic server restart

### Development Server Files

#### **`dev_server.py` - Auto-Reload Server**
**Purpose**: Provides nodemon-like functionality for Flask development.

**Key Features:**
- **File watching**: Monitors `./`, `static/`, and `templates/` directories
- **Debouncing**: Prevents multiple restarts from rapid file changes
- **Process management**: Automatically kills and restarts Flask server
- **Clean output**: Shows which files changed and restart status

**How it works:**
1. Starts Flask server as a subprocess
2. Sets up file system watchers using `watchdog`
3. Detects file modifications
4. Terminates old Flask process
5. Starts new Flask process
6. Provides status feedback

**Usage:**
```bash
python dev_server.py
```

**Output example:**
```
🚀 Starting Flask development server with auto-reload...
📁 Watching for changes in: ./, static/, templates/
🛑 Press Ctrl+C to stop

🔄 File changed: static/interactive_solver.html
🔄 Restarting Flask server...
✅ Flask server restarted!
```

### Development Workflow

#### **For Different File Types:**

**Python Files (`app.py`, `interactive_solver.py`):**
- Edit file
- Server auto-restarts (both standard and dev server)
- Refresh browser

**Template Files (`templates/*.html`):**
- Edit file  
- Server auto-restarts (both standard and dev server)
- Refresh browser

**Static Files (`static/*.html`):**
- Edit file
- **Standard server**: Manual refresh required
- **Dev server**: Auto-restart, then refresh browser

#### **Recommended Workflow:**
1. **Start development server:**
   ```bash
   python dev_server.py
   ```

2. **Make changes to any file**

3. **Watch for auto-restart message**

4. **Refresh browser to see changes**

### Troubleshooting Development Server

#### **Common Issues:**

**Server won't start:**
```bash
# Check if port 5001 is in use
netstat -ano | findstr :5001

# Kill process if needed
taskkill /PID <process_id> /F
```

**Auto-reload not working:**
- Ensure `debug=True` in `app.py`
- Check file permissions
- Verify `watchdog` is installed

**Multiple restarts:**
- The debouncing feature should prevent this
- If it persists, check for temporary files (`.tmp`, `~`)

#### **Performance Tips:**
- **Exclude large files**: Add `.gitignore` patterns to avoid watching unnecessary files
- **Use SSD**: File watching is faster on solid-state drives
- **Close other applications**: Reduces system load during development

### Production vs Development

#### **Development Server (`dev_server.py`):**
- ✅ Auto-reload enabled
- ✅ Debug mode enabled
- ✅ File watching active
- ❌ Not suitable for production

#### **Production Server:**
- ❌ Auto-reload disabled
- ❌ Debug mode disabled
- ✅ Optimized for performance
- ✅ Use `gunicorn` or similar

**Switching to production:**
```bash
# Development
python dev_server.py

# Production
gunicorn app:app
```

---

## Environment Variables

### Development Environment Variables
The project uses environment variables for configuration. In development, these are set with defaults:

**`SECRET_KEY`**: Used for Flask session security
- **Development**: `'dev-secret-key-change-in-production'`
- **Production**: Should be set to a secure random string

**`DATABASE_URL`**: Database connection string
- **Development**: `sqlite:///crossword_solver.db`
- **Production**: PostgreSQL or other production database

### Setting Environment Variables

#### **Windows PowerShell:**
```powershell
# Set for current session
$env:SECRET_KEY="your-secret-key"

# Set permanently (user level)
[Environment]::SetEnvironmentVariable("SECRET_KEY", "your-secret-key", "User")
```

#### **Windows Command Prompt:**
```cmd
# Set for current session
set SECRET_KEY=your-secret-key

# Set permanently
setx SECRET_KEY "your-secret-key"
```

#### **Using .env file (Recommended):**
Create a `.env` file in your project root:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///crossword_solver.db
FLASK_ENV=development
```

Then install and use python-dotenv:
```bash
pip install python-dotenv
```

And update `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
``` 