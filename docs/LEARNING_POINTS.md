# Learning Points - Python Programming Concepts

This document captures key Python programming concepts and learning points encountered while working on the Listener Maths Crossword project.

## Table of Contents
- [Comments and Documentation](#comments-and-documentation)
- [Type Hints and the `typing` Module](#type-hints-and-the-typing-module)
- [Decorators](#decorators)
- [Data Classes](#data-classes)
- [Object-Oriented Programming](#object-oriented-programming)
- [Advanced Data Structures](#advanced-data-structures)
- [List Comprehensions](#list-comprehensions)
- [Lambda Functions](#lambda-functions)
- [Recursion](#recursion)
- [Context Managers](#context-managers)
- [Inheritance](#inheritance)
- [Built-in Functions and Iteration](#built-in-functions-and-iteration)
- [Error Handling](#error-handling)
- [Strategic Decision Making](#strategic-decision-making)

---

## Strategic Decision Making

### OCR vs. Ground Truth Data: A Strategic Pivot

**Context**: The project initially attempted to use OpenCV and Tesseract OCR for automated puzzle parsing, but encountered significant reliability and development challenges.

#### The Challenge
- **OCR Accuracy**: Tesseract struggled with small, printed numbers in grid cells
- **Development Bottleneck**: Debugging OCR issues consumed significant development time
- **Cross-Platform Issues**: OCR setup and dependencies varied across development environments
- **Learning Focus**: OCR debugging was taking time away from core programming concepts

#### The Decision
To maintain project momentum and focus on core algorithmic development, the decision was made to **transition to ground truth data**:

```python
# Instead of OCR detection:
def detect_clue_numbers_ocr(self) -> Dict[int, int]:
    # OCR code that was unreliable...
    
# Use hard-coded ground truth data:
def detect_clue_numbers_ocr(self) -> Dict[int, int]:
    # Updated mapping based on visual review of the actual puzzle
    detected_numbers = {
        1: 0,   # Clue 1 in cell 0
        2: 1,   # Clue 2 in cell 1
        3: 2,   # Clue 3 in cell 2
        # ... etc
    }
    return detected_numbers
```

#### Benefits Achieved
1. **Reliability**: 100% accurate data input, eliminating OCR errors
2. **Development Speed**: Focus shifted from debugging OCR to core algorithm development
3. **Cross-Platform Consistency**: No dependency on system-specific OCR installations
4. **Learning Focus**: More time available for advanced programming concepts

#### Lessons Learned

##### Strategic Decision Making
- **Pragmatic Approach**: Sometimes simpler solutions enable faster progress
- **Risk Assessment**: Identify development bottlenecks early and mitigate them
- **Learning Priorities**: Focus on core programming concepts over peripheral technologies
- **Iterative Development**: Start simple, add complexity as needed

##### Project Management
- **Documentation**: Clear documentation of decisions and their rationale
- **Future Planning**: Maintain infrastructure for potential future enhancements
- **Resource Allocation**: Balance technical ambition with practical constraints
- **Adaptability**: Be willing to pivot when initial approaches prove problematic

##### Technical Architecture
- **Separation of Concerns**: Keep data input separate from core algorithms
- **Maintainability**: Simple text files easier to modify and version control
- **Framework Preservation**: Maintain OCR infrastructure for potential future use
- **Validation**: Ground truth data provides reliable foundation for testing

#### Code Example: Ground Truth Border Detection
```python
class SystematicGridParser:
    def __init__(self, grid_image_path: str, clues_image_path: str = None):
        # Ground truth border data from user
        self.thick_right_borders = {3, 8, 9, 10, 11, 12, 13, 19, 24, 30, 32, 38, 43, 49, 50, 51, 52, 53, 54, 59}
        self.thick_bottom_borders = {3, 4, 6, 9, 14, 17, 22, 24, 25, 26, 29, 30, 31, 33, 38, 41, 46, 49, 51, 52}
    
    def is_thick_border(self, cell_index: int, direction: str) -> bool:
        """Check if a cell has a thick border using ground truth data"""
        if direction == 'right':
            return cell_index in self.thick_right_borders
        elif direction == 'bottom':
            return cell_index in self.thick_bottom_borders
        return False
```

#### Future Considerations
While the current implementation uses ground truth data, the framework remains in place for future OCR integration:

```python
# Future OCR integration could look like:
def is_thick_border(self, cell_index: int, direction: str) -> bool:
    """Check if a cell has a thick border using OCR or ground truth"""
    if self.use_ocr:
        return self.detect_border_ocr(cell_index, direction)
    else:
        # Use ground truth data as fallback
        return self.is_thick_border_ground_truth(cell_index, direction)
```

This strategic decision demonstrates the importance of **pragmatic problem-solving** and **adaptive project management** in software development.

---

## Comments and Documentation

### `#` Comments (Single-line comments)

**Purpose**: Brief code explanations and inline clarifications

**Characteristics**:
- Single line only - everything after `#` on that line is ignored
- Can appear at the end of a line of code (inline comments)
- No special meaning - just ignored by the Python interpreter
- Common uses: brief explanations, TODO notes, disabling code temporarily

**Examples**:
```python
# This is a single-line comment
position: Tuple[int, int]  # (row, col) - inline comment
self.clues = {}  # clue_id -> ListenerClue
self.solved_cells = {}  # cell_index -> digit
```

### `"""` Comments (Docstrings)

**Purpose**: Function, class, and module documentation

**Characteristics**:
- Multi-line - can span multiple lines
- Special meaning - Python treats these as documentation strings
- Accessible at runtime - can be retrieved using `.__doc__` attribute
- Used by tools - IDEs, documentation generators, and `help()` function
- Convention - first line should be a brief summary, followed by detailed explanation

**Examples**:
```python
def get_solution(self) -> Optional[int]:
    """Get the solution if this clue is solved, otherwise None."""
    if self.is_solved():
        return list(self.valid_solutions)[0]
    return None

class ListenerClue:
    """Enhanced clue class for Listener puzzles with unique identifiers"""
    
    def __init__(self, clue_id: str, direction: str, cell_indices: Tuple[int, ...], 
                 parameters: Tuple[int, int, int]):
        """
        Initialize a ListenerClue.
        
        Args:
            clue_id: Unique identifier like "A1", "D1"
            direction: Direction of the clue ("ACROSS" or "DOWN")
            cell_indices: Tuple of cell indices this clue occupies
            parameters: Tuple of (a, b, c) parameters for find_solutions
        """
```

### When to Use Which

| Use `#` for: | Use `"""` for: |
|-------------|----------------|
| Brief explanations of complex code | Function and class documentation |
| TODO notes | API documentation |
| Disabling code temporarily | Detailed explanations of what something does |
| Inline clarifications | Documentation accessible via `help()` or IDEs |

---

## Type Hints and the `typing` Module

### Purpose
Type hints help with:
- **Code Documentation** - Making code more readable and self-documenting
- **IDE Support** - Better autocomplete, error detection, and refactoring tools
- **Static Type Checking** - Tools like mypy can catch type-related bugs before runtime
- **API Clarity** - Clear contracts for function parameters and return values

### Import Statement
```python
from typing import Dict, List, Set, Tuple, Optional
```

### Common Type Hints

#### `Dict[KeyType, ValueType]`
```python
# Parameter type hint
def update_from_constraints(self, solved_cells: Dict[int, int]) -> bool:
    # solved_cells maps cell_index (int) to digit (int)

# Class attribute type hint  
self.clues: Dict[str, List[Clue]] = {
    'ACROSS': [],
    'DOWN': []
}
# Maps direction (str) to list of clues

self.clue_cells: Dict[int, Set[int]] = {}
# Maps clue number (int) to set of cell indices (int)
```

#### `List[ElementType]`
```python
# Return type hints
def get_valid_solutions(self) -> List[int]:
    return list(self.valid_solutions)

def get_clues_by_direction(self, direction: str) -> List[ListenerClue]:
    return [clue for clue in self.clues.values() if clue.direction == direction]

# Parameter type hints
def _solve_recursive(self, clues: List[Clue], index: int) -> bool:

# Dataclass field
possible_solutions: List[int] = None
```

#### `Set[ElementType]`
```python
# Class attribute
self.clue_cells: Dict[int, Set[int]] = {}  # Set of cell indices
```

#### `Tuple[Type1, Type2, ...]`
```python
# Fixed-size tuples
position: Tuple[int, int]  # (row, col) - exactly 2 integers
parameters: Tuple[int, int, int]  # (a, b, c) - exactly 3 integers

# Variable-length tuples
cell_indices: Tuple[int, ...]  # Variable number of integers

# Return type
def get_row_col(self, cell_index: int) -> Tuple[int, int]:
    return cell_index // self.size, cell_index % self.size
```

#### `Optional[Type]`
```python
# Return type hints
def get_solution(self) -> Optional[int]:
    # Returns int or None
    if self.is_solved():
        return list(self.valid_solutions)[0]
    return None

def get_clue(self, clue_id: str) -> Optional[ListenerClue]:
    # Returns ListenerClue or None
    return self.clues.get(clue_id)
```

### Benefits in This Project
1. **Complex Data Structures**: Clear relationships between nested data structures
2. **Grid Coordinates**: `Tuple[int, int]` clearly indicates row/column pairs
3. **Nullable Returns**: `Optional[int]` makes it clear when a function might return `None`
4. **Collection Types**: Distinguishes between different collection types and their mutability
5. **API Contracts**: Function signatures clearly show expected and returned data types

---

## Decorators

### `@property` Decorator

**Purpose**: Creates a computed property that can be accessed like an attribute

**Example from the project**:
```python
@property
def number(self) -> int:
    """Extract the numeric part from clue_id for backward compatibility"""
    return int(self.clue_id[1:])
```

**How it works**:
- Instead of calling `clue.number()` as a method, you can access it as `clue.number`
- Dynamically computes the value by extracting the numeric part from `self.clue_id[1:]`
- Provides backward compatibility with code expecting a `number` attribute

**Usage**:
```python
# If clue_id = "A1"
clue.number  # Returns 1 (the integer extracted from "A1"[1:])
clue.clue_id  # Returns "A1" (the full string identifier)
```

### `@dataclass` Decorator

**Purpose**: Automatically generates special methods for classes that primarily store data

**Example**:
```python
@dataclass
class Clue:
    number: int
    direction: str  # 'ACROSS' or 'DOWN'
    length: int
    position: Tuple[int, int]  # (row, col)
    parameters: Tuple[int, int, int]  # (a, b, c) for find_solutions
    possible_solutions: List[int] = None
    cell_indices: Tuple[int, ...] = None  # Cell indices (1-64) this clue occupies
```

**What it provides**:
- `__init__` method
- `__repr__` method
- `__eq__` method
- Other special methods as needed

---

## Data Classes

### Purpose
Data classes are a way to create classes that are primarily used to store data. They automatically generate common methods like `__init__`, `__repr__`, and `__eq__`.

### Example from the project
```python
@dataclass
class Clue:
    number: int
    direction: str  # 'ACROSS' or 'DOWN'
    length: int
    position: Tuple[int, int]  # (row, col)
    parameters: Tuple[int, int, int]  # (a, b, c) for find_solutions
    possible_solutions: List[int] = None
    cell_indices: Tuple[int, ...] = None  # Cell indices (1-64) this clue occupies
```

### Benefits
- **Less boilerplate code** - No need to write `__init__`, `__repr__`, etc.
- **Type hints** - Fields are automatically typed
- **Immutability options** - Can make instances immutable with `frozen=True`
- **Default values** - Easy to specify default values for fields

---

## Object-Oriented Programming

### Class Design Patterns

#### 1. Composition over Inheritance
The project uses composition extensively:
```python
class ListenerPuzzle:
    def __init__(self):
        self.clues = {}  # clue_id -> ListenerClue
        self.solved_cells = {}  # cell_index -> digit
        self.solving_order = []  # List of clue_ids in order they were solved
        self.backtrack_stack = []  # Stack of puzzle states for backtracking
```

#### 2. Encapsulation
Private state with public interfaces:
```python
class ListenerClue:
    def __init__(self, ...):
        self.valid_solutions = set(self.possible_solutions)  # Private state
        self.rejected_solutions = set()  # Private state
    
    def get_valid_solutions(self) -> List[int]:  # Public interface
        return list(self.valid_solutions)
    
    def eliminate_solution(self, solution: int, reason: str = "constraint") -> bool:  # Public interface
        # Controlled access to private state
        if solution in self.valid_solutions:
            self.valid_solutions.remove(solution)
            self.rejected_solutions.add(solution)
            return True
        return False
```

#### 3. Method Chaining and Fluent Interfaces
```python
# Methods that return self for chaining
def add_clue(self, clue: ListenerClue) -> None:
    self.clues[clue.clue_id] = clue
    # Could return self for chaining if needed
```

---

## Advanced Data Structures

### Sets for Efficient Lookups
```python
self.valid_solutions = set(self.possible_solutions)
self.rejected_solutions = set()  # Solutions that were eliminated and can be restored
self.tried_solutions = set()  # Solutions that have been tried in backtracking
```

**Benefits**:
- O(1) membership testing (`in` operator)
- Automatic deduplication
- Set operations (union, intersection, difference)

### Dictionaries for Mapping
```python
self.clues = {}  # clue_id -> ListenerClue
self.solved_cells = {}  # cell_index -> digit
```

**Benefits**:
- O(1) key-based lookups
- Flexible key-value relationships
- Easy to add/remove mappings

### Tuples for Immutable Data
```python
position: Tuple[int, int]  # (row, col) - immutable coordinates
parameters: Tuple[int, int, int]  # (a, b, c) - immutable parameters
cell_indices: Tuple[int, ...]  # Variable-length immutable sequence
```

**Benefits**:
- Immutable (can't be accidentally modified)
- Memory efficient
- Can be used as dictionary keys
- Clear intent (this data shouldn't change)

---

## List Comprehensions

### Purpose
List comprehensions provide a concise way to create lists based on existing sequences or iterables.

### Basic Syntax
```python
[expression for item in iterable if condition]
```

### Examples from the Project

#### Simple List Comprehension
```python
# Create a list of valid solutions
return [s for s in self.valid_solutions if s not in self.tried_solutions]

# Filter clues by direction
return [clue for clue in self.clues.values() if clue.direction == direction]

# Filter clues by number
return [clue for clue in self.clues.values() if clue.number == number]

# Filter solved/unsolved clues
return [clue for clue in self.clues.values() if clue.is_solved()]
return [clue for clue in self.clues.values() if not clue.is_solved()]
```

#### Nested List Comprehension
```python
# Create 2D grid
grid = [[' ' for _ in range(8)] for _ in range(8)]
self.grid = [[0 for _ in range(size)] for _ in range(size)]

# Create grid with cell indices
grid = [[i + j*8 for j in range(8)] for i in range(8)]
```

#### List Comprehension with Conditional Logic
```python
# Filter elimination history
self.elimination_history = [(s, r) for s, r in self.elimination_history if s != solution]

# Filter cells with clues
cells_with_clues = [cell.index for cell in self.cells if cell.clue_number is not None]

# Filter cells with specific clue number
cells_with_this_clue = [cell.index for cell in self.cells if cell.clue_number == clue_number]
```

### Benefits
- **Concise** - More readable than equivalent for loops
- **Functional style** - Emphasizes data transformation
- **Performance** - Often faster than equivalent for loops
- **Readability** - Clear intent when used appropriately

### When to Use
- **Use list comprehensions** for simple transformations and filtering
- **Use for loops** for complex logic or when you need side effects
- **Avoid nested comprehensions** beyond 2-3 levels for readability

---

## Lambda Functions

### Purpose
Lambda functions are small, anonymous functions that can be defined inline.

### Syntax
```python
lambda parameters: expression
```

### Examples from the Project

#### Lambda Functions in Sorting
```python
# Sort clues by number of solutions
all_clues.sort(key=lambda x: len(x.possible_solutions))

# Sort clues by number
all_clues.sort(key=lambda x: x.number)

# Sort clues by solution count (with special handling for unclued)
for clue in sorted(unsolved, key=lambda c: len(c.valid_solutions) if not c.is_undefined else float('inf')):

# Sort by multiple criteria
candidates.sort(key=lambda c: (-c.potential_impact, len(c.solutions)))
```

#### Lambda Functions in Filtering
```python
# Count different types of clues
print(f"Clued clues: {len([c for c in manager.clues.values() if not c.parameters.is_unclued])}")
print(f"Unclued clues: {len([c for c in manager.clues.values() if c.parameters.is_unclued])}")
```

### Benefits
- **Inline definition** - No need to define separate functions for simple operations
- **Functional programming** - Enables functional programming patterns
- **Readability** - Can make code more readable when used appropriately

### When to Use
- **Use lambdas** for simple, one-line operations
- **Use regular functions** for complex logic or when the function is used multiple times
- **Avoid complex lambdas** - Keep them simple and readable

---

## Recursion

### Purpose
Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller subproblems.

### Examples from the Project

#### Backtracking Recursion
```python
def _backtrack_recursive(self, depth: int, max_depth: int) -> bool:
    """Recursive backtracking implementation."""
    if depth >= max_depth:
        return False
    
    # Save current state
    self.save_state()
    
    # Find clue with fewest solutions to try
    clue_to_try = self.get_clue_with_fewest_solutions()
    if not clue_to_try:
        return False
    
    print(f"Backtracking: trying clue {clue_to_try.clue_id} at depth {depth}")
    
    # Try each solution for this clue
    for solution in clue_to_try.get_untried_solutions():
        # Mark this solution as tried
        clue_to_try.mark_solution_tried(solution)
        
        # Temporarily set this solution
        original_solutions = set(clue_to_try.valid_solutions)
        clue_to_try.valid_solutions = {solution}
        
        # Try to solve with this assumption
        try:
            # Propagate constraints
            self.propagate_constraints(clue_to_try)
            self.update_unclued_clues()
            
            # Try to solve the rest (recursive call)
            if self.solve_with_backtracking(depth + 1, max_depth):
                return True
            
        except Exception as e:
            print(f"Error during backtracking: {e}")
        
        finally:
            # Restore original state
            self.restore_state()
            clue_to_try.valid_solutions = original_solutions
    
    return False
```

#### Recursive Solving
```python
def _solve_recursive(self, clues: List[Clue], index: int) -> bool:
    """Recursive helper function for solving."""
    if index == len(clues):
        return True

    clue = clues[index]

    for solution in clue.possible_solutions:
        if self.is_valid_placement(clue, solution):
            # Try placing the solution
            self.place_solution(clue, solution)
            
            # Recursive call to solve remaining clues
            if self._solve_recursive(clues, index + 1):
                return True
            
            # Backtrack
            self.remove_solution(clue)

    return False
```

### Key Components of Recursion
1. **Base case** - Condition that stops the recursion
2. **Recursive case** - The function calls itself with a smaller problem
3. **State management** - Saving and restoring state for backtracking

### Benefits
- **Elegant solutions** - Can express complex algorithms simply
- **Natural for certain problems** - Backtracking, tree traversal, divide-and-conquer
- **State preservation** - Can maintain state across recursive calls

### Considerations
- **Stack depth** - Can cause stack overflow for deep recursion
- **Memory usage** - Each recursive call uses stack space
- **Debugging** - Can be harder to debug than iterative solutions

---

## Context Managers

### Purpose
Context managers provide a way to manage resources that need to be properly acquired and released, such as file handles.

### Syntax
```python
with context_manager() as variable:
    # Use the resource
    pass
# Resource is automatically released
```

### Examples from the Project

#### File Handling
```python
# Reading files
with open('Listener 4869 clues.txt', 'r') as f:
    content = f.read()

# Writing files
with open("solution_sets.json", 'w') as f:
    json.dump(data, f, indent=2)

# Reading with encoding
with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)
```

#### Error Handling with Context Managers
```python
try:
    # Propagate constraints
    self.propagate_constraints(clue_to_try)
    self.update_unclued_clues()
    
    # Try to solve the rest
    if self.solve_with_backtracking(depth + 1, max_depth):
        return True
    
except Exception as e:
    print(f"Error during backtracking: {e}")

finally:
    # Restore original state (always executed)
    self.restore_state()
    clue_to_try.valid_solutions = original_solutions
```

### Benefits
- **Automatic cleanup** - Resources are properly released even if exceptions occur
- **Cleaner code** - No need for explicit try/finally blocks
- **Exception safety** - Ensures cleanup happens even with errors

---

## Inheritance

### Purpose
Inheritance allows a class to inherit attributes and methods from another class, enabling code reuse and polymorphism.

### Example from the Project

#### Class Inheritance
```python
class EfficientListenerClue(ListenerClue):
    """Efficient clue class that handles unclued clues differently"""
    
    def __init__(self, clue_id: str, direction: str, cell_indices: Tuple[int, ...], 
                 parameters: Tuple[int, int, int]):
        self.clue_id = clue_id
        self.direction = direction
        self.cell_indices = cell_indices
        self.length = len(cell_indices)
        self.b = parameters[1]
        self.c = parameters[2]
        
        # Check if this is an unclued clue
        self.is_undefined = (self.b == 0 and self.c == 0)
        
        if self.is_undefined:
            # For unclued clues, don't store all possible solutions
            # Just track that it's unclued and will be constrained by crossing clues
            self.valid_solutions = set()  # Empty set - will be populated as constraints are applied
            self.original_solution_count = float('inf')  # Infinite possibilities
            self.is_constrained = False  # Track if constraints have been applied
        else:
            # Generate solutions for clued clues as normal
            from listener import find_solutions
            self.valid_solutions = set(find_solutions(self.length, self.b, self.c))
            self.original_solution_count = len(self.valid_solutions)
            self.is_constrained = True
        
        # Backtracking support
        self.rejected_solutions = set()
        self.elimination_history = []
        self.tried_solutions = set()
```

### Benefits
- **Code reuse** - Inherit functionality from parent class
- **Polymorphism** - Can use child class where parent class is expected
- **Specialization** - Override methods to provide specialized behavior

### When to Use
- **Use inheritance** when there's a clear "is-a" relationship
- **Use composition** when there's a "has-a" relationship
- **Prefer composition over inheritance** for flexibility

---

## Built-in Functions and Iteration

### `enumerate()`
Returns an iterator that yields tuples of (index, value) pairs.

#### Examples
```python
# Iterate with index
for i, cell_index in enumerate(self.cell_indices):
    if cell_index in solved_cells:
        expected_digit = solved_cells[cell_index]
        actual_digit = int(solution_str[i])
        if expected_digit != actual_digit:
            solutions_to_remove.append(solution)
            break

# Iterate with custom start index
for i, (clue_num, solution) in enumerate(self.puzzle.solution_history, 1):
    print(f"{i}. Clue {clue_num}: {solution}")
```

### `range()`
Creates a sequence of numbers.

#### Examples
```python
# Create range for grid iteration
for row in range(self.grid_size):
    for col in range(self.grid_size):
        # Process each cell

# Create range for solution generation
start = 10**(self.length - 1)
end = 10**self.length
self.possible_solutions = list(range(start, end))

# Create range for grid initialization
self.grid = [[0 for _ in range(size)] for _ in range(size)]
```

### `zip()`
Combines multiple iterables into tuples.

#### Examples
```python
# Combine two lists
for solution, reason in zip(solutions, reasons):
    print(f"Solution {solution}: {reason}")
```

### Benefits
- **Clean iteration** - No need for manual index management
- **Memory efficient** - Generates values on demand
- **Readable code** - Clear intent for iteration patterns

---

## Error Handling

### Purpose
Error handling allows programs to gracefully handle unexpected situations and continue execution.

### Examples from the Project

#### Try-Except-Finally Pattern
```python
try:
    # Propagate constraints
    self.propagate_constraints(clue_to_try)
    self.update_unclued_clues()
    
    # Try to solve the rest
    if self.solve_with_backtracking(depth + 1, max_depth):
        return True
    
except Exception as e:
    print(f"Error during backtracking: {e}")

finally:
    # Restore original state (always executed)
    self.restore_state()
    clue_to_try.valid_solutions = original_solutions
```

#### Context Manager Error Handling
```python
with open(filename, 'r') as f:
    content = f.read()
    # File is automatically closed even if an exception occurs
```

### Benefits
- **Robust code** - Programs don't crash on unexpected errors
- **Graceful degradation** - Can handle errors and continue
- **Resource cleanup** - Ensures resources are properly released

### Best Practices
- **Catch specific exceptions** - Don't catch all exceptions unless necessary
- **Use finally for cleanup** - Ensure resources are released
- **Log errors appropriately** - Provide useful error information
- **Don't suppress errors silently** - Always handle or log errors

---

## Best Practices Observed

### 1. Type Safety
- Use type hints consistently
- Use `Optional` for nullable values
- Use specific collection types (`List`, `Set`, `Dict`)

### 2. Documentation
- Use docstrings for public APIs
- Use `#` comments for implementation details
- Include examples in docstrings

### 3. Error Handling
- Return `None` or `Optional` types for missing values
- Use boolean returns for success/failure
- Provide meaningful error messages

### 4. Code Organization
- Separate concerns (data classes, logic classes, utility functions)
- Use meaningful variable names
- Keep methods focused and single-purpose

### 5. Performance Considerations
- Use sets for membership testing
- Use dictionaries for key-based lookups
- Avoid unnecessary list comprehensions when sets would work

---

## Common Patterns

### 1. Factory Methods
```python
def create_snapshot(self) -> dict:
    """Create a snapshot of the current state for backtracking."""
    return {
        'valid_solutions': set(self.valid_solutions),
        'rejected_solutions': set(self.rejected_solutions),
        'elimination_history': list(self.elimination_history),
        'tried_solutions': set(self.tried_solutions)
    }
```

### 2. State Management
```python
def save_state(self) -> None:
    """Save current puzzle state for backtracking."""
    state = {
        'solved_cells': dict(self.solved_cells),
        'solving_order': list(self.solving_order),
        'clue_states': {clue_id: clue.create_snapshot() for clue_id, clue in self.clues.items()}
    }
    self.backtrack_stack.append(state)
```

### 3. Iterator Patterns
```python
def get_untried_solutions(self) -> List[int]:
    """Get solutions that haven't been tried yet."""
    return [s for s in self.valid_solutions if s not in self.tried_solutions]
```

---

*This document will be updated as new programming concepts are encountered in the project.* 