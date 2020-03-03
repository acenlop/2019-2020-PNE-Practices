import socket

IP = "212.128.253.142"
PORT = 8080

#Step 1: Creating the socket:
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Step 2: Bind the socket to the servers IP and PORT
ls.bind((IP, PORT))

#OPTIONAL: for the error
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Step 3: Convert to a listening socket
ls.listen()

print("Server is configured!")

#Step 4: Wait for clients to connect
(cs, client_ip_port) = ls.accept()

msg_raw = cs.recv(2000)
msg = msg_raw.decode()

print(f"Received message: {msg}")

ls.close()