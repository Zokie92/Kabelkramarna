
#!/usr/bin/env python3
"""
Network Scanner Project
Students: [Mattias E, Kaj, Ludde JM, Mattias L, Niclas F]
Start date: [2025-10-20]
"""
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
GREEN = "\033[32m"
BLUE    = "\033[34m"

width = 60

DESCRIPTION = """Kabelkramarna network scanner — simple, educational port/network scanner.

Scans local networks to discover hosts and open ports using Python sockets.
Designed for learning socket programming, error handling, and performance tradeoffs.
Use only on networks and hosts you own or have explicit permission to scan.
"""

def colored_banner():
    print() 
    print(BOLD + GREEN + "=" * width + RESET)
    print(BOLD + BLUE + "  ##  Kabelkramarnas Fancy Port Scanner ## ".center(width) + RESET)
    print(BOLD + GREEN + "=" * width + RESET)
    print() 

def print_colored_description():
    print()
    print(BOLD + MAGENTA + "=== Kabelkramarna network scanner ===" + RESET)
    print(CYAN + DESCRIPTION.strip() + RESET)
    print(BOLD + YELLOW + "Note:" + RESET + " " + GREEN + "Only scan systems you own or have permission to scan." + RESET)
    print()


########### STEG 1 ###########

import socket
import sys

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

