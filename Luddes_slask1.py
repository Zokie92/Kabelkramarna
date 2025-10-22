import socket

def check_port(host, port, timeout=3):
    open_ports = []
    closed_ports = []

    try:
        # Skapa en socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Försök ansluta
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} på {host} är ÖPPEN.")
            open_ports.append(port)
        else:
            print(f"Port {port} på {host} är STÄNGD eller otillgänglig.")
            closed_ports.append(port)
    except socket.gaierror:
        print("Fel: Ogiltigt värdnamn.")
    except socket.timeout:
        print("Fel: Timeout – värden svarar inte.")
        closed_ports.append(port)
    except Exception as e:
        print(f"Fel: {e}")
        closed_ports.append(port)
    finally:
        sock.close()

    return open_ports, closed_ports


    

# Testa på scanme.nmap.org, port 80

check_port("scanme.nmap.org", 80)
# Testa på localhost, port 9999
check_port("scanme.nmap.org", 9999)
#testa på localhost, port 22
check_port("scanme.nmap.org", 22)
#testa på localhost, port 444
check_port("scanme.nmap.org", 444)
#testa på localhost, port 8080
check_port("scanme.nmap.org", 8080)
#testa på localhost, port 3306
check_port("scanme.nmap.org", 3306)
#testa på localhost, port 5432
check_port("scanme.nmap.org", 5432)




