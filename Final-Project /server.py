import http.server
import socketserver
import termcolor
from pathlib import Path
import termcolor as tc
from Seq1 import Seq
import json

# Define the Server's port
PORT = 8080
IP = "127.0.0.1"
BASES = ["A", "T","G","C"]

#URL
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

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        req_line = self.requestline.split(' ')

        list_resource = (req_line[1]).split('?')
        first_resource = list_resource[0]
        contents = Path('Error.html').read_text()
        self.send_response(404)


        try:
            if first_resource == "/":      # Directs you to Main page html
                # Read the file
                contents = Path('index.html').read_text()
                self.send_response(200)

            elif first_resource == "/listSpecies":     #Go go the list of species
                contents = f"""<!DOCTYPE html>
                <html lang = "en">
                <head>
                 <meta charset = "utf-8" >
                 <title>List of species in the browser</title >
                </head >
                <body>
                <p>The total number of species in ensembl is: 267</p>"""
                get_value = list_resource[1]
                seq_n = get_value.split('?')
                seq_name, index = seq_n[0].split("=")
                index = int(index)
                contents += f"""<p>The number of species you selected are: {index} </p>"""

                ENDPOINT = 'info/species'            #we add ENDPOINT to URL
                # Connect with the server
                conn = http.client.HTTPConecction(SERVER)
                REQUEST = ENDPOINT + PARAMS          #easier

                try:
                    conn.request('GET', REQUEST)
                except ConnectionRefusedError:  # If the connection fails we print an error message
                    print("ERROR! Cannot connect to the Server")
                    exit()

                # response
                response = conn.getresponse()        # .getresponse() method that returns the reponse information from the server
                data = response.read().decode("utf-8")  # It is necessary to decode the information

                limit_list = []
                data = json.loads(data)       # loads(). is a method from JSON library  (read JSON response)
                limit = data["species"]
                if index > len(limit):
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
                    for element in limit:
                        limit_list.append(element["display_name"])
                        if len(limit_list) == index:
                            contents += f"""<p>The species are: </p>"""
                            for specie in limit_list:
                                contents += f"""<p> - {specie} </p>"""
                    contents += f"""<a href="/">Main page</a></body></html>"""     #to go back to the main page = index.html

            elif first_resource == "/karyotype":
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
                # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                # position of the sequence
                seq_n = get_value.split('?')
                seq_name, name_sp = seq_n[0].split("=")

                ENDPOINT = 'info/assembly/'  # we add ENDPOINT to URL
                # Connect with the server
                conn = http.client.HTTPConecction(SERVER)
                REQUEST = ENDPOINT + name_sp + PARAMS  # easier for connecting

                try:
                    conn.request('GET', REQUEST)
                except ConnectionRefusedError:  # If the connection fails we print an error message
                    print("ERROR! Cannot connect to the Server")
                    exit()

                # response
                response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server
                data = response.read().decode("utf-8")  # It is necessary to decode the information
                karyotype_data = data["karyotype"]
                for chromosome in karyotype_data:
                    contents += f"""<p> - {chromosome} </p>"""
                    contents += f"""<a href="/">Main page </a></body></html>"""         #to go back to the main page = index.html

            elif first_resource == "/chromosomeLength":
                content = ???????
                # We get the arguments that go after the ? symbol
                pair = list_resource[1]
                # We have a couple of elements, we need the sequence that we previously wrote and the operation to perform
                # that we previously selected
                pairs = pair.split('&')
                species_name, specie = pairs[0].split("=")
                chromosome_index, chromosome = pairs[1].split("=")

                ENDPOINT = 'info/assembly/'  # we add ENDPOINT to URL
                # Connect with the server
                conn = http.client.HTTPConecction(SERVER)
                REQUEST = ENDPOINT + specie + PARAMS  # easier

                try:
                    conn.request('GET', REQUEST)
                except ConnectionRefusedError:  # If the connection fails we print an error message
                    print("ERROR! Cannot connect to the Server")
                    exit()

                # response
                response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server
                data = response.read().decode("utf-8")  # It is necessary to decode the information
                data = json.loads(data)
                chromosome_data = data["top_level_region"]
                for chromo in chromosome_data:
                    if chromo["name"] == str(chromosome):
                        length = chromo["length"]
                        contents = f"""<!DOCTYPE html><html lang = "en"><head><meta charset = "utf-8" ><title> Length Chromosome</title >
                                            </head ><body><h2> The length of the chromosome is: {length}</h2><a href="/"> Main page</a"""


        except (KeyError, ValueError, IndexError, TypeError):
            contents = Path('error.html').read_text()


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








