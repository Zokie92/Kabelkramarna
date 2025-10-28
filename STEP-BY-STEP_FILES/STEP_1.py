import socket
import sys

print("Use this tool only on systems you own or are authorized to test.\nUnauthorized scanning is prohibited and may be illegal.\nFor safe test targets, use hosts like scanme.nmap.org.")

target = input("Choose a target to scan using URL or IP-adress: ")
scan_port = int(input("Select a port number to scan: "))

print(f"\nScanning port {scan_port} of target {target}...")

try:
    socket.setdefaulttimeout(2)
    scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        scan_sock.connect((target, scan_port))
        print("Port is open.")
    except Exception as e:
        print(f"Port is closed or unreachable: {e}")
    finally:
        scan_sock.close()
except ValueError:
    print("Please enter a valid positive number.")
