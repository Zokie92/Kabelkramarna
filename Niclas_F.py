import socket, sys, time

host = "scanme.nmap.org"
start_port = 22
end_port = 100
timeout_seconds = 2

def scan(port):
    try:
        s = socket.create_connection((host, port), timeout_seconds)
        s.close()
        return True
    except:
        return False

print("välkommen till niclas portscan-tjänst")
if input("vill du skanna port 80? (ja/nej) ").strip().lower() not in ("ja","j"):
    sys.exit()
print("Port 80:", "ÖPPEN" if scan(80) else "STÄNGD")

if input("vill du skanna portarna 22-100 också? (ja/nej) ").strip().lower() not in ("ja","j"):
    print("Avslutar, ingen intervallskanning.")
    sys.exit()

print(f"Skannar {host} portar {start_port}-{end_port} med timeout {timeout_seconds}s…")

open_ports = []
for port in range(start_port, end_port + 1):
    if scan(port):
        print(f"Port {port}: ÖPPEN")
        open_ports.append(port)
    else:
        print(f"Port {port}: STÄNGD")

print("Skanningen är klar!")
print(f"De öppna portarna är: {open_ports}")
# Steg 3:
import socket # importera socket från bibiloteket för nätverksanslutningar.

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
        except Exception:
            return ""

open_ports = [80]
host = "scanme.nmap.org"

for port in open_ports:
    banner = try_banner(host, port, timeout_seconds)
    if banner:
        print(f"{port}: banner - {banner}")
    else:
        print(f"{port}: ingen banner mottagen")

