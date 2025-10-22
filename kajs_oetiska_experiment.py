
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

for port in range (20, 101):
    scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1) # Timeout set in seconds

    connection = scan_sock.connect_ex((target, port))

    if connection == 0:
        print(f"Port {port}: OPEN")
    else:
        print(f"Port {port}: CLOSED")

    scan_sock.close()