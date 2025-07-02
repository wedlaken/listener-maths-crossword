#!/usr/bin/env python3
"""
Enhanced Interactive Crossword Solver with Anagram Grid Constraints
Adds validation for the second stage anagram grid requirements.
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
from anagram_grid_solver import find_anagram_multiples, generate_anagrams, validate_anagram_constraints

def validate_unclued_solution_for_anagram(clue_id: str, solution: int) -> Tuple[bool, List[str]]:
    """
    Validate that an unclued solution will work in the anagram grid.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check if solution has anagram multiples
    multiples = find_anagram_multiples(solution, max_digits=6)
    if not multiples:
        errors.append(f"Solution {solution} has no valid anagram multiples")
        return False, errors
    
    # Check first digit constraint
    first_digit = int(str(solution)[0])
    if first_digit > 5:
        errors.append(f"Solution {solution} starts with {first_digit} > 5 (anagram multiple would be too long)")
        return False, errors
    
    return True, errors

def generate_anagram_validation_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate HTML for anagram validation section."""
    html = ['<div class="anagram-validation-section">']
    html.append('  <h3>Anagram Grid Validation</h3>')
    html.append('  <div class="anagram-status">')
    html.append('    <div class="status-item">')
    html.append('      <span class="status-label">Stage 1 Complete:</span>')
    html.append('      <span class="status-value" id="stage1-status">❌ Incomplete</span>')
    html.append('    </div>')
    html.append('    <div class="status-item">')
    html.append('      <span class="status-label">Unclued Solutions Valid:</span>')
    html.append('      <span class="status-value" id="unclued-status">❌ Not checked</span>')
    html.append('    </div>')
    html.append('    <div class="status-item">')
    html.append('      <span class="status-label">Anagram Grid Possible:</span>')
    html.append('      <span class="status-value" id="anagram-status">❌ Not checked</span>')
    html.append('    </div>')
    html.append('  </div>')
    html.append('  <div class="anagram-details" id="anagram-details" style="display: none;">')
    html.append('    <h4>Unclued Solution Analysis</h4>')
    html.append('    <div id="unclued-analysis"></div>')
    html.append('  </div>')
    html.append('</div>')
    
    return '\n'.join(html)

def generate_enhanced_interactive_html(clue_objects: Dict[Tuple[int, str], ListenerClue]) -> str:
    """Generate the complete enhanced interactive HTML interface."""
    
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
    anagram_section = generate_anagram_validation_html(clue_objects)
    
    # Insert anagram section before the closing body tag
    base_html = base_html.replace('</body>', f'{anagram_section}\n</body>')
    
    # Add anagram validation JavaScript
    anagram_js = '''
        // Anagram validation functions
        function validateAnagramConstraints() {
            const uncluedClues = ['12_ACROSS', '14_ACROSS', '7_DOWN', '8_DOWN'];
            const analysis = [];
            let allValid = true;
            
            for (const clueId of uncluedClues) {
                const clue = clueObjects[clueId];
                if (clue.possible_solutions.length === 1) {
                    const solution = clue.possible_solutions[0];
                    const multiples = findAnagramMultiples(solution);
                    
                    if (multiples.length > 0) {
                        analysis.push(`<div class="valid-solution">✓ ${clueId}: ${solution} has ${multiples.length} anagram multiples</div>`);
                    } else {
                        analysis.push(`<div class="invalid-solution">✗ ${clueId}: ${solution} has no anagram multiples</div>`);
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
        
        function findAnagramMultiples(number) {
            // Simplified anagram multiple finder
            const digits = String(number).split('').sort().join('');
            const multiples = [];
            
            // Check multiples up to 6 digits
            for (let i = 2; i <= 999999 / number; i++) {
                const multiple = number * i;
                if (String(multiple).length <= 6) {
                    const multipleDigits = String(multiple).split('').sort().join('');
                    if (multipleDigits === digits && multiple !== number) {
                        multiples.push(multiple);
                    }
                }
            }
            
            return multiples;
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
            // Call original function
            originalApplySolution(clueId, solution);
            
            // Update anagram status
            updateAnagramStatus();
        };
        
        // Initialize anagram status
        document.addEventListener('DOMContentLoaded', function() {
            updateAnagramStatus();
        });
    '''
    
    # Insert JavaScript before the closing script tag
    base_html = base_html.replace('</script>', f'{anagram_js}\n</script>')
    
    # Add CSS for anagram validation
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
        
        .anagram-details {
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
    base_html = base_html.replace('</style>', f'{anagram_css}\n</style>')
    
    return base_html

def main():
    """Main function to generate enhanced interactive solver."""
    print("=== ENHANCED INTERACTIVE CROSSWORD SOLVER ===")
    print("Now with Anagram Grid Validation!")
    
    # Load clue objects using systematic grid parser and clue classes
    from interactive_solver import load_clue_objects
    grid_clues, clue_objects, clue_manager = load_clue_objects()
    
    print(f"Loaded {len(grid_clues)} grid clues")
    print(f"Loaded {len(clue_objects)} clue objects")
    
    # Generate enhanced interactive HTML
    html_content = generate_enhanced_interactive_html(clue_objects)
    
    # Save and open
    filename = "enhanced_interactive_solver.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated enhanced interactive solver: {filename}")
    print("Open this file in a web browser to use the enhanced solver")
    print("Features:")
    print("- Real-time anagram constraint validation")
    print("- Unclued solution analysis")
    print("- Stage 2 grid possibility checking")
    
    # Try to open in browser
    try:
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        print("Opened in default web browser")
    except:
        print("Please open the HTML file manually in your web browser")

if __name__ == "__main__":
    main() 