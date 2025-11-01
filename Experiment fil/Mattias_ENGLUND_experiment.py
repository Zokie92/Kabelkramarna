# portscanner_colored_full.py
import socket
import sys
from typing import Tuple
import time
from datetime import datetime
from colorama import init, Fore, Style

# Init colorama (autoreset så vi slipper återställa manuellt)
init(autoreset=True)

# Färgkonstanter (förenklade namn)
C_HEAD = Fore.CYAN + Style.BRIGHT
C_OK = Fore.GREEN + Style.BRIGHT
C_FAIL = Fore.RED + Style.BRIGHT
C_WARN = Fore.YELLOW + Style.BRIGHT
C_ERR = Fore.MAGENTA + Style.BRIGHT
C_RESET = Style.RESET_ALL

print(C_WARN + "Use this tool only on systems you own or are authorized to test.")
print(C_WARN + "Unauthorized scanning is prohibited and may be illegal.")
print(C_WARN + "For safe test targets, use hosts like scanme.nmap.org.\n" + C_RESET)


def id_service(target: str, port: int, timeout: float = 1.0) -> Tuple[str, str]:
    """Probar en port och försöker gissa tjänst via banner eller portnummer."""
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
                time.sleep(0.2)
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

        # Enkel heuristik för gissning
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


def scan_ports(target: str, start: int, end: int, timeout: float = 1.0, presentation: str = "all"):
    results = []
    open_results = []
    closed_results = []
    error_results = []

    # Header
    print(C_HEAD + "\nNätverksskanner v1.0")
    print(C_HEAD + "=" * 50)
    print(f"Mål: {target}")
    print(f"Portintervall: {start}-{end}")
    print(f"Timeout: {timeout} sekund(er)")
    print(C_HEAD + "=" * 50 + C_RESET)

    total_ports = end - start + 1
    bar_length = 30
    start_time = time.time()

    for port in range(start, end + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            res = sock.connect_ex((target, port))
            if res == 0:
                banner, service = id_service(target, port, timeout=timeout)
                status = "OPEN"
                color = color_for_status(status)
                if banner:
                    short_banner = banner.splitlines()[0] if banner.splitlines() else banner
                    line_plain = f"Port {port} [ÖPPEN] - {service} ({short_banner})"
                    line = f"{color}{line_plain}{C_RESET}"
                else:
                    line_plain = f"Port {port} [ÖPPEN] - {service} (Ingen banner)"
                    line = f"{color}{line_plain}{C_RESET}"

                open_results.append(line)
                results.append(line_plain)
                # Skriv öppna portar direkt så de syns
                print(line)
            else:
                status = "CLOSED"
                color = color_for_status(status)
                line_plain = f"Port {port} [STÄNGD]"
                line = f"{color}{line_plain}{C_RESET}"
                if presentation == "all":
                    print(line)
                closed_results.append(line)
                results.append(line_plain)
        except Exception as e:
            status = "ERROR"
            color = color_for_status(status)
            line_plain = f"Port {port} [FEL] - {e}"
            line = f"{color}{line_plain}{C_RESET}"
            error_results.append(line)
            results.append(line_plain)
        finally:
            sock.close()

        # Progress-bar (färgad)
        current = port - start + 1
        percent = (current / total_ports) * 100
        filled_len = int(round(bar_length * current / float(total_ports)))
        bar = "█" * filled_len + "░" * (bar_length - filled_len)
        # Gör progress-gul för synlighet
        print(f"\r{C_WARN}Skannar... [{bar}] {percent:5.1f}% ({current}/{total_ports}){C_RESET}", end="", flush=True)

    # Slut på skanning
    print("\n\n" + C_OK + "Skanning klar!" + C_RESET)
    elapsed = time.time() - start_time

    # Resultatvisning
    print("\nResultat:")
    print("-" * 50)
    if open_results:
        for line in open_results:
            print(line)
    else:
        print(Fore.YELLOW + "Inga öppna portar hittades." + C_RESET)

    if presentation == "all":
        if closed_results:
            print("\nStängda portar:")
            for line in closed_results:
                print(line)
        if error_results:
            print("\nFel under skanning:")
            for line in error_results:
                print(line)

    print(C_HEAD + "=" * 50 + C_RESET)
    print(f"Skanning slutförd på {elapsed:.1f} sekunder")
    print(f"{len(open_results)} öppna portar hittades")
    footer = f"[Scan complete. End time: {datetime.now().replace(microsecond=0)}]"
    results.append(footer)
    print(C_ERR + footer + C_RESET)

    # Returnera "rensade" resultatrader (utan colorama-koder) för att kunna spara i fil
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


def get_int_input(prompt, default=None, minval=0, maxval=65535):
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
    print(" ")
    print("##########################################################")
    print("###### Welcome to Kabelkramarnas fancy Port-Scanner ######")
    print("##########################################################")
    print(" ")
    print(C_WARN + "We do not take responsibility for this scanner being used for anything shady.")
    print("Only scan hosts you are the admin of or specifically have permission to scan.")
    print("For scanning remote targets please use scanme.nmap.org or similar URLs used för testing." + C_RESET)
    print(" ")

    try:
        while True:
            target_host = input("Select a target host to scan using either URL or IP-adress: ").strip()
            start = get_int_input("Define port scan range from port (enter port number): ")
            end = get_int_input("To port: ")
            if end < start:
                print(C_WARN + "End port must be a higher number than start port. Please try again." + C_RESET)
                continue

            presentation = input("Type ALL to show result of every port or OPEN to only show open ports: ").lower().strip()
            if presentation not in ("all", "open"):
                print(C_WARN + "Invalid presentation choice, defaulting to ALL." + C_RESET)
                presentation = "all"

            timeout = input("Set a timeout for each port in seconds. Use '.' for a decimal (press Enter for default 1s): ").strip()
            try:
                timeout_val = float(timeout) if timeout else 1.0
            except ValueError:
                timeout_val = 1.0

            # Kör skanningen och samla resultatrader (utan färgkoder)
            result_lines = scan_ports(target_host, start, end, timeout=timeout_val, presentation=presentation)

            save_choice = input("Would you like to save the results to a file? (y/n): ").lower().strip()
            if save_choice == "y":
                fname = input("Enter filename (or press Enter to auto-generate): ").strip()
                save_results_to_file(result_lines, fname if fname else None)

            again = input("Would you like to scan a new range of ports? (y/n): ").lower().strip()
            if again != "y":
                print(C_HEAD + "Exiting program.\nThanks for scanning responsibly!" + C_RESET)
                break

    except KeyboardInterrupt:
        print("\n" + C_WARN + "User interrupted. Shutting down." + C_RESET)