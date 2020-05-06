import http.server
import socketserver
import termcolor
from pathlib import Path
from Seq1 import Seq
import json

# Define the Server's port, IP and BASES
PORT = 8080
IP = "127.0.0.1"
BASES = ["A", "T","G","C"]

#URL w/o the ENDPOINT (different for each option)
SERVER = 'rest.ensembl.org'
PARAMS = '?content-type=application/json'
URL = SERVER + PARAMS


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line in green
        termcolor.cprint(self.requestline, 'green')

        req_line = self.requestline.split(' ')  #splits request line by spaces

        list_resource = (req_line[1]).split('?')  #First we get the first request line and path, then the arguments after the ? symbol
        first_resource = list_resource[0]      #sets the first argument

        contents = Path('Error.html').read_text()    #in case of error
        self.send_response(404)

        #-----------------------------MAIN PROGRAM------------------------------


        try:
            if first_resource == "/":      #Returns the Main page for accessing all the other services
                # Read the file
                contents = Path('index.html').read_text()     #contents in index.html
                self.send_response(200)


            # ------ListSpecies

            elif first_resource == "/listSpecies":     #list of the names of species stored in the ensembl
                contents = f"""<!DOCTYPE html>
                                <html lang = "en">
                                <head>
                                 <meta charset = "utf-8" >
                                 <title>List of species in the browser</title >
                                </head >
                                <body>
                                <p>The total number of species in ensembl is: 267</p>"""


                get_value = list_resource[1]    #go to the first argument
                seq_n = get_value.split('?')    #splits the argument by ?
                seq_name, index = seq_n[0].split("=")    #then splits by the =
                index = int(index)
                contents += f"""<p>The number of species you selected are: {index} </p>""" #prints the total number of species selected

                ENDPOINT = 'info/species'            #we add ENDPOINT to URL
                REQUEST = ENDPOINT + PARAMS

                # Connect with the server
                conn = http.client.HTTPConecction(SERVER)

                try:
                    conn.request('GET', REQUEST)       #connection request
                except ConnectionRefusedError:           # If the connection fails we print an error message
                    print("ERROR! Cannot connect to the Server")
                    exit()

                # read response message from server
                response = conn.getresponse()        # .getresponse() method returns the response information from the server
                data = response.read().decode("utf-8")  # It is necessary to decode the information

                limit_list = []               #list to store all species within limit
                data = json.loads(data)       # loads(). is a method from JSON library  (read JSON response)
                limit = data["species"]
                if index > len(limit):         #in case there are more species than the limit
                    contents = f"""<!DOCTYPE html>
                                            <html lang = "en">
                                            <head>
                                             <meta charset = "utf-8" >
                                             <title>ERROR</title >
                                            </head>
                                            <body>
                                            <p>ERROR LIMIT OUT OF RANGE. Introduce a valid limit value</p>
                                            <a href="/">Main page</a></body></html>"""
                else:
                    for element in limit:       #iteration to get all the species in the limit
                        limit_list.append(element["display_name"])     #appends to list
                        if len(limit_list) == index:
                            contents += f"""<p>The species are: </p>"""
                            for specie in limit_list:         #iteration to print
                                contents += f"""<p> - {specie} </p>"""
                    contents += f"""<a href="/">Main page</a></body></html>"""     #to go back to the main page = index.html


            #------Karyotype

            elif first_resource == "/karyotype":         #returns the names of the chromosomes of the chosen species
                contents = f"""<!DOCTYPE html>
                                <html lang = "en">
                                <head>
                                    <meta charset = "utf-8">
                                     <title> Karyotype </title >
                                </head >
                                <body>
                                <h2> The names of the chromosomes are:</h2>"""

                # We get the arguments that go after the ? symbol
                get_value = list_resource[1]

                # We get the seq index and name of species
                seq_n = get_value.split('?')    #splits the argument by ?
                seq_name, name_sp = seq_n[0].split("=")     #then splits by the =

                ENDPOINT = 'info/assembly/'  # we add ENDPOINT to URL
                REQUEST = ENDPOINT + name_sp + PARAMS  # easier for connecting

                # Connect with the server
                conn = http.client.HTTPConecction(SERVER)


                try:
                    conn.request('GET', REQUEST)     #connection request
                except ConnectionRefusedError:  # If the connection fails we print an error message
                    print("ERROR! Cannot connect to the Server")
                    exit()

                # read response message from server
                response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server
                data = response.read().decode("utf-8")  # It is necessary to decode the information = utf-8

                karyotype_data = data["karyotype"]

                for chromosome in karyotype_data:     #iteration to print all the chromosomes
                    contents += f"""<p> - {chromosome} </p>"""
                    contents += f"""<a href="/">Main page </a></body></html>"""         #to return to the main page = index.html



            # ------ChromosomeLength

            elif first_resource == "/chromosomeLength":         #returns the length of the chromosome named "chromo" of the given species
                #html for when no chromosome index is written
                content = f"""<!DOCTYPE html>                  
                            <html lang = "en">
                            <head>
                             <meta charset = "utf-8" >
                             <title>ERROR</title >
                            </head>
                            <body>
                            <p>ERROR INVALID VALUE. Introduce an integer value for chromosome</p>
                            <a href="/">Main page</a></body></html>"""

                # We get the arguments that go after the ? symbol, it gives us the SPECIE&CHROMOSOME
                pair = list_resource[1]

                # We have to separate both the species name and the chromo index inputed
                pairs = pair.split('&')

                species_name, specie = pairs[0].split("=")
                chromosome_index, chromosome = pairs[1].split("=")

                ENDPOINT = 'info/assembly/'  # we add ENDPOINT to URL
                REQUEST = ENDPOINT + specie + PARAMS

                # Connect with the server
                conn = http.client.HTTPConecction(SERVER)


                try:
                    conn.request('GET', REQUEST)  #connection request
                except ConnectionRefusedError:  # If the connection fails we print an error message
                    print("ERROR! Cannot connect to the Server")
                    exit()

                # response message from the server
                response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

                data = response.read().decode("utf-8")  # It is necessary to decode the information
                data = json.loads(data)     # loads(). is a method from JSON library  (read JSON response)

                chromosome_data = data["top_level_region"]  #list to save all the chromosomes

                for chromo in chromosome_data:    #iteration to get all chromo from list
                    if chromo["name"] == str(chromosome):
                        length = chromo["length"]
                        contents = f"""<!DOCTYPE html><html lang = "en"><head><meta charset = "utf-8" ><title> Length Chromosome</title >
                                            </head ><body><h2> The length of the chromosome is: {length}</h2><a href="/"> Main page</a"""


        except (KeyError, ValueError, IndexError, TypeError):      #treats all kinds of errors, redirects to error.html page
            contents = Path('Error.html').read_text()


        # Generating the response message
        self.send_response(error_code)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()



















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


    print()
    print(f"Server: {SERVER}")
    print(f"URL:{URL}")

    #Connect with the server
    conn = http.client.HTTPConecction(SERVER)

    # Print the connection information
    tc.cprint(f"\nConnecting to server: {server}", 'blue')
    tc.cprint(f"URL : {URL}", 'blue')


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








