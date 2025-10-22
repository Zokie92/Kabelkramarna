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
            return ("", "unknown")
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
        elif "mongodb" in banner_lower or port == 27017:
            guessed = "MongoDB"

        # If we already guessed from the banner, return that result
        if guessed != "unknown":
            return (banner, guessed)

        # Fallback: send lightweight probes for common ports to try to identify protocol
        probes = {
            80: b"GET / HTTP/1.0\r\n\r\n",
            443: b"GET / HTTP/1.0\r\n\r\n",
            21: b"USER anonymous\r\n",
            25: b"HELO example.com\r\n",
            110: b"\r\n",
            143: b"\r\n",
            3306: b"\x00",
            5432: b"\x00",
            6379: b"*1\r\n$4\r\nPING\r\n",
            27017: b"\x00",
        }

        probe = probes.get(port)
        if not probe:
            return (banner, "unknown")

        probe_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe_sock.settimeout(timeout)
        try:
            probe_sock.connect((target, port))
            try:
                probe_sock.sendall(probe)
                data = probe_sock.recv(1024)
                probe_resp = data.decode('utf-8', errors='ignore').lower()
            except Exception:
                probe_resp = ""
        except Exception:
            return (banner, "unknown")
        finally:
            probe_sock.close()

        # analyze probe response
        if "http/" in probe_resp or "server:" in probe_resp or "<html" in probe_resp:
            guessed = "HTTP"
        elif "ftp" in probe_resp or "220 " in probe_resp:
            guessed = "FTP"
        elif "mysql" in probe_resp:
            guessed = "MySQL"
        elif "postgres" in probe_resp or "postgresql" in probe_resp:
            guessed = "PostgreSQL"
        elif "redis" in probe_resp:
            guessed = "Redis"
        elif "mongodb" in probe_resp:
            guessed = "MongoDB"

        return (banner, guessed)
    
    def if_id_protocol(target: str, port: int, timeout: float = 1.0) -> tuple[str, str]:
        scan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan.settimeout(timeout)
        try:
            scan.connect((target, port))
            return ("Connected", "active")
        except socket.timeout:
            return ("", "timeout")
        except Exception as e:
            return ("", str(e))
        finally:
            scan.close()
            def id_protocol(tartget: str, port: int, timeout: float = 1.0) -> tuple[str, str]:
                def scan_ports_with_service(target: str, port: int, timeout: float = 1.0) -> tuple[str, str]:
    





    


            

        




    
        







