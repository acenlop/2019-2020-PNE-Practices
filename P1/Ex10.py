from Seq1 import Seq

#---MAIN PROGRAM

print("-----| Practice 1, Exercise 10 |------")

s = Seq("")

FOLDER = "../Session-04/"
gene = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
txt = ".txt"

for element in gene:
    counter = 0
    base = ''
    s = s.read_fasta(FOLDER + element + txt)
    for i, t in (s.count()).items():
        while t > counter:
            counter = t
            base = i
    print("Gene ", element, " : Most frequent base:", base)