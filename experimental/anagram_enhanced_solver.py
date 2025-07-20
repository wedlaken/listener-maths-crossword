#!/usr/bin/env python3
"""
Anagram-Enhanced Interactive Crossword Solver
Integrates anagram validation for unclued solutions with existing solution set structure
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
import webbrowser
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from systematic_grid_parser import parse_grid, ClueTuple
from clue_classes import ListenerClue, ClueFactory, ClueManager, ClueParameters
from utils import find_anagram_multiples, generate_anagrams, validate_anagram_constraints

class AnagramEnhancedClueManager(ClueManager):
    """Enhanced clue manager with anagram validation for unclued clues."""
    
    def __init__(self):
        super().__init__()
        self.unclued_validation_data = self._load_unclued_validation()
        self.unclued_solution_sets = self._load_unclued_solution_sets()
    
    def _load_unclued_validation(self) -> Dict:
        """Load unclued validation data."""
        try:
            with open('data/unclued_validation.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: unclued_validation.json not found. Run scripts/generate_unclued_solution_sets.py first.")
            return {'valid_candidates': [], 'candidate_multiples': {}}
    
    def _load_unclued_solution_sets(self) -> Dict[str, List[int]]:
        """Load unclued solution sets."""
        try:
            with open('data/unclued_solution_sets.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: unclued_solution_sets.json not found. Run scripts/generate_unclued_solution_sets.py first.")
            return {}
    
    def validate_unclued_solution(self, clue_id: str, solution: int) -> Tuple[bool, List[str]]:
        """
        Validate an unclued solution against anagram constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if solution is in our valid candidates
        valid_candidates = set(self.unclued_validation_data.get('valid_candidates', []))
        if solution not in valid_candidates:
            errors.append(f"Solution {solution} is not a valid unclued candidate (no anagram multiples)")
            return False, errors
        
        # Check first digit constraint
        first_digit = int(str(solution)[0])
        if first_digit > 5:
            errors.append(f"Solution {solution} starts with {first_digit} > 5 (anagram multiple would be too long)")
            return False, errors
        
        # Get anagram multiples for feedback
        multiples = self.unclued_validation_data.get('candidate_multiples', {}).get(str(solution), [])
        if multiples:
            errors.append(f"✓ Valid! {solution} has {len(multiples)} anagram multiples: {multiples[:3]}{'...' if len(multiples) > 3 else ''}")
        
        return True, errors
    
    def get_unclued_suggestions(self, clue_id: str, current_constraints: Dict[int, int] = None) -> List[int]:
        """
        Get suggested solutions for an unclued clue based on current grid constraints.
        
        Args:
            clue_id: The unclued clue ID
            current_constraints: Current solved cells {cell_index: digit}
        
        Returns:
            List of suggested solutions
        """
        if clue_id not in self.unclued_solution_sets:
            return []
        
        all_candidates = self.unclued_solution_sets[clue_id]
        
        if not current_constraints:
            return all_candidates[:10]  # Return first 10 for display
        
        # Filter based on current grid constraints
        filtered_candidates = []
        for candidate in all_candidates:
            candidate_str = str(candidate).zfill(6)
            is_valid = True
            
            # Check each cell position
            for i, cell_index in enumerate(self.clues[int(clue_id.split('_')[0])].cell_indices):
                if cell_index in current_constraints:
                    expected_digit = current_constraints[cell_index]
                    actual_digit = int(candidate_str[i])
                    if expected_digit != actual_digit:
                        is_valid = False
                        break
            
            if is_valid:
                filtered_candidates.append(candidate)
                if len(filtered_candidates) >= 10:  # Limit to 10 suggestions
                    break
        
        return filtered_candidates

def generate_anagram_enhanced_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate the complete anagram-enhanced interactive HTML interface."""
    
    # Convert clue objects to JSON for JavaScript
    clue_data = {}
    for (number, direction), clue in clue_objects.items():
        clue_data[f"{number}_{direction}"] = {
            'number': clue.number,
            'direction': clue.direction,
            'cell_indices': list(clue.cell_indices),
            'length': clue.length,
            'is_unclued': clue.parameters.is_unclued,
            'possible_solutions': list(clue.possible_solutions),
            'original_solution_count': clue.original_solution_count
        }
    
    # Generate the base HTML from interactive_solver.py
    from interactive_solver import generate_interactive_html
    base_html = generate_interactive_html(clue_objects)
    
    # Add anagram validation section
    anagram_section = '''
        <div class="anagram-validation-section">
            <h3>Anagram Grid Validation</h3>
            <div class="anagram-status">
                <div class="status-item">
                    <span class="status-label">Stage 1 Complete:</span>
                    <span class="status-value" id="stage1-status">❌ Incomplete</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Unclued Solutions Valid:</span>
                    <span class="status-value" id="unclued-status">❌ Not checked</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Anagram Grid Possible:</span>
                    <span class="status-value" id="anagram-status">❌ Not checked</span>
                </div>
            </div>
            <div class="anagram-details" id="anagram-details" style="display: none;">
                <h4>Unclued Solution Analysis</h4>
                <div id="unclued-analysis"></div>
            </div>
            <div class="anagram-suggestions" id="anagram-suggestions" style="display: none;">
                <h4>Unclued Solution Suggestions</h4>
                <div id="suggestions-list"></div>
            </div>
        </div>
    '''
    
    # Insert anagram section before the closing body tag
    base_html = base_html.replace('</body>', f'{anagram_section}\n</body>')
    
    # Add enhanced anagram validation JavaScript
    anagram_js = '''
        // Enhanced anagram validation functions
        let uncluedValidationData = null;
        let uncluedSolutionSets = null;
        
        // Load validation data
        async function loadUncluedData() {
            try {
                const [validationResponse, solutionSetsResponse] = await Promise.all([
                    fetch('data/unclued_validation.json'),
                    fetch('data/unclued_solution_sets.json')
                ]);
                
                if (validationResponse.ok) {
                    uncluedValidationData = await validationResponse.json();
                }
                
                if (solutionSetsResponse.ok) {
                    uncluedSolutionSets = await solutionSetsResponse.json();
                }
                
                console.log('Loaded unclued validation data:', uncluedValidationData ? 'success' : 'failed');
                console.log('Loaded unclued solution sets:', uncluedSolutionSets ? 'success' : 'failed');
            } catch (error) {
                console.log('Could not load unclued data:', error);
            }
        }
        
        function validateUncluedSolution(clueId, solution) {
            if (!uncluedValidationData) {
                return { valid: true, errors: ['Validation data not loaded'] };
            }
            
            const validCandidates = new Set(uncluedValidationData.valid_candidates);
            const errors = [];
            
            if (!validCandidates.has(solution)) {
                errors.push(`Solution ${solution} is not a valid unclued candidate (no anagram multiples)`);
                return { valid: false, errors };
            }
            
            // Check first digit constraint
            const firstDigit = parseInt(String(solution)[0]);
            if (firstDigit > 5) {
                errors.push(`Solution ${solution} starts with ${firstDigit} > 5 (anagram multiple would be too long)`);
                return { valid: false, errors };
            }
            
            // Get anagram multiples for feedback
            const multiples = uncluedValidationData.candidate_multiples[solution] || [];
            if (multiples.length > 0) {
                errors.push(`✓ Valid! ${solution} has ${multiples.length} anagram multiples: ${multiples.slice(0, 3).join(', ')}${multiples.length > 3 ? '...' : ''}`);
            }
            
            return { valid: true, errors };
        }
        
        function getUncluedSuggestions(clueId) {
            if (!uncluedSolutionSets || !uncluedSolutionSets[clueId]) {
                return [];
            }
            
            const allCandidates = uncluedSolutionSets[clueId];
            
            // Filter based on current grid constraints
            const filteredCandidates = [];
            for (const candidate of allCandidates) {
                const candidateStr = String(candidate).padStart(6, '0');
                let isValid = true;
                
                // Check each cell position against current solved cells
                const clue = clueObjects[clueId];
                for (let i = 0; i < clue.cell_indices.length; i++) {
                    const cellIndex = clue.cell_indices[i];
                    if (cellIndex in solvedCells) {
                        const expectedDigit = solvedCells[cellIndex];
                        const actualDigit = parseInt(candidateStr[i]);
                        if (expectedDigit !== actualDigit) {
                            isValid = false;
                            break;
                        }
                    }
                }
                
                if (isValid) {
                    filteredCandidates.push(candidate);
                    if (filteredCandidates.length >= 10) {
                        break;
                    }
                }
            }
            
            return filteredCandidates;
        }
        
        function showUncluedSuggestions(clueId) {
            const suggestions = getUncluedSuggestions(clueId);
            const suggestionsDiv = document.getElementById('suggestions-list');
            
            if (suggestions.length > 0) {
                const suggestionsHtml = suggestions.map(s => 
                    `<div class="suggestion-item" onclick="applyUncluedSuggestion('${clueId}', ${s})">${s}</div>`
                ).join('');
                suggestionsDiv.innerHTML = suggestionsHtml;
                document.getElementById('anagram-suggestions').style.display = 'block';
            } else {
                suggestionsDiv.innerHTML = '<div class="no-suggestions">No valid suggestions based on current constraints</div>';
                document.getElementById('anagram-suggestions').style.display = 'block';
            }
        }
        
        function applyUncluedSuggestion(clueId, solution) {
            // Apply the suggested solution
            applySolutionToGrid(clueId, solution.toString());
            
            // Hide suggestions
            document.getElementById('anagram-suggestions').style.display = 'none';
        }
        
        function validateAnagramConstraints() {
            const uncluedClues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN'];
            const analysis = [];
            let allValid = true;
            
            for (const clueId of uncluedClues) {
                const clue = clueObjects[clueId];
                if (clue.possible_solutions.length === 1) {
                    const solution = clue.possible_solutions[0];
                    const validation = validateUncluedSolution(clueId, solution);
                    
                    if (validation.valid) {
                        analysis.push(`<div class="valid-solution">✓ ${clueId}: ${solution} - ${validation.errors[0] || 'Valid'}</div>`);
                    } else {
                        analysis.push(`<div class="invalid-solution">✗ ${clueId}: ${solution} - ${validation.errors[0]}</div>`);
                        allValid = false;
                    }
                } else {
                    analysis.push(`<div class="unsolved">? ${clueId}: Not yet solved</div>`);
                    allValid = false;
                }
            }
            
            document.getElementById('unclued-analysis').innerHTML = analysis.join('');
            document.getElementById('unclued-status').textContent = allValid ? '✅ Valid' : '❌ Invalid';
            document.getElementById('anagram-details').style.display = 'block';
            
            return allValid;
        }
        
        function updateAnagramStatus() {
            // Check if Stage 1 is complete
            let stage1Complete = true;
            for (const clue of Object.values(clueObjects)) {
                if (clue.possible_solutions.length !== 1) {
                    stage1Complete = false;
                    break;
                }
            }
            
            document.getElementById('stage1-status').textContent = stage1Complete ? '✅ Complete' : '❌ Incomplete';
            
            if (stage1Complete) {
                const uncluedValid = validateAnagramConstraints();
                document.getElementById('anagram-status').textContent = uncluedValid ? '✅ Possible' : '❌ Impossible';
            } else {
                document.getElementById('anagram-status').textContent = '❌ Not checked';
            }
        }
        
        // Override the original applySolutionToGrid function
        const originalApplySolution = applySolutionToGrid;
        applySolutionToGrid = function(clueId, solution) {
            // For unclued clues, validate against anagram constraints
            if (clueObjects[clueId].is_unclued) {
                const validation = validateUncluedSolution(clueId, parseInt(solution));
                if (!validation.valid) {
                    showNotification(validation.errors[0], 'error');
                    return;
                }
            }
            
            // Call original function
            originalApplySolution(clueId, solution);
            
            // Update anagram status
            updateAnagramStatus();
        };
        
        // Add suggestion button to unclued clues
        function addSuggestionButtons() {
            const uncluedClues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN'];
            
            uncluedClues.forEach(clueId => {
                const clueElement = document.querySelector(`[data-clue="${clueId}"]`);
                if (clueElement) {
                    const inputDiv = clueElement.querySelector('.solution-input');
                    if (inputDiv) {
                        const suggestionButton = document.createElement('button');
                        suggestionButton.textContent = 'Get Suggestions';
                        suggestionButton.className = 'suggestion-button';
                        suggestionButton.onclick = () => showUncluedSuggestions(clueId);
                        inputDiv.appendChild(suggestionButton);
                    }
                }
            });
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadUncluedData().then(() => {
                updateAnagramStatus();
                addSuggestionButtons();
            });
        });
    '''
    
    # Insert JavaScript before the closing script tag
    base_html = base_html.replace('</script>', f'{anagram_js}\n</script>')
    
    # Add CSS for enhanced anagram validation
    anagram_css = '''
        .anagram-validation-section {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #17a2b8;
        }
        
        .anagram-validation-section h3 {
            margin-top: 0;
            color: #333;
        }
        
        .anagram-status {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .status-label {
            font-weight: bold;
            color: #666;
        }
        
        .status-value {
            font-weight: bold;
        }
        
        .anagram-details, .anagram-suggestions {
            margin-top: 15px;
            padding: 10px;
            background-color: white;
            border-radius: 4px;
        }
        
        .valid-solution {
            color: #28a745;
            font-weight: bold;
        }
        
        .invalid-solution {
            color: #dc3545;
            font-weight: bold;
        }
        
        .unsolved {
            color: #6c757d;
            font-style: italic;
        }
        
        .suggestion-button {
            background-color: #17a2b8;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            margin-left: 8px;
        }
        
        .suggestion-button:hover {
            background-color: #138496;
        }
        
        .suggestion-item {
            padding: 4px 8px;
            margin: 2px 0;
            background-color: #e9ecef;
            border-radius: 4px;
            cursor: pointer;
            font-family: monospace;
        }
        
        .suggestion-item:hover {
            background-color: #dee2e6;
        }
        
        .no-suggestions {
            color: #6c757d;
            font-style: italic;
        }
    '''
    
    # Insert CSS before the closing style tag
    base_html = base_html.replace('</style>', f'{anagram_css}\n</style>')
    
    return base_html

def main():
    """Main function to generate anagram-enhanced interactive solver."""
    print("=== ANAGRAM-ENHANCED INTERACTIVE CROSSWORD SOLVER ===")
    print("Now with intelligent unclued solution validation and suggestions!")
    
    # Load clue objects using systematic grid parser and clue classes
    from interactive_solver import load_clue_objects
    grid_clues, clue_objects, clue_manager = load_clue_objects()
    
    print(f"Loaded {len(grid_clues)} grid clues")
    print(f"Loaded {len(clue_objects)} clue objects")
    
    # Generate enhanced interactive HTML
    html_content = generate_anagram_enhanced_html(clue_objects)
    
    # Save and open
    filename = "anagram_enhanced_solver.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated anagram-enhanced solver: {filename}")
    print("Open this file in a web browser to use the enhanced solver")
    print("Features:")
    print("- Real-time anagram constraint validation for unclued solutions")
    print("- Intelligent solution suggestions based on grid constraints")
    print("- Fast validation using pre-computed candidate sets")
    print("- Stage 2 grid possibility checking")
    print("- Integration with existing solution set structure")
    
    # Try to open in browser
    try:
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        print("Opened in default web browser")
    except:
        print("Please open the HTML file manually in your web browser")

if __name__ == "__main__":
    main() 