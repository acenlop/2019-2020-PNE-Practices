from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 7

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP= "212.128.253.142"
PORT_1 = 8080
PORT_2 = 8081

c_1 = Client(IP, PORT_1)   #unir ip y port juntos
print(c_1)

c_2 = Client(IP, PORT_2)
print(c_2)

FOLDER = "../Session-04/"
file_name = FOLDER + "FRAT1.txt"
s = Seq("")
s = s.read_fasta(file_name)
s = str(s)
