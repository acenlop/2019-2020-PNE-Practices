from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 6

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.253.142"
PORT = 8080
c = Client(IP, PORT)   #unir ip y port
print(c)

FOLDER = "../Session-04/"
file_name = FOLDER + "FRAT1.txt"
s = Seq("")
s = s.read_fasta(file_name)
s = str(s)