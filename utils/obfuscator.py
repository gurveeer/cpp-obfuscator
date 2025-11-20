"""
Core obfuscation logic
Handles code parsing, identifier extraction, and replacement
"""
import re
from collections import OrderedDict


# C/C++ keywords (common set)
CPP_KEYWORDS = {
    "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool", "break",
    "case", "catch", "char", "char16_t", "char32_t", "class", "compl", "const", "constexpr",
    "const_cast", "continue", "decltype", "default", "delete", "do", "double", "dynamic_cast",
    "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto",
    "if", "inline", "int", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq",
    "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register",
    "reinterpret_cast", "return", "short", "signed", "sizeof", "static", "static_assert",
    "static_cast", "struct", "switch", "template", "this", "thread_local", "throw", "true",
    "try", "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual", "void",
    "volatile", "wchar_t", "while", "xor", "xor_eq", "override", "final", "import", "module"
}

# Common std symbols we won't mangle by default
STD_COMMON = {
    "std", "size_t", "string", "vector", "map", "unordered_map", "list", "shared_ptr",
    "unique_ptr", "make_shared", "make_unique", "cout", "cin", "cerr", "printf", "scanf",
    "malloc", "free", "nullptr"
}

IDENT_RE = re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')
STRING_OR_CHAR = re.compile(r'("([^"\\]|\\.)*")|(\'([^\'\\]|\\.)*\')', re.DOTALL)
PREPROCESSOR = re.compile(r'^[ \t]*#[^\n]*', re.MULTILINE)
C_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
CPP_COMMENT = re.compile(r'//.*?(?=\n|$)')


def remove_comments(code: str) -> str:
    """Remove C-style and C++-style comments while preserving line structure"""
    code = C_COMMENT.sub(lambda m: ' ' * (m.end() - m.start()), code)
    code = CPP_COMMENT.sub(lambda m: ' ' * (m.end() - m.start()), code)
    return code


def find_string_spans(code: str):
    """Find all string and character literal spans"""
    spans = []
    for m in STRING_OR_CHAR.finditer(code):
        spans.append((m.start(), m.end()))
    return spans


def is_in_spans(pos, spans):
    """Check if position is within any span"""
    for a, b in spans:
        if a <= pos < b:
            return True
    return False


def gather_identifiers(code: str, keep_set):
    """Return ordered set of candidate identifiers to obfuscate"""
    spans = find_string_spans(code)
    identifiers = OrderedDict()
    for m in IDENT_RE.finditer(code):
        name = m.group(0)
        start = m.start()
        if is_in_spans(start, spans):
            continue
        if name in CPP_KEYWORDS or name.isdigit():
            continue
        if name in keep_set:
            continue
        if name not in identifiers:
            identifiers[name] = None
    return list(identifiers.keys())


def gen_obf_name(index: int) -> str:
    """Generate obfuscated names (prefix + binary-like string)"""
    base = format(index + 0x100, 'b')
    if index % 2 == 0:
        return "O" + base
    else:
        return "l" + base


def build_replacement_map(id_list, start_index=0):
    """Build mapping from original to obfuscated names"""
    mapping = OrderedDict()
    for i, name in enumerate(id_list):
        mapping[name] = gen_obf_name(i + start_index)
    return mapping


def replace_identifiers(code: str, mapping: dict, keep_set):
    """Replace identifiers in code according to mapping"""
    spans = find_string_spans(code)

    def repl(m):
        name = m.group(0)
        pos = m.start()
        if is_in_spans(pos, spans):
            return name
        if name in mapping:
            return mapping[name]
        return name

    return IDENT_RE.sub(repl, code)


def process_file(in_path, out_path, mapping, keep_set):
    """Process a single file and write obfuscated output"""
    text = in_path.read_text(encoding='utf-8')
    no_comments = remove_comments(text)
    obf_text = replace_identifiers(no_comments, mapping, keep_set)
    out_path.write_text(obf_text, encoding='utf-8')


def write_map_file(map_path, mapping: dict):
    """Write the obfuscation mapping to a file"""
    with map_path.open('w', encoding='utf-8') as f:
        for orig, obf in mapping.items():
            f.write(f"{orig} -> {obf}\n")


def load_keep_list(path):
    """Load keep-list from file"""
    s = set()
    if not path or not path.exists():
        return s
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        s.add(line)
    return s
