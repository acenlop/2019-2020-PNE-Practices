from Seq1 import Seq

#---MAIN PROGRAM

print("-----| Practice 1, Exercise 7 |------")

# -- Create sequences:
s1 = Seq("")
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")


print("Sequence", 1, ": (Length:", s1.len() ,")", s1)
print(f"Bases: {s1.count()}")
print(f"Reverse: {s1.reverse()}")

print("Sequence", 2, ": (Length:", s2.len() ,")", s2)
print(f"Bases: {s2.count()}")
print(f"Reverse: {s2.reverse()}")

print("Sequence", 3, ": (Length:", s3.len() ,")", s3)
print(f"Bases: {s3.count()}")
print(f"Reverse: {s3.reverse()}")