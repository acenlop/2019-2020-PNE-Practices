import http.server
import socketserver
#import termcolor
from pathlib import Path
from Seq1 import Seq
import json

# Define the Server's port, IP and BASES
PORT = 8080
IP = "127.0.0.1"
BASES = ["A","T","G","C"]

#URL w/o the ENDPOINT (different for each option)
SERVER = 'rest.ensembl.org'
PARAMS = '?content-type=application/json'

# Connect with the server
conn = http.client.HTTPConnection(SERVER)


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

  def do_GET(self):
      """This method is called whenever the client invokes the GET method
      in the HTTP protocol request"""

      # Print the request line in green
      #termcolor.c
      print(self.requestline)

      req_line = self.requestline.split(' ')  #splits request line by spaces

      list_resource = (req_line[1]).split('?')  #First we get the first request line and path, then the arguments after the ? symbol
      first_resource = list_resource[0]      #sets the first argument

      contents = Path('Error.html').read_text()    #in case of error
      self.send_response(404)

      #----------------------------------- MAIN PROGRAM ---------------------------------


      try:
          if first_resource == "/":      #Returns the Main page for accessing all the other services
              # Read the file
              contents = Path('index.html').read_text()     #contents in index.html
              self.send_response(200)

          # --------------------------- BASIC LEVEL ------------------------------------
          # ------ListSpecies

          elif first_resource == "/listSpecies":     #list of the names of species stored in the ensembl
              contents = f"""<!DOCTYPE html>
                              <html lang = "en">
                              <head>
                               <meta charset = "utf-8" >
                               <title>List of species in the browser</title >
                              </head>
                              <body style="background-color:#DCF3FB">
                              <h1 style="color:#32A2C9"> List of species</h1>
                              <p style="color:#19B4E6"><b>The total number of species in ensembl is: 267</b></p>"""

              get_value = list_resource[1]    #go to the first argument
              seq_n = get_value.split('?')    #splits the argument by ?
              seq_name, index = seq_n[0].split("=")    #then splits by the =
              index = int(index)
              contents += f"""<p><b>The number of species you selected are: {index} </b> </p>""" #prints the total number of species selected

              ENDPOINT = 'info/species'            #we add ENDPOINT to URL
              PARAMS = '?content-type=application/json'
              REQUEST = ENDPOINT + PARAMS


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
                                          <body style="background-color:red">
                                          <h1>ERROR</h1>
                                          <p>NUMBER INTRODUCED IS OUT OF RANGE. Introduce a valid limit value, between 0 and 286</p>
                                          <p> Go back to the Main Page: <a href="/">Main page</a> </p> </body></html>"""
              else:
                  for element in limit:       #iteration to get all the species in the limit
                      limit_list.append(element["display_name"])     #appends to list

                      if len(limit_list) == index:
                          contents += f"""<p>The species are: </p>"""
                          for specie in limit_list:         #iteration to print
                              contents += f"""<p> - {specie} </p>"""
                  contents += f"""<p> Go back to the Main Page: <a href="/">Main page</a> </p> </body></html>"""     #to go back to the main page = index.html


          #------Karyotype

          elif first_resource == "/karyotype":         #returns the names of the chromosomes of the chosen species
              contents = f"""<!DOCTYPE html>
                              <html lang = "en">
                              <head>
                                  <meta charset = "utf-8">
                                   <title> Karyotype </title >
                              </head >
                              <body style="background-color:#DCF3FB">
                              <h1 style="color:#32A2C9">Karyotype</h1>
                              <h2 style="color:#19B4E6"> The names of the chromosomes are: </h2>"""

              # We get the arguments that go after the ? symbol
              get_value = list_resource[1]

              # We get the seq index and name of species
              seq_n = get_value.split('?')    #splits the argument by ?
              seq_name, name_sp = seq_n[0].split("=")     #then splits by the =

              ENDPOINT = 'info/assembly/'  # we add ENDPOINT to URL
              PARAMS = '?content-type=application/json'
              REQUEST = ENDPOINT + name_sp + PARAMS  # easier for connecting


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
                  contents += f"""<p>Go back to the main page: <a href="/">Main page </a></p> </body></html>"""         #to return to the main page = index.html



          # ------ChromosomeLength

          elif first_resource == "/chromosomeLength":         #returns the length of the chromosome named "chromo" of the given species
              # We get the arguments that go after the ? symbol, it gives us the SPECIE&CHROMOSOME
              pair = list_resource[1]

              # We have to separate both the species name and the chromo index inputed
              pairs = pair.split('&')

              species_name, specie = pairs[0].split("=")
              chromosome_index, chromosome = pairs[1].split("=")


              ENDPOINT = 'info/assembly/'  # we add ENDPOINT to URL
              PARAMS = '?content-type=application/json'
              REQUEST = ENDPOINT + specie + PARAMS


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
                      contents = f"""<!DOCTYPE html>
                                              <html lang = "en">
                                              <head>
                                              <meta charset = "utf-8" >
                                              <title> Length Chromosome</title >
                                              </head>
                                              <body style="background-color:#DCF3FB">
                                              <h1 style="color:#32A2C9">Chromosome Length</h1>
                                              <p style="color:#19B4E6"><b> The length of chromosome {chromosome} is: {length}</b></p>
                                              <p>Go back to the Main Page: <a href="/"> Main page</a></p>"""

                  else: # html for when no chromosome index is written
                      content = f"""<!DOCTYPE html>                
                                              <html lang = "en">
                                              <head>
                                               <meta charset = "utf-8" >
                                               <title>ERROR</title>
                                              </head>
                                              <body style="background-color: red">
                                              <h1>ERROR --> INVALID VALUE</h1>
                                              <p> Introduce a valid integer value for chromosome</p>
                                              <p>Go back to the Main Page: <a href="/">Main page</a></p> </body></html>"""



          #---------------------------------- MEDIUM LEVEL ------------------------------------------

          # ------GeneSeq

          elif first_resource == "/geneSeq":     #Return the sequence of a given human gene
              contents = f"""<!DOCTYPE html>
                              <html lang = "en">          
                              <head>
                              <meta charset = "utf-8">
                              <title> Gene Sequence </title >
                              </head>"""


              get_value = list_resource[1]    #go to the first argument

              # We have to separate the human gene from the sequence
              seq_n = get_value.split('?')     # We get the arguments that go after the ? symbo
              seq_name, name_seq = seq_n[0].split("=")

              contents += f"""<body style="background-color:#FCF7DC">
                            <h1 style="color:#D6085C"> Gene Sequence </h1>
                            <p style="color:#D6085C"><b>The sequence of gene {name_seq} is: </b></p>"""

                      # First Endpoint (homosapiens) and program

              FIRST_ENDPOINT = 'xrefs/symbol/homo_sapiens/'  # first endpoint is to get to the homo sapiens
              PARAMS = '?content-type=application/json'
              FIRST_REQUEST = FIRST_ENDPOINT + name_seq + PARAMS


              try:
                  conn.request('GET', FIRST_REQUEST)  # connection request
              except ConnectionRefusedError:  # If the connection fails we print an error message
                  print("ERROR! Cannot connect to the Server")
                  exit()

              # response message from the server
              response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

              data = response.read().decode("utf-8")  # It is necessary to decode the information
              data = json.loads(data)  # loads(). is a method from JSON library  (read JSON response)

              id_gene = data[0]
              id_gene = id_gene["id"]

                      #Second Endpoint and program

              SECOND_ENDPOINT = 'sequence/id/'  # second endpoint is to get the specific gene
              PARAMS = '?content-type=application/json'
              SECOND_REQUEST = SECOND_ENDPOINT + id_gene + PARAMS

              try:
                  conn.request('GET', SECOND_REQUEST)  # connection request

              except ConnectionRefusedError:  # If the connection fails we print an error message
                  print("ERROR! Cannot connect to the Server")
                  exit()

              # response message from the server
              response2 = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

              data2 = response2.read().decode("utf-8")  # It is necessary to decode the information
              data2 = json.loads(data2)  # loads(). is a method from JSON library  (read JSON response)

              sequence = data2["seq"]
              contents += f"""<p style="color:#D6085C">{sequence}</p>
                                <p>Go back to the Main Page: <a href="/"> Main page</a></p> </body></html>""" #redirects to main page



          # ------GeneInfo

          elif first_resource == "/geneInfo":      #Return information about a human gene
              contents = f"""<!DOCTYPE html>
                                  <html lang = "en">          
                                  <head>
                                  <meta charset = "utf-8">
                                  <title> Gene Information</title>
                                  </head>"""

              get_value = list_resource[1]  # go to the first argument

              # We have to separate the human gene from the sequence
              seq_n = get_value.split('?')  # We get the arguments that go after the ? symbol
              seq_name, name_seq = seq_n[0].split("=")

              contents += f"""<body style="background-color:#FCF7DC">
                                <h1 style="color:#D6085C"> Gene Information </h1>
                                <p style="color:#D6085C"> The information about gene {name_seq} is:  </p>"""

                          # First Endpoint and program

              FIRST_ENDPOINT = 'xrefs/symbol/homo_sapiens/'  # first endpoint is to ....
              PARAMS = '?content-type=application/json'
              FIRST_REQUEST = FIRST_ENDPOINT + name_seq + PARAMS


              try:
                  conn.request('GET', FIRST_REQUEST)  # connection request

              except ConnectionRefusedError:  # If the connection fails we print an error message
                  print("ERROR! Cannot connect to the Server")
                  exit()

              # response message from the server
              response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

              data = response.read().decode("utf-8")  # It is necessary to decode the information
              data = json.loads(data)  # loads(). is a method from JSON library  (read JSON response)

              id_gene = data[0]
              id_gene = id_gene["id"]

                       # Second Endpoint and program

              SECOND_ENDPOINT = 'lookup/id/'  # second endpoint is to ....
              PARAMS = '?content-type=application/json'
              SECOND_REQUEST = SECOND_ENDPOINT + id_gene + PARAMS

              try:
                  conn.request('GET', SECOND_REQUEST)  # connection request

              except ConnectionRefusedError:  # If the connection fails we print an error message
                  print("ERROR! Cannot connect to the Server")
                  exit()

              # response message from the server
              response2 = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

              data2 = response2.read().decode("utf-8")  # It is necessary to decode the information
              data2 = json.loads(data2)  # loads(). is a method from JSON library  (read JSON response)

              length = int(data2["end"]) - int(data2["start"])

              contents += f"""<p style="color:#D6085C"> The gene starts at: {data2["start"]} </p>
                              <p style="color:#D6085C"> The gene ends at: {data2["end"]} </p>
                              <p style="color:#D6085C"> The gene length is: {length}</p>
                              <p style="color:#D6085C"> The gene id is at: {id_gene} </p> 
                              <p style="color:#D6085C"> The gene is on chromosome: {data2["seq_region_name"]} </p>
                              <p> Go back to the Main Page: <a href="/">Main page</a> </p> </body></html>"""  #redirects to main page

          # ------GeneCalc

          elif first_resource == "/geneCalc":  # Return information about a human gene
              contents = f"""<!DOCTYPE html>
                                          <html lang = "en">          
                                          <head>
                                          <meta charset = "utf-8">
                                          <title> Gene Calculations </title>
                                          </head>"""

              get_value = list_resource[1]  # go to the first argument

              # We have to separate the human gene from the sequence
              seq_n = get_value.split('?')  # We get the arguments that go after the ? symbo

              seq_name, name_seq = seq_n[0].split("=")

                          # First Endpoint and program

              FIRST_ENDPOINT = 'xrefs/symbol/homo_sapiens/'  # first endpoint is to ....
              PARAMS = '?content-type=application/json'
              FIRST_REQUEST = FIRST_ENDPOINT + name_seq + PARAMS

              try:
                  conn.request('GET', FIRST_REQUEST)  # connection request

              except ConnectionRefusedError:  # If the connection fails we print an error message
                  print("ERROR! Cannot connect to the Server")
                  exit()

              # response message from the server
              response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

              data = response.read().decode("utf-8")  # It is necessary to decode the information
              data = json.loads(data)  # loads(). is a method from JSON library  (read JSON response)

              id_gene = data[0]
              id_gene = id_gene["id"]

                      # Second Endpoint and program

              SECOND_ENDPOINT = 'sequence/id/'  # second endpoint is to ....
              SECOND_REQUEST = SECOND_ENDPOINT + id_gene + PARAMS

              try:
                  conn.request('GET', SECOND_REQUEST)  # connection request

              except ConnectionRefusedError:  # If the connection fails we print an error message
                  print("ERROR! Cannot connect to the Server")
                  exit()

              # response message from the server
              response2 = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

              data2 = response2.read().decode("utf-8")  # It is necessary to decode the information
              data2 = json.loads(data2)  # loads(). is a method from JSON library  (read JSON response)

              sequence = Seq(data2["seq"])


              contents += f"""<body style="background-color:#FCF7DC">
                                <h1 style="color:#D6085C"> Gene Calculations </h1>
                                <p style="color:#D6085C"> The length of gene {name_seq} is: {sequence.len()} </p>"""

              BASES = ["A", "T", "G", "C"]

              for base in BASES:
                  perc_base = round(sequence.count_base(base) * 100 / sequence.len(), 2)
                  contents += f"""<p> {base} : {sequence.count_base(base)} ({perc_base}%) </p>"""

              contents += f"""<p> Go back to the Main Page: <a href="/">Main page</a> </p> </body></html>"""  # redirects to main page

          # ------GeneList

          elif first_resource == "/geneList":       #Return the names of the genes located in the chromosome "chromo" from the start to end positions
              contents = f"""<!DOCTYPE html>
                                <html lang = "en">          
                                <head>
                                <meta charset = "utf-8">
                                <title> Gene List </title>
                                </head>"""
              pair = list_resource[1]  # go to the first argument

              # We have to separate the human gene from the sequence
              pairs = pair.split('&')     # We get the arguments that go after the & symbol

              value_chromo, chromo = pairs[0].split("=")
              chromosome_start, start = pairs[1].split("=")
              chromosome_end, end = pairs[2].split("=")

              contents += f"""<body style="background-color:#FCF7DC">
                                <h1 style="color:#D6085C"> Gene List </h1>
                                <p style="color:#D6085C"> List of genes of the chromosome {chromo}, which goes from {start} to {end} </p>"""

              ENDPOINT = 'overlap/region/human/'  # we add ENDPOINT to URL
              PARAMS = '?feature=gene;content-type=application/json'
              REQUEST = ENDPOINT + chromo + ":" + start + "-" + end + PARAMS


              try:
                  conn.request('GET', REQUEST)  # connection request

              except ConnectionRefusedError:  # If the connection fails we print an error message
                  print("ERROR! Cannot connect to the Server")
                  exit()

              # response message from the server
              response = conn.getresponse()  # .getresponse() method that returns the reponse information from the server

              data = response.read().decode("utf-8")  # It is necessary to decode the information
              data = json.loads(data)  # loads(). is a method from JSON library  (read JSON response)

              for element in data:
                  print(element["external_name"])
                  contents += f"""<p style="color:#D6085C">{element["external_name"]}</p>"""

              contents += f"""<p> Go back to the Main Page: <a href="/">Main page</a></p> </body></html>"""




          # Open the form1.html file
          # Read the index from th

          # Define the content-type header:
          if 'json=1' in req_line:
              self.send_header('Content-Type', 'application/json')
              self.send_header('Content-Length', len(str.encode(contents)))

          else:
              self.send_header('Content-Type', 'text/html')
              self.send_header('Content-Length', len(str.encode(contents)))

          # The header is finished
          self.end_headers()

          # Send the response message
          self.wfile.write(str.encode(contents))

          return


      except (KeyError, ValueError, IndexError, TypeError):
          contents = Path('Error.html').read_text()

# ------------------------
# - Server MAIN program (taken from previous practices)
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
       print("Stopped by the user")
       httpd.server_close()

