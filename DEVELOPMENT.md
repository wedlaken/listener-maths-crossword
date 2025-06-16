# Development Notes

## Project Setup

### Virtual Environment
- Each machine needs its own virtual environment
- Activate before working on the project:
  - MacBook: `source venv/bin/activate`
  - Windows: `.\venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

### Machine-Specific Notes

#### Windows PC
- Primary development machine
- Uses PowerShell (may need execution policy adjustment)
- If PowerShell restrictions occur:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

#### MacBook
- Secondary development machine
- Uses zsh shell
- No PowerShell restrictions

## Development Workflow

### Git Workflow
1. Always pull before starting work
2. Make changes
3. Commit with descriptive messages
4. Push to GitHub
5. On other machine, pull changes

### Package Management
- When adding new packages:
  1. Install in venv: `pip install <package-name>`
  2. Update requirements: `pip freeze > requirements.txt`
  3. Commit updated requirements.txt
  4. On other machine: `pip install -r requirements.txt`

## Project Context

### Key Components
1. `listener.py`: Core number-finding module
2. `crossword_solver.py`: Grid and solving logic
3. `puzzle_reader.py`: Image processing and OCR

### Important Decisions
- Using OpenCV and Tesseract for OCR
- Using SymPy for prime number operations
- 8x8 grid structure

### Known Issues
- Image quality crucial for OCR accuracy
- Need good lighting for puzzle photos
- Tesseract installation required on both machines

## Development Tips
1. Test OCR with small sections first
2. Keep puzzle images in `images/` directory
3. Use high-resolution images (min 1200x1200)
4. Avoid OneDrive/iCloud sync issues by using GitHub

## Future Enhancements
1. Add support for different grid sizes
2. Implement parallel processing
3. Add graphical user interface
4. Add support for different clue formats
5. Implement solution verification

## Resources
- [OpenCV Documentation](https://docs.opencv.org/)
- [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract)
- [SymPy Documentation](https://docs.sympy.org/) 