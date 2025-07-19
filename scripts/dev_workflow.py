#!/usr/bin/env python3
"""
Development Workflow Script
Automates the process of generating HTML from interactive_solver.py and deploying to Flask app.
"""

import os
import sys
import subprocess
import time
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

def check_git_status():
    """Check if there are uncommitted changes."""
    try:
        result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        return result.stdout.strip() != ""
    except:
        return False

def main():
    """Main development workflow."""
    print("Interactive Crossword Solver - Development Workflow")
    print("=" * 60)
    
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
    
    # Step 3: Check for uncommitted changes
    if check_git_status():
            print("\nGit Status: You have uncommitted changes")
    print("Tip: Consider committing your changes before deploying:")
    print("   git add .")
    print("   git commit -m 'Update interactive solver'")
    print("   git push")
    else:
        print("\nGit Status: No uncommitted changes")
    
    # Step 4: Test Flask app locally (optional)
    print("\nStep 4: Testing Flask app locally")
    print("Tip: To test the Flask app locally:")
    print("   python app.py")
    print("   # Then visit http://localhost:5001")
    
    # Step 5: Deploy to Render (if git changes exist)
    if check_git_status():
        print("\nStep 5: Deploy to Render")
        print("Tip: To deploy to Render:")
        print("   git add .")
        print("   git commit -m 'Update interactive solver'")
        print("   git push")
        print("   # Render will automatically deploy from GitHub")
    else:
        print("\nStep 5: Deploy to Render")
        print("Tip: No changes to deploy. If you want to force a deployment:")
        print("   git add .")
        print("   git commit -m 'Force deployment'")
        print("   git push")
    
    print("\n" + "=" * 60)
    print("Development workflow completed!")
    print("\nSummary:")
    print("   [SUCCESS] HTML generated from interactive_solver.py")
    print("   [SUCCESS] Static file saved to static/interactive_solver.html")
    print("   [SUCCESS] Ready for Flask app deployment")
    print("\nYour Flask app should now have the latest changes!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 