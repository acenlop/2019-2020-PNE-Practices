import socket
import termcolor

class Client:
    def __init__(self, ip, port):  # ip changes depending on the pc used
        self.port = int(port)
        self.ip = ip

    def ping(self):
        print("OK")

    def 