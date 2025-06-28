"""
Test script to show a typical clue object (10 across) and its generated solutions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from systematic_grid_parser import SystematicGridParser, ClueTuple
from crossword_solver import ListenerClue
from listener import find_solutions

def test_clue_10_across():
    """Test creating and examining clue 10 across"""
    
    print("TESTING CLUE 10 ACROSS")
    print("="*50)
    
    # Step 1: Get the clue tuple from systematic parser
    print("Step 1: Getting clue tuple from systematic parser...")
    parser = SystematicGridParser('Listener grid 4869.png')
    parser.parse_grid_structure()
    
    # Find clue 10 across
    clue_10_tuple = None
    for clue_tuple in parser.get_all_clues():
        if clue_tuple.number == 10 and clue_tuple.direction == 'ACROSS':
            clue_10_tuple = clue_tuple
            break
    
    if not clue_10_tuple:
        print("Error: Could not find clue 10 across")
        return
    
    print(f"Found clue 10 tuple: {clue_10_tuple}")
    print(f"  Cell indices: {clue_10_tuple.cell_indices}")
    print(f"  Length: {clue_10_tuple.length}")
    
    # Step 2: Get the parameters for clue 10
    print("\nStep 2: Getting clue parameters...")
    
    # From the clues file, clue 10 is "10 3:104"
    b = 3  # number of prime factors
    c = 104  # difference between largest and smallest prime factor
    a = clue_10_tuple.length  # number of digits
    
    print(f"Parameters: a={a}, b={b}, c={c}")
    
    # Step 3: Test listener.py directly
    print("\nStep 3: Testing listener.py find_solutions directly...")
    solutions = find_solutions(a, b, c)
    print(f"Listener.py found {len(solutions)} solutions: {solutions}")
    
    # Step 4: Create ListenerClue object
    print("\nStep 4: Creating ListenerClue object...")
    parameters = (a, b, c)
    clue_10 = ListenerClue(
        number=clue_10_tuple.number,
        direction=clue_10_tuple.direction,
        cell_indices=clue_10_tuple.cell_indices,
        parameters=parameters
    )
    
    # Step 5: Examine the clue object
    print("\nStep 5: Examining the ListenerClue object...")
    print(f"Clue object: {clue_10}")
    print(f"  Number: {clue_10.number}")
    print(f"  Direction: {clue_10.direction}")
    print(f"  Cell indices: {clue_10.cell_indices}")
    print(f"  Length: {clue_10.length}")
    print(f"  Parameters: a={a}, b={clue_10.b}, c={clue_10.c}")
    print(f"  Is undefined: {clue_10.is_undefined}")
    print(f"  Original solution count: {clue_10.original_solution_count}")
    print(f"  Current valid solutions: {len(clue_10.valid_solutions)}")
    print(f"  All valid solutions: {clue_10.get_valid_solutions()}")
    print(f"  Is solved: {clue_10.is_solved()}")
    
    # Step 6: Test solution elimination
    print("\nStep 6: Testing solution elimination...")
    if clue_10.get_valid_solutions():
        first_solution = clue_10.get_valid_solutions()[0]
        print(f"Eliminating first solution: {first_solution}")
        eliminated = clue_10.eliminate_solution(first_solution)
        print(f"Elimination successful: {eliminated}")
        print(f"Remaining solutions: {len(clue_10.valid_solutions)}")
    
    return clue_10

def test_unclued_clue():
    """Test creating an unclued clue (like 12, 14, 7, or 8)"""
    
    print("\n" + "="*50)
    print("TESTING UNCLUED CLUE")
    print("="*50)
    
    # Create a mock unclued clue tuple
    unclued_tuple = ClueTuple(
        number=12,
        direction='ACROSS',
        cell_indices=(25, 26, 27, 28),  # Example cell indices
        length=4,
        parameters=(4, 0, 0)  # Add the missing parameters field
    )
    
    # Create unclued clue with b=0, c=0 (our special case)
    parameters = (4, 0, 0)  # a=4, b=0, c=0 indicates unclued
    unclued_clue = ListenerClue(
        number=unclued_tuple.number,
        direction=unclued_tuple.direction,
        cell_indices=unclued_tuple.cell_indices,
        parameters=parameters
    )
    
    print(f"Unclued clue object: {unclued_clue}")
    print(f"  Is undefined: {unclued_clue.is_undefined}")
    print(f"  Original solution count: {unclued_clue.original_solution_count}")
    print(f"  Current valid solutions: {len(unclued_clue.valid_solutions)}")
    print(f"  First 5 solutions: {unclued_clue.get_valid_solutions()[:5]}")
    print(f"  Last 5 solutions: {unclued_clue.get_valid_solutions()[-5:]}")

def main():
    """Main test function"""
    print("LISTENER MATHS CROSSWORD - CLUE OBJECT TEST")
    print("="*60)
    
    try:
        # Test clue 10 across
        clue_10 = test_clue_10_across()
        
        # Test unclued clue
        test_unclued_clue()
        
        print("\n" + "="*60)
        print("TEST COMPLETE")
        print("="*60)
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 