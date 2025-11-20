"""
File scanning and discovery utilities
"""
from pathlib import Path


def discover_cpp_files(inputs):
    """
    Discover all C++ files from input paths
    Returns list of Path objects and list of warnings
    """
    in_paths = []
    warnings = []

    for p in inputs:
        pth = Path(p)
        if pth.is_dir():
            for f in pth.rglob('*'):
                if f.suffix in ('.cpp', '.cc', '.c', '.h', '.hpp', '.cxx'):
                    in_paths.append(f)
        elif pth.is_file():
            in_paths.append(pth)
        else:
            warnings.append(f"Path not found: {p}")

    return in_paths, warnings
