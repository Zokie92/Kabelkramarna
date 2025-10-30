import socket
import argparse
import concurrent.futures
import sys
import time
import json
import csv
from concurrent.futures import as_completed

# Optional niceties: color output and progress bar
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    _HAS_COLOR = True
except Exception:
    _HAS_COLOR = False

try:
    from tqdm import tqdm
    _HAS_TQDM = True
except Exception:
    _HAS_TQDM = False


def check_port(host, port, timeout=3):
    """Return True if port is open on host, False otherwise."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        try:
            sock.close()
        except Exception:
            pass


def parse_ports(ports_str):
    """Parse strings like '22,80,8000-8005' into a sorted list of ports."""
    ports = set()
    if not ports_str:
        return []
    for part in ports_str.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                start, end = part.split('-', 1)
                start = int(start); end = int(end)
            except ValueError:
                raise ValueError(f"Invalid range: {part}")
            if start > end:
                raise ValueError(f"Invalid range (start>end): {part}")
            for p in range(max(1, start), min(65535, end) + 1):
                ports.add(p)
        else:
            try:
                p = int(part)
            except ValueError:
                raise ValueError(f"Invalid port: {part}")
            if 1 <= p <= 65535:
                ports.add(p)
            else:
                raise ValueError(f"Port out of range 1-65535: {p}")
    return sorted(ports)


def id_protocol(target, port, timeout=1.0):
    """Try to read a banner and guess the protocol. Returns (banner, guess)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    banner = ""
    try:
        sock.connect((target, port))
        try:
            data = sock.recv(4096)
            banner = data.decode('utf-8', errors='ignore').strip()
        except socket.timeout:
            banner = ""
        except Exception:
            banner = ""
    except Exception:
        return ("", "unknown")
    finally:
        try:
            sock.close()
        except Exception:
            pass

    b = banner.lower()
    if not b:
        # no immediate banner  try lightweight probe for common ports
        probe_map = {
            80: b"HEAD / HTTP/1.0\r\n\r\n",
            8080: b"HEAD / HTTP/1.0\r\n\r\n",
            443: b"HEAD / HTTP/1.0\r\n\r\n",
            21: b"USER anonymous\r\n",
            25: b"HELO example.com\r\n",
            110: b"\r\n",
            143: b"\r\n",
            3306: b"\x00",
            5432: b"\x00",
            6379: b"*1\r\n$4\r\nPING\r\n",
        }
        probe = probe_map.get(port)
        if probe:
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.settimeout(timeout)
            try:
                sock2.connect((target, port))
                try:
                    sock2.sendall(probe)
                    time.sleep(0.1)
                    data = sock2.recv(4096)
                    banner = data.decode('utf-8', errors='ignore').strip()
                except Exception:
                    banner = ""
            except Exception:
                banner = ""
            finally:
                try:
                    sock2.close()
                except Exception:
                    pass

    b = banner.lower()
    guessed = "unknown"
    if "ssh-" in b or port == 22:
        guessed = "SSH"
    elif "http/" in b or "server:" in b or port in (80, 8080, 8000):
        guessed = "HTTP"
    elif b.startswith("220") or port in (21, 25):
        guessed = "FTP"
    elif "imap" in b or port == 143:
        guessed = "IMAP"
    elif "pop3" in b or port == 110:
        guessed = "POP3"
    elif "mysql" in b or port == 3306:
        guessed = "MySQL"
    elif "postgres" in b or port == 5432:
        guessed = "PostgreSQL"
    elif "redis" in b or port == 6379:
        guessed = "Redis"
    elif "mongodb" in b or port == 27017:
        guessed = "MongoDB"

    return (banner, guessed)


def scan_ports(host, ports, timeout=1.0, workers=100, identify=False):
    """Scan ports concurrently. Returns dict port->(is_open, banner, guess).
    If identify=True then run id_protocol for open ports."""
    results = {}
    workers = max(1, min(workers, len(ports)))
    pbar = None
    if _HAS_TQDM:
        pbar = tqdm(total=len(ports), desc=f"Skannar {host}", unit="port", 
                   ncols=60, bar_format='{desc}: {percentage:3.0f}%|{bar}|')

    # First phase: Scan all ports and collect results
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(check_port, host, p, timeout): p for p in ports}
        for fut in as_completed(futures):
            p = futures[fut]
            try:
                is_open = fut.result()
            except Exception:
                is_open = False
            banner = ""
            guess = ""
            if is_open and identify:
                banner, guess = id_protocol(host, p, timeout=timeout)
            results[p] = (is_open, banner, guess)
            if pbar:
                pbar.update(1)
    if pbar:
        pbar.close()

    # Second phase: Print results in a clean list format
    print(f"\nResultat för {host}:")
    print("-" * 60)
    
    # First show open ports
    open_ports = [(p, results[p][1], results[p][2]) for p in sorted(results) if results[p][0]]
    if open_ports:
        if _HAS_COLOR:
            print(f"{Fore.GREEN}Öppna portar:{Style.RESET_ALL}")
        else:
            print("Öppna portar:")
        for p, banner, guess in open_ports:
            if _HAS_COLOR:
                port_line = f"  {Fore.GREEN}Port {p:<6}{Style.RESET_ALL}"
            else:
                port_line = f"  Port {p:<6}"
            if identify and guess:
                port_line += f" - {guess}"
                if banner:
                    port_line += f" ({banner})"
            print(port_line)
    else:
        if _HAS_COLOR:
            print(f"{Fore.YELLOW}Inga öppna portar hittades{Style.RESET_ALL}")
        else:
            print("Inga öppna portar hittades")
    
    # Then show closed ports if there aren't too many
    closed_ports = [p for p in sorted(results) if not results[p][0]]
    if closed_ports:
        if len(closed_ports) <= 10:  # Only show closed ports if there aren't too many
            if _HAS_COLOR:
                print(f"\n{Fore.RED}Stängda portar:{Style.RESET_ALL}")
            else:
                print("\nStängda portar:")
            for p in closed_ports:
                if _HAS_COLOR:
                    print(f"  {Fore.RED}Port {p}{Style.RESET_ALL}")
                else:
                    print(f"  Port {p}")
        else:
            if _HAS_COLOR:
                print(f"\n{Fore.RED}Stängda portar:{Style.RESET_ALL} {len(closed_ports)} portar")
            else:
                print(f"\nStängda portar: {len(closed_ports)} portar")
    
    print("-" * 60)
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description='Enkel TCP-portscanner')
    parser.add_argument('host', nargs='?', default='scanme.nmap.org')
    parser.add_argument('-p', '--ports', default='22,80,443,8080,3306')
    parser.add_argument('-t', '--timeout', type=float, default=1.0)
    parser.add_argument('-w', '--workers', type=int, default=100)
    parser.add_argument('-i', '--identify', action='store_true', help='Försök identifiera tjänster på öppna portar')
    parser.add_argument('-o', '--output', choices=['json', 'csv'], default=None, help='Spara resultat till fil i JSON eller CSV')
    parser.add_argument('-f', '--output-file', default=None, help='Filnamn för sparade resultat (standard: scan_results.json/csv)')
    parser.add_argument('--no-progress', action='store_true', help='Inaktivera progressindikator (tqdm)')
    args = parser.parse_args(argv)

    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"Fel i port-specifikation: {e}")
        return 2

    if not ports:
        print("Inga portar att skanna.")
        return 1

    # If user disabled progress, pretend tqdm not available
    global _HAS_TQDM
    if args.no_progress:
        _HAS_TQDM = False

    results = scan_ports(args.host, ports, timeout=args.timeout, workers=args.workers, identify=args.identify)

    # Optionally write results
    if args.output:
        out_file = args.output_file
        if not out_file:
            out_file = f"scan_results.{args.output}"
        try:
            if args.output == 'json':
                serial = {p: {'open': results[p][0], 'banner': results[p][1], 'guess': results[p][2]} for p in sorted(results)}
                with open(out_file, 'w', encoding='utf-8') as fh:
                    json.dump({'host': args.host, 'results': serial}, fh, indent=2, ensure_ascii=False)
            else:  # csv
                with open(out_file, 'w', encoding='utf-8', newline='') as fh:
                    writer = csv.writer(fh)
                    writer.writerow(['port', 'open', 'guess', 'banner'])
                    for p in sorted(results):
                        is_open, banner, guess = results[p]
                        writer.writerow([p, is_open, guess, banner])
            print(f"Resultat sparade i {out_file}")
        except Exception as e:
            print(f"Kunde inte skriva fil: {e}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
