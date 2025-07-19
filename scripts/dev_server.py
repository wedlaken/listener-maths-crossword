#!/usr/bin/env python3
"""
Development server with auto-reload for static files
Similar to nodemon for Flask development
"""

import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FlaskReloadHandler(FileSystemEventHandler):
    def __init__(self, flask_process):
        self.flask_process = flask_process
        self.last_modified = {}
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Skip temporary files
        if event.src_path.endswith('~') or event.src_path.endswith('.tmp'):
            return
        
        # Check if file was actually modified (not just touched)
        current_time = time.time()
        if event.src_path in self.last_modified:
            if current_time - self.last_modified[event.src_path] < 1:
                return  # Debounce rapid changes
        
        self.last_modified[event.src_path] = current_time
        
        print(f"\n🔄 File changed: {event.src_path}")
        print("🔄 Restarting Flask server...")
        
        # Kill the current Flask process
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process.wait()
        
        # Start a new Flask process
        self.flask_process = subprocess.Popen([sys.executable, 'app.py'])
        print("✅ Flask server restarted!")

def main():
    print("🚀 Starting Flask development server with auto-reload...")
    print("📁 Watching for changes in: ./, static/, templates/")
    print("🛑 Press Ctrl+C to stop")
    
    # Start Flask server
    flask_process = subprocess.Popen([sys.executable, 'app.py'])
    
    # Set up file watcher
    event_handler = FlaskReloadHandler(flask_process)
    observer = Observer()
    
    # Watch current directory, static, and templates
    observer.schedule(event_handler, '.', recursive=True)
    observer.schedule(event_handler, 'static', recursive=True)
    observer.schedule(event_handler, 'templates', recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping development server...")
        observer.stop()
        if flask_process:
            flask_process.terminate()
    
    observer.join()
    print("✅ Development server stopped.")

if __name__ == '__main__':
    main() 