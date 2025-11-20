"""
Dead code generator for enhanced obfuscation
Generates code blocks that never execute but add complexity
"""
import random


def generate_dead_function(func_name, return_type="int"):
    """Generate a dead function that looks legitimate"""
    templates = [
        # Template 1: Complex calculation
        f"""
{return_type} {func_name}({return_type} x, {return_type} y) {{
    {return_type} result = 0;
    for ({return_type} i = 0; i < x; ++i) {{
        result += (i * y) % 997;
    }}
    return result;
}}
""",
        # Template 2: Array manipulation
        f"""
{return_type} {func_name}({return_type}* arr, {return_type} n) {{
    {return_type} sum = 0;
    for ({return_type} i = 0; i < n; ++i) {{
        sum ^= arr[i];
    }}
    return sum;
}}
""",
        # Template 3: Recursive function
        f"""
{return_type} {func_name}({return_type} n) {{
    if (n <= 1) return 1;
    return {func_name}(n - 1) + {func_name}(n - 2);
}}
""",
        # Template 4: String-like operation
        f"""
{return_type} {func_name}(const char* s) {{
    {return_type} hash = 0;
    while (*s) {{
        hash = hash * 31 + *s++;
    }}
    return hash;
}}
""",
        # Template 5: Bitwise operations
        f"""
{return_type} {func_name}({return_type} a, {return_type} b) {{
    {return_type} result = a;
    result ^= b;
    result = (result << 3) | (result >> 29);
    return result & 0xFFFFFFFF;
}}
""",
    ]
    return random.choice(templates)


def generate_dead_class(class_name):
    """Generate a dead class that looks legitimate"""
    templates = [
        # Template 1: Simple data holder
        f"""
class {class_name} {{
private:
    int data;
    int count;
public:
    {class_name}() : data(0), count(0) {{}}
    void set(int val) {{ data = val; count++; }}
    int get() const {{ return data; }}
    int getCount() const {{ return count; }}
}};
""",
        # Template 2: Calculator-like class
        f"""
class {class_name} {{
private:
    double value;
public:
    {class_name}(double v = 0.0) : value(v) {{}}
    void add(double x) {{ value += x; }}
    void multiply(double x) {{ value *= x; }}
    double result() const {{ return value; }}
    void reset() {{ value = 0.0; }}
}};
""",
        # Template 3: Container-like class
        f"""
class {class_name} {{
private:
    int* buffer;
    int capacity;
    int size;
public:
    {class_name}(int cap) : capacity(cap), size(0) {{
        buffer = new int[capacity];
    }}
    ~{class_name}() {{ delete[] buffer; }}
    void push(int val) {{
        if (size < capacity) buffer[size++] = val;
    }}
    int pop() {{
        return size > 0 ? buffer[--size] : 0;
    }}
}};
""",
    ]
    return random.choice(templates)


def generate_dead_conditional(var_name="x"):
    """Generate a conditional that always evaluates to false"""
    templates = [
        f"if ({var_name} < {var_name} - 1)",  # Always false
        f"if ({var_name} != {var_name})",  # Always false
        f"if ({var_name} > {var_name} + 1)",  # Always false
        f"if (false && {var_name})",  # Always false
        f"if (0 && {var_name})",  # Always false
        f"if ({var_name} && !{var_name})",  # Always false
    ]
    return random.choice(templates)


def generate_dead_code_block():
    """Generate a complete dead code block"""
    operations = [
        "int dummy = 0;",
        "for (int i = 0; i < 0; ++i) { dummy++; }",
        "while (false) { break; }",
        "if (0) { return -1; }",
        "int temp = 1 + 1; temp *= 0;",
    ]
    return "\n    ".join(random.sample(operations, min(3, len(operations))))


def inject_dead_code(code, num_functions=3, num_classes=2):
    """
    Inject dead code into the source
    
    Args:
        code: Original source code
        num_functions: Number of dead functions to add
        num_classes: Number of dead classes to add
    
    Returns:
        Code with dead code injected
    """
    dead_code_parts = []
    
    # Generate dead functions
    for i in range(num_functions):
        func_name = f"O{random.randint(100000000, 999999999)}"
        dead_code_parts.append(generate_dead_function(func_name))
    
    # Generate dead classes
    for i in range(num_classes):
        class_name = f"l{random.randint(100000000, 999999999)}"
        dead_code_parts.append(generate_dead_class(class_name))
    
    # Combine dead code
    dead_code = "\n".join(dead_code_parts)
    
    # Find a good insertion point (after includes, before main code)
    lines = code.split('\n')
    insert_pos = 0
    
    # Find last #include or using statement
    for i, line in enumerate(lines):
        if line.strip().startswith('#include') or line.strip().startswith('using'):
            insert_pos = i + 1
    
    # Insert dead code
    lines.insert(insert_pos, "\n// my Boiler coDe")
    lines.insert(insert_pos + 1, dead_code)
    lines.insert(insert_pos + 2, "// I can write the code., but i will not\n")
    
    return '\n'.join(lines)


def add_dead_conditionals(code, probability=0.1):
    """
    Add dead conditional blocks throughout the code
    
    Args:
        code: Original source code
        probability: Probability of adding dead code after each line
    
    Returns:
        Code with dead conditionals added
    """
    lines = code.split('\n')
    result = []
    
    for line in lines:
        result.append(line)
        
        # Skip empty lines, comments, and preprocessor directives
        stripped = line.strip()
        if not stripped or stripped.startswith('//') or stripped.startswith('#'):
            continue
        
        # Add dead conditional with some probability
        if random.random() < probability and '{' in line:
            indent = len(line) - len(line.lstrip())
            dead_cond = generate_dead_conditional()
            dead_block = generate_dead_code_block()
            result.append(' ' * (indent + 4) + dead_cond + ' {')
            result.append(' ' * (indent + 8) + dead_block)
            result.append(' ' * (indent + 4) + '}')
    
    return '\n'.join(result)
