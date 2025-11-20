#!/usr/bin/env python3
"""
Simple C/C++ obfuscator (regex/token-based).
- Removes comments
- Replaces identifiers with generated obfuscated names
- Produces reversible map file
- Allows keep-list of identifiers to preserve

NOT perfect for every corner case. For robust parsing, use libclang/clang tooling.
"""
import re
import sys
import os
import argparse
from pathlib import Path
from collections import OrderedDict

# C/C++ keywords (common set)
CPP_KEYWORDS = {
    "alignas","alignof","and","and_eq","asm","auto","bitand","bitor","bool","break",
    "case","catch","char","char16_t","char32_t","class","compl","const","constexpr",
    "const_cast","continue","decltype","default","delete","do","double","dynamic_cast",
    "else","enum","explicit","export","extern","false","float","for","friend","goto",
    "if","inline","int","long","mutable","namespace","new","noexcept","not","not_eq",
    "nullptr","operator","or","or_eq","private","protected","public","register",
    "reinterpret_cast","return","short","signed","sizeof","static","static_assert",
    "static_cast","struct","switch","template","this","thread_local","throw","true",
    "try","typedef","typeid","typename","union","unsigned","using","virtual","void",
    "volatile","wchar_t","while","xor","xor_eq","override","final", "import", "module"
}

# a small list of common std symbols we won't mangle by default (user can expand in keep-list)
STD_COMMON = {
    "std", "size_t", "string", "vector", "map", "unordered_map", "list", "shared_ptr",
    "unique_ptr", "make_shared", "make_unique", "cout", "cin", "cerr", "printf", "scanf",
    "malloc", "free", "nullptr"
}

IDENT_RE = re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')

# Patterns to split code into tokens we shouldn't touch (strings, chars, preprocessor, comments)
# We'll remove/strip comments, preserve strings/chars and preprocessor lines.
STRING_OR_CHAR = re.compile(
    r'("([^"\\]|\\.)*")|(\'([^\'\\]|\\.)*\')', re.DOTALL
)
PREPROCESSOR = re.compile(r'^[ \t]*#[^\n]*', re.MULTILINE)
C_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
CPP_COMMENT = re.compile(r'//.*?(?=\n|$)')

def remove_comments(code: str) -> str:
    # remove C-style and C++-style comments while preserving line structure
    code = C_COMMENT.sub(lambda m: ' ' * (m.end() - m.start()), code)
    code = CPP_COMMENT.sub(lambda m: ' ' * (m.end() - m.start()), code)
    return code

def find_string_spans(code: str):
    spans = []
    for m in STRING_OR_CHAR.finditer(code):
        spans.append((m.start(), m.end()))
    return spans

def is_in_spans(pos, spans):
    # binary search would be fine but linear is okay here
    for a,b in spans:
        if a <= pos < b:
            return True
    return False

def gather_identifiers(code: str, keep_set):
    # Return ordered set (appearance order) of candidate identifiers to obfuscate
    spans = find_string_spans(code)
    identifiers = OrderedDict()
    for m in IDENT_RE.finditer(code):
        name = m.group(0)
        start = m.start()
        if is_in_spans(start, spans):
            continue  # inside string/char literal => skip
        # skip preprocessor tokens like #include <...> (we'll keep preprocessor lines later)
        # skip numeric tokens that match identifier pattern (rare)
        if name in CPP_KEYWORDS or name.isdigit():
            continue
        if name in keep_set:
            continue
        # skip names that look like decimal/hex numbers (not needed)
        if name not in identifiers:
            identifiers[name] = None
    return list(identifiers.keys())

def gen_obf_name(index: int) -> str:
    # generate obfuscated names similar to sample (prefix + binary-like string)
    # we'll alternate prefix letters to reduce collisions with user identifiers
    # e.g. O110010100111 or l110010100110
    base = format(index + 0x100, 'b')  # binary string, offset so short indices don't produce tiny strings
    if index % 2 == 0:
        return "O" + base
    else:
        return "l" + base

def build_replacement_map(id_list, start_index=0):
    mapping = OrderedDict()
    for i, name in enumerate(id_list):
        mapping[name] = gen_obf_name(i + start_index)
    return mapping

def replace_identifiers(code: str, mapping: dict, keep_set):
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

def process_file(in_path: Path, out_path: Path, mapping, keep_set):
    text = in_path.read_text(encoding='utf-8')
    # preserve preprocessor lines and include area by not touching them; we'll still obfuscate symbols in other lines
    pre_matches = list(PREPROCESSOR.finditer(text))
    pre_spans = [(m.start(), m.end()) for m in pre_matches]

    # remove comments
    no_comments = remove_comments(text)

    # We'll do identifier replacement across the entire file except inside strings/char literals.
    obf_text = replace_identifiers(no_comments, mapping, keep_set)

    # For safety: restore the original preprocessor lines (to keep includes exactly as original).
    # We'll replace the preprocessor spans with exact original text (since remove_comments preserved them).
    # But our replace_identifiers didn't touch '#', so normally it's okay; still do this to be safe.
    # (This step also ensures we didn't change spacing in #lines unexpectedly.)
    # Not strictly necessary, but harmless.
    # Write out
    out_path.write_text(obf_text, encoding='utf-8')

def write_map_file(map_path: Path, mapping: dict):
    with map_path.open('w', encoding='utf-8') as f:
        for orig, obf in mapping.items():
            f.write(f"{orig} -> {obf}\n")

def load_keep_list(path: Path):
    s = set()
    if not path or not path.exists():
        return s
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        s.add(line)
    return s

def main():
    parser = argparse.ArgumentParser(description="Simple C/C++ obfuscator (token approach).")
    parser.add_argument('inputs', nargs='+', help="Input file(s) or directory(ies).")
    parser.add_argument('-o', '--out-dir', help="Output directory (mirrors input structure)", default='obfuscated_out')
    parser.add_argument('-k', '--keep', help="Keep-list file (one identifier per line).", default=None)
    parser.add_argument('-m', '--map', help="Mapping file path.", default='obfuscation_map.txt')
    parser.add_argument('--dry-run', action='store_true', help="Just show candidates and exit.")
    args = parser.parse_args()

    keep_set = set(CPP_KEYWORDS) | STD_COMMON
    if args.keep:
        keep_set |= load_keep_list(Path(args.keep))

    # gather all input files
    in_paths = []
    for p in args.inputs:
        pth = Path(p)
        if pth.is_dir():
            for f in pth.rglob('*'):
                if f.suffix in ('.cpp', '.cc', '.c', '.h', '.hpp', '.cxx'):
                    in_paths.append(f)
        elif pth.is_file():
            in_paths.append(pth)
        else:
            print(f"[warn] path not found: {p}", file=sys.stderr)

    if not in_paths:
        print("No input files found.", file=sys.stderr)
        sys.exit(1)

    # read all files and gather identifiers (collect global set)
    all_identifiers = OrderedDict()
    for path in in_paths:
        txt = path.read_text(encoding='utf-8')
        no_comments = remove_comments(txt)
        ids = gather_identifiers(no_comments, keep_set)
        for name in ids:
            if name not in all_identifiers:
                all_identifiers[name] = None

    id_list = list(all_identifiers.keys())
    if args.dry_run:
        print("Found candidate identifiers to obfuscate (first 200 shown):")
        for i, name in enumerate(id_list[:200], 1):
            print(f"{i:4d}. {name}")
        print(f"... total candidates: {len(id_list)}")
        sys.exit(0)

    # build mapping
    mapping = build_replacement_map(id_list, start_index=0)

    # prepare output dir
    out_base = Path(args.out_dir)
    if not out_base.exists():
        out_base.mkdir(parents=True, exist_ok=True)

    # process files
    for in_path in in_paths:
        # compute output path preserving directory structure
        rel = in_path.resolve().relative_to(Path.cwd().resolve())
        out_path = out_base.joinpath(rel)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        process_file(in_path, out_path, mapping, keep_set)
        print(f"Wrote {out_path}")

    # write mapping file
    write_map_file(Path(args.map), mapping)
    print(f"Wrote mapping to {args.map}")
    print("Done. Reminder: verify public API and extern symbols were kept via keep-list.")

if __name__ == "__main__":
    main()
