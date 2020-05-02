import http.client
import json
import termcolor as tc
from Seq1 import Seq

def seq_information(bases):
    seq_info = Seq(bases)  # Use de Seq() class here
    min_count = 0
    most_frecuent_base = ""

    for base, count in seq_info.count().items():
        # .items() returns the base and the count for each base , then we print
        percentage = round(count / seq_info.len() * 100, 2)  # round(,2) only shows to decimal numbers
        tc.cprint(f"{base}:", 'blue', end=' ')
        print(f" {count} ({percentage}%)")

        # here we look for the most frecuent base
        if min_count < count:
            min_count = count
            most_frecuent_base = base

GENES = dict(FRAT1='ENSG00000165879',
            ADA='ENSG00000196839',
            FXN='ENSG00000165060',
            RNU6_269P='ENSG00000212379',
            MIR633='ENSG00000207552',
            TTTY4C='ENSG00000228296',
            RBMY2YP='ENSG00000227633',
            FGFR3='ENSG00000068078',
            KDR='ENSG00000128052',
            ANK2='ENSG000000145362')

for gene in GENES:
    SERVER = 'rest.ensembl.org'
    ENDPOINT = '/sequence/id/' + GENES[gene]
    PARAMS = '?content-type=application/json'
    REQ = ENDPOINT + PARAMS
    URL = SERVER + REQ

    print()
    print(f"Server: {SERVER}")
    print(f"URL:{URL}")

    #Connect with the server
    conn = http.client.HTTPConecction(SERVER)

    # Print the connection information
    tc.cprint(f"\nConnecting to server: {server}", 'blue')
    tc.cprint(f"URL : {URL}", 'blue')

    method = 'GET'   #bc we only use the get method

    try:
        conn.request(method, REQ)
    except ConnectionRefusedError:  # If the connection fails we print an error message
        print("ERROR! Cannot connect to the Server")
        exit()

    # response and status
    response = conn.getresponse()
    # .getresponse() method that returns the reponse information from the server

    #Print the status line -- OK
    tc.cprint(f"Response received!: {response.status} {response.reason}\n", 'blue')

    data = response.read().decode("utf-8")  # It is necessary to decode the information
    # read JSON
    info_api = json.loads(data)  # loads(). is a method from JSON library  (read JSON response)

    # Obtain information . We use 'seq' and 'desc' as keys
    sequence = info_api['seq']
    description = info_api['desc']

    # PRINTING info
    tc.cprint("Gene: ", 'green', end="")
    print(gene)

    tc.cprint("Description: ", 'green', end="")
    print(description)

    tc.cprint("Total length: ", 'green', end="")    #stored function in seq_information
    print(len(seq_info))

    tc.print("Most frequent Base: ", 'green', end="")
    print(most_frecuent_base)