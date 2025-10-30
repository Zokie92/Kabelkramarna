###### PORT SCANNER DELUXE MED EXTRA MYCKET STARK SÅS ######

import socket
import sys
from typing import Tuple
import time
from datetime import datetime

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


# Nästa funktion ska returnera resultatet. 

def scan_ports(target: str, start: int, end: int, timeout: float = 1.0, presentation: str = "all"): 
    results = [] 

    print(f"Scanning {target} from port {start} to {end}.\nTimeout set to: {timeout} ")
    
def scan_ports(target: str, start: int, end: int, timeout: float = 1.0, presentation: str = "all"): 
    results = [] 
    open_results = []
    closed_results = []
    error_results = []

    # Header till användaren
    print(f"\nNätverksskanner v1.0")
    print("="*50)
    print(f"Mål: {target}")
    print(f"Portintervall: {start}-{end}")
    print(f"Timeout: {timeout} sekund(er)")
    print("="*50)

    total_ports = end - start + 1
    bar_length = 25  # längre progress-bar
    start_time = time.time()

    for port in range(start, end + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            res = sock.connect_ex((target, port))
            if res == 0:
                banner, service = id_service(target, port, timeout=timeout)
                if banner:
                    line = f"Port {port} [ÖPPEN] - {service} ({banner.splitlines()[0] if banner.splitlines() else banner})"
                else:
                    line = f"Port {port} [ÖPPEN] - {service} (Ingen banner)"
                open_results.append(line)
                results.append(line)
            else:
                line = f"Port {port} [STÄNGD]"
                if presentation == "all":
                    print(line)
                closed_results.append(line)
                results.append(line)
        except Exception as e:
            line = f"Port {port} [FEL] - {e}"
            error_results.append(line)
            results.append(line)
        finally:
            sock.close()

        # Progress-bar
        current = port - start + 1
        percent = (current / total_ports) * 100
        filled_len = int(round(bar_length * current / float(total_ports)))
        bar = "█" * filled_len + "░" * (bar_length - filled_len)
        print(f"\rSkannar... [{bar}] {percent:5.1f}% ({current}/{total_ports})", end="")

    # Slut på skanning
    print("\n\nSkanning klar!")
    elapsed = time.time() - start_time

    # Resultatvisning
    print("\nResultat:")
    print("-"*50)
    for line in open_results:
        print(line)
    if presentation == "all":
        for line in closed_results + error_results:
            print(line)

    print("="*50)
    print(f"Skanning slutförd på {elapsed:.1f} sekunder")
    print(f"{len(open_results)} öppna portar hittades")
    footer = f"[Scan complete. End time: {datetime.now().replace(microsecond=0)}]"
    results.append(footer)
    print(footer)

    return results


def save_results_to_file(lines, filename=None):
    if not filename:
        # Använd säker timestamp för filnamn (inga kolon eller mellanslag)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portscan_{timestamp}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
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


if __name__ == "__main__":
    print(" ")
    print("##########################################################")
    print("###### Welcome to Kabelkramarnas fancy Port-Scanner ######")
    print("##########################################################")
    print(" ")
    print("We do not take responsibility for this scanner being used for anything shady.")
    print("Only scan hosts you are the admin of or specifically have permission to scan.")
    print("For scanning remote targets please use scanme.nmap.org or similar URLs used för testing.")
    print(" ")

    try:
        while True:
            target_host = input("Select a target host to scan using either URL or IP-adress: ").strip()
            start = get_int_input("Define port scan range from port (enter port number): ")
            end = get_int_input("To port: ")
            if end < start:
                print("End port must be a higher number than start port. Please try again.")
                continue

            presentation = input("Type ALL to show result of every port or OPEN to only show open ports: ").lower().strip()
            if presentation not in ("all", "open"):
                print("Invalid presentation choice, defaulting to ALL.")
                presentation = "all"

            timeout = input("Set a timeout for each port in seconds. Use '.' for a decimal (press Enter for default 1s): ").strip()
            try:
                timeout_val = float(timeout) if timeout else 1.0
            except ValueError:
                timeout_val = 1.0

            # Kör skanningen och samla resultatrader
            result_lines = scan_ports(target_host, start, end, timeout=timeout_val, presentation=presentation)

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