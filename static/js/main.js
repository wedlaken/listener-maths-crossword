/**
 * Main Application Entry Point
 * Initializes all modules and coordinates their interactions
 */

class CrosswordSolverApp {
    constructor() {
        this.gridManager = null;
        this.clueManager = null;
        this.stateManager = null;
        this.anagramManager = null;
        this.init();
    }

    async init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeModules());
        } else {
            this.initializeModules();
        }
    }

    initializeModules() {
        console.log('Initializing Crossword Solver...');

        try {
            // Initialize grid manager first
            this.gridManager = new GridManager();
            console.log('✓ Grid Manager initialized');

            // Initialize clue manager
            this.clueManager = new ClueManager(this.gridManager);
            console.log('✓ Clue Manager initialized');

            // Initialize state manager
            this.stateManager = new StateManager(this.gridManager);
            console.log('✓ State Manager initialized');

            // Initialize anagram manager
            this.anagramManager = new AnagramManager(this.gridManager, this.clueManager);
            console.log('✓ Anagram Manager initialized');

            // Try to load saved state from localStorage
            const loaded = this.stateManager.loadStateFromLocalStorage();
            if (loaded) {
                console.log('✓ Loaded saved state from browser');
            }

            // Setup keyboard shortcuts
            this.setupKeyboardShortcuts();

            // Mark app as ready
            document.body.classList.add('app-ready');
            console.log('✓ Crossword Solver ready!');

        } catch (error) {
            console.error('Error initializing app:', error);
            this.showError('Failed to initialize application. Please refresh the page.');
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Z for undo
            if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
                e.preventDefault();
                this.stateManager.undo();
            }

            // Ctrl/Cmd + Shift + Z or Ctrl/Cmd + Y for redo
            if ((e.ctrlKey || e.metaKey) && (e.shiftKey && e.key === 'z' || e.key === 'y')) {
                e.preventDefault();
                this.stateManager.redo();
            }

            // Ctrl/Cmd + S for save
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                this.stateManager.saveState();
            }

            // Escape to close dropdowns
            if (e.key === 'Escape') {
                this.closeAllDropdowns();
            }
        });
    }

    closeAllDropdowns() {
        const dropdowns = document.querySelectorAll('.solution-dropdown, .solution-input');
        dropdowns.forEach(dropdown => {
            dropdown.style.display = 'none';
        });
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'app-error';
        errorDiv.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #f44336;
            color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            z-index: 10001;
            max-width: 400px;
            text-align: center;
        `;
        errorDiv.innerHTML = `
            <h3 style="margin: 0 0 15px 0;">Error</h3>
            <p style="margin: 0 0 20px 0;">${message}</p>
            <button onclick="this.parentElement.remove()" style="
                background: white;
                color: #f44336;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
            ">Close</button>
        `;
        document.body.appendChild(errorDiv);
    }

    // Public API methods for external interaction
    getGridState() {
        return this.gridManager.getAllCellValues();
    }

    setGridState(cellValues) {
        this.gridManager.updateCells(cellValues);
    }

    clearGrid() {
        this.gridManager.clearGrid();
    }

    saveState() {
        return this.stateManager.saveState();
    }

    loadState() {
        return this.stateManager.loadState();
    }
}

// Initialize the app when script loads
let app;
if (typeof window !== 'undefined') {
    app = new CrosswordSolverApp();
    
    // Expose app instance globally for debugging
    window.crosswordApp = app;
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CrosswordSolverApp;
}
