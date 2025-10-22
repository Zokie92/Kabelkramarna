import socket

host = "scanme.nmap.org"
port = 80
timeout_seconds = 1.0

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

if portscan(port):
    print("öppen")
else: 
    print("stängd")

    