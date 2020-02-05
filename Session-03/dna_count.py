#EXCERCICE 2

user_input = input("Introduce the sequence: ")

letterA = 0
letterC = 0
letterT = 0
letterG = 0
for character in user_input:
    if character == "A":
        letterA = letterA + 1
    elif character == "C":
        letterC = letterC + 1
    elif character == "T":
        letterT = letterT + 1
    elif character == "G":
        letterG = letterG + 1

print("Total length:", len(user_input))
print("The base A appears", letterA, "times")
print("The base C appears", letterC, "times")
print("The base T appears", letterT, "times")
print("The base G appears", letterG, "times")
