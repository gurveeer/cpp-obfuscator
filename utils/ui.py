"""
Terminal UI components for the obfuscator
Provides colors, animations, and formatted output
"""
import time


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    BLINK = '\033[5m'


def print_banner():
    """Display the application banner"""
    banner = f"""
{Colors.OKCYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   {Colors.BOLD}█▀▀ █▀█ █▀▄ █▀▀   █▀█ █▄▄ █▀▀ █ █ █▀ █▀▀ ▄▀█ ▀█▀ █▀█ █▀█{Colors.ENDC}{Colors.OKCYAN}   ║
║   {Colors.BOLD}█▄▄ █▄█ █▄▀ ██▄   █▄█ █▄█ █▀  █▄█ ▄█ █▄▄ █▀█  █  █▄█ █▀▄{Colors.ENDC}{Colors.OKCYAN}   ║
║                                                               ║
║              {Colors.WARNING}Advanced C++ Identifier Obfuscation{Colors.ENDC}{Colors.OKCYAN}              ║
║                    {Colors.DIM}v2.0 - Terminal Edition{Colors.ENDC}{Colors.OKCYAN}                   ║
╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)


def print_step(step_num, total_steps, message):
    """Print a step indicator"""
    print(f"{Colors.OKBLUE}[{step_num}/{total_steps}]{Colors.ENDC} {Colors.BOLD}{message}{Colors.ENDC}")


def print_success(message):
    """Print a success message"""
    print(f"{Colors.OKGREEN}✓{Colors.ENDC} {message}")


def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.WARNING}⚠{Colors.ENDC} {message}")


def print_error(message):
    """Print an error message"""
    print(f"{Colors.FAIL}✗{Colors.ENDC} {message}")


def print_info(message):
    """Print an info message"""
    print(f"{Colors.OKCYAN}ℹ{Colors.ENDC} {message}")


def animate_progress(message, duration=0.5):
    """Display an animated progress indicator"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f'\r{Colors.OKCYAN}{frames[i % len(frames)]}{Colors.ENDC} {message}', end='', flush=True)
        time.sleep(0.08)
        i += 1
    print(f'\r{Colors.OKGREEN}✓{Colors.ENDC} {message}')


def print_stats_box(title, stats):
    """Print a formatted statistics box"""
    max_len = max(len(k) + len(str(v)) for k, v in stats.items()) + 5
    width = max(max_len, len(title)) + 4

    print(f"\n{Colors.HEADER}┌{'─' * width}┐{Colors.ENDC}")
    print(f"{Colors.HEADER}│{Colors.BOLD} {title.center(width - 2)} {Colors.ENDC}{Colors.HEADER}│{Colors.ENDC}")
    print(f"{Colors.HEADER}├{'─' * width}┤{Colors.ENDC}")

    for key, value in stats.items():
        padding = width - len(key) - len(str(value)) - 4
        print(f"{Colors.HEADER}│{Colors.ENDC} {Colors.OKCYAN}{key}{Colors.ENDC}{' ' * padding}{Colors.OKGREEN}{value}{Colors.ENDC} {Colors.HEADER}│{Colors.ENDC}")

    print(f"{Colors.HEADER}└{'─' * width}┘{Colors.ENDC}\n")
