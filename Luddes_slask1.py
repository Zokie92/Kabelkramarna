import socket

def check_port(host, port, timeout=3):
    open_ports = []
    closed_ports = []

    try:
        # Skapa en socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Försök ansluta
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} på {host} är ÖPPEN.")
            open_ports.append(port)
        else:
            print(f"Port {port} på {host} är STÄNGD eller otillgänglig.")
            closed_ports.append(port)
    except socket.gaierror:
        print("Fel: Ogiltigt värdnamn.")
    except socket.timeout:
        print("Fel: Timeout – värden svarar inte.")
        closed_ports.append(port)
    except Exception as e:
        print(f"Fel: {e}")
        closed_ports.append(port)
    finally:
        sock.close()

    return open_ports, closed_ports

if __name__ == "__main__":
    host = input("Ange värd (t.ex. 127.0.0.1 eller example.com): ")
    start_port = int(input("Ange startport: "))
    end_port = int(input("Ange slutport: "))

    open_ports = []
    closed_ports = []

    for port in range(start_port, end_port + 1):
        op, cp = check_port(host, port)
        open_ports.extend(op)
        closed_ports.extend(cp)

    print(f"Öppna portar: {open_ports}")
    print(f"Stängda portar: {closed_ports}")
    
    def id_protocol(target: str, port: int, timeout: float = 1.0) -> tuple[str, str]:
        scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan_sock.settimeout(timeout)
        try:
            scan_sock.connect((target, port))
            try:
                banner = scan_sock.recv(1024).decode('utf-8', errors='ignore').strip()
            except Exception:
                banner = ""
        except Exception:
            # Could not connect; return unknown
            return "unknown", ""
        finally:
            scan_sock.close()

        banner_lower = banner.lower()
        guessed = "unknown"
        if "ssh-" in banner_lower or port == 22:
            guessed = "SSH"
        elif "http/" in banner_lower or "server:" in banner_lower or port in (80, 8080, 8000):
            guessed = "HTTP"
        elif banner_lower.startswith("220") or port == 25:
            guessed = "FTP"
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
        







