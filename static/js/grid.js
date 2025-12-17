/**
 * Grid Module
 * Handles grid display, cell interactions, and visual updates
 */

class GridManager {
    constructor() {
        this.cells = {};
        this.selectedClue = null;
        this.grid = null;
        this.init();
    }

    init() {
        this.grid = document.querySelector('.crossword-grid');
        if (!this.grid) {
            console.error('Grid not found');
            return;
        }
        this.setupCells();
        this.attachEventListeners();
    }

    setupCells() {
        const cellElements = document.querySelectorAll('.grid-cell');
        cellElements.forEach(cell => {
            const cellIndex = parseInt(cell.dataset.cell);
            this.cells[cellIndex] = {
                element: cell,
                value: cell.querySelector('.cell-value')?.textContent || '',
                clueNumber: cell.querySelector('.grid-clue-number')?.textContent || null
            };
        });
    }

    attachEventListeners() {
        // Cell click handlers would go here
        Object.values(this.cells).forEach(cell => {
            cell.element.addEventListener('click', (e) => this.handleCellClick(e));
        });
    }

    handleCellClick(event) {
        const cell = event.currentTarget;
        const cellIndex = parseInt(cell.dataset.cell);
        
        // Highlight clicked cell
        this.clearHighlights();
        cell.classList.add('highlighted');
        
        // Dispatch custom event for other modules
        document.dispatchEvent(new CustomEvent('cellClicked', {
            detail: { cellIndex, cell }
        }));
    }

    clearHighlights() {
        Object.values(this.cells).forEach(cell => {
            cell.element.classList.remove('highlighted', 'clue-highlight');
        });
    }

    highlightClue(clueId, cellIndices) {
        this.clearHighlights();
        cellIndices.forEach(index => {
            if (this.cells[index]) {
                this.cells[index].element.classList.add('clue-highlight');
            }
        });
        this.selectedClue = clueId;
    }

    updateCell(cellIndex, value) {
        if (!this.cells[cellIndex]) return;
        
        const cell = this.cells[cellIndex];
        let valueDiv = cell.element.querySelector('.cell-value');
        
        if (value) {
            if (!valueDiv) {
                valueDiv = document.createElement('div');
                valueDiv.className = 'cell-value';
                cell.element.appendChild(valueDiv);
            }
            valueDiv.textContent = value;
            cell.value = value;
        } else {
            if (valueDiv) {
                valueDiv.remove();
            }
            cell.value = '';
        }
    }

    updateCells(cellValues) {
        Object.entries(cellValues).forEach(([index, value]) => {
            this.updateCell(parseInt(index), value);
        });
    }

    getCellValue(cellIndex) {
        return this.cells[cellIndex]?.value || '';
    }

    getAllCellValues() {
        const values = {};
        Object.entries(this.cells).forEach(([index, cell]) => {
            if (cell.value) {
                values[index] = cell.value;
            }
        });
        return values;
    }

    clearGrid() {
        Object.keys(this.cells).forEach(index => {
            this.updateCell(parseInt(index), '');
        });
    }

    setReadOnly(readonly) {
        Object.values(this.cells).forEach(cell => {
            if (readonly) {
                cell.element.classList.add('readonly');
            } else {
                cell.element.classList.remove('readonly');
            }
        });
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GridManager;
}
