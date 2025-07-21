import pytesseract
import cv2
import numpy as np
import shutil

def test_tesseract_installation():
    """Test if Tesseract is properly installed and accessible."""
    print("Testing Tesseract Installation:")
    print("=" * 40)
    
    # Check if tesseract is in PATH
    tesseract_path = shutil.which('tesseract')
    if tesseract_path:
        print(f"✓ Tesseract found at: {tesseract_path}")
    else:
        print("✗ Tesseract not found in PATH")
        return False
    
    # Test pytesseract version
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract version: {version}")
    except Exception as e:
        print(f"✗ Error getting Tesseract version: {e}")
        return False
    
    # Test basic OCR functionality
    try:
        # Create a simple test image with numbers
        test_image = np.ones((100, 200), dtype=np.uint8) * 255
        cv2.putText(test_image, "123", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)
        
        # Try to read it
        text = pytesseract.image_to_string(test_image, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        print(f"✓ Basic OCR test successful: '{text.strip()}'")
        return True
    except Exception as e:
        print(f"✗ Basic OCR test failed: {e}")
        return False

def test_grid_image_ocr():
    """Test OCR on the actual grid image."""
    print("\nTesting OCR on Grid Image:")
    print("=" * 40)
    
    try:
        # Load the grid image
        grid_image = cv2.imread('Listener grid 4869.png')
        if grid_image is None:
            print("✗ Could not load grid image")
            return False
        
        print(f"✓ Grid image loaded: {grid_image.shape}")
        
        # Test OCR on a small region (top-left cell)
        cell_width = grid_image.shape[1] // 8
        cell_height = grid_image.shape[0] // 8
        
        # Extract top-left cell
        cell_region = grid_image[0:cell_height//2, 0:cell_width//2]
        cell_gray = cv2.cvtColor(cell_region, cv2.COLOR_BGR2GRAY)
        _, cell_bin = cv2.threshold(cell_gray, 180, 255, cv2.THRESH_BINARY_INV)
        
        # Try OCR
        config = '--psm 7 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(cell_bin, config=config)
        print(f"✓ Top-left cell OCR result: '{text.strip()}'")
        
        return True
    except Exception as e:
        print(f"✗ Grid image OCR test failed: {e}")
        return False

if __name__ == "__main__":
    # Test installation
    if test_tesseract_installation():
        # Test grid image
        test_grid_image_ocr()
    else:
        print("\nTesseract is not properly installed. Please install it first.")
        print("You can download it from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("Or use: pip install pytesseract") 