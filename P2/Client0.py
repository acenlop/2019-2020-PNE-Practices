import socket
import termcolor

class Client:
    def __init__(self, ip, port):  # ip changes depending on the pc used
        self.port = int(port)
        self.ip = ip

    def ping(self):
        print("OK")

    def __str__(self):
        return(f"Connection to SERVER at {self.ip}, PORT: {self.port}")