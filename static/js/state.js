/**
 * State Management Module
 * Handles saving and loading puzzle state
 */

class StateManager {
    constructor(gridManager) {
        this.gridManager = gridManager;
        this.undoStack = [];
        this.redoStack = [];
        this.maxUndoSteps = 50;
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.setupAutoSave();
    }

    attachEventListeners() {
        // Undo button
        const undoBtn = document.getElementById('undo-btn');
        if (undoBtn) {
            undoBtn.addEventListener('click', () => this.undo());
        }

        // Redo button
        const redoBtn = document.getElementById('redo-btn');
        if (redoBtn) {
            redoBtn.addEventListener('click', () => this.redo());
        }

        // Reset button
        const resetBtn = document.getElementById('reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.reset());
        }

        // Save button
        const saveBtn = document.getElementById('save-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveState());
        }

        // Load button
        const loadBtn = document.getElementById('load-btn');
        if (loadBtn) {
            loadBtn.addEventListener('click', () => this.loadState());
        }

        // Listen for solution applications to add to undo stack
        document.addEventListener('solutionApplied', (e) => {
            this.addToUndoStack();
        });
    }

    setupAutoSave() {
        // Auto-save every 30 seconds
        setInterval(() => {
            this.saveStateToLocalStorage();
        }, 30000);

        // Save on page unload
        window.addEventListener('beforeunload', () => {
            this.saveStateToLocalStorage();
        });
    }

    addToUndoStack() {
        const currentState = this.getCurrentState();
        this.undoStack.push(currentState);
        
        // Limit stack size
        if (this.undoStack.length > this.maxUndoSteps) {
            this.undoStack.shift();
        }

        // Clear redo stack when new action is performed
        this.redoStack = [];
        
        this.updateUndoRedoButtons();
    }

    getCurrentState() {
        return {
            cells: this.gridManager.getAllCellValues(),
            timestamp: Date.now()
        };
    }

    undo() {
        if (this.undoStack.length === 0) return;

        const currentState = this.getCurrentState();
        this.redoStack.push(currentState);

        const previousState = this.undoStack.pop();
        this.restoreState(previousState);
        
        this.updateUndoRedoButtons();
    }

    redo() {
        if (this.redoStack.length === 0) return;

        const currentState = this.getCurrentState();
        this.undoStack.push(currentState);

        const nextState = this.redoStack.pop();
        this.restoreState(nextState);
        
        this.updateUndoRedoButtons();
    }

    restoreState(state) {
        // Clear grid first
        this.gridManager.clearGrid();
        
        // Apply saved cell values
        if (state.cells) {
            this.gridManager.updateCells(state.cells);
        }
    }

    updateUndoRedoButtons() {
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');

        if (undoBtn) {
            undoBtn.disabled = this.undoStack.length === 0;
        }
        if (redoBtn) {
            redoBtn.disabled = this.redoStack.length === 0;
        }
    }

    reset() {
        if (!confirm('Are you sure you want to reset the entire grid? This cannot be undone.')) {
            return;
        }

        this.addToUndoStack(); // Save current state before reset
        this.gridManager.clearGrid();
        
        // Notify backend
        fetch('/reset_grid', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        }).catch(error => {
            console.error('Error resetting grid:', error);
        });
    }

    async saveState() {
        const state = this.getCurrentState();
        
        try {
            const response = await fetch('/api/save_state', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(state)
            });

            const data = await response.json();
            
            if (data.success) {
                this.showMessage('State saved successfully!', 'success');
            } else {
                this.showMessage('Failed to save state: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('Error saving state:', error);
            this.showMessage('Network error. Could not save state.', 'error');
        }
    }

    async loadState() {
        try {
            const response = await fetch('/api/load_state', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();
            
            if (data.success && data.state) {
                this.addToUndoStack(); // Save current state before loading
                this.restoreState(data.state);
                this.showMessage('State loaded successfully!', 'success');
            } else {
                this.showMessage('No saved state found.', 'info');
            }
        } catch (error) {
            console.error('Error loading state:', error);
            this.showMessage('Network error. Could not load state.', 'error');
        }
    }

    saveStateToLocalStorage() {
        const state = this.getCurrentState();
        try {
            localStorage.setItem('crossword_state', JSON.stringify(state));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }

    loadStateFromLocalStorage() {
        try {
            const savedState = localStorage.getItem('crossword_state');
            if (savedState) {
                const state = JSON.parse(savedState);
                this.restoreState(state);
                return true;
            }
        } catch (error) {
            console.error('Error loading from localStorage:', error);
        }
        return false;
    }

    showMessage(message, type = 'info') {
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            background-color: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(messageDiv);

        // Remove after 3 seconds
        setTimeout(() => {
            messageDiv.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                messageDiv.remove();
            }, 300);
        }, 3000);
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StateManager;
}
