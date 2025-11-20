# 📁 Project Structure

## Overview

The C++ Code Obfuscator is organized into modular components for maintainability and extensibility.

```
cpp-obfuscator/
├── obfuscate_cpp.py      # Main entry point and orchestration
├── run.py                # Helper script for quick tasks
├── utils/                # Core modules package
│   ├── __init__.py       # Package initialization
│   ├── obfuscator.py     # Core obfuscation logic
│   ├── ui.py             # Terminal UI components
│   └── file_scanner.py   # File discovery utilities
├── keep_list.txt         # Protected identifiers list
├── obfuscation_map.txt   # Generated mapping file
├── README.md             # User documentation
└── PROJECT_STRUCTURE.md  # This file
```

## Module Breakdown

### 🎯 `obfuscate_cpp.py` (Main Entry Point)
**Purpose**: Application orchestration and command-line interface

**Key Functions**:
- `main()` - Entry point, argument parsing, workflow coordination
- `run_dry_run()` - Preview mode implementation
- `analyze_files()` - Coordinate file analysis
- `obfuscate_files()` - Coordinate obfuscation process

**Responsibilities**:
- Parse command-line arguments
- Coordinate the 5-step obfuscation workflow
- Handle user interaction and error reporting
- Integrate all modules from utils package

---

### 🛠️ `run.py` (Helper Script)
**Purpose**: Quick shortcuts for common tasks

**Key Functions**:
- `run_command()` - Execute shell commands
- `main()` - Command dispatcher

**Commands**:
- `preview` - Dry-run obfuscation
- `obfuscate` - Full obfuscation with keep-list
- `test` - Run test example
- `clean` - Remove output directories
- `help` - Show help

---

### 📦 `utils/` Package

#### `utils/__init__.py`
**Purpose**: Package initialization and exports

**Exports**:
- All public functions from submodules
- Clean API for importing

---

### 🔧 `utils/obfuscator.py` (Core Logic)
**Purpose**: Core obfuscation algorithms and transformations

**Key Components**:
- `CPP_KEYWORDS` - Set of C++ reserved keywords
- `STD_COMMON` - Common standard library identifiers

**Key Functions**:
- `remove_comments()` - Strip C/C++ comments
- `find_string_spans()` - Locate string literals
- `gather_identifiers()` - Extract identifiers from code
- `gen_obf_name()` - Generate obfuscated names
- `build_replacement_map()` - Create identifier mapping
- `replace_identifiers()` - Perform actual obfuscation
- `process_file()` - Process single file
- `write_map_file()` - Save mapping to file
- `load_keep_list()` - Load protected identifiers

**Responsibilities**:
- Regex-based code parsing
- Identifier extraction and filtering
- Name generation and replacement
- File I/O for code and mappings

---

### 🎨 `utils/ui.py` (Terminal UI)
**Purpose**: Visual presentation and user feedback

**Key Components**:
- `Colors` - ANSI color codes class

**Key Functions**:
- `print_banner()` - Display ASCII art banner
- `print_step()` - Show step progress
- `print_success()` - Success messages (✓)
- `print_warning()` - Warning messages (⚠)
- `print_error()` - Error messages (✗)
- `print_info()` - Info messages (ℹ)
- `animate_progress()` - Animated spinner
- `print_stats_box()` - Formatted statistics table

**Responsibilities**:
- Terminal color management
- Progress indicators and animations
- Formatted output (boxes, tables)
- User-friendly messaging

---

### 📂 `utils/file_scanner.py` (File Discovery)
**Purpose**: File system operations and discovery

**Key Functions**:
- `discover_cpp_files()` - Find all C++ files from input paths

**Responsibilities**:
- Recursive directory traversal
- File type filtering (.cpp, .h, .hpp, etc.)
- Path validation and error reporting

---

## Data Flow

```
┌─────────────────┐
│  User Input     │
│  (CLI args)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  obfuscate_cpp.py (Main)            │
│  - Parse arguments                  │
│  - Initialize keep-list             │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  file_scanner.py                    │
│  - Discover C++ files               │
│  - Validate paths                   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  obfuscator.py                      │
│  - Remove comments                  │
│  - Extract identifiers              │
│  - Build mapping                    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  obfuscator.py                      │
│  - Replace identifiers              │
│  - Write obfuscated files           │
│  - Save mapping file                │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  ui.py                              │
│  - Display results                  │
│  - Show statistics                  │
└─────────────────────────────────────┘
```

## Extension Points

### Adding New Features

1. **Custom Name Generators**
   - Modify `gen_obf_name()` in `obfuscator.py`
   - Add new naming strategies

2. **Additional File Types**
   - Update `discover_cpp_files()` in `file_scanner.py`
   - Add new file extensions

3. **Enhanced UI**
   - Add new functions to `ui.py`
   - Customize colors and animations

4. **Advanced Parsing**
   - Replace regex with AST-based parsing in `obfuscator.py`
   - Integrate libclang or similar

5. **Configuration Files**
   - Add config file support in `obfuscate_cpp.py`
   - Support JSON/YAML configuration

## Testing Strategy

### Unit Tests (Recommended)
```python
# test_obfuscator.py
from obfuscator import remove_comments, gather_identifiers

def test_remove_comments():
    code = "int x; // comment"
    assert "comment" not in remove_comments(code)

def test_gather_identifiers():
    code = "int myVar = 5;"
    keep_set = {"int"}
    ids = gather_identifiers(code, keep_set)
    assert "myVar" in ids
    assert "int" not in ids
```

### Integration Tests
```bash
# Test full workflow
python obfuscate_cpp.py test_input.cpp --dry-run
python obfuscate_cpp.py test_input.cpp -k keep_list.txt
```

## Performance Considerations

- **Regex Performance**: Current implementation uses regex for parsing
  - Fast for small-medium files
  - May be slow for very large codebases
  - Consider AST-based parsing for production use

- **Memory Usage**: Loads entire files into memory
  - Suitable for typical source files
  - May need streaming for huge files

- **Parallelization**: Currently single-threaded
  - Could parallelize file processing
  - Use `multiprocessing` for large projects

## Dependencies

- **Python 3.6+** (required)
- **Standard Library Only**:
  - `re` - Regular expressions
  - `sys` - System operations
  - `os` - OS interface
  - `argparse` - CLI parsing
  - `time` - Timing and delays
  - `pathlib` - Path operations
  - `collections` - OrderedDict

**No external dependencies required!**

## Future Enhancements

- [ ] AST-based parsing (libclang integration)
- [ ] Multi-threaded file processing
- [ ] Configuration file support
- [ ] Deobfuscation tool
- [ ] Web interface
- [ ] IDE plugins
- [ ] Custom obfuscation strategies
- [ ] Incremental obfuscation
- [ ] Symbol table analysis
- [ ] Cross-reference preservation
