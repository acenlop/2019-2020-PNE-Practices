from Seq0 import *
FOLDER = "../Session-04/"

filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]
genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
base = ["A", "C", "T", "G"]

print("-----| Exercise 4 |------")

counter = 0
for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print("Gene", genes[counter])
    counter += 1
    seq_count_base(seq,base)