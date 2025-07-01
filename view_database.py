#!/usr/bin/env python3
"""
Simple database viewer for the crossword solver database
"""

import sqlite3
import json
from pathlib import Path

def view_database():
    """View the contents of the crossword solver database"""
    
    db_path = Path("instance/crossword_solver.db")
    
    if not db_path.exists():
        print(f"Database file not found: {db_path}")
        return
    
    print("=" * 60)
    print("CROSSWORD SOLVER DATABASE VIEWER")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\n📋 Tables found: {[table[0] for table in tables]}")
    
    # View Users table
    print("\n" + "=" * 40)
    print("👥 USERS TABLE")
    print("=" * 40)
    
    cursor.execute("SELECT id, email, created_at FROM user;")
    users = cursor.fetchall()
    
    if users:
        print(f"Found {len(users)} user(s):")
        for user_id, email, created_at in users:
            print(f"  ID: {user_id} | Email: {email} | Created: {created_at}")
    else:
        print("No users found")
    
    # View Puzzle Sessions table
    print("\n" + "=" * 40)
    print("🧩 PUZZLE SESSIONS TABLE")
    print("=" * 40)
    
    cursor.execute("""
        SELECT id, user_id, puzzle_id, solved_cells, user_selected_solutions, 
               solution_history, created_at, updated_at 
        FROM puzzle_session;
    """)
    sessions = cursor.fetchall()
    
    if sessions:
        print(f"Found {len(sessions)} puzzle session(s):")
        for session in sessions:
            session_id, user_id, puzzle_id, solved_cells, user_selected_solutions, \
            solution_history, created_at, updated_at = session
            
            print(f"\n  Session ID: {session_id}")
            print(f"  User ID: {user_id}")
            print(f"  Puzzle ID: {puzzle_id}")
            print(f"  Created: {created_at}")
            print(f"  Updated: {updated_at}")
            
            # Parse and display solved cells
            if solved_cells:
                try:
                    cells = json.loads(solved_cells)
                    print(f"  Solved Cells: {len(cells)} cells filled")
                    if cells:
                        print(f"    Sample: {dict(list(cells.items())[:5])}")
                except json.JSONDecodeError:
                    print(f"  Solved Cells: Invalid JSON: {solved_cells}")
            else:
                print(f"  Solved Cells: None")
            
            # Parse and display user selected solutions
            if user_selected_solutions:
                try:
                    solutions = json.loads(user_selected_solutions)
                    print(f"  User Selected Solutions: {len(solutions)} solutions")
                    if solutions:
                        print(f"    Solutions: {solutions}")
                except json.JSONDecodeError:
                    print(f"  User Selected Solutions: Invalid JSON: {user_selected_solutions}")
            else:
                print(f"  User Selected Solutions: None")
            
            # Parse and display solution history
            if solution_history:
                try:
                    history = json.loads(solution_history)
                    print(f"  Solution History: {len(history)} entries")
                    if history:
                        print(f"    Latest: {history[-1] if history else 'None'}")
                except json.JSONDecodeError:
                    print(f"  Solution History: Invalid JSON: {solution_history}")
            else:
                print(f"  Solution History: None")
    else:
        print("No puzzle sessions found")
    
    # Show database schema
    print("\n" + "=" * 40)
    print("🏗️  DATABASE SCHEMA")
    print("=" * 40)
    
    for table_name, in tables:
        print(f"\n📋 Table: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, name, data_type, not_null, default_value, primary_key = col
            pk = " (PRIMARY KEY)" if primary_key else ""
            nn = " NOT NULL" if not_null else ""
            print(f"  - {name}: {data_type}{nn}{pk}")
    
    conn.close()
    print("\n" + "=" * 60)
    print("Database viewing complete!")
    print("=" * 60)

if __name__ == "__main__":
    view_database() 