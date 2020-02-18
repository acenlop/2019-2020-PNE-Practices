from Seq0 import *
FOLDER = "../Session-04/"

filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]
genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
d = {"A": 0, "C": 0, "T": 0, "G": 0}

print("-----| Exercise 5 |------")

counter = 0
for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print(d['A'], d['T'], d['C'], d['G'])
    
