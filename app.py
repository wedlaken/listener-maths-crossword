#!/usr/bin/env python3
"""
CS50 Final Project: Interactive Crossword Solver
Flask web application with SQLite database for user management and puzzle state persistence.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration - supports both SQLite (development) and PostgreSQL (production)
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Production: Use PostgreSQL from environment variable
    # Fix for Render's postgres:// vs postgresql:// issue
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"🔧 Using PostgreSQL database: {database_url}")
else:
    # Development: Use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crossword_solver.db'
    print(f"🔧 Using SQLite database: instance/crossword_solver.db")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PuzzleSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    puzzle_id = db.Column(db.String(50), nullable=False)
    solved_cells = db.Column(db.Text)  # JSON string
    user_selected_solutions = db.Column(db.Text)  # JSON string
    solution_history = db.Column(db.Text)  # JSON string
    # Anagram state fields
    anagram_solved_cells = db.Column(db.Text)  # JSON string
    anagram_user_selected_solutions = db.Column(db.Text)  # JSON string
    anagram_clue_objects = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_solved_cells(self):
        return json.loads(self.solved_cells) if self.solved_cells else {}
    
    def set_solved_cells(self, cells_dict):
        self.solved_cells = json.dumps(cells_dict)
    
    def get_user_selected_solutions(self):
        return json.loads(self.user_selected_solutions) if self.user_selected_solutions else []
    
    def set_user_selected_solutions(self, solutions_list):
        self.user_selected_solutions = json.dumps(solutions_list)
    
    def get_solution_history(self):
        return json.loads(self.solution_history) if self.solution_history else []
    
    def set_solution_history(self, history_list):
        self.solution_history = json.dumps(history_list)
    
    # Anagram state methods
    def get_anagram_solved_cells(self):
        return json.loads(self.anagram_solved_cells) if self.anagram_solved_cells else {}
    
    def set_anagram_solved_cells(self, cells_dict):
        self.anagram_solved_cells = json.dumps(cells_dict)
    
    def get_anagram_user_selected_solutions(self):
        return json.loads(self.anagram_user_selected_solutions) if self.anagram_user_selected_solutions else []
    
    def set_anagram_user_selected_solutions(self, solutions_list):
        self.anagram_user_selected_solutions = json.dumps(solutions_list)
    
    def get_anagram_clue_objects(self):
        return json.loads(self.anagram_clue_objects) if self.anagram_clue_objects else {}
    
    def set_anagram_clue_objects(self, clue_objects_dict):
        self.anagram_clue_objects = json.dumps(clue_objects_dict)

# Initialize database tables (works with both local and Gunicorn)
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('solver'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered')
            return render_template('register.html')
        
        # Create new user
        try:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {e}")
            flash('Registration failed. Please try again.')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please enter both email and password')
            return render_template('login.html')
        
        try:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['email'] = user.email
                print(f"✅ User {email} logged in successfully")
                return redirect(url_for('solver'))
            else:
                print(f"❌ Login failed for {email} - invalid credentials")
                flash('Invalid email or password')
        except Exception as e:
            print(f"❌ Login error: {e}")
            flash('Login failed. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/solver')
def solver():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get or create puzzle session for current user
    try:
        puzzle_session = PuzzleSession.query.filter_by(
            user_id=session['user_id'], 
            puzzle_id='Listener_4869'
        ).first()
        
        if not puzzle_session:
            puzzle_session = PuzzleSession(
                user_id=session['user_id'],
                puzzle_id='Listener_4869'
            )
            db.session.add(puzzle_session)
            db.session.commit()
    except Exception as e:
        print(f"Error accessing puzzle session: {e}")
    
    return render_template('solver.html', user_email=session['email'])

# API Routes for puzzle state management
@app.route('/api/save_state', methods=['POST'])
def save_state():
    print("=== SAVE STATE API CALLED ===")
    print(f"User ID in session: {session.get('user_id')}")
    
    if 'user_id' not in session:
        print("ERROR: No user_id in session")
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    print(f"Received data: {data}")
    
    try:
        puzzle_session = PuzzleSession.query.filter_by(
            user_id=session['user_id'], 
            puzzle_id='Listener_4869'
        ).first()
        
        if not puzzle_session:
            print("Creating new puzzle session")
            puzzle_session = PuzzleSession(
                user_id=session['user_id'],
                puzzle_id='Listener_4869'
            )
            db.session.add(puzzle_session)
        else:
            print("Found existing puzzle session")
        
        puzzle_session.set_solved_cells(data.get('solved_cells', {}))
        puzzle_session.set_user_selected_solutions(data.get('user_selected_solutions', []))
        puzzle_session.set_solution_history(data.get('solution_history', []))
        # Save anagram state
        puzzle_session.set_anagram_solved_cells(data.get('anagram_solved_cells', {}))
        puzzle_session.set_anagram_user_selected_solutions(data.get('anagram_user_selected_solutions', []))
        puzzle_session.set_anagram_clue_objects(data.get('anagram_clue_objects', {}))
        
        print("About to commit to database...")
        db.session.commit()
        print("Database commit successful!")
        return jsonify({'success': True})
    except Exception as e:
        print(f"Database commit failed: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/load_state')
def load_state():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        puzzle_session = PuzzleSession.query.filter_by(
            user_id=session['user_id'], 
            puzzle_id='Listener_4869'
        ).first()
        
        if not puzzle_session:
            return jsonify({
                'solved_cells': {},
                'user_selected_solutions': [],
                'solution_history': [],
                'anagram_solved_cells': {},
                'anagram_user_selected_solutions': [],
                'anagram_clue_objects': {}
            })
        
        return jsonify({
            'solved_cells': puzzle_session.get_solved_cells(),
            'user_selected_solutions': puzzle_session.get_user_selected_solutions(),
            'solution_history': puzzle_session.get_solution_history(),
            'anagram_solved_cells': puzzle_session.get_anagram_solved_cells(),
            'anagram_user_selected_solutions': puzzle_session.get_anagram_user_selected_solutions(),
            'anagram_clue_objects': puzzle_session.get_anagram_clue_objects()
        })
    except Exception as e:
        print(f"Error loading state: {e}")
        return jsonify({'error': str(e)}), 500

# Direct route to serve interactive solver (fallback for static file issues)
@app.route('/interactive_solver')
def interactive_solver():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with open('static/interactive_solver.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        return "Interactive solver file not found", 404

# Debug route to test static file serving
@app.route('/debug/static_test')
def static_test():
    import os
    static_files = []
    try:
        for file in os.listdir('static'):
            static_files.append(file)
    except Exception as e:
        static_files.append(f"Error listing static directory: {e}")
    
    return jsonify({
        'static_files': static_files,
        'static_dir_exists': os.path.exists('static'),
        'interactive_solver_exists': os.path.exists('static/interactive_solver.html')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
