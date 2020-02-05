#EXERCICE 3
letterA = 0
letterC = 0
letterT = 0
letterG = 0
counter = 0


with open(dna.txt, "r") as f:
    for character in dna.txt:
        counter = counter + 1
        if character == "A":
            letterA = letterA + 1
        elif character == "C":
            letterC = letterC + 1
        elif character == "T":
            letterT = letterT + 1
        elif character == "G":
            letterG = letterG + 1


print("Total number of bases:", counter)
print("The base A appears", letterA, "times")
print("The base C appears", letterC, "times")
print("The base T appears", letterT, "times")
print("The base G appears", letterG, "times")