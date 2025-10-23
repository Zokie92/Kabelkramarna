import socket

host = "scanme.nmap.org"
timeout_seconds = 2.0

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_seconds)
    try:
        s.connect((host, port))
        return True
    except Exception:
        return False
    finally:
        s.close()

# Steg 1: Kontroll av en enskild port (exempel port 80)
if portscan(80):
    print("Port 80: öppen")
else:
    print("Port 80: stängd")

print("\nSkanning av portarna 1-100 hos scanme.nmap.org/:")
# Steg 2: Skanning av portintervall
open_ports = []
for port in range(22, 101):
    if portscan(port):
        print(f"{port}: öppen")
        open_ports.append(port)
    else:
        print(f"{port}: stängd")

import socket

def try_banner(host, port, timeout=3):
    probes = {80: b"HEAD / HTTP/1.0\r\n\r\n"}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            probe = probes.get(port)
            if probe:
                s.sendall(probe)
            data = s.recv(2048)
            return data.decode(errors='ignore').strip()
        except Exception:
            return ""

open_ports = [80]
host = "scanme.nmap.org"

for port in open_ports:
    banner = try_banner(host, port)
    if banner:
        print(f"{port}: banner - {banner}")
    else:
        print(f"{port}: ingen banner mottagen")

