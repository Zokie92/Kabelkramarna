#!/usr/bin/env python3
import socket
import sys


def start_client(host="0.0.0.0", port=8080):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Connecting to {host}:{port}...")
        # Establishing the connection from client to server
        client_socket.connect((host, port))
        print("Connected!")

        # Setting up the "ping" message
        message = "ping"
        print(f"Seding: {message}")
        # Sending "ping" message to server
        client_socket.sendall(message.encode("utf-8"))

        try:
            # Setting timeout to 2 seconds (we don't want to wait forever do we?)
            client_socket.settimeout(2.0)

            # Read 1024 bytes of the response from server
            data = client_socket.recv(1024)

            # Check to see if we've received any response from the server
            if data:
                # Parse that response as UTF-8
                response = data.decode("utf-8")
                print(f"Received from server: {response}")
        # Handle timeout exception (error)
        except socket.timeout:
            print("No response from server (timeout)")
    # Handle exception in general (errors)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    # No matter what, error or not, close the socket.
    finally:
        client_socket.close()
        print("Connection closed")


if __name__ == "__main__":
    start_client()
