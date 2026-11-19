# =================================================================================================
# Contributing Authors:	    <Daniel Kee Tam, >
# Email Addresses:          <daniel.keetam@uky.edu, >
# Date:                     <11/18/2026>
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
SCREENWIDTH = 640
SCREENHEIGHT = 480

# =================================================================================================
# Author:	                Daniel Kee Tam
# Purpose:                  Function to handle client connections and messages (aids in threading)
# Pre:                      An accepted connection with an assigned player number/side
# Post:                     The connection is closed
# =================================================================================================
def handle_client(conn: socket.socket, addr: tuple[str, int], player_num: int, player_side: str) -> None:

    try:
        # send inital message to client to confirm connection and to welcome them to the server
        welcome_message = f"Welcome to the pong server player {player_num}!" f"You are playing on the {player_side} side of the screen.\n"
        conn.sendall(welcome_message.encode("utf-8"))

        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Player {player_num} disconnected. (User address: {addr})")
                break

            message = data.decode("utf-8")
            print(f"Player {player_num}: {message}")

    # handle the case where the player disconnects unexpectedly
    except ConnectionResetError:
        print(f"Player {player_num} disconnected. (User address: {addr})")

    # close the connection when the player disconnects or an error occurs
    finally:
        conn.close()

# =================================================================================================
# Author:	                Daniel Kee Tam
# Purpose:                  Function handle server socket, and to listen for incoming connections
#                           and spawn threads for each client
# Pre:                      None
# Post:                     Server is running and listening for incoming connections, 
#                           and threads are spawned for each client
# =================================================================================================
def main() -> None:
    # we use a TCP socket for the server (reliable and connection-oriented)
    tcp_sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to allow the server to be restarted quickly after it is closed
    tcp_sock_server.bind((HOST, PORT))
    tcp_sock_server.listen()
    print(f"Server is listening on {HOST}:{PORT}")

     # loop to accept two players 
    connections = []  # list to keep track of connections
    for player_num in range(1, 3):
        player_side = "left" if player_num == 1 else "right"

        # accept incoming connection, add it to the list of connections, and spawn a new thread for the player
        conn, addr = tcp_sock_server.accept() 
        connections.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_num, player_side))
        thread.start()
        print (f"Player {player_num} connected. (User address: {addr})")

    # once both players connect, stop listening for new connections
    print("Both players connected.")
    tcp_sock_server.close()

    # handle closing all connections when the server is ready to close (for testing purposes)
    while True:
        serverCloseNum = input("Would you like to close the server? If so write CLOSE: ")
        if serverCloseNum == "CLOSE":
            for conn in connections:  # Assuming conn is the connection object for each client
                conn.sendall(str("CLOSE\n").encode("utf-8"))  # send a message to the clients to close the connection
            break

    # ----------- !!!testing!!! ----------------
    # server only closes when all players leave, ctrl-c stops new players from connecting for 
    # try:
        # connect to the host and port, then listen for incoming connections.
        # also print a message to the console to let the user know the server is listening
    #    tcp_sock_server.bind((HOST, PORT))
    #    tcp_sock_server.listen()
    #    print(f"Server is listening on {HOST}:{PORT}")

        # loop to accept incoming connections and spawn a new thread for each player
    #    while True:
    #        conn, addr = tcp_sock_server.accept()
    #        thread = threading.Thread(target=handle_client, args=(conn, addr))
    #        thread.start()

    # ctrl-c to also close the listening socket
    #except KeyboardInterrupt: 
    #    print("\nClosing the listening socket (No more players allowed).")

    # close the server socket when the server is shutting down
    #finally:
    #   print("Server is shutting down, all players have disconnected.")
    #    tcp_sock_server.close()
     # ----------- !!!testing!!! ----------------

# runs the main function when the file is executed directly
if __name__ == "__main__":
    main()