

## Help ## This script attempts to connect to a specific port on a remote server (scanme.nmap.org) to check if the port is open or closed.
"""
Mattias Experiment Script
Student: Mattias E
Start date: 2025-10-22
"""     
"""
**Vanliga portar:**
- Port 80: HTTP (webbplatser)
- Port 443: HTTPS (säkra webbplatser)
- Port 22: SSH (säker fjärråtkomst)
- Port 21: FTP (filöverföring)
**Mål:** Skapa ett program som kontrollerar om EN specifik port är öppen på EN målvärd.
**Vad du behöver ta reda på:**
1. Hur man importerar och använder Pythons `socket`-bibliotek
2. Hur man skapar en socket-anslutning till en specifik IP-adress och port
3. Hur man avgör om anslutningen lyckades eller misslyckades
4. Hur man hanterar att anslutningen stängs ordentligt
**Testa din kod på:**
- `scanme.nmap.org`
- Port 80
**Frågor att diskutera i din grupp:**
- Vad händer när du försöker ansluta till en stängd port?
- Vilket undantag/fel ger Python dig?
- Varför behöver vi stänga socketen efter testning?
"""

import socket  # Importing the socket library to handle network connections 
target_port = [22, 21, 80, 443]  # List of common ports to check
def check_port(host, port): 
    """Funktion för att kontrollera om en specifik port är öppen på en given värd."""
    try:
        # Skapa en socket-objekt
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Skapar en TCP/IP-socket
        sock.settimeout(1)  # Sätt en timeout för anslutningen
        result = sock.connect_ex((host, port))  # Försök att ansluta till värden på den angivna porten
        if result == 0:
            print(f"Port {port} är ÖPPEN på {host}.") # Om anslutningen lyckas
        else: # Om anslutningen misslyckas
            print(f"Port {port} är STÄNGD på {host}.") # Om anslutningen misslyckas
    except socket.error as e: # Hantera socket-fel
        print(f"Ett fel uppstod: {e}") # Skriv ut felmeddelandet
    finally: 
        sock.close()  # Stäng socketen efter testning
if __name__ == "__main__": # Huvudprogrammet
    target_host = "scanme.nmap.org"  # Målvärd att skanna
    for port in target_port: 
        check_port(target_host, port)  # Kontrollera varje port i listan








