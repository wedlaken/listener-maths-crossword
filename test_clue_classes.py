"""
Test script for the new clue classes
Demonstrates how to create and manage ListenerClue objects with actual puzzle data
"""

from systematic_grid_parser import SystematicGridParser, ClueTuple
from clue_classes import ClueFactory, ClueManager, ListenerClue, ClueParameters
from typing import Dict, List, Tuple

def load_clue_parameters() -> Dict[int, Tuple[int, int]]:
    """Load clue parameters from the text file"""
    clue_parameters = {}
    
    try:
        with open('Listener 4869 clues.txt', 'r') as f:
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
        print("Error: Listener 4869 clues.txt not found")
        return {}
    except Exception as e:
        print(f"Error reading clues file: {e}")
        return {}

def create_clue_objects() -> ClueManager:
    """Create ListenerClue objects from systematic parser and clue parameters"""
    
    # Step 1: Get grid structure from systematic parser
    print("Step 1: Parsing grid structure...")
    parser = SystematicGridParser('Listener grid 4869.png')
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
    
    # Test solving a simple clue
    print("\n" + "-"*40)
    print("Testing clue solving and constraint propagation...")
    
    # Find a clued clue with few solutions to test with
    test_clue = None
    for clue in manager.clues.values():
        if not clue.parameters.is_unclued and len(clue.possible_solutions) <= 5:
            test_clue = clue
            break
    
    if test_clue:
        print(f"\nTesting with clue {test_clue.number} {test_clue.direction}")
        print(f"Solutions: {test_clue.get_valid_solutions()}")
        
        if test_clue.get_valid_solutions():
            # Apply the first solution
            solution = test_clue.get_valid_solutions()[0]
            print(f"Applying solution: {solution}")
            
            eliminated = manager.apply_solution(test_clue.number, solution)
            print(f"Eliminated {len(eliminated)} solutions from other clues")
            
            if eliminated:
                print("Eliminated solutions:")
                for clue_num, sol in eliminated:
                    if sol != -1:
                        print(f"  Clue {clue_num}: {sol}")
                    else:
                        print(f"  Clue {clue_num}: constraint update")
            
            print("\nState after applying solution:")
            manager.print_state()
        else:
            print("No solutions available for testing")
    else:
        print("No suitable test clue found")
    
    # Test unclued clue constraint updates
    print("\n" + "-"*40)
    print("Testing unclued clue constraint updates...")
    
    unclued_clues = manager._get_unclued_clues()
    if unclued_clues:
        print(f"Found {len(unclued_clues)} unclued clues:")
        for clue in unclued_clues:
            print(f"  {clue}")
        
        # Show how unclued clues get constrained by solved cells
        if manager.solved_cells:
            print(f"\nUnclued clues are constrained by {len(manager.solved_cells)} solved cells")
            for clue in unclued_clues:
                original_count = clue.original_solution_count
                current_count = len(clue.possible_solutions)
                if current_count < original_count:
                    print(f"  Clue {clue.number}: {current_count}/{original_count} solutions remaining")
    else:
        print("No unclued clues found")

def test_crossing_clues(manager: ClueManager):
    """Test finding crossing clues"""
    print("\n" + "="*60)
    print("TESTING CROSSING CLUES")
    print("="*60)
    
    # Find clues that cross each other
    for clue_number in sorted(manager.clues.keys()):
        clue = manager.clues[clue_number]
        crossing = clue.get_crossing_clues(manager.clues)
        
        if crossing:
            print(f"\nClue {clue_number} {clue.direction} crosses with:")
            for cross_clue in crossing:
                print(f"  Clue {cross_clue.number} {cross_clue.direction} (cells: {cross_clue.cell_indices})")
        else:
            print(f"\nClue {clue_number} {clue.direction} has no crossing clues")

def main():
    """Main test function"""
    print("LISTENER MATHS CROSSWORD - CLUE CLASSES TEST")
    print("="*60)
    
    try:
        # Create clue objects
        manager = create_clue_objects()
        
        # Test basic functionality
        test_clue_interactions(manager)
        
        # Test crossing clues
        test_crossing_clues(manager)
        
        # Final summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        print(f"Total clues: {len(manager.clues)}")
        print(f"Clued clues: {len([c for c in manager.clues.values() if not c.parameters.is_unclued])}")
        print(f"Unclued clues: {len([c for c in manager.clues.values() if c.parameters.is_unclued])}")
        print(f"Solved cells: {len(manager.solved_cells)}")
        
        # Show some example solutions
        print("\nExample solutions for clued clues:")
        for clue in manager.clues.values():
            if not clue.parameters.is_unclued and len(clue.possible_solutions) <= 3:
                solutions = clue.get_valid_solutions()
                print(f"  Clue {clue.number} {clue.direction}: {solutions}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 