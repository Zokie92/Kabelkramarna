
#### Simpel Port-Scanner för specifika portar
"""
import socket

socket.setdefaulttimeout(2)

test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    test_socket.connect(("scanme.nmap.org", 80))
    print("Port is open.")
except Exception as e:
    print(f"Port is closed or unreachable: {e}")
finally:
    test_socket.close()
"""

#### Port-Scanner för portintervall

import socket
target = "scanme.nmap.org"

print(f"Scanning {target}...")

open_ports = [] #### Skapa en lista över öppna portar istället för att printa ut en efter en

for port in range (20, 101): #### Här kan vi justera intervallet av portar som scannas
    scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET avser IPv4-adresser --- SOCK_STREAM anger TCP som protokoll
    socket.setdefaulttimeout(1) # Timeout justeras i sekunder, variabeln 1 = 1 sekund

    connection = scan_sock.connect_ex((target, port))

    if connection == 0:  #### Om porten är öppen
        open_ports.append(port) #### Lägg till port i listan open_ports

    scan_sock.close() #### Stäng uppkopplingen

print(f"Scan complete. Open porst: {open_ports}") #### Printar lista över öppna portar