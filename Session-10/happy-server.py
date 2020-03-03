import socket

IP = "212.128.253.142"
PORT = 8080

#Step 1: Creating the socket:
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#OPTIONAL: for the error
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Step 2: Bind the socket to the servers IP and PORT
ls.bind((IP, PORT))

#Step 3: Convert to a listening socket
ls.listen()

print("Server is configured!")

while True:
    try:
        #Step 4: Wait for clients to connect
        (cs, client_ip_port) = ls.accept()

    except KeyboardInterrupt:
        print("Server is done!")
        ls.close()
        exit()

    else:
        #Step 5: Receiving info from the client
        msg_raw = cs.recv(2000)
        msg = msg_raw.decode()

        print(f"Received message: {msg}")

        #Step 6: Send a response message from the client
        response = "Hi! I am a happy server."
        cs.send(response.encode())

        cs.close()
