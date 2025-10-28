
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
    print("Invalid entry. Please select a numerical value.")
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

############# V3 ################

"""

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

  
### Denna funktion ska försöka läsa en banner från målets port och avgöra tjänsten. Retur: (banner:text, guessed_service) - banner_text kan vara '' om data inte hittats.
   
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

    print(f"\n---- SCAN INITIATED ----\n \nScanning target: {target}\nPort range: {start} to {end}.\nTimeout set to: {timeout}\n \nScanning...\n")

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
    scan_ports_with_service(target_host, start, end, timeout = 1)

"""





#### Port-Scanner som även identifierar tjänster för öppna portar

import socket
import time
from datetime import datetime

def id_protocol(target: str, port: int, timeout: float = 2.0) -> (str, str):
    """"
    Denna funktion ska försöka läsa en banner från målets port och avgöra tjänsten.
    Retur: (banner:text, guessed_service) - banner_text kan vara '' om data inte hittats.
    """
    scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scan_sock.settimeout(timeout)

    try:
        result = scan_sock.connect_ex((target, port))
        if result != 0:
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

        # Enkel heuristik för gissning
        if "ssh-" in banner_lower or port == 22:
            guessed = "SSH"
        elif "http/" in banner_lower or "server:" in banner_lower or port in (80, 8080, 8000):
            guessed = "HTTP"
        elif banner_lower.startswith("220") or port == 25:
            guessed = "SMTP"
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

        return (banner, guessed)

    finally:
        scan_sock.close()


def scan_ports_with_service(target: str, start: int, end: int, timeout: float = 1.0, presentation: str = "all"):
    """
    Skannar portintervallet användaren valt och försöker identifiera tjänst för öppna portar.
    Returnerar lista av resultatrader.
    """
    header = f"---- SCAN INITIATED ----\nScanning target: {target}\nPort range: {start} to {end}\nTimeout: {timeout}s\nStart time: {datetime.now().isoformat()}\n"
    print("\n" + header + "\nScanning...\n")
    results = [header]

    for port in range(start, end + 1):
        scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan_sock.settimeout(timeout)
        try:
            res = scan_sock.connect_ex((target, port))
            if res == 0:
                banner, service = id_protocol(target, port, timeout=2.0)
                if banner:
                    line = f"Port {port}: OPEN - {service} - Banner: {banner.splitlines()[0]}"
                else:
                    line = f"Port {port}: OPEN - {service} - No banner received."
                print(line)
                results.append(line)
            else:
                line = f"Port {port}: CLOSED"
                if presentation == "all":
                    print(line)
                    results.append(line)
        except Exception as e:
            line = f"Port {port}: ERROR - {e}"
            print(line)
            results.append(line)
        finally:
            scan_sock.close()

    footer = f"\nScan complete. End time: {datetime.now().isoformat()}\n"
    print(footer)
    results.append(footer)
    return results

def save_results_to_file(lines, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portscan_{timestamp}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"Results saved to: {filename}")
    except Exception as e:
        print(f"Could not save file: {e}")

def get_int_input(prompt, default=None, minval=0, maxval=65535):
    """
    Hjälpfunktion för att läsa integer från input och validera intervallet.
    """
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            iv = int(val)
            if iv < minval or iv > maxval:
                print(f"Enter a number between {minval} and {maxval}.")
                continue
            return iv
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    print(" ")
    print("##########################################################")
    print("###### Welcome to Kabelkramarnas fancy Port-Scanner ######")
    print("##########################################################")
    print(" ")
    print("We do not take responsibility for this scanner being used for anything shady.")
    print("Only scan hosts you are the admin of or specifically have permission to scan.")
    print("For scanning remote targets please use scanme.nmap.org or similar URLs used for testing.")
    print(" ")

    try:
        while True:
            target_host = input("Select a target host to scan using either URL or IP-adress: ")
            start = get_int_input("Define port scan range from port (enter port number): ")
            end = get_int_input("To port: ")
            if end < start:
                print("End port must be a higher number than start port. Please try again.")
                continue

            presentation = input("Type ALL to show result of every port or OPEN to only show open ports: ").lower().strip()
            if presentation not in ("all", "open"):
                print("Invalid presentation choice, defaulting to ALL.")
                presentation = "all"

            timeout = input("Set a timeout for each port in seconds. Use '.' for a decimal (press Enter for default 1s): ").strip()
            try:
                timeout_val = float(timeout) if timeout else 1.0
            except ValueError:
                timeout_val = 1.0

            # Kör skanningen och samla resultatrader
            result_lines = scan_ports_with_service(target_host, start, end, timeout=timeout_val, presentation=presentation)

            # Alternativ för att logga resultatet i en text-fil
            save_choice = input("Would you like to save the results to a file? (y/n): ").lower().strip()
            if save_choice == "y":
                fname = input("Enter filename (or press Enter to auto-generate): ").strip()
                save_results_to_file(result_lines, fname if fname else None)

            # Fråga om ny skanning
            again = input("Would you like to scan a new range of ports? (y/n): ").lower().strip()
            if again != "y":
                print("Exiting program.\nThanks for doing some shady stuff with us.\nRemember to scan responsibly!")
                break

    except KeyboardInterrupt:
        print("\nUser interrupted. Shutting down.")