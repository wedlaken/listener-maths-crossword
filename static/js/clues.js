/**
 * Clues Module
 * Handles clue interactions, solution selection, and application
 */

class ClueManager {
    constructor(gridManager) {
        this.gridManager = gridManager;
        this.clues = {};
        this.clueElements = {};
        this.init();
    }

    init() {
        this.setupClues();
        this.attachEventListeners();
    }

    setupClues() {
        const clueElements = document.querySelectorAll('.clue');
        clueElements.forEach(clueEl => {
            const clueId = clueEl.dataset.clue;
            const gridType = clueEl.dataset.gridType || 'initial';
            
            this.clueElements[clueId] = {
                element: clueEl,
                gridType: gridType,
                dropdown: clueEl.querySelector('.solution-dropdown'),
                select: clueEl.querySelector('.solution-select'),
                applyButton: clueEl.querySelector('.apply-solution'),
                input: clueEl.querySelector('.solution-text-input')
            };
        });
    }

    attachEventListeners() {
        Object.entries(this.clueElements).forEach(([clueId, clue]) => {
            // Clue header click - toggle dropdown
            const header = clue.element.querySelector('.clue-header');
            if (header) {
                header.addEventListener('click', () => this.toggleClueDropdown(clueId));
            }

            // Apply button click
            if (clue.applyButton) {
                clue.applyButton.addEventListener('click', () => this.applySolution(clueId));
            }

            // Select change - auto apply on selection
            if (clue.select) {
                clue.select.addEventListener('change', () => {
                    if (clue.select.value) {
                        this.applySolution(clueId);
                    }
                });
            }

            // Input enter key
            if (clue.input) {
                clue.input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.applySolution(clueId);
                    }
                });
            }
        });

        // Listen for cell clicks to highlight corresponding clue
        document.addEventListener('cellClicked', (e) => {
            this.highlightClueForCell(e.detail.cellIndex);
        });
    }

    toggleClueDropdown(clueId) {
        const clue = this.clueElements[clueId];
        if (!clue) return;

        // Hide all other dropdowns first
        Object.entries(this.clueElements).forEach(([id, c]) => {
            if (id !== clueId && c.dropdown) {
                c.dropdown.style.display = 'none';
            }
            if (id !== clueId && c.input?.parentElement) {
                c.input.parentElement.style.display = 'none';
            }
        });

        // Toggle this dropdown
        if (clue.dropdown) {
            const isVisible = clue.dropdown.style.display !== 'none';
            clue.dropdown.style.display = isVisible ? 'none' : 'block';
        }
        if (clue.input?.parentElement) {
            const isVisible = clue.input.parentElement.style.display !== 'none';
            clue.input.parentElement.style.display = isVisible ? 'none' : 'block';
        }

        // Highlight the clue
        this.highlightClue(clueId);
    }

    highlightClue(clueId) {
        // Remove highlight from all clues
        Object.values(this.clueElements).forEach(clue => {
            clue.element.classList.remove('active-clue');
        });

        // Highlight selected clue
        const clue = this.clueElements[clueId];
        if (clue) {
            clue.element.classList.add('active-clue');
        }

        // Dispatch event for grid highlighting
        document.dispatchEvent(new CustomEvent('clueSelected', {
            detail: { clueId }
        }));
    }

    highlightClueForCell(cellIndex) {
        // Find which clue this cell belongs to and highlight it
        // This would need clue-to-cells mapping from the backend
        console.log('Highlighting clue for cell:', cellIndex);
    }

    async applySolution(clueId) {
        const clue = this.clueElements[clueId];
        if (!clue) return;

        let solution = '';
        
        if (clue.select && clue.select.value) {
            solution = clue.select.value;
        } else if (clue.input && clue.input.value) {
            solution = clue.input.value;
        }

        if (!solution) return;

        try {
            // Send to backend
            const response = await fetch('/apply_solution', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    clue_id: clueId,
                    solution: solution,
                    grid_type: clue.gridType
                })
            });

            const data = await response.json();

            if (data.success) {
                // Update grid with new values
                if (data.updated_cells) {
                    this.gridManager.updateCells(data.updated_cells);
                }

                // Update solution counts if provided
                if (data.solution_counts) {
                    this.updateSolutionCounts(data.solution_counts);
                }

                // Hide dropdown after successful application
                if (clue.dropdown) {
                    clue.dropdown.style.display = 'none';
                }
                if (clue.input?.parentElement) {
                    clue.input.parentElement.style.display = 'none';
                    clue.input.value = '';
                }

                // Dispatch success event
                document.dispatchEvent(new CustomEvent('solutionApplied', {
                    detail: { clueId, solution, data }
                }));
            } else {
                console.error('Failed to apply solution:', data.error);
                this.showError(clueId, data.error);
            }
        } catch (error) {
            console.error('Error applying solution:', error);
            this.showError(clueId, 'Network error. Please try again.');
        }
    }

    updateSolutionCounts(counts) {
        Object.entries(counts).forEach(([clueId, count]) => {
            const countElement = document.getElementById(`solution-count-${clueId}`);
            if (countElement) {
                const word = count === 1 ? 'solution' : 'solutions';
                countElement.textContent = `${count} ${word}`;
            }
        });
    }

    showError(clueId, message) {
        const errorElement = document.getElementById(`error-${clueId}`);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'inline';
            setTimeout(() => {
                errorElement.style.display = 'none';
            }, 3000);
        }
    }

    updateClueDropdowns(clueId, solutions) {
        const clue = this.clueElements[clueId];
        if (!clue || !clue.select) return;

        // Clear existing options except placeholder
        clue.select.innerHTML = '<option value="">-- Select a solution --</option>';

        // Add new solutions
        solutions.forEach(solution => {
            const option = document.createElement('option');
            option.value = solution;
            option.textContent = solution;
            clue.select.appendChild(option);
        });
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ClueManager;
}
