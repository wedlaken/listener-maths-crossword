/**
 * Anagram Module
 * Handles anagram grid display and interactions
 */

class AnagramManager {
    constructor(gridManager, clueManager) {
        this.gridManager = gridManager;
        this.clueManager = clueManager;
        this.anagramGrid = null;
        this.isVisible = false;
        this.init();
    }

    init() {
        this.anagramGrid = document.getElementById('anagram-grid');
        this.anagramSection = document.getElementById('anagram-section');
        this.attachEventListeners();
        this.checkCompletion();
    }

    attachEventListeners() {
        // Listen for solution applications to check if puzzle is complete
        document.addEventListener('solutionApplied', () => {
            setTimeout(() => this.checkCompletion(), 500);
        });

        // Check completion button (if exists)
        const checkBtn = document.getElementById('check-completion-btn');
        if (checkBtn) {
            checkBtn.addEventListener('click', () => this.checkCompletion());
        }
    }

    async checkCompletion() {
        try {
            const response = await fetch('/check_completion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cells: this.gridManager.getAllCellValues()
                })
            });

            const data = await response.json();

            if (data.complete) {
                this.showAnagramGrid(data.anagram_data);
            }
        } catch (error) {
            console.error('Error checking completion:', error);
        }
    }

    showAnagramGrid(anagramData) {
        if (this.isVisible) return;

        if (this.anagramSection) {
            this.anagramSection.style.display = 'block';
            this.isVisible = true;

            // Scroll to anagram section
            this.anagramSection.scrollIntoView({ behavior: 'smooth' });

            // Show congratulations message
            this.showCongratulations();

            // Populate anagram grid if data provided
            if (anagramData && anagramData.cells) {
                this.populateAnagramGrid(anagramData.cells);
            }
        }
    }

    hideAnagramGrid() {
        if (this.anagramSection) {
            this.anagramSection.style.display = 'none';
            this.isVisible = false;
        }
    }

    populateAnagramGrid(cells) {
        // Populate the anagram grid cells
        Object.entries(cells).forEach(([index, value]) => {
            const cell = this.anagramGrid?.querySelector(`[data-cell="${index}"]`);
            if (cell) {
                let valueDiv = cell.querySelector('.cell-value');
                if (!valueDiv) {
                    valueDiv = document.createElement('div');
                    valueDiv.className = 'cell-value';
                    cell.appendChild(valueDiv);
                }
                valueDiv.textContent = value;
            }
        });
    }

    showCongratulations() {
        const message = document.createElement('div');
        message.className = 'congratulations-message';
        message.innerHTML = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                z-index: 10000;
                text-align: center;
                max-width: 500px;
                animation: popIn 0.5s ease-out;
            ">
                <h2 style="margin: 0 0 20px 0; font-size: 2em;">🎉 Congratulations! 🎉</h2>
                <p style="margin: 0 0 20px 0; font-size: 1.2em;">
                    You've completed the initial grid!
                </p>
                <p style="margin: 0; font-size: 1em; opacity: 0.9;">
                    Now solve the anagram grid below to finish the puzzle.
                </p>
            </div>
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                z-index: 9999;
            "></div>
        `;

        document.body.appendChild(message);

        // Remove after 4 seconds
        setTimeout(() => {
            message.style.animation = 'fadeOut 0.5s ease-out';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 4000);
    }

    async applyAnagramSolution(clueId, solution) {
        try {
            const response = await fetch('/apply_anagram_solution', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    clue_id: clueId,
                    solution: solution
                })
            });

            const data = await response.json();

            if (data.success) {
                // Update anagram grid cells
                if (data.updated_cells) {
                    this.populateAnagramGrid(data.updated_cells);
                }

                // Check if anagram grid is complete
                if (data.anagram_complete) {
                    this.showFinalCongratulations();
                }

                return true;
            }
        } catch (error) {
            console.error('Error applying anagram solution:', error);
        }
        return false;
    }

    showFinalCongratulations() {
        const message = document.createElement('div');
        message.className = 'final-congratulations';
        message.innerHTML = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 50px;
                border-radius: 20px;
                box-shadow: 0 25px 70px rgba(0,0,0,0.4);
                z-index: 10000;
                text-align: center;
                max-width: 600px;
                animation: popIn 0.6s ease-out;
            ">
                <h1 style="margin: 0 0 30px 0; font-size: 3em;">🏆 PUZZLE COMPLETE! 🏆</h1>
                <p style="margin: 0 0 25px 0; font-size: 1.4em;">
                    Congratulations on solving both grids!
                </p>
                <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">
                    You've successfully completed this Listener Crossword.
                </p>
            </div>
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.6);
                z-index: 9999;
            " onclick="this.parentElement.remove()"></div>
        `;

        document.body.appendChild(message);

        // Click anywhere to dismiss
        message.addEventListener('click', () => message.remove());
    }
}

// CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes popIn {
        0% {
            transform: translate(-50%, -50%) scale(0.5);
            opacity: 0;
        }
        100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }
    }
    
    @keyframes fadeOut {
        0% {
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }
    
    @keyframes slideIn {
        0% {
            transform: translateX(400px);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        0% {
            transform: translateX(0);
            opacity: 1;
        }
        100% {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnagramManager;
}
