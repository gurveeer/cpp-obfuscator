# 🚀 Quick Start Guide

Get started with the C++ Code Obfuscator in 5 minutes!

## Installation

No installation needed! Just Python 3.6+

```bash
# Clone or download the project
git clone <your-repo-url>
cd cpp-obfuscator

# Verify Python version
python --version  # Should be 3.6 or higher
```

## Basic Usage

### 1. Obfuscate a Single File

```bash
python obfuscate_cpp.py mycode.cpp
```

Output:
- `obfuscated_out/mycode.cpp` - Obfuscated code
- `obfuscation_map.txt` - Mapping file

### 2. Preview Before Obfuscating

```bash
python obfuscate_cpp.py mycode.cpp --dry-run
```

This shows what identifiers will be obfuscated without making changes.

### 3. Use a Keep-List

Create `my_keep_list.txt`:
```
main
MyPublicAPI
MyClass
important_function
```

Then run:
```bash
python obfuscate_cpp.py mycode.cpp -k my_keep_list.txt
```

### 4. Obfuscate Multiple Files

```bash
# Multiple files
python obfuscate_cpp.py file1.cpp file2.cpp file3.h

# Entire directory
python obfuscate_cpp.py src/

# Multiple directories
python obfuscate_cpp.py src/ include/ lib/
```

### 5. Custom Output Directory

```bash
python obfuscate_cpp.py mycode.cpp -o my_output_folder
```

## Common Workflows

### Workflow 1: Quick Obfuscation

```bash
# 1. Preview
python obfuscate_cpp.py mycode.cpp --dry-run

# 2. Obfuscate
python obfuscate_cpp.py mycode.cpp

# 3. Check output
cat obfuscated_out/mycode.cpp
```

### Workflow 2: Project Obfuscation

```bash
# 1. Create keep-list with your public APIs
echo "main" > keep_list.txt
echo "MyPublicClass" >> keep_list.txt
echo "public_function" >> keep_list.txt

# 2. Preview
python obfuscate_cpp.py src/ -k keep_list.txt --dry-run

# 3. Obfuscate entire project
python obfuscate_cpp.py src/ -k keep_list.txt -o obfuscated_src

# 4. Verify compilation
cd obfuscated_src
g++ *.cpp -o myprogram
```

### Workflow 3: Competitive Programming

```bash
# Obfuscate your solution
python obfuscate_cpp.py solution.cpp -k keep_list.txt

# Submit obfuscated version
cat obfuscated_out/solution.cpp
```

## Understanding the Output

### Terminal Output

```
╔═══════════════════════════════════════════════════════════════╗
║   █▀▀ █▀█ █▀▄ █▀▀   █▀█ █▄▄ █▀▀ █ █ █▀ █▀▀ ▄▀█ ▀█▀ █▀█ █▀█   ║
╚═══════════════════════════════════════════════════════════════╝

[1/5] Initializing obfuscation engine...
✓ Loaded keep-list: keep_list.txt (50 custom identifiers)

[2/5] Scanning for target files...
✓ Found 3 file(s) to process

[3/5] Analyzing identifiers...
┌───────────────────────────────────┐
│          ANALYSIS RESULTS         │
├───────────────────────────────────┤
│ Files scanned                 3 │
│ Identifiers to obfuscate    120 │
└───────────────────────────────────┘

[4/5] Generating obfuscation mapping...
✓ Generated 120 obfuscated identifiers

[5/5] Obfuscating files...
✓ Obfuscated 3 file(s)

✓ Operation completed successfully
```

### Mapping File Format

`obfuscation_map.txt`:
```
calculate_sum -> O100000000
result -> l100000001
temp_var -> O100000010
my_function -> l100000011
```

## Tips & Tricks

### 1. Start with Dry Run
Always use `--dry-run` first to see what will be obfuscated:
```bash
python obfuscate_cpp.py mycode.cpp --dry-run | less
```

### 2. Build Your Keep-List Gradually
Start with an empty keep-list, run dry-run, then add identifiers you want to keep:
```bash
# See what will be obfuscated
python obfuscate_cpp.py mycode.cpp --dry-run > candidates.txt

# Review and create keep-list
nano keep_list.txt

# Obfuscate with keep-list
python obfuscate_cpp.py mycode.cpp -k keep_list.txt
```

### 3. Use Provided Keep-List
The project includes `keep_list.txt` with common C++ standard library identifiers:
```bash
python obfuscate_cpp.py mycode.cpp -k keep_list.txt
```

### 4. Verify Compilation
Always compile the obfuscated code to ensure it works:
```bash
python obfuscate_cpp.py mycode.cpp
g++ obfuscated_out/mycode.cpp -o test
./test
```

### 5. Keep Mapping File Safe
If you need to deobfuscate later, keep `obfuscation_map.txt` safe:
```bash
cp obfuscation_map.txt backups/mapping_$(date +%Y%m%d).txt
```

## Troubleshooting

### Problem: "No input files found"
**Solution**: Check file paths and extensions
```bash
# Make sure files exist
ls mycode.cpp

# Check supported extensions: .cpp, .cc, .c, .h, .hpp, .cxx
```

### Problem: Too many identifiers obfuscated
**Solution**: Add more items to keep-list
```bash
# Use the provided comprehensive keep-list
python obfuscate_cpp.py mycode.cpp -k keep_list.txt
```

### Problem: Obfuscated code doesn't compile
**Solution**: Check for missing keep-list entries
```bash
# Common culprits:
# - Template parameters
# - Macro names
# - External library symbols
# - Public API functions

# Add them to keep-list
echo "MyTemplateParam" >> keep_list.txt
echo "MY_MACRO" >> keep_list.txt
```

### Problem: Want different obfuscation style
**Solution**: Modify `gen_obf_name()` in `obfuscator.py`
```python
def gen_obf_name(index: int) -> str:
    # Current: O100000000, l100000001
    # Custom: _a0, _a1, _a2, etc.
    return f"_a{index}"
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
- Customize `obfuscator.py` for your needs
- Create custom keep-lists for your projects

## Examples

### Example 1: Simple Function

**Before** (`example.cpp`):
```cpp
#include <iostream>
using namespace std;

int add(int a, int b) {
    int result = a + b;
    return result;
}

int main() {
    cout << add(5, 3) << endl;
    return 0;
}
```

**Command**:
```bash
python obfuscate_cpp.py example.cpp -k keep_list.txt
```

**After** (`obfuscated_out/example.cpp`):
```cpp
#include <iostream>
using namespace std;

int O100000000(int l100000001, int O100000010) {
    int l100000011 = l100000001 + O100000010;
    return l100000011;
}

int main() {
    cout << O100000000(5, 3) << endl;
    return 0;
}
```

### Example 2: Class Obfuscation

**Before**:
```cpp
class Calculator {
    int value;
public:
    void setValue(int v) { value = v; }
    int getValue() { return value; }
};
```

**After** (with `Calculator` in keep-list):
```cpp
class Calculator {
    int O100000000;
public:
    void l100000001(int O100000010) { O100000000 = O100000010; }
    int l100000011() { return O100000000; }
};
```

---

**Happy Obfuscating! 🔒**
