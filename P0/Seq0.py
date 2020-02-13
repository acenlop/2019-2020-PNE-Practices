def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    file_contents = Path(FILENAME).read_text()
    f = file_contents.split('\n')
    cadena = ''.join(f[1::])
    print(cadena)