# 🚀 Quick Obfuscation with input.cpp

## Super Simple Usage

Just run:
```bash
python run.py
```

That's it! 🎉

## How It Works

1. Create or edit `input.cpp` with your C++ code
2. Run `python run.py` (no arguments needed!)
3. Find obfuscated code in `obfuscated_out/input.cpp`

## Example Workflow

```bash
# 1. Edit your code
notepad input.cpp

# 2. Obfuscate (just run without arguments!)
python run.py

# 3. Check the output
type obfuscated_out\input.cpp

# 4. Compile and test
g++ obfuscated_out\input.cpp -o test.exe
test.exe
```

## Example input.cpp

```cpp
#include <iostream>
using namespace std;

int calculate(int x, int y) {
    int result = x + y;
    return result;
}

int main() {
    int a = 10;
    int b = 20;
    cout << "Result: " << calculate(a, b) << endl;
    return 0;
}
```

## After Obfuscation

```cpp
#include <iostream>
using namespace std;

int O100000000(int l100000001, int O100000010) {
    int l100000011 = l100000001 + O100000010;
    return l100000011;
}

int main() {
    int O100000100 = 10;
    int l100000101 = 20;
    cout << "Result: " << O100000000(O100000100, l100000101) << endl;
    return 0;
}
```

## Other Commands

If you need more control:

```bash
# Preview what will be obfuscated
python run.py preview input.cpp

# Clean output directories
python run.py clean

# Run test with test files
python run.py test

# Show help
python run.py help
```

## Notes

- `input.cpp` is in `.gitignore` (won't be committed)
- Output goes to `obfuscated_out/` directory
- Mapping saved to `obfuscation_map.txt`
- All standard library identifiers are protected by default

## Tips

💡 **Quick iteration**: Edit `input.cpp` → Run `python run.py` → Check output → Repeat

💡 **Keep your APIs**: Add public function names to `keep_list.txt`

💡 **Verify compilation**: Always compile the obfuscated code to ensure it works

---

**Happy Obfuscating! 🔒**
