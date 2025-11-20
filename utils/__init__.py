"""
Utils package for C++ Code Obfuscator
Contains core modules for obfuscation functionality
"""

from .obfuscator import (
    CPP_KEYWORDS,
    STD_COMMON,
    remove_comments,
    gather_identifiers,
    build_replacement_map,
    process_file,
    write_map_file,
    load_keep_list
)

from .ui import (
    Colors,
    print_banner,
    print_step,
    print_success,
    print_warning,
    print_error,
    print_info,
    animate_progress,
    print_stats_box
)

from .file_scanner import discover_cpp_files

try:
    from .dead_code_generator import inject_dead_code, generate_dead_function
except ImportError:
    inject_dead_code = None
    generate_dead_function = None

__all__ = [
    # Obfuscator
    'CPP_KEYWORDS',
    'STD_COMMON',
    'remove_comments',
    'gather_identifiers',
    'build_replacement_map',
    'process_file',
    'write_map_file',
    'load_keep_list',
    # UI
    'Colors',
    'print_banner',
    'print_step',
    'print_success',
    'print_warning',
    'print_error',
    'print_info',
    'animate_progress',
    'print_stats_box',
    # File Scanner
    'discover_cpp_files',
]
