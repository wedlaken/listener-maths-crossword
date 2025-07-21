# Import Hub System Guide

## Overview

The project uses a centralized import hub system via `utils.py` to manage imports from multiple folders (`archive`, `experimental`, `scripts`). This provides a clean, consistent interface for accessing functionality across the codebase.

## How the Import Hub Works

### 1. Centralized Import Management

The `utils.py` file contains an `ImportHub` class that:
- Registers imports from various modules
- Provides graceful fallback for missing modules
- Logs import success/failure for debugging
- Creates convenient aliases for commonly used imports

### 2. Import Registration

```python
# Example from utils.py
hub.register_import(
    'parse_grid', 
    'archive.systematic_grid_parser.parse_grid',
    description="Grid parsing functionality"
)
```

### 3. Convenient Aliases

```python
# Direct access to imports
from utils import parse_grid, ListenerPuzzle, find_anagram_multiples
```

## When to Use the Import Hub

### ✅ **DO Use Import Hub For:**
- Most functionality from `archive/` modules
- Most functionality from `experimental/` modules  
- Core utility functions
- Anagram-related functions
- Grid parsing functions

### ❌ **DON'T Use Import Hub For:**
- Direct imports from modules that import from `utils` (circular imports)
- Core modules in the root directory (like `listener.py`)

## Path Management Requirements

### **Files That Need sys.path:**

#### 1. **Test Files That Import from utils**
```python
# tests/test_listener_validation.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import find_solutions, get_prime_factors_with_multiplicity
```

**Why needed:** When running from the `tests/` directory, Python can't find `utils.py` in the root directory.

#### 2. **Files That Import Directly from experimental modules**
```python
# tests/test_backtracking.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'experimental'))
from experimental.puzzle_integration import integrate_puzzle as create_puzzle_from_files
```

**Why needed:** These files bypass the import hub to avoid circular imports.

### **Files That DON'T Need sys.path:**

#### 1. **Files That Use Only the Import Hub**
```python
# tests/simple_test.py
from utils import find_anagram_multiples, generate_anagrams
```

**Why not needed:** The import hub handles all path management internally.

#### 2. **Scripts Run from Project Root**
```python
# scripts/script_name.py
from utils import function_name
```

**Why not needed:** When run from project root, `utils.py` is in the current directory.

## Best Practices

### 1. **Prefer Import Hub When Possible**
```python
# ✅ DO: Use import hub
from utils import parse_grid, ListenerPuzzle

# ❌ DON'T: Direct imports (unless necessary)
from archive.systematic_grid_parser import parse_grid
```

### 2. **Handle Missing Imports Gracefully**
```python
# ✅ DO: Check for None values
if parse_grid is None:
    print("ERROR: parse_grid function not available")
    return
```

### 3. **Use Direct Imports Only When Necessary**
```python
# ✅ DO: Direct import to avoid circular dependency
from experimental.puzzle_integration import integrate_puzzle

# ❌ DON'T: Create circular imports
from utils import create_puzzle_from_files  # This would create a circle
```

## Current File Status

### **Files Using Import Hub (No sys.path needed):**
- `tests/simple_test.py`
- `tests/test_actual_solution.py`
- `tests/test_anagram_clue.py`
- `tests/test_anagram_constraints.py`
- `tests/test_anagram_fix.py`
- `tests/test_clue_classes.py`
- `tests/test_forward_search.py`
- `tests/test_listener_puzzle.py`
- `tests/test_realistic_anagrams.py`

### **Files That Need sys.path:**

#### **For utils imports:**
- `tests/test_listener_validation.py`

#### **For direct experimental imports:**
- `tests/test_backtracking.py`
- `tests/test_simple_backtracking.py`
- `tests/test_puzzle_presentation.py`

## Troubleshooting

### **Common Issues:**

#### 1. **ModuleNotFoundError: No module named 'utils'**
**Solution:** Add path setup to the file:
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

#### 2. **Circular Import Error**
**Solution:** Import directly from the source module instead of through utils:
```python
# Instead of: from utils import create_puzzle_from_files
from experimental.puzzle_integration import integrate_puzzle as create_puzzle_from_files
```

#### 3. **Import Hub Shows Failed Imports**
**Solution:** Check that the source module exists and the function/class is correctly named.

## Future Improvements

1. **Package Installation**: Install the project as a package to eliminate all sys.path requirements
2. **Module Reorganization**: Restructure modules to eliminate circular dependencies
3. **Enhanced Error Handling**: Add more specific error messages for common import issues

## Summary

The import hub system provides a clean, maintainable way to manage imports across the project. While some files still need sys.path for technical reasons, the system significantly reduces import complexity and provides better error handling and debugging capabilities.

**Key Principle:** Use the import hub when possible, use direct imports only when necessary to avoid circular dependencies or when importing from core modules. 