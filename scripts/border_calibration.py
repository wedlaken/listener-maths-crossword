import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Set

@dataclass
class GridCell:
    """Represents a cell in the 8x8 grid with index 0-63"""
    index: int  # 0-63, left to right, top to bottom
    row: int    # 0-7
    col: int    # 0-7

class BorderCalibrator:
    def __init__(self, grid_image_path: str):
        self.grid_image = cv2.imread(grid_image_path)
        if self.grid_image is None:
            raise ValueError(f"Could not load image: {grid_image_path}")
        
        self.grid_size = 8
        self.cells = []
        for i in range(64):
            row = i // self.grid_size
            col = i % self.grid_size
            self.cells.append(GridCell(index=i, row=row, col=col))
        
        # Ground truth border positions from user
        self.thick_right_borders = {3, 8, 9, 10, 11, 12, 13, 14, 19, 24, 30, 32, 38, 43, 49, 50, 51, 52, 53, 54, 59}
        self.thick_bottom_borders = {3, 4, 6, 9, 14, 17, 22, 24, 25, 26, 29, 30, 31, 33, 38, 41, 46, 49, 51, 52}
    
    def sample_border_region(self, cell_index: int, direction: str, sample_percentage: float = 0.8) -> np.ndarray:
        """Sample border region with specified percentage of cell size"""
        if cell_index < 0 or cell_index >= 64:
            return None
        
        cell = self.cells[cell_index]
        cell_width = self.grid_image.shape[1] // self.grid_size
        cell_height = self.grid_image.shape[0] // self.grid_size
        
        # Calculate border position
        if direction == 'right':
            # Check right border (ACROSS clue end)
            if cell.col == self.grid_size - 1:  # Rightmost cell
                return None
            
            x_border = (cell.col + 1) * cell_width
            # Use specified sampling percentage
            margin = (1 - sample_percentage) / 2
            y_start = cell.row * cell_height + int(cell_height * margin)
            y_end = (cell.row + 1) * cell_height - int(cell_height * margin)
            
        elif direction == 'bottom':
            # Check bottom border (DOWN clue end)
            if cell.row == self.grid_size - 1:  # Bottom cell
                return None
            
            y_border = (cell.row + 1) * cell_height
            # Use specified sampling percentage
            margin = (1 - sample_percentage) / 2
            x_start = cell.col * cell_width + int(cell_width * margin)
            x_end = (cell.col + 1) * cell_width - int(cell_width * margin)
        
        else:
            return None
        
        # Sample border region
        sample_width = int(min(cell_width, cell_height) * 0.06)  # ±3%
        
        if direction == 'right':
            border_region = self.grid_image[y_start:y_end, x_border-sample_width//2:x_border+sample_width//2]
        else:  # bottom
            border_region = self.grid_image[y_border-sample_width//2:y_border+sample_width//2, x_start:x_end]
        
        return border_region
    
    def get_border_intensity(self, cell_index: int, direction: str, sample_percentage: float = 0.8) -> float:
        """Get border intensity for a specific cell and direction"""
        border_region = self.sample_border_region(cell_index, direction, sample_percentage)
        if border_region is None or border_region.size == 0:
            return 255.0  # Default to white if no region
        
        # Convert to grayscale if needed
        if len(border_region.shape) == 3:
            gray_border = cv2.cvtColor(border_region, cv2.COLOR_BGR2GRAY)
        else:
            gray_border = border_region
        
        return np.mean(gray_border)
    
    def calibrate_thresholds(self) -> Tuple[float, float]:
        """Calibrate thresholds based on ground truth data"""
        print("Calibrating border detection thresholds...")
        
        # Collect all border intensities
        thick_right_intensities = []
        thin_right_intensities = []
        thick_bottom_intensities = []
        thin_bottom_intensities = []
        
        # Check all cells for right borders
        for cell in self.cells:
            if cell.col < self.grid_size - 1:  # Not rightmost column
                intensity = self.get_border_intensity(cell.index, 'right')
                if cell.index in self.thick_right_borders:
                    thick_right_intensities.append(intensity)
                else:
                    thin_right_intensities.append(intensity)
        
        # Check all cells for bottom borders
        for cell in self.cells:
            if cell.row < self.grid_size - 1:  # Not bottom row
                intensity = self.get_border_intensity(cell.index, 'bottom')
                if cell.index in self.thick_bottom_borders:
                    thick_bottom_intensities.append(intensity)
                else:
                    thin_bottom_intensities.append(intensity)
        
        # Calculate statistics
        print(f"Right borders - Thick: {len(thick_right_intensities)}, Thin: {len(thin_right_intensities)}")
        print(f"Bottom borders - Thick: {len(thick_bottom_intensities)}, Thin: {len(thin_bottom_intensities)}")
        
        if thick_right_intensities:
            print(f"Right thick borders - Min: {min(thick_right_intensities):.2f}, Max: {max(thick_right_intensities):.2f}, Mean: {np.mean(thick_right_intensities):.2f}")
        if thin_right_intensities:
            print(f"Right thin borders - Min: {min(thin_right_intensities):.2f}, Max: {max(thin_right_intensities):.2f}, Mean: {np.mean(thin_right_intensities):.2f}")
        if thick_bottom_intensities:
            print(f"Bottom thick borders - Min: {min(thick_bottom_intensities):.2f}, Max: {max(thick_bottom_intensities):.2f}, Mean: {np.mean(thick_bottom_intensities):.2f}")
        if thin_bottom_intensities:
            print(f"Bottom thin borders - Min: {min(thin_bottom_intensities):.2f}, Max: {max(thin_bottom_intensities):.2f}, Mean: {np.mean(thin_bottom_intensities):.2f}")
        
        # Calculate optimal thresholds
        if thick_right_intensities and thin_right_intensities:
            max_thick_right = max(thick_right_intensities)
            min_thin_right = min(thin_right_intensities)
            right_threshold = (max_thick_right + min_thin_right) / 2
        else:
            right_threshold = 143.19  # Default
        
        if thick_bottom_intensities and thin_bottom_intensities:
            max_thick_bottom = max(thick_bottom_intensities)
            min_thin_bottom = min(thin_bottom_intensities)
            bottom_threshold = (max_thick_bottom + min_thin_bottom) / 2
        else:
            bottom_threshold = 143.19  # Default
        
        print(f"\nRecommended thresholds:")
        print(f"Right border threshold: {right_threshold:.2f}")
        print(f"Bottom border threshold: {bottom_threshold:.2f}")
        
        return right_threshold, bottom_threshold
    
    def test_thresholds(self, right_threshold: float, bottom_threshold: float) -> None:
        """Test the thresholds against ground truth"""
        print(f"\nTesting thresholds - Right: {right_threshold:.2f}, Bottom: {bottom_threshold:.2f}")
        
        # Test right borders
        correct_right = 0
        total_right = 0
        for cell in self.cells:
            if cell.col < self.grid_size - 1:
                intensity = self.get_border_intensity(cell.index, 'right')
                predicted_thick = intensity < right_threshold
                actual_thick = cell.index in self.thick_right_borders
                if predicted_thick == actual_thick:
                    correct_right += 1
                total_right += 1
        
        # Test bottom borders
        correct_bottom = 0
        total_bottom = 0
        for cell in self.cells:
            if cell.row < self.grid_size - 1:
                intensity = self.get_border_intensity(cell.index, 'bottom')
                predicted_thick = intensity < bottom_threshold
                actual_thick = cell.index in self.thick_bottom_borders
                if predicted_thick == actual_thick:
                    correct_bottom += 1
                total_bottom += 1
        
        print(f"Right border accuracy: {correct_right}/{total_right} ({100*correct_right/total_right:.1f}%)")
        print(f"Bottom border accuracy: {correct_bottom}/{total_bottom} ({100*correct_bottom/total_bottom:.1f}%)")
        print(f"Overall accuracy: {(correct_right + correct_bottom)}/{(total_right + total_bottom)} ({100*(correct_right + correct_bottom)/(total_right + total_bottom):.1f}%)")

def main():
    """Calibrate border detection thresholds"""
    calibrator = BorderCalibrator('data/Listener grid 4869.png')
    right_threshold, bottom_threshold = calibrator.calibrate_thresholds()
    calibrator.test_thresholds(right_threshold, bottom_threshold)

if __name__ == "__main__":
    main() 