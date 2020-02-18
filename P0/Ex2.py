from Seq0 import *
FOLDER = "../Session-04/"

FILENAME = "U5.txt"
seq = seq_read_fasta(FOLDER + FILENAME)
print("The first 20 bases are:", seq[0:20]) #coger de 1 a 20