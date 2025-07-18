#!/usr/bin/env python3
"""
Quick Development Script
Fast local development workflow without Git operations.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n[WORKING] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Quick development workflow - no Git operations."""
    print("Interactive Crossword Solver - Quick Development")
    print("=" * 50)
    
    # Step 1: Generate HTML from interactive_solver.py
    print("\nStep 1: Generating HTML from interactive_solver.py")
    if not run_command("python interactive_solver.py", "Generating interactive solver HTML"):
        print("[ERROR] Failed to generate HTML. Please check for errors in interactive_solver.py")
        return False
    
    # Step 2: Check if static file was created
    static_file = Path("static/interactive_solver.html")
    if not static_file.exists():
        print("[ERROR] Static file not found. Check if save_html_to_static() is working.")
        return False
    
    print(f"[SUCCESS] Static file created: {static_file}")
    
    # Step 3: Optional - Test Flask app locally
    print("\nStep 3: Ready for testing")
    print("To test the Flask app locally:")
    print("   python app.py")
    print("   # Then visit http://localhost:5001")
    
    print("\n" + "=" * 50)
    print("Quick development completed!")
    print("\nSummary:")
    print("   [SUCCESS] HTML generated from interactive_solver.py")
    print("   [SUCCESS] Static file saved to static/interactive_solver.html")
    print("   [SUCCESS] Ready for Flask app testing")
    print("\nWhen ready to deploy:")
    print("   git add .")
    print("   git commit -m 'Update interactive solver'")
    print("   git push")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 