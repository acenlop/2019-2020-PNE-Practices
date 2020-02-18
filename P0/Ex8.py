from Seq0 import *
import collections
FOLDER = "../Session-04/"

filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]
gene = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
base = ["A", "C", "T", "G"]

print("-----| Exercise 8 |------")

counter = 0
for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print("Gene", gene[counter], "Most frequent base:", collections.Counter(seq).most_common(1)[0])
    counter += 1