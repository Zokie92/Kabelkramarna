
#### Simpel Port-Scanner för specifika portar
"""
import socket

port_scan = int(input("Select a port to scan: "))
    try:
        socket.setdefaulttimeout(2)

        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            test_socket.connect(("scanme.nmap.org", port_scan))
            print("Port is open.")
        except Exception as e:
            print(f"Port is closed or unreachable: {e}")
        finally:
            test_socket.close()
    except ValueError:
        print("Invalid entry. Please select a numerical value.)
"""

#### Port-Scanner för portintervall

"""

import socket
target = "scanme.nmap.org"

print(f"Scanning {target}...")

open_ports = [] #### Skapa en lista över öppna portar istället för att printa ut en efter en

for port in range (20, 101): #### Här kan vi justera intervallet av portar som scannas
    scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET avser IPv4-adresser --- SOCK_STREAM anger TCP som protokoll
    socket.setdefaulttimeout(1) # Timeout justeras i sekunder, variabeln 1 = 1 sekund

    connection = scan_sock.connect_ex((target, port)) #### Target är i detta fallet scanme.nmap.org och port är portar i det valda intervallet

    if connection == 0:  #### Om porten är öppen
        open_ports.append(port) #### Lägg till port i listan open_ports

    scan_sock.close() #### Stäng uppkopplingen

print(f"Scan complete. Open ports: {open_ports}") #### Printar lista över öppna portar

"""



#### Port-Scanner som även identifierar tjänster för öppna portar

import socket
import time

print(" ")
print("##########################################################")
print("###### Welcome to Kabelkramarnas fancy Port-Scanner ######")
print("##########################################################")
print(" ")
print("Here we could use an input for you to decide what tagret host to scan....")
print("But for obvious legal reasons our variable target_host is set to scanme.nmap.org")
print(" ")
start = int(input("Define port scan range from port (enter port number): "))
end = int(input("To port: "))
presentation = input("Type ALL to show result of every port or OPEN to only show open ports: ").lower().strip()


def id_protocol(target: str, port: int, timeout: float = 2.0) -> (str, str):

    """"
    Denna funktion ska försöka läsa en banner från målets port och avgöra tjänsten.
    Retur: (banner:text, guessed_service) - banner_text kan vara '' om data inte hittats.
    """
    scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scan_sock.settimeout(timeout)

    try:
        result = scan_sock.connect_ex((target, port))
        if result != 0: #### 0 är lyckad anslutning och i detta fall är allt utom lyckad anslutning
            return ("", "unknown")
        
        try:
            data = scan_sock.recv(4096)
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
                scan_sock.sendall(probe)
                time.sleep(0.2)
                data = scan_sock.recv(4096)
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

        if "ssh-" in banner_lower or port == 22:
            guessed = "SSH"
        elif "http/" in banner_lower or "server:" in banner_lower or port in (80, 8080, 8000):
            guessed = "HTTP"
        elif banner_lower.startswith("220") or port == 25:
            guessed = "FTP"
        elif "ftp" in banner_lower or port == 21:
            guessed == "FTP"
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
        scan_sock.close()


def scan_ports_with_service(target: str, start: int, end: int, timeout: float = 1.0):

    print(f"Scanning {target} in port range {start} to {end}... ")

    ### PRINTA BARA ÖPPNA PORTAR
    if presentation == "open":
        for port in range(start, end + 1):
            scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan_sock.settimeout(timeout)
            try:
                result = scan_sock.connect_ex((target, port))
                if result == 0:
                    banner, service = id_protocol(target, port, timeout = 2.0)
                    print(f"Port {port}: OPEN - {service} - Banner: {banner}")
            except Exception as e:
                    print(f"Port {port}: ERROR - {e}")
            finally:
                scan_sock.close()
            
    ### PRINTA ALLA SKANNADE PORTAR
    elif presentation == "all":
        for port in range(start, end + 1):
            scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan_sock.settimeout(timeout)        
            try:
                result = scan_sock.connect_ex((target, port))
                if result == 0:
                    banner, service = id_protocol(target, port, timeout = 2.0)
                    if banner:
                        print(f"Port {port}: OPEN - {service} - Banner: {banner.splitlines()[0]}")
                    else:
                        print(f"Port {port}: OPEN - {service} - No banner received.")
                else:
                    print(f"Port {port}: CLOSED")
            except Exception as e:
                print(f"Port {port}: ERROR - {e}")
            finally:
                scan_sock.close()
    else:
        print("Invalid entry.")
    
    print(" ")
    print("Scan complete...\nThank you for doing some really shady stuff with us.")
    print(" ")


if __name__ == "__main__":
    
    target_host = "scanme.nmap.org"
    scan_ports_with_service(target_host, start, end, timeout = 0.5)