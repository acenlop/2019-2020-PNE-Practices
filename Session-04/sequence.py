from pathlib import Path

# -- Constant with the new of the file to open
FILENAME = "ADA.txt"

# -- Open and read the file
file_contents = Path(FILENAME).read_text().split('\n')[1:]
cadena = ''.join(file_contents)

# -- Print the contents on the console
print(len(cadena))
