import cv2
import numpy as np
from puzzle_reader import ListenerPuzzleReader

def test_puzzle_detection():
    """Test puzzle detection and output the results in a clear format."""
    print("Testing Puzzle Detection")
    print("=" * 50)
    
    # Create reader
    reader = ListenerPuzzleReader('Listener grid 4869.png', 'Listener 4869 clues.png')
    
    # Extract clues without visualizations
    reader.extract_clues()
    
    print("\n" + "=" * 50)
    print("DETECTED CLUES SUMMARY")
    print("=" * 50)
    
    # Print all clues in a clear format
    all_clues = []
    for direction in ['ACROSS', 'DOWN']:
        for clue in reader.clues[direction]:
            all_clues.append(clue)
    
    # Sort by clue number
    all_clues.sort(key=lambda x: x.number)
    
    print(f"\nTotal clues detected: {len(all_clues)}")
    print(f"Across clues: {len(reader.clues['ACROSS'])}")
    print(f"Down clues: {len(reader.clues['DOWN'])}")
    
    print("\nClue Details:")
    print("-" * 80)
    print(f"{'Clue':<4} {'Dir':<6} {'Length':<6} {'Cell Indices':<30} {'Parameters':<20}")
    print("-" * 80)
    
    for clue in all_clues:
        cell_indices_str = str(clue.cell_indices)
        params_str = f"a={clue.parameters[0]}, b={clue.parameters[1]}, c={clue.parameters[2]}"
        print(f"{clue.number:<4} {clue.direction:<6} {clue.length:<6} {cell_indices_str:<30} {params_str:<20}")
    
    print("\n" + "=" * 50)
    print("CLUE TUPLES FOR VERIFICATION")
    print("=" * 50)
    
    # Print just the tuples for easy verification
    for clue in all_clues:
        print(f"Clue {clue.number} {clue.direction}: {clue.cell_indices}")
    
    print("\n" + "=" * 50)
    print("UNDEFINED CLUES (need constraint solving)")
    print("=" * 50)
    
    undefined_clues = [clue for clue in all_clues if clue.parameters[1] == -1 or clue.parameters[2] == -1]
    for clue in undefined_clues:
        print(f"Clue {clue.number} {clue.direction}: {clue.cell_indices} (length={clue.length})")
    
    print(f"\nTotal undefined clues: {len(undefined_clues)}")
    
    return reader

if __name__ == "__main__":
    test_puzzle_detection() 