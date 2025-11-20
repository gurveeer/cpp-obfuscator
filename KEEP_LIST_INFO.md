# 📋 Keep List Information

## Overview

The `keep_list.txt` file contains **1,473 protected identifiers** that will NOT be obfuscated.

## Statistics

- **Total Protected**: 1,473 identifiers
- **C++ Keywords**: 107 reserved words
- **Custom Identifiers**: 1,366 standard library items

## Categories

### 1. Custom API (4 items)
Your public functions and classes that should remain readable.

### 2. C++ Keywords (107 items)
All C++ reserved words including C++20 keywords.

### 3. Standard Types (30 items)
Common type definitions like `size_t`, `int8_t`, `uint32_t`, etc.

### 4. I/O Streams (30 items)
`iostream`, `cin`, `cout`, `cerr`, `endl`, etc.

### 5. Containers (50+ items)
All STL containers and their methods:
- `vector`, `map`, `set`, `unordered_map`, etc.
- Methods: `push_back`, `insert`, `erase`, `size`, etc.

### 6. Strings (30+ items)
String types and operations:
- `string`, `wstring`, `string_view`
- Methods: `substr`, `find`, `c_str`, `length`, etc.

### 7. Algorithms (150+ items)
All `<algorithm>` functions:
- `sort`, `find`, `binary_search`, `transform`, etc.

### 8. Iterators (30+ items)
Iterator types and operations:
- `iterator`, `const_iterator`, `reverse_iterator`
- `begin`, `end`, `advance`, `distance`, etc.

### 9. Utility (40+ items)
`pair`, `tuple`, `swap`, `move`, `forward`, etc.

### 10. Smart Pointers & Memory (60+ items)
- `unique_ptr`, `shared_ptr`, `weak_ptr`
- `make_unique`, `make_shared`
- Memory management functions

### 11. Functional (40+ items)
Function objects and utilities:
- `function`, `bind`, `ref`, `invoke`
- Operators: `plus`, `minus`, `less`, `greater`, etc.

### 12. Numeric & Math (100+ items)
All math functions from `<cmath>`:
- `abs`, `sqrt`, `pow`, `sin`, `cos`, `tan`
- `ceil`, `floor`, `round`, `log`, `exp`, etc.

### 13. Limits & Constants (50+ items)
- `numeric_limits`, `INT_MAX`, `LONG_MIN`
- Math constants: `M_PI`, `M_E`, `INFINITY`, `NAN`

### 14. Random (40+ items)
Random number generation:
- `random_device`, `mt19937`, `uniform_int_distribution`

### 15. Chrono (20+ items)
Time utilities:
- `chrono`, `duration`, `system_clock`
- `seconds`, `milliseconds`, `nanoseconds`

### 16. Thread & Concurrency (60+ items)
Threading and synchronization:
- `thread`, `mutex`, `lock_guard`, `atomic`
- `future`, `promise`, `async`

### 17. Exception Handling (40+ items)
All exception types:
- `exception`, `runtime_error`, `logic_error`
- `bad_alloc`, `bad_cast`, `out_of_range`

### 18. Type Traits (100+ items)
All type trait templates:
- `is_same`, `is_integral`, `is_pointer`
- `remove_const`, `add_reference`, `decay`

### 19. Concepts (C++20) (40+ items)
- `same_as`, `integral`, `floating_point`
- `constructible_from`, `swappable`, etc.

### 20. Ranges (C++20) (50+ items)
Range views and adaptors:
- `ranges`, `views`, `filter`, `transform`

### 21. Variant, Optional, Any (30+ items)
- `variant`, `optional`, `any`
- `visit`, `holds_alternative`, `has_value`

### 22. Comparison (C++20) (20+ items)
Three-way comparison:
- `strong_ordering`, `weak_ordering`
- `compare_three_way`

### 23. Format (C++20) (10+ items)
- `format`, `format_to`, `vformat`

### 24. Regex (30+ items)
Regular expressions:
- `regex`, `smatch`, `regex_match`, `regex_search`

### 25. Filesystem (C++17) (60+ items)
File system operations:
- `path`, `exists`, `create_directory`
- `copy_file`, `remove`, `rename`

### 26. I/O Manipulators (40+ items)
- `setw`, `setprecision`, `fixed`, `hex`
- `boolalpha`, `left`, `right`

### 27. Complex Numbers (20+ items)
- `complex`, `real`, `imag`, `abs`, `arg`

### 28. Valarray (10+ items)
- `valarray`, `slice`, `gslice`

### 29. Locale (30+ items)
- `locale`, `isspace`, `toupper`, `tolower`

### 30. C Standard Library (200+ items)
All C library functions:
- stdio.h: `printf`, `scanf`, `fopen`, `fclose`
- string.h: `strcpy`, `strcmp`, `strlen`, `memcpy`
- stdlib.h: `malloc`, `free`, `rand`, `qsort`
- time.h: `time`, `clock`, `strftime`
- And many more...

### 31. Compiler Builtins (30+ items)
GCC/Clang built-in functions:
- `__builtin_popcount`, `__builtin_clz`
- `__builtin_expect`, `__builtin_prefetch`

### 32. Policy Based Data Structures (15+ items)
GNU PBDS:
- `tree`, `trie`, `order_of_key`, `find_by_order`

### 33. Bit Manipulation (C++20) (15+ items)
- `bit_cast`, `popcount`, `countl_zero`
- `rotl`, `rotr`, `has_single_bit`

### 34. Source Location (C++20) (5+ items)
- `source_location`, `line`, `column`, `file_name`

### 35. Competitive Programming (30+ items)
Common macros and typedefs:
- `ll`, `ull`, `pii`, `pll`, `vi`, `vll`
- `pb`, `mp`, `eb`, `MOD`, `INF`, `EPS`

## How to Add Custom Identifiers

Edit `keep_list.txt` and add your identifiers under the "CUSTOM API" section:

```
# ============================================================================
# CUSTOM API (Add your public functions/classes here)
# ============================================================================
my_public_api_function
MyExportedClass
MyClass
my_important_function
PUBLIC_CONSTANT
```

## Benefits

✅ **Comprehensive**: Covers all standard C++ library
✅ **Organized**: Categorized by functionality
✅ **Documented**: Comments explain each section
✅ **No Duplicates**: Cleaned and deduplicated
✅ **Up-to-date**: Includes C++20 features

## Notes

- All identifiers are case-sensitive
- One identifier per line
- Lines starting with `#` are comments
- Empty lines are ignored
- Standard library identifiers are automatically protected by the obfuscator

## Maintenance

When adding new identifiers:
1. Add them to the appropriate section
2. Keep alphabetical order within sections
3. Add comments for clarity
4. Test with `python run.py test`

---

**Last Updated**: 2025-11-20  
**Version**: 2.1.0  
**Total Identifiers**: 1,473
