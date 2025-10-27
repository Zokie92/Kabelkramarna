import socket # Import av bibliotek
from datetime import datetime # Import av datum och tid
from colorama import Fore, Back, Style, init
init(autoreset=True)


""""
# Övning 1

test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
test_socket.settimeout(0.5)

try:
    test_socket.connect_ex(("scanme.nmap.org", 80))
    print("Port is open.")
except Exception as e:
    print(f"Port is closed: {e}")
finally:
    test_socket.close()


# Övning 2

target = "scanme.nmap.org" # Målet för scanning
open_ports = [] # Lista över öppna portar

# Banner
print("\n\n\nPORT SCANNER")
print("=" * 40)
print("Scanning: " + target)
print("Scanning started: " + str(datetime.now()).split(".")[0])
print("=" * 40)


for port in range(20, 81): # Sätter ett intervall av portar som ska scannas

    scan = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Skapar en socket (IPv4 och TCP)
    scan.settimeout(0.5) # Sätter en timeout

    # Försöker skapa en connection
    result = scan.connect_ex((target, port)) # Target är "scanme.nmap.org" och portar ifrån det valda intervallet

    if result == 0: # Här kollar vi om porten är öppen.
        open_ports.append(port) # Om port är öppen läggs den i listan med öpnna portar.
    else:
        continue
        
    scan.close() # Stänger socket efter scanning.


print(f"Complete scan of: {target}. Open ports: {open_ports}") # Skriver ut en lista med öppna portar.
"""

# Övning 3

def grab_banner(host, port, timeout=0.5):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(timeout)
    

    try:
        client_scan = client.connect_ex((host, port))
        if client_scan != 0:
            return None

        
        try:
            data = client.recv(1024)
        except socket.timeout:
            data = b""

        if not data:
            probes = {80: f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode()}
            probe = probes.get(port, b"\r\n")
                
            try:
                client.sendall(probe)
            except Exception:
                pass
            try:
                data = client.recv(1024)
            except socket.timeout:
                data = b""

        if not data:
            return None

        return data.decode("utf-8", errors="replace").split("\r\n")[0].strip()
     
    except Exception:
        return None
    
    finally:
        client.close()
        
    
if __name__ == "__main__":
    host = "scanme.nmap.org"
    open_ports = []
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    total_ports = end_port - start_port + 1
    print(f"Scanning ports {start_port} to {end_port}...\n")

    for i, port in enumerate(range(start_port, end_port + 1), 1):
        banner = grab_banner(host, port, timeout=0.5)
        if banner:
            open_ports.append((port, banner))

        percent = i / total_ports * 100
        print(f"Scanning {percent:.1f} % complete", end="\r")

    print("\n\n===== Open ports =====\n")

    if not open_ports:
        print(Fore.RED + "No open ports found.")
    else:
        for port, banner in open_ports:
            print(Fore.GREEN + f"Port: {port} - {banner}")
        
