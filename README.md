# 🔒 C++ Code Obfuscator - Terminal Edition

Advanced C++ identifier obfuscation tool with a sleek hacker-themed terminal interface.

> 📚 **New here?** Check the [Documentation Index](INDEX.md) for a complete guide to all documentation.

## ✨ Features

- 🎯 **Smart Obfuscation**: Replaces identifiers with binary-style obfuscated names
- 🛡️ **Protected Identifiers**: Keep standard library and custom identifiers safe
- 🔄 **Reversible Mapping**: Generate mapping files for deobfuscation
- 📊 **Visual Progress**: Real-time progress indicators and statistics
- 🎨 **Hacker Aesthetic**: Cool terminal UI with colors and animations
- 📁 **Batch Processing**: Process multiple files and directories at once

## 🚀 Quick Start

### Super Quick (Recommended)

```bash
# 1. Create input.cpp with your code
# 2. Run (no arguments needed!)
python run.py

# That's it! Output in obfuscated_out/input.cpp
```

### Basic Usage

```bash
# Obfuscate a single file
python obfuscate_cpp.py mycode.cpp

# Obfuscate with keep-list
python obfuscate_cpp.py mycode.cpp -k keep_list.txt

# Obfuscate entire directory
python obfuscate_cpp.py src/ -o obfuscated_src

# Preview without obfuscating
python obfuscate_cpp.py mycode.cpp --dry-run
```

### Command Line Options

```
positional arguments:
  inputs                Input file(s) or directory(ies)

options:
  -h, --help            Show help message
  -o, --out-dir DIR     Output directory (default: obfuscated_out)
  -k, --keep FILE       Keep-list file (one identifier per line)
  -m, --map FILE        Mapping file path (default: obfuscation_map.txt)
  --dry-run             Preview candidates without obfuscating
```

## 📝 Keep List

The keep-list file protects identifiers from obfuscation. It should contain one identifier per line:

```
main
std
cout
cin
vector
my_public_api_function
MyExportedClass
```

### What to Include in Keep List

- ✅ Standard library functions and types
- ✅ Public API functions
- ✅ Exported classes and methods
- ✅ External library symbols
- ✅ Macro names
- ✅ Template parameters you want to preserve

## 🎯 Example

### Before Obfuscation
```cpp
int calculate_sum(int a, int b) {
    int result = a + b;
    return result;
}
```

### After Obfuscation
```cpp
int O100000000(int l100000001, int O100000010) {
    int l100000011 = l100000001 + O100000010;
    return l100000011;
}
```

## 📊 Output

The tool generates:
1. **Obfuscated files** in the output directory
2. **Mapping file** (`obfuscation_map.txt`) showing original → obfuscated names
3. **Statistics** about the obfuscation process

### Sample Output

```
╔═══════════════════════════════════════════════════════════════╗
║   █▀▀ █▀█ █▀▄ █▀▀   █▀█ █▄▄ █▀▀ █ █ █▀ █▀▀ ▄▀█ ▀█▀ █▀█ █▀█   ║
║   █▄▄ █▄█ █▄▀ ██▄   █▄█ █▄█ █▀  █▄█ ▄█ █▄▄ █▀█  █  █▄█ █▀▄   ║
╚═══════════════════════════════════════════════════════════════╝

[1/5] Initializing obfuscation engine...
✓ Loaded keep-list: keep_list.txt (620 custom identifiers)
[2/5] Scanning for target files...
✓ Found 5 file(s) to process
[3/5] Analyzing identifiers...
✓ Extracting and analyzing code structure

┌───────────────────────────────────┐
│          ANALYSIS RESULTS         │
├───────────────────────────────────┤
│ Files scanned                 5 │
│ Unique identifiers          150 │
│ Protected identifiers       727 │
│ Identifiers to obfuscate    150 │
└───────────────────────────────────┘

✓ Operation completed successfully
```

## ⚠️ Important Notes

- **Not Production-Ready**: This is a regex-based obfuscator. For robust parsing, use libclang/clang tooling
- **Verify Public APIs**: Always check that public API symbols are in the keep-list
- **Test Thoroughly**: Compile and test obfuscated code before deployment
- **Keep Mapping Safe**: Store the mapping file securely if you need to deobfuscate later

## 📦 Project Structure

The project is modularized for maintainability:

```
cpp-obfuscator/
├── obfuscate_cpp.py      # Main entry point
├── run.py                # Helper script
├── utils/                # Core modules package
│   ├── obfuscator.py     # Core obfuscation logic
│   ├── ui.py             # Terminal UI components
│   └── file_scanner.py   # File discovery
├── keep_list.txt         # Protected identifiers
└── README.md             # Documentation
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed architecture.

## 🛠️ Technical Details

### Obfuscation Strategy

1. **Comment Removal**: Strips C-style and C++-style comments
2. **Identifier Extraction**: Finds all identifiers using regex
3. **Filtering**: Excludes keywords, standard library, and keep-list items
4. **Name Generation**: Creates binary-style obfuscated names (O100000000, l100000001, etc.)
5. **Replacement**: Replaces identifiers while preserving strings and preprocessor directives

### Protected by Default

- All C++ keywords
- Common standard library symbols (std, vector, cout, cin, etc.)
- Standard types (size_t, string, etc.)
- Memory functions (malloc, free, etc.)

### Module Responsibilities

- **obfuscate_cpp.py**: Orchestration and CLI
- **run.py**: Helper script for quick tasks
- **utils/obfuscator.py**: Core parsing and transformation
- **utils/ui.py**: Visual feedback and formatting
- **utils/file_scanner.py**: File system operations

## 📄 License

This tool is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to enhance the obfuscation logic, add more features, or improve the terminal UI!

---

**Made with ❤️ for developers who love terminal aesthetics**
