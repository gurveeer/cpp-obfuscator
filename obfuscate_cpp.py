#!/usr/bin/env python3
"""
C++ Code Obfuscator - Terminal Edition
Advanced identifier obfuscation with reversible mapping
"""
import sys
import time
import argparse
from pathlib import Path
from collections import OrderedDict

from utils.ui import (
    Colors, print_banner, print_step, print_success,
    print_warning, print_error, print_info,
    animate_progress, print_stats_box
)
from utils.obfuscator import (
    CPP_KEYWORDS, STD_COMMON,
    remove_comments, gather_identifiers,
    build_replacement_map, process_file,
    write_map_file, load_keep_list
)
from utils.file_scanner import discover_cpp_files


def run_dry_run(id_list):
    """Display preview of identifiers to be obfuscated"""
    print(f"\n{Colors.HEADER}═══ DRY RUN MODE - Preview Only ═══{Colors.ENDC}\n")
    print(f"{Colors.BOLD}Candidate identifiers to obfuscate:{Colors.ENDC}\n")

    display_count = min(200, len(id_list))
    for i, name in enumerate(id_list[:display_count], 1):
        color = Colors.OKCYAN if i % 2 == 0 else Colors.OKBLUE
        print(f"{color}{i:4d}.{Colors.ENDC} {name}")

    if len(id_list) > display_count:
        print(f"\n{Colors.DIM}... and {len(id_list) - display_count} more{Colors.ENDC}")

    print(f"\n{Colors.OKGREEN}Total candidates: {len(id_list)}{Colors.ENDC}")


def analyze_files(in_paths, keep_set):
    """Analyze files and gather identifiers"""
    all_identifiers = OrderedDict()
    file_stats = {}

    for path in in_paths:
        txt = path.read_text(encoding='utf-8')
        no_comments = remove_comments(txt)
        ids = gather_identifiers(no_comments, keep_set)
        file_stats[path.name] = len(ids)
        for name in ids:
            if name not in all_identifiers:
                all_identifiers[name] = None

    return list(all_identifiers.keys()), file_stats


def obfuscate_files(in_paths, out_base, mapping, keep_set):
    """Obfuscate all input files"""
    processed_files = []

    for idx, in_path in enumerate(in_paths, 1):
        rel = in_path.resolve().relative_to(Path.cwd().resolve())
        out_path = out_base.joinpath(rel)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        animate_progress(f"Processing [{idx}/{len(in_paths)}] {in_path.name}", 0.2)
        process_file(in_path, out_path, mapping, keep_set)
        processed_files.append(out_path)

    return processed_files


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description=f"{Colors.BOLD}C++ Code Obfuscator{Colors.ENDC} - Advanced identifier obfuscation",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('inputs', nargs='+', help="Input file(s) or directory(ies)")
    parser.add_argument('-o', '--out-dir', help="Output directory (default: obfuscated_out)", default='obfuscated_out')
    parser.add_argument('-k', '--keep', help="Keep-list file (one identifier per line)", default=None)
    parser.add_argument('-m', '--map', help="Mapping file path (default: obfuscation_map.txt)", default='obfuscation_map.txt')
    parser.add_argument('--dry-run', action='store_true', help="Preview candidates without obfuscating")
    args = parser.parse_args()

    # Step 1: Initialize
    print_step(1, 5, "Initializing obfuscation engine...")
    time.sleep(0.3)

    keep_set = set(CPP_KEYWORDS) | STD_COMMON
    if args.keep:
        keep_path = Path(args.keep)
        if keep_path.exists():
            keep_set |= load_keep_list(keep_path)
            print_success(f"Loaded keep-list: {Colors.DIM}{args.keep}{Colors.ENDC} ({len(keep_set) - len(CPP_KEYWORDS) - len(STD_COMMON)} custom identifiers)")
        else:
            print_warning(f"Keep-list file not found: {args.keep}")

    print_info(f"Protected identifiers: {Colors.BOLD}{len(keep_set)}{Colors.ENDC}")

    # Step 2: Scan files
    print_step(2, 5, "Scanning for target files...")
    animate_progress("Discovering C++ files", 0.5)

    in_paths, warnings = discover_cpp_files(args.inputs)

    for warning in warnings:
        print_warning(warning)

    if not in_paths:
        print_error("No input files found")
        sys.exit(1)

    print_success(f"Found {Colors.BOLD}{len(in_paths)}{Colors.ENDC} file(s) to process")

    # Step 3: Analyze identifiers
    print_step(3, 5, "Analyzing identifiers...")
    animate_progress("Extracting and analyzing code structure", 0.8)

    id_list, file_stats = analyze_files(in_paths, keep_set)

    stats = {
        "Files scanned": len(in_paths),
        "Unique identifiers": len(id_list),
        "Protected identifiers": len(keep_set),
        "Identifiers to obfuscate": len(id_list)
    }
    print_stats_box("ANALYSIS RESULTS", stats)

    # Dry run mode
    if args.dry_run:
        run_dry_run(id_list)
        sys.exit(0)

    # Step 4: Generate mapping
    print_step(4, 5, "Generating obfuscation mapping...")
    animate_progress("Creating identifier transformation map", 0.6)

    mapping = build_replacement_map(id_list, start_index=0)
    print_success(f"Generated {Colors.BOLD}{len(mapping)}{Colors.ENDC} obfuscated identifiers")

    # Step 5: Obfuscate files
    print_step(5, 5, "Obfuscating files...")

    out_base = Path(args.out_dir)
    if not out_base.exists():
        out_base.mkdir(parents=True, exist_ok=True)
        print_info(f"Created output directory: {Colors.DIM}{args.out_dir}{Colors.ENDC}")

    processed_files = obfuscate_files(in_paths, out_base, mapping, keep_set)
    print_success(f"Obfuscated {Colors.BOLD}{len(processed_files)}{Colors.ENDC} file(s)")

    # Write mapping file
    print_info("Writing obfuscation map...")
    write_map_file(Path(args.map), mapping)
    print_success(f"Mapping saved: {Colors.DIM}{args.map}{Colors.ENDC}")

    # Final statistics
    final_stats = {
        "Input files": len(in_paths),
        "Output files": len(processed_files),
        "Identifiers obfuscated": len(mapping),
        "Identifiers protected": len(keep_set),
        "Output directory": args.out_dir,
        "Mapping file": args.map
    }
    print_stats_box("OBFUSCATION COMPLETE", final_stats)

    print(f"{Colors.OKGREEN}{Colors.BOLD}✓ Operation completed successfully{Colors.ENDC}")
    print(f"{Colors.WARNING}⚠ Remember to verify public API symbols are in keep-list{Colors.ENDC}\n")


if __name__ == "__main__":
    main()
