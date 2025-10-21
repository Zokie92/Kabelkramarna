


import socket

def check_port(host, port, timeout=3):
    try:
        # Skapa en socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Försök ansluta
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} på {host} är ÖPPEN.")
        else:
            print(f"Port {port} på {host} är STÄNGD eller otillgänglig.")
    except socket.gaierror:
        print("Fel: Ogiltigt värdnamn.")
    except socket.timeout:
        print("Fel: Timeout – värden svarar inte.")
    except Exception as e:
        print(f"Fel: {e}")
    finally:
        sock.close()

# Testa på scanme.nmap.org, port 80
check_port("scanme.nmap.org", 80)
# Testa på localhost, port 9999
check_port("localhost", 9999)
#testa på localhost, port 22
check_port("localhost", 22)
#testa på localhost, port 444
check_port("localhost", 444)
#testa på localhost, port 8080
check_port("localhost", 8080)
#testa på localhost, port 3306
check_port("localhost", 3306)

