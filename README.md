# Listener Maths Crossword Solver

A Python-based solver for mathematical crossword puzzles from The Listener. The solver uses image processing, OCR, and constraint satisfaction algorithms to solve 8x8 mathematical crossword puzzles.

## Features

- Image processing of puzzle grid and clues
- OCR-based clue number and parameter detection
- Automatic grid structure detection
- Interactive verification of detected elements
- Constraint-based puzzle solving
- Visual feedback and progress tracking

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- Tesseract OCR
- SymPy
- Matplotlib
- Colorama

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/listener-maths-crossword.git
cd listener-maths-crossword
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

1. Take photos of your puzzle:
   - Grid image (8x8)
   - Clue list image

2. Place images in the `images` directory

3. Run the solver:
```bash
python puzzle_reader.py
```

4. Verify the detection results

5. Let the solver find the solution

## Project Structure

```
listener-maths-crossword/
├── images/              # Directory for puzzle images
├── listener.py          # Core number generation module
├── crossword_solver.py  # Grid and solving logic
├── puzzle_reader.py     # Image processing and OCR
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Development

- The project uses Python virtual environments for dependency management
- Image processing parameters can be adjusted in `puzzle_reader.py`
- OCR settings can be modified for better accuracy
- The solving algorithm can be optimized in `crossword_solver.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Listener for the original puzzles
- OpenCV and Tesseract for image processing and OCR
- SymPy for mathematical operations 