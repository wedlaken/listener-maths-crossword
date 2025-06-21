import cv2
import numpy as np
from puzzle_reader import ListenerPuzzleReader

def test_basic_detection():
    """Test basic detection without the full verification process."""
    print("Testing basic puzzle detection...")
    
    try:
        # Create reader
        reader = ListenerPuzzleReader('Listener grid 4869.png', 'Listener 4869 clues.png')
        
        # Test preprocessing
        print("Preprocessing image...")
        reader.preprocess_image()
        
        # Test clue number detection
        print("Detecting clue numbers in grid...")
        clue_cells = reader.detect_clue_numbers_in_grid()
        print(f"Found clue numbers in {len(clue_cells)} cells")
        
        # Test clue extraction
        print("Extracting clues...")
        reader.extract_clues()
        
        # Print the detected tuples
        print("\nDetected clue tuples:")
        print("=" * 40)
        
        # Get all clues and sort by number
        all_clues = []
        for direction in ['ACROSS', 'DOWN']:
            for clue in reader.clues[direction]:
                all_clues.append(clue)
        
        all_clues.sort(key=lambda x: x.number)
        
        for clue in all_clues:
            print(f"Clue {clue.number} {clue.direction}: {clue.cell_indices}")
        
        return all_clues
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_basic_detection() 