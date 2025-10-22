import socket

test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    test_socket.connect(("scanme.nmap.org", 80))
    print("Port is open!")
except:
    print("Port is closed.")
finally:
    test_socket.close()
