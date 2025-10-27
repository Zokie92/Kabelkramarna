
#!/usr/bin/env python3
"""
Network Scanner Project
Students: [Mattias E, Kaj, Ludde JM, Mattias L, Niclas F]
Start date: [2025-10-20]
"""

import socket
import time
import sys


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
GREEN = "\033[32m"
BLUE    = "\033[34m"

width = 60

def colored_banner():
    print() 
    print(BOLD + CYAN + "=" * width + RESET)
    print() 
    print("  ##  Kabelkramarnas Fancy Port Scanner  ## ".center(width) + RESET)
    print() 
    print(BOLD + CYAN + "=" * width + RESET)
    print()  

colored_banner()

########### STEG 1 ###########

import socket
import sys

print("Scanning target: scanme.nmap.org...")
port_scan = int(input("Select a port to scan: "))
try:
    socket.setdefaulttimeout(2)

    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        test_socket.connect(("scanme.nmap.org", port_scan))
        print("Port is open.")
    except Exception as e:
        print(f"Port is closed or unreachable: {e}")
    finally:
        test_socket.close()
except ValueError:
    print("Invalid entry. Please select a numerical value.")

########### STEG 2 ###########

