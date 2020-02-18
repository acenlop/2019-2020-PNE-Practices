from Seq0 import *
FOLDER = "../Session-04/"

filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]
genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

print("-----| Exercise 3 |------")
counter = 0
for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print("Gene", genes[counter], "---> Length:", seq_len(seq))
    counter += 1