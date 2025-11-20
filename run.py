#!/usr/bin/env python3
"""
Helper script for common obfuscation tasks
Quick shortcuts for typical workflows
"""
import sys
import subprocess
from pathlib import Path


def run_command(cmd):
    """Execute a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode


def main():
    # If no arguments, auto-obfuscate input.cpp
    if len(sys.argv) < 2:
        input_file = Path("input.cpp")
        if input_file.exists():
            print("╔═══════════════════════════════════════════════════════════════╗")
            print("║              Auto-Obfuscating input.cpp                       ║")
            print("╚═══════════════════════════════════════════════════════════════╝")
            print()
            return run_command([
                "python", "obfuscate_cpp.py",
                "input.cpp", "-k", "keep_list.txt",
                "-o", "obfuscated_out", "--dead-code", "--randomize-spacing"
            ])
        else:
            print("""
╔═══════════════════════════════════════════════════════════════╗
║                    Quick Run Helper                           ║
╚═══════════════════════════════════════════════════════════════╝

Usage: python run.py [command] [args]

Default: If no command given, obfuscates input.cpp (if it exists)

Commands:
  preview <file>       Preview obfuscation (dry-run)
  obfuscate <file>     Obfuscate with keep-list
  obfuscate+ <file>    Obfuscate with dead code injection
  test                 Run test (uses obfuscate_input.cpp or test_example.cpp)
  clean                Remove output directories
  help                 Show this help

Examples:
  python run.py                      # Auto-obfuscate input.cpp
  python run.py preview mycode.cpp
  python run.py obfuscate mycode.cpp
  python run.py test
  python run.py clean

Note: Create input.cpp in the root directory for quick obfuscation
""")
            sys.exit(1)

    command = sys.argv[1]

    if command == "preview":
        if len(sys.argv) < 3:
            print("Error: Please specify a file")
            sys.exit(1)
        file = sys.argv[2]
        return run_command([
            "python", "obfuscate_cpp.py",
            file, "-k", "keep_list.txt", "--dry-run"
        ])

    elif command == "obfuscate":
        if len(sys.argv) < 3:
            print("Error: Please specify a file")
            sys.exit(1)
        file = sys.argv[2]
        return run_command([
            "python", "obfuscate_cpp.py",
            file, "-k", "keep_list.txt"
        ])

    elif command == "obfuscate+":
        if len(sys.argv) < 3:
            print("Error: Please specify a file")
            sys.exit(1)
        file = sys.argv[2]
        print("Enhanced obfuscation with dead code injection and spacing randomization...")
        return run_command([
            "python", "obfuscate_cpp.py",
            file, "-k", "keep_list.txt", "--dead-code", "--randomize-spacing"
        ])

    elif command == "test":
        # Check if obfuscate_input.cpp exists, otherwise use test_example.cpp
        test_file = "obfuscate_input.cpp" if Path("obfuscate_input.cpp").exists() else "test_example.cpp"
        print(f"Running test with {test_file}...")
        return run_command([
            "python", "obfuscate_cpp.py",
            test_file, "-k", "keep_list.txt",
            "-o", "obfuscated_out"
        ])

    elif command == "clean":
        print("Cleaning output directories...")
        dirs = ["obfuscated_out", "test_output", "obfuscated_output"]
        for d in dirs:
            path = Path(d)
            if path.exists():
                import shutil
                shutil.rmtree(path)
                print(f"✓ Removed {d}")
        
        # Remove mapping file
        map_file = Path("obfuscation_map.txt")
        if map_file.exists():
            map_file.unlink()
            print("✓ Removed obfuscation_map.txt")
        
        print("✓ Clean complete")
        return 0

    elif command == "help":
        return run_command(["python", "obfuscate_cpp.py", "--help"])

    else:
        print(f"Unknown command: {command}")
        print("Run 'python run.py' for help")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
