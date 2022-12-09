import socket
import codecs
from threading import Thread


def listen_for_client(cs, separator):
    while True:
        try:
            msg = cs.recv(1024).decode()
            if not msg:
                # If the message is empty, the client has disconnected
                break

            # Encrypt the message using the rot13 algorithm
            msg = codecs.encode(msg, "rot13")

            msg = msg.replace(separator, ": ")

            # Loop through all connected clients and send the message to each of them
            for client_socket in client_sockets:
                client_socket.send(msg.encode())
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            # When the loop ends, remove the client socket from the list of connected clients
            client_sockets.remove(cs)


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5184
separator_token = "<SEP>"

client_sockets = set()

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        try:
            # Accept incoming connections
            client_socket, client_address = s.accept()
        except Exception as e:
            print(f"[!] Error: {e}")
        else:
            # Add the client socket to the list of connected clients
            client_sockets.add(client_socket)

            # Start a new thread to listen for messages from this client
            t = Thread(target=listen_for_client, args=(client_socket, separator_token))
            t.daemon = True
            t.start()
