# Code Navigation and Review Tips

## VS Code Navigation Shortcuts

### Windows/Linux Shortcuts
- **Go to Definition**: `F12` or `Ctrl+Click` on function/variable
- **Go to References**: `Shift+F12` - find all usages
- **Go to Line**: `Ctrl+G` - jump to specific line number
- **Find in File**: `Ctrl+F` - search within current file
- **Find in Workspace**: `Ctrl+Shift+F` - search across all files
- **Outline View**: `Ctrl+Shift+O` - shows all functions/classes in file
- **Symbol Search**: `Ctrl+T` - search for symbols across workspace
- **Bracket Matching**: `Ctrl+Shift+\` - jump between matching brackets
- **Fold/Unfold**: `Ctrl+Shift+[` and `Ctrl+Shift+]` - collapse code blocks
- **Split Editor**: `Ctrl+\` - view multiple parts simultaneously
- **Command Palette**: `Ctrl+Shift+P`
- **Quick Open**: `Ctrl+P`

### Mac Shortcuts
- **Go to Definition**: `Cmd+Click` or `F12`
- **Go to References**: `Shift+F12`
- **Go to Line**: `Cmd+G`
- **Find in File**: `Cmd+F`
- **Find in Workspace**: `Cmd+Shift+F`
- **Outline View**: `Cmd+Shift+O` - shows all functions/classes in file
- **Symbol Search**: `Cmd+T`
- **Bracket Matching**: `Cmd+Shift+\`
- **Fold/Unfold**: `Cmd+Option+[` and `Cmd+Option+]`
- **Split Editor**: `Cmd+\`
- **Command Palette**: `Cmd+Shift+P`
- **Quick Open**: `Cmd+P`

## Code Review Workflow

### 1. Initial File Review
1. **Start with Outline**: `Ctrl+Shift+O` (or `Cmd+Shift+O` on Mac) to understand structure
2. **Use Breadcrumbs**: Click breadcrumb trail at top to navigate
3. **Minimap**: Use right sidebar to see file overview
4. **Bookmarks**: Install "Bookmarks" extension for marking important lines

### 2. Deep Dive Navigation
1. **Function Navigation**: Use outline view to jump to function definitions
2. **Import Tracking**: `F12` on imports to see source files
3. **Error Navigation**: `F8` to jump between errors/warnings
4. **Git Integration**: `Ctrl+Shift+G` to see line-by-line changes

### 3. Advanced Review Techniques
- **Split Editor**: View multiple parts of code simultaneously
- **Compare Files**: Use diff view to compare versions
- **Search and Replace**: Use regex patterns for complex searches
- **Multi-cursor Editing**: `Alt+Click` (or `Option+Click` on Mac) for multiple cursors

## Printing Code Cleanly

### Method 1: GitHub Print (Recommended)
1. Go to your GitHub repository
2. Navigate to the file you want to print
3. Click on it to view the code
4. Press `Ctrl+P` (or `Cmd+P` on Mac)
5. GitHub automatically provides clean, print-optimized version

### Method 2: Terminal Output
```bash
# For any file with line numbers
cat -n filename.py > print_version.txt

# For syntax-highlighted output (if you install pygments)
pip install pygments
pygmentize -f terminal filename.py > print_version.txt
```

### Method 3: IDE Print Function
- **VS Code**: `File` → `Print` from menu (if available)
- **PyCharm**: `File` → `Print`
- **Sublime Text**: `File` → `Print`

### Method 4: Plain Text Editor Method
1. Select all code (`Ctrl+A` or `Cmd+A`)
2. Copy (`Ctrl+C` or `Cmd+C`)
3. Paste into a plain text editor (Notepad, TextEdit, etc.)
4. Print from there

## Recommended Learning Resources

### Official Documentation
- [VS Code Navigation Guide](https://code.visualstudio.com/docs/editor/editingevolved)
- [VS Code Keyboard Shortcuts Reference](https://code.visualstudio.com/docs/getstarted/keybindings)
- [VS Code Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)

### Interactive Tutorials
- **VS Code Learn**: Built-in tutorial - `Ctrl+Shift+P` → "Help: Interactive Playground"
- **Codecademy's VS Code Course**: Free interactive tutorial
- [VS Code Learn Website](https://code.visualstudio.com/learn/)

### YouTube Channels
- **Traversy Media**: "VS Code Tips and Tricks" series
- **Programming with Mosh**: "VS Code Tutorial for Beginners"
- **The Net Ninja**: "VS Code Shortcuts" videos
- **Fireship**: "VS Code Pro Tips" series

### Books
- **"Visual Studio Code: End-to-End Editing and Debugging"** by Bruce Johnson
- **"Mastering VS Code"** by Christopher Pitt
- **"VS Code: The Complete Guide"** by James Quick

## Useful VS Code Extensions for Navigation

### Essential Extensions
- **Bracket Pair Colorizer**: Visualizes matching brackets
- **Indent Rainbow**: Colorizes indentation levels
- **GitLens**: Enhanced Git capabilities and line history
- **Python Docstring Generator**: Auto-generates docstrings
- **Bookmarks**: Mark and navigate to important lines
- **Path Intellisense**: Autocompletes filenames
- **Auto Rename Tag**: Automatically rename paired HTML/XML tags

### Code Review Extensions
- **Code Spell Checker**: Catches spelling mistakes in code
- **SonarLint**: Code quality and security analysis
- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **Error Lens**: Inline error messages

## Python-Specific Navigation Tips

### For Python Files
- **Function Navigation**: Use `Ctrl+Shift+O` to see all functions
- **Import Tracking**: `F12` on imports to see source files
- **Class Navigation**: Jump between class definitions and methods
- **Docstring Navigation**: Use outline to find function documentation
- **Error Navigation**: `F8` to jump between errors/warnings

### Python Extensions
- **Python**: Microsoft's official Python extension
- **Pylance**: Enhanced Python language support
- **Python Docstring Generator**: Auto-generates docstrings
- **Python Indent**: Smart Python indentation
- **Python Type Hint**: Type hint support

## Troubleshooting

### Common Issues
- **Shortcuts not working**: Check keyboard layout settings
- **Extensions not loading**: Reload VS Code (`Ctrl+Shift+P` → "Developer: Reload Window")
- **Performance issues**: Disable unnecessary extensions
- **Git integration problems**: Check Git installation and credentials

### Getting Help
- **VS Code Documentation**: [https://code.visualstudio.com/docs](https://code.visualstudio.com/docs)
- **VS Code GitHub Issues**: [https://github.com/microsoft/vscode/issues](https://github.com/microsoft/vscode/issues)
- **Stack Overflow**: Tag questions with `visual-studio-code`
- **VS Code Community**: [https://code.visualstudio.com/community](https://code.visualstudio.com/community)

## Quick Reference Cheat Sheet

### Most Used Shortcuts
| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Go to Definition | `F12` | `F12` |
| Go to References | `Shift+F12` | `Shift+F12` |
| Outline View | `Ctrl+Shift+O` | `Cmd+Shift+O` |
| Find in File | `Ctrl+F` | `Cmd+F` |
| Find in Workspace | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Go to Line | `Ctrl+G` | `Cmd+G` |
| Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Split Editor | `Ctrl+\` | `Cmd+\` |

### File Navigation
| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Quick Open | `Ctrl+P` | `Cmd+P` |
| Go to Symbol | `Ctrl+T` | `Cmd+T` |
| Go to Symbol in File | `Ctrl+Shift+O` | `Cmd+Shift+O` |
| Navigate Back | `Alt+←` | `Ctrl+-` |
| Navigate Forward | `Alt+→` | `Ctrl+Shift+-` |

---

*Last updated: January 2025*
*For the latest shortcuts and features, always refer to the official VS Code documentation.* 