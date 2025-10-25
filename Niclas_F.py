import socket
import sys
import time

host = "scanme.nmap.org"
start_port = 22
end_port = 80
timeout_seconds = 2


def scan(port):
    try:
        s = socket.create_connection((host, port), timeout_seconds)
        s.close()
        return True
    except:
        return False

def try_banner(host, port, timeout_seconds):
    probes = {80: b"HEAD / HTTP/1.0\r\n\r\n"}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout_seconds)
        try:
            s.connect((host, port))
            probe = probes.get(port)
            if probe:
                s.sendall(probe)
            data = s.recv(2048)
            return data.decode(errors='ignore').strip()
        except:
            return None

print("Välkommen till Niclas nätverksskanner-tjänst")
if input("Vill du skanna port 80? (ja/nej) ").strip().lower() not in ("ja", "j"):
    sys.exit()
start_time = time.time()

open_ports = []
if scan(80):
    open_ports.append(80)
print("Port 80:", "ÖPPEN" if 80 in open_ports else "STÄNGD")

if input("Vill du skanna portarna 22-80 också? (ja/nej) ").strip().lower() not in ("ja", "j"):
    print("\nResultat:")
    print("---------\n")
print(f"Skannar {host} portar {start_port}-{end_port} med timeout {timeout_seconds}s…")

for port in range(start_port, end_port + 1):
    if scan(port):
        print(f"Port {port}: ÖPPEN")
        open_ports.append(port)
    else:
        print(f"Port {port}: STÄNGD")

print("Skanningen är klar!")
print(f"De öppna portarna är: {open_ports}")

# Banner-grabbing för öppna portar
print("\nBanner-resultat för öppna portar:")
for port in open_ports:
    banner = try_banner(host, port, timeout_seconds)
    if banner:
        print(f"{port}: banner - {banner}")
    else:
        print(f"{port}: ingen banner mottagen")