import socket #importera socket från bibiloteket för nätverksanslutningar.

host = "scanme.nmap.org" # hostserverns namn.
timeout_seconds = 2.0 # 2 sekund delay på scanningen.

print(f"hej! här har du bara möjlighet att scanna en specifik port och i detta fallet är det port 80")
if input("vill du göra detta? (ja/nej):").lower() != "ja":


def portscan(port): # tilldela en funktion med (def) för portscan i detta fallet.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socker för (ipv4 och TCP).
    s.settimeout(timeout_seconds) # vi sätter en timeout delay för hinna scanna ordentligt.
    try: # nu startar scriptet och vi försöker köra.
        s.connect((host, port)) # ansluter till hosten och porten.
        return True # om vi får anslutning
    except Exception: # om något går fel så fångar vi up detta och förhindrar programmet att krascha helt oväntat.
        return False # om vi inte får anslutning
    finally: # slutet på scriptet oavsett vad.
        s.close() # nu slutar anslutningen.
# Steg 1: Kontroll av en enskild port (exempel port 80)
if portscan(80): # om portscanen 80 lyckas eller inte
    print("Port 80: öppen") #skrivs ut i terminalen
else: # annars om
    print("Port 80: stängd")# skrivs ut i terminalen 

print("\nSkanning av portarna 1-100 hos scanme.nmap.org/:") # skrivs ut i terminalen

# Steg 2: Skanning av portintervall
open_ports = [] #
for port in range(22, 101): # portarna imellan 22 och 101 som vi vill scanna
    if portscan(port): #
        print(f"{port}: öppen") #
        open_ports.append(port) #
    else:
        print(f"{port}: stängd")
# Steg 3: 
import socket # importera socket från bibiloteket för nätverksanslutningar.

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

