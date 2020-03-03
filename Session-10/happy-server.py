import socket

IP = "212.128.240.50"
PORT = 8080

#Step 1: Creating the socket:
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Step 2: Bind the socket to the servers IP and PORT
ls.bind((IP, PORT))

#Step 3: Convert to a listening socket
ls.listen()

print("Server is configured!")

ls.close()