from Seq0 import *
FOLDER = "../Session-04/"

print("-----| Exercise 6 |------")

FILENAME = "U5.txt"
gene = "U5"

print("Gene", gene)
seq = seq_read_fasta(FOLDER + FILENAME)

print("Frag:", seq[0:20])
print("Reverse:", seq_reverse(seq[0:20]))