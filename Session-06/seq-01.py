class Seq:
    """A class for representing sequence objects"""
    def __init__(self, strbases):
        self.strbases = strbases
        print("New sequence created!")

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)

class Gene(Seq):
    pass



#Main program

s1 = Seq("AACGTC")      #OBJECT
g = Gene("ACTAGAT")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {g}")

len1 = s1.len()
print(f"The length of the sequence 1 is {len1}")
print(f"The length of the gene is {g.len()}")