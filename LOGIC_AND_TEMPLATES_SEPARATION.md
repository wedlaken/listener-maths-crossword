# Logic and Templates Separation Guide

## Overview
This document explains how the Flask application separates logic from display, and where to make different types of changes.

---

## **File Structure & Responsibilities**

### **Logic Files (Python) - Core Functionality**
- `interactive_solver.py` - Core solving logic, constraint propagation, solution generation
- `clue_classes.py` - Clue management, solution sets, mathematical operations
- `crossword_solver.py` - Grid structure, solving algorithms, puzzle parsing
- `app.py` - Flask web framework, database models, API routes

### **Display Files (HTML/Templates) - User Interface**
- `templates/solver.html` - Main solver page wrapper (loads interactive solver)
- `templates/base.html` - Base layout with navigation, Bootstrap styling
- `static/interactive_solver.html` - The actual interactive grid (your original display)

---

## **How the Display Works**

### **Request Flow:**
```
User visits localhost:5000/solver
    ↓
Flask serves templates/solver.html
    ↓
solver.html loads static/interactive_solver.html in an iframe
    ↓
interactive_solver.html runs your original JavaScript/Python logic
```

### **File Dependencies:**
- **Flask Framework**: `app.py` → `templates/solver.html` → `static/interactive_solver.html`
- **Core Logic**: `interactive_solver.py` → `static/interactive_solver.html`
- **Data Models**: `clue_classes.py` → `interactive_solver.py`

---

## **Where to Make Changes**

### **1. Grid Display & Interactive Elements**
**File:** `static/interactive_solver.html`
**Examples:**
- Grid layout and styling
- Cell appearance and behavior
- Clue list formatting
- Button positioning and styling
- **Popup positioning and appearance** ← **YOUR CURRENT NEED**

### **2. Page Layout & Navigation**
**File:** `templates/solver.html`
**Examples:**
- Overall page structure
- Save/Load button positioning
- User info display
- Page title and headers

### **3. Site-Wide Layout**
**File:** `templates/base.html`
**Examples:**
- Navigation bar
- Bootstrap theme
- Global styling
- Footer content

### **4. Solving Logic**
**File:** `interactive_solver.py`
**Examples:**
- Constraint propagation algorithms
- Solution generation
- Grid state management
- Undo/redo functionality

### **5. Clue Management**
**File:** `clue_classes.py`
**Examples:**
- Clue parsing and validation
- Solution set generation
- Mathematical operations

### **6. Database & User Management**
**File:** `app.py`
**Examples:**
- User registration/login
- Progress saving/loading
- API endpoints
- Database models

---

## **Recent Changes Made**

### **Change 1: Popup Positioning (2025-06-26)**
**Issue:** Solution selection notifications appeared in top-right corner, looking messy
**File Changed:** `static/interactive_solver.html`
**What Changed:** 
- Moved notifications from `top: 20px; right: 20px` to `top: 450px; left: 50%; transform: translateX(-50%)`
- Added `width: 600px` to match grid width
- Added `text-align: center` for better appearance
**Result:** Notifications now appear centered under the grid

### **Change 2: Remove Redundant Login Status (2025-06-26)**
**Issue:** "Logged in as: email" badge was redundant since login status already shown in page header
**File Changed:** `templates/solver.html`
**What Changed:** Removed the `<span class="badge bg-success me-2">Logged in as: {{ user_email }}</span>` line
**Result:** Cleaner interface without duplicate login information

### **Change 3: Fix Iframe Height and Popup Positioning (2025-06-26)**
**Issue 1:** Iframe was too short (650px) and didn't show the full clue list
**File Changed:** `templates/solver.html`
**What Changed:** Increased iframe height from `650px` to `1200px`
**Result:** Full content including clue list is now visible

**Issue 2:** Popup appeared in center of window instead of below puzzle grid
**File Changed:** `static/interactive_solver.html`
**What Changed:** Moved notification from `top: 470px` to `top: 1020px`
**Result:** Popup now appears below the puzzle grid as intended

### **Change 4: Auto-Reload Development Server Setup (2025-06-26)**
**Issue:** Manual server restart required for static file changes
**Files Added:** `dev_server.py`, updated `requirements.txt`
**What Changed:** 
- Created development server with file watching using `watchdog`
- Added `watchdog` and `flask-socketio` to requirements
- Comprehensive documentation in `PROJECT_ENVIRONMENT_SETUP.md` and `TECHNICAL_DOCUMENTATION.md`
**Result:** Full auto-reload functionality like nodemon - all file types now auto-restart the server
**Test Status:** ✅ Successfully tested - server auto-restarts when `static/interactive_solver.html` is modified

---

## **Your Specific Case: Popup Positioning**

### **Current Issue:**
The solution selection popup appears above the clue list and looks messy.

### **Solution:**
**File to edit:** `static/interactive_solver.html`

### **What to change:**
1. **CSS Positioning**: Find the popup CSS and change positioning
2. **JavaScript Positioning**: Update the JavaScript that shows/hides the popup
3. **HTML Structure**: Possibly move the popup HTML element

### **Example changes needed:**
```css
/* Current (messy positioning) */
.popup {
    position: absolute;
    top: 10px;
    left: 50%;
}

/* Better positioning (under grid) */
.popup {
    position: absolute;
    top: 400px; /* Adjust based on grid height */
    left: 50%;
    transform: translateX(-50%);
    width: 600px; /* Match grid width */
}
```

---

## **Development Workflow**

### **For Display Changes:**
1. Edit `static/interactive_solver.html`
2. Refresh browser at `localhost:5000/solver`
3. Changes appear immediately

### **For Logic Changes:**
1. Edit `interactive_solver.py`
2. Restart Flask server (`Ctrl+C`, then `python app.py`)
3. Refresh browser

### **For Template Changes:**
1. Edit files in `templates/` folder
2. Refresh browser
3. Changes appear immediately

---

## **Auto-Reload Options (Like nodemon)**

### **Current Setup:**
- ✅ **Python files** (`app.py`, `interactive_solver.py`) auto-reload with `debug=True`
- ✅ **Template files** (`templates/*.html`) auto-reload with `debug=True`
- ❌ **Static files** (`static/*.html`) do NOT auto-reload

### **Option 1: Manual Refresh (Current)**
- Edit `static/interactive_solver.html`
- Refresh browser manually

### **Option 2: Use Development Server with Auto-Reload**
```bash
# Install watchdog
pip install watchdog

# Run development server
python dev_server.py
```
This will watch all files and restart Flask automatically when changes are detected.

### **Option 3: Use Flask-SocketIO for Live Reload**
For even more advanced live reloading (like hot module replacement).

---

## **Key Points to Remember**

### **Display vs Logic:**
- **Display**: How things look and where they appear (HTML/CSS/JavaScript in templates)
- **Logic**: How things work and what they do (Python algorithms and data processing)

### **Your Popup Issue:**
- **Display Problem**: Popup appears in wrong place
- **Solution**: Edit `static/interactive_solver.html` (CSS/JavaScript positioning)
- **Not Logic**: The popup functionality works, just positioning is wrong

### **Testing Changes:**
- Display changes: Refresh browser
- Logic changes: Restart Flask server
- Template changes: Refresh browser

---

## **Common Change Scenarios**

### **Scenario 1: Change Grid Colors**
- **File:** `static/interactive_solver.html`
- **What:** CSS styles for grid cells
- **Test:** Refresh browser

### **Scenario 2: Add New Solving Algorithm**
- **File:** `interactive_solver.py`
- **What:** Python logic for new algorithm
- **Test:** Restart server

### **Scenario 3: Change Page Layout**
- **File:** `templates/solver.html`
- **What:** HTML structure and Bootstrap classes
- **Test:** Refresh browser

### **Scenario 4: Add Database Field**
- **File:** `app.py`
- **What:** Database model changes
- **Test:** Restart server, may need database migration

---

**This guide will be updated as we make changes and discover new patterns!** 