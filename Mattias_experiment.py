
### What im i doing? ####


import socket # Importerar socket-biblioteket för nätverkskommunikation

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Skapar en TCP/IP-socket
socket.setdefaulttimeout(2) # Sätter en standard timeout på 2 sekunder för socket operationer   
## Försöker ansluta till en specifik port på scanme.nmap.org


try: ## Försöker ansluta
    c_socket.connect(("scanme.nmap.org", 22)) # Försöker ansluta till scanme.nmap.org på port 22
    print(f"Port is open!") # Om anslutningen lyckas, porten är öppen
except Exception as e: # Om ett undantag inträffar
    print(f"Port is closed or unreachable: {e}") # Fångar eventuella undantag och skriver ut felmeddelande
finally: # Slutligen
    c_socket.close() # Stänger socketen efter användning

if __name__ == "__main__":
    pass # 

### Mattias experiment ###
print("Detta funkar förhoppningsvis.")



 

