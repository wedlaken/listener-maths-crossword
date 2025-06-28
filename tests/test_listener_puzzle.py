from crossword_solver import ListenerClue, ListenerPuzzle
from puzzle_reader import ListenerPuzzleReader

def test_listener_puzzle():
    """Test the new ListenerPuzzle data structure."""
    print("Testing ListenerPuzzle data structure...")
    
    # Create a puzzle
    puzzle = ListenerPuzzle()
    
    # Add some example clues (using the tuples from our previous detection)
    clues_data = [
        (1, 'ACROSS', (1, 2, 3, 4), (4, 2, 1)),      # Clue 1 ACROSS: [1, 2, 3, 4]
        (2, 'DOWN', (2, 10), (2, 1, 0)),             # Clue 2 DOWN: [2, 10]
        (3, 'DOWN', (3, 11, 19, 27), (4, 3, 2)),     # Clue 3 DOWN: [3, 11, 19, 27]
        (5, 'ACROSS', (5, 6, 7), (3, 1, 0)),         # Clue 5 ACROSS: [5, 6, 7]
        (6, 'DOWN', (6, 14, 22), (3, 2, 1)),         # Clue 6 DOWN: [6, 14, 22]
        (8, 'DOWN', (8, 16, 24, 32), (4, 2, 1)),     # Clue 8 DOWN: [8, 16, 24, 32]
    ]
    
    # Add clues to the puzzle
    for clue_num, direction, cell_indices, parameters in clues_data:
        clue = ListenerClue(clue_num, direction, cell_indices, parameters)
        puzzle.add_clue(clue)
        print(f"Added {clue}")
    
    # Print initial state
    print("\nInitial puzzle state:")
    puzzle.print_puzzle_state()
    
    # Test constraint propagation
    print("\nTesting constraint propagation...")
    
    # Let's say we know the solution for clue 1
    print("Applying solution for Clue 1 ACROSS: 1234")
    eliminated = puzzle.apply_constraint(1, 1234)
    if eliminated:
        print(f"Eliminated {len(eliminated)} incompatible solutions")
    
    puzzle.print_puzzle_state()
    
    # Test overlapping clues
    print("\nTesting overlapping clues...")
    cell_2_clues = puzzle.get_clues_for_cell(2)
    print(f"Clues that use cell 2: {[clue.number for clue in cell_2_clues]}")
    
    overlapping = puzzle.get_overlapping_clues(1)
    print(f"Clues overlapping with Clue 1: {[clue.number for clue in overlapping]}")
    
    # Try to solve the puzzle
    print("\nAttempting to solve puzzle...")
    success = puzzle.solve()
    
    if success:
        print("Puzzle solved successfully!")
        puzzle.print_solution()
    else:
        print("Puzzle could not be solved automatically.")
        puzzle.print_solution()

def test_with_real_data():
    """Test with data from the actual puzzle reader."""
    print("\n" + "="*60)
    print("TESTING WITH REAL PUZZLE DATA")
    print("="*60)
    
    try:
        # Create reader and extract clues
        reader = ListenerPuzzleReader('Listener grid 4869.png', 'Listener 4869 clues.png')
        reader.preprocess_image()
        reader.extract_clues()
        
        # Create puzzle from detected clues
        puzzle = ListenerPuzzle()
        
        # Convert detected clues to ListenerClue objects
        for direction in ['ACROSS', 'DOWN']:
            for listener_clue in reader.clues[direction]:
                # Create ListenerClue with the detected data
                clue = ListenerClue(
                    listener_clue.number,
                    listener_clue.direction,
                    listener_clue.cell_indices,
                    listener_clue.parameters
                )
                puzzle.add_clue(clue)
        
        print(f"Created puzzle with {len(puzzle.clues)} clues")
        
        # Print initial state
        puzzle.print_puzzle_state()
        
        # Try to solve
        success = puzzle.solve()
        
        if success:
            print("Puzzle solved successfully!")
            puzzle.print_solution()
        else:
            print("Puzzle could not be solved automatically.")
            puzzle.print_solution()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_listener_puzzle()
    test_with_real_data() 