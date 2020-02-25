from Seq1 import Seq

#---MAIN PROGRAM

print("-----| Practice 1, Exercise 9 |------")

FOLDER = "../Session-04/"
FILENAME = FOLDER + "U5.txt"

s = Seq("")
s= s.read_fasta(FILENAME)

print("Sequence", ": (Length:", s.len() ,")", s)
print(f"Bases: {s.count()}")
print(f"Reverse: {s.reverse()}")
print(f"Comp: {s.complement()}")

