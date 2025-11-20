"""
Spacing obfuscator for enhanced code obfuscation
Randomizes whitespace while maintaining compilation
"""
import random
import re


def randomize_spacing(code: str, intensity=0.3):
    """
    Randomize spacing in code while maintaining compilation
    
    Args:
        code: Source code to obfuscate
        intensity: How aggressive to be (0.0 to 1.0)
    
    Returns:
        Code with randomized spacing
    """
    lines = code.split('\n')
    result = []
    
    for line in lines:
        # Skip empty lines and preprocessor directives
        if not line.strip() or line.strip().startswith('#'):
            result.append(line)
            continue
        
        # Skip lines that are just comments
        if line.strip().startswith('//'):
            result.append(line)
            continue
        
        # Randomize this line
        if random.random() < intensity:
            line = randomize_line_spacing(line)
        
        result.append(line)
    
    return '\n'.join(result)


def randomize_line_spacing(line: str):
    """
    Randomize spacing within a single line
    Maintains indentation and doesn't break syntax
    """
    # Preserve leading indentation
    indent = len(line) - len(line.lstrip())
    content = line[indent:]
    
    if not content:
        return line
    
    # Patterns where we can safely add/remove spaces
    # Around operators
    content = randomize_operator_spacing(content)
    
    # Around parentheses and brackets
    content = randomize_bracket_spacing(content)
    
    # Around commas
    content = randomize_comma_spacing(content)
    
    return ' ' * indent + content


def randomize_operator_spacing(text: str):
    """Randomize spacing around operators"""
    # First, protect compound operators by marking them
    # Protect +=, -=, *=, /=, %=, &=, |=, ^=, <<=, >>=, ==, !=, <=, >=, &&, ||, ++, --
    protected_ops = [
        '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
        '<<=', '>>=', '==', '!=', '<=', '>=', '&&', '||',
        '++', '--', '->', '::', '<<', '>>'
    ]
    
    # Mark protected operators with placeholders
    placeholders = {}
    for i, op in enumerate(protected_ops):
        placeholder = f'__OP{i}__'
        placeholders[placeholder] = op
        text = text.replace(op, placeholder)
    
    # Now we can safely add spaces around single operators
    # Only add spaces around operators that are NOT part of compound operators
    if random.random() < 0.4:
        # Add spaces around = (but not ==, !=, <=, >=, +=, etc.)
        text = re.sub(r'([a-zA-Z0-9_\)])\s*=\s*([a-zA-Z0-9_(])', r'\1  =  \2', text)
    
    if random.random() < 0.3:
        # Add spaces around + (but not ++)
        text = re.sub(r'([a-zA-Z0-9_\)])\s*\+\s*([a-zA-Z0-9_(])', r'\1  +  \2', text)
    
    if random.random() < 0.3:
        # Add spaces around - (but not --)
        text = re.sub(r'([a-zA-Z0-9_\)])\s*-\s*([a-zA-Z0-9_(])', r'\1  -  \2', text)
    
    if random.random() < 0.3:
        # Add spaces around * (but not *=)
        text = re.sub(r'([a-zA-Z0-9_\)])\s*\*\s*([a-zA-Z0-9_(])', r'\1  *  \2', text)
    
    if random.random() < 0.3:
        # Add spaces around < (but not <<, <=)
        text = re.sub(r'([a-zA-Z0-9_\)])\s*<\s*([a-zA-Z0-9_(])', r'\1  <  \2', text)
    
    if random.random() < 0.3:
        # Add spaces around > (but not >>, >=)
        text = re.sub(r'([a-zA-Z0-9_\)])\s*>\s*([a-zA-Z0-9_(])', r'\1  >  \2', text)
    
    # Restore protected operators
    for placeholder, op in placeholders.items():
        text = text.replace(placeholder, op)
    
    return text


def randomize_bracket_spacing(text: str):
    """Randomize spacing around brackets and parentheses"""
    # Sometimes add space after opening bracket
    if random.random() < 0.2:
        text = re.sub(r'\(([^\s])', r'( \1', text)
    
    # Sometimes add space before closing bracket
    if random.random() < 0.2:
        text = re.sub(r'([^\s])\)', r'\1 )', text)
    
    # Sometimes remove space after opening bracket
    if random.random() < 0.2:
        text = re.sub(r'\(\s+', '(', text)
    
    # Sometimes remove space before closing bracket
    if random.random() < 0.2:
        text = re.sub(r'\s+\)', ')', text)
    
    return text


def randomize_comma_spacing(text: str):
    """Randomize spacing around commas"""
    # Sometimes add extra space after comma
    if random.random() < 0.3:
        text = re.sub(r',\s', ',  ', text)
    
    # Sometimes remove space after comma (but keep at least one)
    if random.random() < 0.2:
        text = re.sub(r',\s+', ', ', text)
    
    return text


def add_random_blank_lines(code: str, probability=0.1):
    """
    Add random blank lines throughout the code
    
    Args:
        code: Source code
        probability: Chance of adding blank line after each line
    
    Returns:
        Code with random blank lines
    """
    lines = code.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        result.append(line)
        
        # Don't add blank lines after preprocessor directives
        if line.strip().startswith('#'):
            continue
        
        # Don't add blank lines after opening braces
        if line.strip().endswith('{'):
            continue
        
        # Add random blank line
        if random.random() < probability:
            result.append('')
    
    return '\n'.join(result)


def compress_random_lines(code: str, probability=0.05):
    """
    Randomly compress some lines by removing extra spaces
    
    Args:
        code: Source code
        probability: Chance of compressing each line
    
    Returns:
        Code with some compressed lines
    """
    lines = code.split('\n')
    result = []
    
    for line in lines:
        if random.random() < probability and line.strip():
            # Compress by removing extra spaces
            indent = len(line) - len(line.lstrip())
            content = line[indent:]
            # Remove multiple spaces
            content = re.sub(r'\s+', ' ', content)
            result.append(' ' * indent + content)
        else:
            result.append(line)
    
    return '\n'.join(result)


def randomize_indentation_style(code: str):
    """
    Randomly mix tabs and spaces (carefully to not break Python-like syntax)
    Only for C++ which doesn't care about indentation style
    """
    lines = code.split('\n')
    result = []
    
    for line in lines:
        if not line.strip():
            result.append(line)
            continue
        
        # Get indentation level
        indent = len(line) - len(line.lstrip())
        content = line[indent:]
        
        # Randomly choose between spaces and tabs (but keep consistent per line)
        if random.random() < 0.3:
            # Use tabs (1 tab = 4 spaces)
            new_indent = '\t' * (indent // 4) + ' ' * (indent % 4)
        else:
            # Keep spaces
            new_indent = ' ' * indent
        
        result.append(new_indent + content)
    
    return '\n'.join(result)


def apply_spacing_obfuscation(code: str, level='medium'):
    """
    Apply spacing obfuscation with specified level
    
    Args:
        code: Source code
        level: 'light', 'medium', or 'heavy'
    
    Returns:
        Obfuscated code
    """
    if level == 'light':
        intensity = 0.2
        blank_prob = 0.05
        compress_prob = 0.03
    elif level == 'heavy':
        intensity = 0.5
        blank_prob = 0.15
        compress_prob = 0.1
    else:  # medium
        intensity = 0.4
        blank_prob = 0.1
        compress_prob = 0.1
    
    # Apply transformations
    code = randomize_spacing(code, intensity)
    code = add_random_blank_lines(code, blank_prob)
    code = compress_random_lines(code, compress_prob)
    
    # Optionally mix indentation styles
    if random.random() < 0.5:
        code = randomize_indentation_style(code)
    
    return code
