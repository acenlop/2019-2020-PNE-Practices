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