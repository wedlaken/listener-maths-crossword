"""
Test script for the new clue classes
Demonstrates how to create and manage ListenerClue objects with actual puzzle data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import SystematicGridParser, ClueTuple
from clue_classes import ClueFactory, ClueManager, ListenerClue, ClueParameters
from typing import Dict, List, Tuple

def load_clue_parameters() -> Dict[int, Tuple[int, int]]:
    """Load clue parameters from the text file"""
    clue_parameters = {}
    
    try:
        with open('data/Listener 4869 clues.txt', 'r') as f:
            lines = f.readlines()
        
        current_direction = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower() == 'across':
                current_direction = 'ACROSS'
            elif line.lower() == 'down':
                current_direction = 'DOWN'
            elif current_direction and ':' in line:
                # Parse clue line: "number b:c" or "number Unclued"
                parts = line.split()
                if len(parts) >= 2:
                    clue_number = int(parts[0])
                    
                    if parts[1].lower() == 'unclued':
                        # Unclued clues have parameters (-1, -1)
                        clue_parameters[clue_number] = (-1, -1)
                    else:
                        # Parse "b:c" format
                        b_c_parts = parts[1].split(':')
                        if len(b_c_parts) == 2:
                            b = int(b_c_parts[0])
                            c = int(b_c_parts[1])
                            clue_parameters[clue_number] = (b, c)
        
        print(f"Loaded {len(clue_parameters)} clue parameters from text file")
        return clue_parameters
        
    except FileNotFoundError:
        print("Error: data/Listener 4869 clues.txt not found")
        return {}
    except Exception as e:
        print(f"Error reading clues file: {e}")
        return {}

def create_clue_objects() -> ClueManager:
    """Create ListenerClue objects from systematic parser and clue parameters"""
    
    # Step 1: Get grid structure from systematic parser
    print("Step 1: Parsing grid structure...")
    parser = SystematicGridParser('data/Listener grid 4869.png')
    parser.parse_grid_structure()
    
    # Step 2: Load clue parameters
    print("Step 2: Loading clue parameters...")
    clue_params = load_clue_parameters()
    
    # Step 3: Create clue manager and add clues
    print("Step 3: Creating clue objects...")
    manager = ClueManager()
    
    # Get all clue tuples from parser
    all_clue_tuples = parser.get_all_clues()
    
    for clue_tuple in all_clue_tuples:
        if clue_tuple.number in clue_params:
            b, c = clue_params[clue_tuple.number]
            
            # Create ListenerClue using factory
            clue = ClueFactory.from_tuple_and_parameters(clue_tuple, b, c)
            manager.add_clue(clue)
            
            print(f"  Added: {clue}")
        else:
            print(f"  Warning: No parameters found for clue {clue_tuple.number}")
    
    return manager

def test_clue_interactions(manager: ClueManager):
    """Test clue interactions and constraint propagation"""
    print("\n" + "="*60)
    print("TESTING CLUE INTERACTIONS")
    print("="*60)
    
    # Print initial state
    print("\nInitial state:")
    manager.print_state()
    
    # Test applying a solution
    print("\nApplying solution for clue 1A = 1234:")
    manager.apply_solution(1, 1234)
    manager.print_state()
    
    # Test constraint propagation
    print("\nTesting constraint propagation:")
    affected_clues = manager.get_affected_clues(1)
    print(f"Clues affected by clue 1: {affected_clues}")
    
    # Test removing a solution
    print("\nRemoving solution for clue 1A:")
    manager.remove_solution(1)
    manager.print_state()

def test_crossing_clues(manager: ClueManager):
    """Test crossing clue functionality"""
    print("\n" + "="*60)
    print("TESTING CROSSING CLUES")
    print("="*60)
    
    # Find clues that cross
    crossing_pairs = manager.find_crossing_clues()
    print(f"Found {len(crossing_pairs)} crossing clue pairs:")
    
    for clue1, clue2 in crossing_pairs[:5]:  # Show first 5
        print(f"  {clue1} crosses {clue2}")
    
    # Test constraint propagation through crossings
    if crossing_pairs:
        clue1, clue2 = crossing_pairs[0]
        print(f"\nTesting constraint propagation between {clue1} and {clue2}")
        
        # Apply solution to first clue
        manager.apply_solution(clue1.number, 1234)
        print(f"Applied solution {1234} to {clue1}")
        
        # Check how it affects the crossing clue
        affected = manager.get_affected_clues(clue1.number)
        print(f"Affected clues: {affected}")

def main():
    """Main test function."""
    print("="*60)
    print("TESTING CLUE CLASSES")
    print("="*60)
    
    try:
        # Create clue objects
        manager = create_clue_objects()
        
        if manager.clues:
            # Test interactions
            test_clue_interactions(manager)
            
            # Test crossing clues
            test_crossing_clues(manager)
            
            print("\n" + "="*60)
            print("ALL TESTS COMPLETED SUCCESSFULLY")
            print("="*60)
        else:
            print("No clues created - cannot run tests")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 