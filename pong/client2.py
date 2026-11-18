import socket

HOST = "10.6.39.125"
PORT = 5001

tcp_sock_client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_sock_client2.connect((HOST, PORT))

while (True):
    message = input("Enter message for server (/quit to stop): ")

    if message.lower() == "/quit":
        break

    tcp_sock_client2.sendall(message.encode())
    print("Message from client2 sent to server" )

tcp_sock_client2.close()



