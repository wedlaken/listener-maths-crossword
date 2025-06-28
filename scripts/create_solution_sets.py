#!/usr/bin/env python3
"""
Create solution sets JSON file from puzzle solution export
"""

import json
import re
from collections import defaultdict

def extract_solution_sets(filename: str = "puzzle_solution_export.txt") -> dict:
    """Extract solution sets from the solution export file."""
    solution_sets = defaultdict(set)
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Look for lines like "1. Clue 5 DOWN: 2048" or "3. Clue 18 ACROSS: 1024"
                match = re.match(r'\d+\.\s*Clue\s+(\d+)\s+(ACROSS|DOWN):\s+(\d+)', line)
                if match:
                    number = int(match.group(1))
                    direction = match.group(2)
                    solution = match.group(3)
                    
                    clue_id = f"{number}_{direction}"
                    solution_sets[clue_id].add(solution)
                    print(f"Found: {clue_id} = {solution}")
    except FileNotFoundError:
        print(f"Warning: Could not find solution export file {filename}")
        return {}
    
    # Convert sets to lists for JSON serialization
    return {clue_id: list(solutions) for clue_id, solutions in solution_sets.items()}

def main():
    """Main function to create solution sets JSON file."""
    print("=== CREATING SOLUTION SETS ===")
    
    solution_sets = extract_solution_sets()
    
    print(f"Extracted {len(solution_sets)} solution sets:")
    for clue_id, solutions in solution_sets.items():
        print(f"  {clue_id}: {len(solutions)} solutions")
    
    # Save to JSON file
    with open("data/solution_sets.json", 'w') as f:
        json.dump(solution_sets, f, indent=2)
    
    print(f"Saved solution sets to data/solution_sets.json")

if __name__ == "__main__":
    main() 