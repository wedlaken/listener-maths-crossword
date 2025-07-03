#!/usr/bin/env python3
"""
Enhanced Interactive Solver with Unclued Validation
Integrates the pre-computed unclued solution sets for better user experience
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

def load_unclued_data() -> Tuple[Set[int], Dict[int, List[int]]]:
    """Load unclued validation data."""
    try:
        with open('data/unclued_validation.json', 'r') as f:
            data = json.load(f)
            valid_candidates = set(data['valid_candidates'])
            candidate_multiples = {int(k): v for k, v in data['candidate_multiples'].items()}
            return valid_candidates, candidate_multiples
    except FileNotFoundError:
        print("Warning: unclued_validation.json not found. Run scripts/generate_unclued_solution_sets.py first.")
        return set(), {}

def generate_enhanced_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate enhanced HTML with unclued validation."""
    
    # Load unclued data
    valid_candidates, candidate_multiples = load_unclued_data()
    
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
    
    # Add unclued validation section
    validation_section = f'''
        <div class="unclued-validation-section">
            <h3>Unclued Solution Validation</h3>
            <div class="validation-info">
                <div class="info-item">
                    <span class="info-label">Valid Candidates:</span>
                    <span class="info-value">{len(valid_candidates)} found</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Candidates:</span>
                    <span class="info-value">{', '.join(map(str, sorted(valid_candidates)))}</span>
                </div>
            </div>
            <div class="validation-status">
                <div class="status-item">
                    <span class="status-label">Unclued Solutions Valid:</span>
                    <span class="status-value" id="unclued-status">❌ Not checked</span>
                </div>
            </div>
            <div class="validation-details" id="validation-details" style="display: none;">
                <h4>Unclued Solution Analysis</h4>
                <div id="unclued-analysis"></div>
            </div>
        </div>
    '''
    
    # Insert validation section before the closing body tag
    base_html = base_html.replace('</body>', f'{validation_section}\n</body>')
    
    # Add validation JavaScript
    validation_js = f'''
        // Unclued validation data
        const validCandidates = new Set({list(valid_candidates)});
        const candidateMultiples = {candidate_multiples};
        
        function validateUncluedSolution(clueId, solution) {{
            if (!validCandidates.has(solution)) {{
                return {{
                    valid: false,
                    error: `Solution ${{solution}} is not a valid unclued candidate. Valid candidates are: ${{Array.from(validCandidates).join(', ')}}`
                }};
            }}
            
            const multiples = candidateMultiples[solution] || [];
            return {{
                valid: true,
                multiples: multiples,
                message: `✓ Valid! ${{solution}} has ${{multiples.length}} anagram multiple(s): ${{multiples.join(', ')}}`
            }};
        }}
        
        function updateUncluedValidation() {{
            const uncluedClues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN'];
            const analysis = [];
            let allValid = true;
            
            for (const clueId of uncluedClues) {{
                const clue = clueObjects[clueId];
                if (clue.possible_solutions.length === 1) {{
                    const solution = clue.possible_solutions[0];
                    const validation = validateUncluedSolution(clueId, solution);
                    
                    if (validation.valid) {{
                        analysis.push(`<div class="valid-solution">${{validation.message}}</div>`);
                    }} else {{
                        analysis.push(`<div class="invalid-solution">✗ ${{clueId}}: ${{validation.error}}</div>`);
                        allValid = false;
                    }}
                }} else {{
                    analysis.push(`<div class="unsolved">? ${{clueId}}: Not yet solved</div>`);
                    allValid = false;
                }}
            }}
            
            document.getElementById('unclued-analysis').innerHTML = analysis.join('');
            document.getElementById('unclued-status').textContent = allValid ? '✅ Valid' : '❌ Invalid';
            document.getElementById('validation-details').style.display = 'block';
        }}
        
        // Override the original applySolutionToGrid function
        const originalApplySolution = applySolutionToGrid;
        applySolutionToGrid = function(clueId, solution) {{
            // For unclued clues, validate against our candidate set
            if (clueObjects[clueId].is_unclued) {{
                const validation = validateUncluedSolution(clueId, parseInt(solution));
                if (!validation.valid) {{
                    showNotification(validation.error, 'error');
                    return;
                }}
                showNotification(validation.message, 'success');
            }}
            
            // Call original function
            originalApplySolution(clueId, solution);
            
            // Update validation status
            updateUncluedValidation();
        }};
        
        // Initialize validation
        document.addEventListener('DOMContentLoaded', function() {{
            updateUncluedValidation();
        }});
    '''
    
    # Insert JavaScript before the closing script tag
    base_html = base_html.replace('</script>', f'{validation_js}\n</script>')
    
    # Add CSS for validation
    validation_css = '''
        .unclued-validation-section {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #28a745;
        }
        
        .unclued-validation-section h3 {
            margin-top: 0;
            color: #333;
        }
        
        .validation-info {
            margin-bottom: 15px;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }
        
        .info-label {
            font-weight: bold;
            color: #666;
        }
        
        .info-value {
            font-weight: bold;
            color: #333;
        }
        
        .validation-status {
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
        
        .validation-details {
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
    '''
    
    # Insert CSS before the closing style tag
    base_html = base_html.replace('</style>', f'{validation_css}\n</style>')
    
    return base_html

def main():
    """Main function to generate enhanced solver."""
    print("=== ENHANCED UNCLUED SOLVER ===")
    print("Now with pre-computed unclued solution validation!")
    
    # Load clue objects
    from interactive_solver import load_clue_objects
    grid_clues, clue_objects, clue_manager = load_clue_objects()
    
    print(f"Loaded {len(grid_clues)} grid clues")
    print(f"Loaded {len(clue_objects)} clue objects")
    
    # Load unclued data
    valid_candidates, candidate_multiples = load_unclued_data()
    print(f"Loaded {len(valid_candidates)} valid unclued candidates")
    
    # Generate enhanced HTML
    html_content = generate_enhanced_html(clue_objects)
    
    # Save and open
    filename = "enhanced_unclued_solver.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated enhanced solver: {filename}")
    print("Open this file in a web browser to use the enhanced solver")
    print("Features:")
    print("- Real-time validation of unclued solutions")
    print("- Pre-computed candidate set (6 valid candidates)")
    print("- Anagram multiple information")
    print("- Clear error messages for invalid solutions")
    
    # Try to open in browser
    try:
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        print("Opened in default web browser")
    except:
        print("Please open the HTML file manually in your web browser")

if __name__ == "__main__":
    main() 