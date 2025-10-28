import socket
import sys

print("Use this tool only on systems you own or are authorized to test.\nUnauthorized scanning is prohibited and may be illegal.\nFor safe test targets, use hosts like scanme.nmap.org.")

target = input("Choose a target to scan using URL or IP-adress: ")
print(f"scanning target {target} in port range 20 to 80")


for port in range(20, 81):
    scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scan_sock.settimeout(1)

    connection = scan_sock.connect_ex((target, port))
    if connection == 0:
        print(f"port {port} is open")
    else:
        print(f"port {port} is closed")
    
    scan_sock.close()
print("scanning is completed...")
