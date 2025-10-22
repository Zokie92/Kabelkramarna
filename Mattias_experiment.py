
### What im i doing? ####


import socket

test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    test_socket.connect(("scanme.nmap.org", 22))
    print(f"Port is open!")
except Exception as e:
    print(f"Port is closed or unreachable: {e}")
finally:
    test_socket.close()

