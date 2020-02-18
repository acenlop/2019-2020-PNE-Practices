from pathlib import Path

def seq_ping():
    print("OK")

def seq_read_fasta(FILENAME):
    file_contents = Path(FILENAME).read_text()
    f = file_contents.split('\n')
    cadena = ''.join(f[1::])
    return cadena

def seq_len(seq):
    return len(seq)

def seq_count_base(seq,base):
    letterA = 0
    letterC = 0
    letterT = 0
    letterG = 0
    for character in seq:
        if character == "A":
            letterA = letterA + 1
        elif character == "C":
            letterC = letterC + 1
        elif character == "T":
            letterT = letterT + 1
        elif character == "G":
            letterG = letterG + 1

    print("A:", letterA)
    print("C:", letterC)
    print("T:", letterT)
    print("G:", letterG)

