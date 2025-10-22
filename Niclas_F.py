import socket # importerat från socket-biblioteket för nätverksanslutningar.

host = "scanme.nmap.org" # hostservern vi försöker ansluta till
port = range(1, 101) # portnumret som testas - (80 - HTTP) 
timeout_seconds = 1.0 # hur länge socket försöker ansluta innan den ger upp.

def portscan(port): # definerar en funktion "kollar upp åt mig"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # använder ipv4 och TCP för en (pålitlig) överföring
    s.settimeout(timeout_seconds) # sätter hur länge socket ska vänta på operation som connect.
    try: # här börjas koden att köras under try: 
        s.connect((host, 80)) #försöker öppna en TCP anslutning imot hosten och porten
        return True # om connect lyckas så skickas svaret tillbaka som "true/ja, porten är öppen"
    except Exception: # fångar alla fel/undantag som man uppstå under när vi försöker ansluta. 
        return False # om ett fel inträffade så skickas det tillbaka som "false/nej, porten är stängd"
    finally: # körs färdigt oavsett vad som händer.
        s.close() #stänger anslutningen vi öppnade mot port 80

if portscan(port): # om porten är öppen
    print("öppen") # skriv öppen i terminalen
else: # annars om
    print("stängd") # skriv stängd i terminalen

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

for port in range(1, 101):
    if portscan(port):
        print(f"{port}: öppen")
    else:
        print(f"{port}: stängd")


    
