from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.253.142"
PORT = 8080
c = Client(IP, PORT)   #unir ip y port
print(c)

# --  message to and from the server
c.debug_talk("Sending U5 Gene to the server...") #send first message

FOLDER = "../Session-04/"
file_name = FOLDER + "U5.txt"
s = Seq("")
s = s.read_fasta(file_name)
s = str(s)

c.debug_talk(s) #send the gene to the server