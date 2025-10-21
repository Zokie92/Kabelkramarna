#!/usr/bin/env python3
import socket
import sys


def start_server(host="0.0.0.0", port=8080):
    # Create a TCP/IP socket of IPv4 family and SOCK_STREAM type
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # To avoid getting the "Address already in use" error
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Thus far we've only set the sockets up. Now we're commiting aka binding
    server_socket.bind((host, port))

    # Listen to the address and port defined above.
    # Now we're essentially executing
    server_socket.listen()

    try:
        while True:
            print("Waiting for a connection...")
            # Wait and accept new connections
            client_socket, client_address = server_socket.accept()

            # Only when a new connection have been accepted
            try:
                print(f"Connection from {client_address}")
                # Receive input from client. Read 1024 bytes (anything exceeding is ignored)
                data = client_socket.recv(1024)

                if data:
                    # Decode the message that is in byte form so we can easily work with it
                    response = data.decode("utf-8")
                    print(f"Received from client: {response}")
                    # Since it's decoded from byte to UTF-8 we can now just check for "ping"
                    if response == "ping":
                        # If we've received "ping" from the client, respond with "pong"
                        client_socket.sendall(b"pong")
            finally:
                # Always close the client socket connection that was established above
                client_socket.close()
    except KeyboardInterrupt:
        # If we receive "Ctrl + C" and the program is forced to close, handle that exception
        print("Good bye!")
        sys.exit(1)
    except Exception as e:
        # Otherwise, handle any other exception
        print("Something went wrong!\nError: {e}")
    finally:
        # Always close the server socket connection that was established above
        server_socket.close()


if __name__ == "__main__":
    start_server()
