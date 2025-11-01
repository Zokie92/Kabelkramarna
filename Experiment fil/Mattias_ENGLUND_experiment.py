# portscanner_colored_full.py
"""
Improved, colorized port scanner with a compact single-line progress display.
Requires: colorama
Install: python3 -m pip install colorama

Usage: python3 portscanner_colored_full.py
Only scan hosts you own or have explicit permission to test.
"""

import socket
import sys
from typing import Tuple, List
import time
from datetime import datetime
import textwrap
from colorama import init, Fore, Style

# Initialize colorama (autoreset so colors won't "leak")
init(autoreset=True)

# Color constants
C_HEAD = Fore.CYAN + Style.BRIGHT
C_OK = Fore.GREEN + Style.BRIGHT
C_FAIL = Fore.RED + Style.BRIGHT
C_WARN = Fore.YELLOW + Style.BRIGHT
C_ERR = Fore.MAGENTA + Style.BRIGHT
C_DIM = Style.DIM
C_RESET = Style.RESET_ALL

# Short helper for safe banner truncation
def shorten_banner(banner: str, width: int = 60) -> str:
    if not banner:
        return ""
    single = banner.splitlines()[0]
    return textwrap.shorten(single, width=width, placeholder="...")


def id_service(target: str, port: int, timeout: float = 1.0) -> Tuple[str, str]:
    """Probe a port and attempt to identify the service by banner or well-known port.
    Returns: (banner, guessed_service)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((target, port))
        if result != 0:
            return ("", "unknown")

        try:
            data = sock.recv(4096)
        except socket.timeout:
            data = b""

        if not data:
            probes = {
                80: b"HEAD / HTTP/1.0\r\n\r\n",
                8080: b"HEAD / HTTP/1.0\r\n\r\n",
                8000: b"HEAD / HTTP/1.0\r\n\r\n",
                443: b"HEAD / HTTP/1.0\r\n\r\n",
                25: b"HELO example.com\r\n",
                21: b"\r\n",
                110: b"\r\n",
                143: b"\r\n",
            }
            probe = probes.get(port, b"\r\n")
            try:
                sock.sendall(probe)
                time.sleep(0.18)
                data = sock.recv(4096)
            except socket.timeout:
                data = b""
            except Exception:
                data = b""

        try:
            banner = data.decode("utf-8", errors="ignore").strip()
        except Exception:
            banner = ""

        banner_lower = banner.lower()
        guessed = "unknown"

        # Simple heuristics
        if "ssh-" in banner_lower or port == 22:
            guessed = "SSH"
        elif "http/" in banner_lower or "server:" in banner_lower or port in (80, 8080, 8000, 443):
            guessed = "HTTP"
        elif banner_lower.startswith("220") or port == 25:
            guessed = "SMTP"
        elif "ftp" in banner_lower or port == 21:
            guessed = "FTP"
        elif "imap" in banner_lower or port == 143:
            guessed = "IMAP"
        elif "pop3" in banner_lower or port == 110:
            guessed = "POP3"
        elif "mysql" in banner_lower or port == 3306:
            guessed = "MySQL"
        elif "postgres" in banner_lower or port == 5432:
            guessed = "PostgreSQL"
        elif "redis" in banner_lower or port == 6379:
            guessed = "Redis"
        elif "mongodb" in banner_lower or port == 27017:
            guessed = "MongoDB"

        return (banner, guessed)

    finally:
        sock.close()


def color_for_status(status: str) -> str:
    if status == "OPEN":
        return C_OK
    elif status == "CLOSED":
        return C_FAIL
    elif status == "ERROR":
        return C_ERR
    else:
        return Fore.WHITE


def format_header(target: str, start: int, end: int, timeout: float) -> None:
    # A nicer boxed header with aligned fields
    now = datetime.now().replace(microsecond=0)
    box_width = 66
    title = "PORT SCANNER"
    print(C_HEAD + "+" + "=" * (box_width - 2) + "+")
    print(C_HEAD + "|" + title.center(box_width - 2) + "|")
    print(C_HEAD + "|" + f" Target: {target}".ljust(box_width - 2) + "|")
    print(C_HEAD + "|" + f" Ports: {start}-{end}".ljust(box_width - 2) + "|")
    print(C_HEAD + "|" + f" Timeout: {timeout} s".ljust(box_width - 2) + "|")
    print(C_HEAD + "|" + f" Started: {now.isoformat(' ')}".ljust(box_width - 2) + "|")
    print(C_HEAD + "+" + "=" * (box_width - 2) + "+" + C_RESET)


def print_single_line_progress(current: int, total: int, elapsed: float, open_count: int, last_open: str, bar_length: int = 30) -> None:
    percent = (current / total) * 100
    filled_len = int(round(bar_length * current / float(total)))
    bar = "█" * filled_len + "░" * (bar_length - filled_len)
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(int(elapsed)))
    # Compose a compact single-line status. It will overwrite itself via \r.
    extra = f" | Open: {open_count}"
    if last_open:
        extra += f" (last: {last_open})"
    print(f"\r{C_WARN}Scanning [{bar}] {percent:6.2f}% ({current}/{total}) Elapsed: {elapsed_str}{extra}{C_RESET}", end="", flush=True)


def scan_ports(target: str, start: int, end: int, timeout: float = 1.0, presentation: str = "all") -> List[str]:
    """Scan ports from start to end (inclusive). Returns a list of plain text result lines (no color codes) for saving."""
    results: List[str] = []
    open_results: List[tuple] = []
    closed_results: List[int] = []
    error_results: List[tuple] = []

    total_ports = end - start + 1
    bar_length = 36
    start_time = time.time()

    format_header(target, start, end, timeout)

    open_count = 0
    last_open_display = ""

    for port in range(start, end + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            res = sock.connect_ex((target, port))
            if res == 0:
                banner, service = id_service(target, port, timeout=timeout)
                status = "OPEN"
                short = shorten_banner(banner, width=58)
                line_plain = f"Port {port} [OPEN] - {service} - {short}"
                open_results.append((port, service, short))
                results.append(line_plain)
                open_count += 1
                last_open_display = f"{port}/{service}"
            else:
                line_plain = f"Port {port} [CLOSED]"
                closed_results.append(port)
                results.append(line_plain)
        except Exception as e:
            line_plain = f"Port {port} [ERROR] - {e}"
            error_results.append((port, str(e)))
            results.append(line_plain)
        finally:
            sock.close()

        # single-line progress update
        current = port - start + 1
        elapsed = time.time() - start_time
        print_single_line_progress(current, total_ports, elapsed, open_count, last_open_display, bar_length)

    # finish
    elapsed = time.time() - start_time
    print()  # newline after progress
    print(C_OK + "\nScan finished" + C_RESET)

    # Pretty results block
    print(C_HEAD + "\nRESULTS".center(66) + C_RESET)
    print(C_HEAD + "-" * 66 + C_RESET)

    if open_results:
        print(C_OK + "Open ports:" + C_RESET)
        print(C_OK + "{:<7} {:<12} {:<60}".format("PORT", "SERVICE", "BANNER") + C_RESET)
        for port, service, short in open_results:
            print(C_OK + "{:<7} {:<12} {:<60}".format(port, service, short) + C_RESET)
    else:
        print(C_WARN + "No open ports found." + C_RESET)

    if presentation == "all":
        if closed_results:
            print(C_FAIL + "\nClosed ports (sample):" + C_RESET)
            sample = closed_results[:200]
            print(C_FAIL + ", ".join(str(p) for p in sample) + ("..." if len(closed_results) > len(sample) else "") + C_RESET)

        if error_results:
            print(C_ERR + "\nErrors during scan:" + C_RESET)
            for port, err in error_results:
                print(C_ERR + f"{port}: {err}" + C_RESET)

    print(C_HEAD + "=" * 66 + C_RESET)
    print(f"Elapsed time: {time.strftime('%H:%M:%S', time.gmtime(int(elapsed)))}")
    print(f"Open ports found: {len(open_results)}")
    footer = f"[Scan complete. End time: {datetime.now().replace(microsecond=0)}]"
    print(C_ERR + footer + C_RESET)

    # return plain lines (no color) for file saving
    results.append(footer)
    return results


def save_results_to_file(lines, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portscan_{timestamp}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(C_OK + f"Results saved to: {filename}" + C_RESET)
    except Exception as e:
        print(C_ERR + f"Could not save file: {e}" + C_RESET)


def get_int_input(prompt, default=None, minval=0, maxval=1025) -> int:
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            iv = int(val)
            if iv < minval or iv > maxval:
                print(C_WARN + f"Enter a number between {minval} and {maxval}." + C_RESET)
                continue
            return iv
        except ValueError:
            print(C_WARN + "Please enter a valid number." + C_RESET)


if __name__ == "__main__":
    print("\n##########################################################")
    print("######       Welcome to the Fancy Port Scanner       #####")
    print("##########################################################\n")
    print(C_WARN + "Only scan hosts you own or have explicit permission to test.")
    print("For safe test targets, use scanme.nmap.org or similar test hosts.\n" + C_RESET)

    try:
        while True:
            target_host = input("Target host (IP or domain) [default: scanme.nmap.org]: ").strip() or "scanme.nmap.org"
            start = get_int_input("Start port (1-1024) [default 1]: ", default=1, minval=0, maxval=1024)
            end = get_int_input("End port (1-1024) [default 1024]: ", default=1024, minval=0, maxval=1024)
            if end < start:
                print(C_WARN + "End port must be greater than or equal to start port. Please try again." + C_RESET)
                continue

            presentation = input("Show ALL ports or only OPEN ports? (all/open) [default: open]: ").lower().strip() or "open"
            if presentation not in ("all", "open"):
                print(C_WARN + "Invalid choice, defaulting to 'open'." + C_RESET)
                presentation = "open"

            timeout = input("Timeout per port in seconds (e.g. 0.5) [default 1.0]: ").strip() or "1.0"
            try:
                timeout_val = float(timeout)
            except ValueError:
                timeout_val = 1.0

            result_lines = scan_ports(target_host, start, end, timeout=timeout_val, presentation=presentation)

            save_choice = input("Save results to file? (y/n) [default: n]: ").lower().strip() or "n"
            if save_choice == "y":
                fname = input("Enter filename (or press Enter to auto-generate): ").strip() or None
                save_results_to_file(result_lines, fname)

            again = input("Scan another target/range? (y/n) [default: n]: ").lower().strip() or "n"
            if again != "y":
                print(C_HEAD + "Exiting. Scan responsibly!" + C_RESET)
                break

    except KeyboardInterrupt:
        print("\n" + C_WARN + "User interrupted. Shutting down." + C_RESET)