

# Steg ett ## This script attempts to connect to a specific port on a remote server (scanme.nmap.org) to check if the port is open or closed.
# Steg två: Utöka koden för att kolla flera portar (22-100)
# Steg tre: Försök hämta banner från öppna portar
### Steg 3: Tjänsteidentifiering (60 minuter)
#**Mål:** När du hittar en öppen port, försök identifiera vilken TJÄNST som körs där.
#**Utmaning:** Olika tjänster svarar olika när du ansluter till dem. Vissa tjänster skickar en "banner" som identifierar dem.
#**Vad du behöver undersöka:**
#1. Hur man tar emot data från en socket efter anslutning
#2. Hur tjänster identifierar sig själva (banner grabbing)
#3. Hur man hanterar tjänster som inte skickar data omedelbart
#**Skapa en funktion som:**
#- Ansluter till en öppen port
#- Försöker ta emot bannern/hälsningen
#- Identifierar vanliga tjänster (HTTP, SSH, FTP, etc.)
#- OBS: Räcker att identifiera en tjänst
#-**Tips:** Vissa tjänster behöver att du skickar data först innan de svarar!

#### Port-Scanner som även identifierar tjänster för öppna portar
"""
import socket
import time
import sys


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
GREEN = "\033[32m"
BLUE    = "\033[34m"

width = 60

def colored_banner():
    print() 
    print(BOLD + GREEN + "=" * width + RESET)
    print(BOLD + BLUE + "  ##  Kabelkramarnas Fancy Port Scanner ## ".center(width) + RESET)
    print(BOLD + GREEN + "=" * width + RESET)
    print()  

colored_banner()

print(CYAN + "Here we could use an input for you to decide what target host to scan..." + RESET)
print(CYAN + "But for obvious legal reasons our variable target_host is set to scanme.nmap.org" + RESET)
print()

def check_for_exit(s: str):
   #Exits the program if the user typed an exit command.
    if s.lower() in ("end", "exit", "quit"):
        print("Exiting the program — goodbye and thank your using our scanner tool!")
        sys.exit(0)
    return False

# Loop until the user enters a valid integer for the start port
while True:
    raw = input("Define port scan range from port (Enter port number)---> ").strip()
    check_for_exit(raw)  # exit if the user typed end/exit/quit
    try:
        start = int(raw)
        break
    except ValueError:
        print("Error: Please enter a valid port number (not text). Example: 80. Please try again...")

# Loop until the user enters a valid integer for the end port that is >= start
while True:
    raw = input("To port: ").strip()
    check_for_exit(raw)  # exit if the user typed end/exit/quit
    try:
        ended = int(raw)
        if ended < start:
            print("Error: 'To port' needs to be bigger or equal to the start port. Please try again...")
            continue
        break
    except ValueError:
        print("Error: You did not type a valid port number (not text). Example: 443. Please try again..."
              "\nNOTE: It needs to be bigger or equal to the start port you chose.")
        

presentation = input("Type ALL to show result of every port or OPEN to only show open ports: ").lower().strip()


def id_protocol(target: str, port: int, timeout: float = 2.0) -> (str, str):
    
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

    for port in range(start, end + 1):
        scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan_sock.settimeout(timeout)
        
        ### PRINTA BARA ÖPPNA PORTAR
        if presentation == "open":
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
    
    print("Scan complete...\nThank you for using Kabelkramarnas fancy Port-Scanner!")

if __name__ == "__main__":
    target_host = "scanme.nmap.org"
    scan_ports_with_service(target_host, start, ended, timeout = 1.0)
"""





# Introduktion.
print("Good day\nMy name is Mattias\nI'm here to calculate everything by two, try me!!! ") # Introducerar programmet och dess syfte.
print("Type 'end' or 'exit' to stop the program.\n") #Ger användaren

# En while-loop som körs tills vi använder 'break' som avslutar loopen (nämns även nedan)
while True:
    # Tar in text (input) från användaren, alltså det användaren skriver in.
    user = input("Enter a number:  ") # Ber användaren att skriva in ett tal med hjälp av (Input)

    # En if som kollar om användaren vill avsluta programmet med 'end' eller 'exit'. 
    if user.lower() in ["end", "exit"]: # Kollar om användarens input är 'end' eller 'exit', oavsett om det är stora eller små bokstäver.
        print("Goodbye And thank you for playing with me, see you later!") # Skrivs ut när användaren vill avsluta programmet.
        break  # Avslutar loopen 

    # Try: används för att fånga upp fel.
    try: # Försök att köra koden inuti detta block.
        # Omvandlar användarens input till ett flyttal (float) för att
        # omvandla tal med decimaler.
        number = float(user)

        # En for loop som körs 1 gång (Behövs denna loopen egentligen, fråga Johan?)
        for i in range(1): # Loopen körs bara en gång.
            # Multiplicerar användarens tal med 2
            result = number * 2
            # Skriver ut resultatet med hjälp av en f-sträng
            print(f"Your number {number} multiplied by 2 is {result:.2f}\n") #skriver ut resultatet med 2 decimaler.

    # Om användaren skriver något som inte går att göra till ett tal.
    except ValueError: 
        print("Enter a valid number, please!") #Skrivs ut om användaren inte skriver in ett giltigt tal.

    # Else körs bara om allt i try-blocket lyckades.
    else:
        print("That worked just fine!") #Skrivs ut om allt gick bra.
