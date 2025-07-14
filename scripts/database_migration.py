#!/usr/bin/env python3
"""
Database Migration Script
Adds new anagram state columns to existing PuzzleSession table.
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate the database to add anagram state columns."""
    
    # Database path
    db_path = 'instance/crossword_solver.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        print("Database will be created when Flask app starts")
        return
    
    print(f"Migrating database: {db_path}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(puzzle_session)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Existing columns: {columns}")
        
        # Add new columns if they don't exist
        new_columns = [
            'anagram_solved_cells',
            'anagram_user_selected_solutions', 
            'anagram_clue_objects'
        ]
        
        for column in new_columns:
            if column not in columns:
                print(f"Adding column: {column}")
                cursor.execute(f"ALTER TABLE puzzle_session ADD COLUMN {column} TEXT")
                print(f"✓ Added column: {column}")
            else:
                print(f"Column already exists: {column}")
        
        # Commit changes
        conn.commit()
        print("✓ Database migration completed successfully!")
        
        # Show final table structure
        cursor.execute("PRAGMA table_info(puzzle_session)")
        final_columns = cursor.fetchall()
        print("\nFinal table structure:")
        for column in final_columns:
            print(f"  {column[1]} ({column[2]})")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database() 