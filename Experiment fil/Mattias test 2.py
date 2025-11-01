###### PORT SCANNER DELUXE MED EXTRA MYCKET STARK SÅS ######
import colorama
import socket
import sys
import json
import csv
from colorama import Fore, Style
import re
from typing import Tuple, List
import time
from datetime import datetime

colorama.init(autoreset=True)

print("Use this tool only on systems you own or are authorized to test.\nUnauthorized scanning is prohibited and may be illegal.\nFor safe test targets, use hosts like scanme.nmap.org.")

# funktion för att proba sockets efter tjänster.
def id_service(target: str, port: int, timeout: float = 1.0) -> Tuple[str, str]:
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
        elif "http/" in banner_lower or "server:" in banner_lower or port in (80, 8080, 8000):
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


# Hjälpfunktion: komprimera en sorterad lista av portar till intervallsträng, t.ex. [1,2,3,5,6] -> "1-3,5-6"
def compress_ports_to_ranges(ports: List[int]) -> str:
    if not ports:
        return ""
    ports = sorted(set(ports))
    ranges = []
    start = prev = ports[0]
    for p in ports[1:]:
        if p == prev + 1:
            prev = p
            continue
        else:
            if start == prev:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{prev}")
            start = prev = p
    # finalize last range
    if start == prev:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{prev}")
    return ",".join(ranges)


# Nästa funktion ska returnera resultatet. 
# presentation parameter removed
def scan_ports(target: str, start: int, end: int, timeout: float = 1.0):
    scan_results = {}  # Dictionary to store scan results per port
    total_ports = end - start + 1 
    scanned_ports = list(range(start, end + 1))
    start_time = datetime.now()
        
    print(f"Scanning {target} from port {start} to {end}.\nTimeout set to: {timeout} ")
    
    # Ensure results list exists for saving/export
    results = []

    for idx, port in enumerate(range(start, end + 1), 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try: 
            res = sock.connect_ex((target, port))
            if res == 0:
                banner, service = id_service(target, port, timeout=timeout)
                # record open
                scan_results[port] = {"status": "open", "service": service, "banner": banner}
                # add colorized line to results
                line_color = f"{Fore.GREEN}port {port}: [OPEN] - {service}"
                if banner:
                    line_color += f" - Banner: {banner.splitlines()[0]}"
                line_color += Style.RESET_ALL
                results.append(line_color)
            else:
                # record closed
                scan_results[port] = {"status": "closed"}
                # we no longer append individual closed lines to results to avoid huge output
        except Exception as e:
            scan_results[port] = {"status": "error", "error": str(e)}
            # Also append error to results for visibility
            results.append(f"Port {port}: [ERROR] - {e}")
        finally:
            sock.close()
    
        # Update progress bar (single-line overwrite)
        progress = int((idx / total_ports) * 30)  # 30 chars wide
        bar = f"[{'█' * progress}{'░' * (30 - progress)}] {int((idx / total_ports) * 100)}%"
        sys.stdout.write(f"\rScanning... {bar}")
        sys.stdout.flush()

    # Calculate scan duration
    duration = datetime.now() - start_time
    
    # Prepare results for display and storage
    # Print summary header
    print("\n")  # Clear progress bar line
    print("-" * 60)
    print(f"Scan Results for {target}")
    print(f"Time: {datetime.now().replace(microsecond=0)}")
    print(f"Duration: {duration.total_seconds():.1f} seconds")
    print("-" * 60)
    results.extend(["-" * 60, f"Scan Results for {target}", 
                   f"Time: {datetime.now().replace(microsecond=0)}", 
                   f"Duration: {duration.total_seconds():.1f} seconds", 
                   "-" * 60])

    # First show open ports
    open_ports = [p for p in scanned_ports if scan_results.get(p, {}).get("status") == "open"]
    if open_ports:
        print(f"\n{Fore.GREEN}Open Ports:{Style.RESET_ALL}")
        results.append("\nOpen Ports:")
        for port in open_ports:
            r = scan_results[port]
            if r.get("banner"):
                line = f"{Fore.GREEN}Port {port:5d}: {r['service']} - Banner: {r['banner'].splitlines()[0]}{Style.RESET_ALL}"
                results.append(f"Port {port:5d}: {r['service']} - Banner: {r['banner'].splitlines()[0]}")
            else:
                line = f"{Fore.GREEN}Port {port:5d}: {r['service']}{Style.RESET_ALL}"
                results.append(f"Port {port:5d}: {r['service']}")
            print(line)
    else:
        print(f"{Fore.YELLOW}No open ports found{Style.RESET_ALL}")
        results.append("No open ports found")

    # Then show closed ports compressed (always shown now)
    closed_ports = [p for p in scanned_ports if scan_results.get(p, {}).get("status") == "closed"]
    if closed_ports:
        compressed = compress_ports_to_ranges(closed_ports)
        print(f"\n{Fore.RED}Closed Ports: {len(closed_ports)} total{Style.RESET_ALL}")
        print(f"{Fore.RED}{compressed}{Style.RESET_ALL}")
        results.append("\nClosed Ports:")
        results.append(f"{len(closed_ports)} ports closed")
        results.append(compressed)

    # Show any errors
    error_ports = [p for p in scanned_ports if scan_results.get(p, {}).get("status") == "error"]
    if error_ports:
        print(f"\n{Fore.YELLOW}Errors:{Style.RESET_ALL}")
        results.append("\nErrors:")
        for port in error_ports:
            line = f"Port {port:5d}: {scan_results[port]['error']}"
            print(line)
            results.append(line)

    print("-" * 60)
    results.append("-" * 60)
    
    return results, scanned_ports

def save_results_to_file(lines, filename=None):
    if not filename:
        timestamp = datetime.now().replace(microsecond=0)
        filename = f"portscan_{timestamp}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(strip_ansi(line) + "\n")
        print(f"Results saved to: {filename}")
    except Exception as e:
        print(f"Could not save file: {e}")

def get_int_input(prompt, default=None, minval=0, maxval=65535):
    """
    Hjälpfunktion för att läsa integer från input och validera intervallet.
    """
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            iv = int(val)
            if iv < minval or iv > maxval:
                print(f"Enter a number between {minval} and {maxval}.")
                continue
            return iv
        except ValueError:
            print("Please enter a valid number.")

###### FUNKTION SOM RENSAR FÄRGER
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def strip_ansi(line: str) -> str:
    return ansi_escape.sub('', line)



if __name__ == "__main__":
    print(" ")
    print("##############################################")
    print(f"{Fore.YELLOW}{Style.BRIGHT}PORT SCANNER DELUXE MED EXTRA MYCKET STARK SÅS{Style.RESET_ALL}")
    print("##############################################")
    print(" ")
    print("We do not take responsibility for this scanner being used for anything shady.")
    print("Only scan hosts you are the admin of or specifically have permission to scan.")
    print("For scanning remote targets please use scanme.nmap.org or similar URLs used for testing.")
    print(" ")

    try:
        while True:
            target_host = input("Select a target host to scan using either URL or IP-adress: ").strip() or "scanme.nmap.org"
            start = get_int_input("Define port scan range from port (enter port number) [default 1]: ", default=1, minval=0, maxval=65535)
            end = get_int_input("To port: ", default=1024, minval=0, maxval=65535)
            if end < start:
                print("End port must be a higher number than start port. Please try again.")
                continue

            timeout = input("Set a timeout for each port in seconds. Use '.' for a decimal (press Enter for default 1s): ").strip()
            try:
                timeout_val = float(timeout) if timeout else 1.0
            except ValueError:
                timeout_val = 1.0

            # Kör skanningen och samla resultatrader
            result_lines, scanned_ports = scan_ports(target_host, start, end, timeout=timeout_val)

            print(f"\nScanned ports: {start} to {end} on host {target_host}\n")

            clean_lines = [strip_ansi(s) for s in result_lines]
            print("\n".join(clean_lines))

            # Alternativ för att logga resultatet i en text-fil
            save_choice = input("Would you like to save the results to a file? (y/n): ").lower().strip()
            if save_choice == "y":
                fname = input("Enter filename (or press Enter to auto-generate): ").strip()
                save_results_to_file(result_lines, fname if fname else None)

            # Fråga om ny skanning
            again = input("Would you like to scan a new range of ports? (y/n): ").lower().strip()
            if again != "y":
                print("Exiting program.\nThanks for doing some shady stuff with us.\nRemember to scan responsibly!")
                break

    except KeyboardInterrupt:
        print("\nUser interrupted. Shutting down.")