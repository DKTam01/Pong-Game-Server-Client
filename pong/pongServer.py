# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
from xmlrpc import server

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

HOST = "0.0.0.0"
PORT = 5001



# Contributing Authors:	    Daniel Keetam
# Email Addresses:          danielkeetam@uky.edu
# Date:                     11/15/2026
# Purpose:                  Function to handle client connections and messages (aids in threading)
def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:

    try:
        print (f"Connected by {addr}")
        conn.sendall("Welcome to the pong server!".encode("utf-8"))

        #display messages received from client    
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                break
            message = data.decode("utf-8")
            print(f"Received message from {addr}: {message}")

    except ConnectionResetError:
        print(f"Client {addr} disconnected")

    finally:
        conn.close()


# Contributing Authors:	    Daniel Keetam
# Email Addresses:          danielkeetam@uky.edu
# Date:                     11/15/2026
# Purpose:                  Function handle server socket, and to listen for 
#                           incoming connections and spawn threads for each client

def main() -> None:
    #We use a TCP socket for the server (reliable and connection-oriented)
    tcp_sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Server only closes when all clients leave, ctrl-c stops new clients from connecting
    try:
        tcp_sock_server.bind((HOST, PORT))
        tcp_sock_server.listen()

        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            conn, addr = tcp_sock_server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

    except KeyboardInterrupt: #ctrl-c to also close a listening socket
        print("\nClosing the listening socket (No more connections allowed).")

    finally:
        print("Server is shutting down, all clients have disconnected.")
        tcp_sock_server.close()


#runs the main function when the file is executed directly
if __name__ == "__main__":
    main()