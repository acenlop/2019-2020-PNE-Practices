import http.server
import socketserver
import termcolor
from pathlib import Path
from Seq1 import Seq

# Define the Server's port
PORT = 8080


def html_response(title="", body=""):
    default_body = f"""
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
  </head>
  <body>{body}
    </body>
    <body>
    <a href="http://127.0.0.1:8080/">Main Page </a>
  </body>
</html>
"""

    return default_body


def argument_command(request_line):
    argument = request_line[request_line.find("=") + 1:]
    return argument


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

def read_file(filename):  # read_file() is the function read_fasta_data() from other practice
    # -- Open and read the file
    file_contents = pathlib.Path(filename).read_text().split("\n")[1:]
    body = "".join(file_contents)
    return body

# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint("  " + self.requestline, 'green')

        # Message to send back to the client
        FOLDER = "../P6/"
        if self.path = "/":
            file = "form-4.html"
            contents = read_file(FOLDER + file)  # read_file() is the function read_fasta_data() from other practice
            # Generating the response message
            self.send_response(200)  # -- Status line: OK!

        elif "/ping" in self.path:
            html = "<h1>PING OK!</h1><p>The SEQ2 server is running...</p>"
            contents = html_response("PING", html)
            self.send_response(200)  # -- Status line: OK!

        elif "/get" in self.path:
            seq_list = ["TGTGAACATTCTGCACAGGTCTCTGGCTGCGCCTGGGCGGGTTTCTT",
                        "CAGGAGGGGACTGTCTGTGTTCTCCCTCCCTCCGAGCTCCAGCCTTC",
                        "CTCCCAGCTCCCTGGAGTCTCTCACGTAGAATGTCCTCTCCACCCC",
                        "GAACTCCTGCAGGTTCTGCAGGCCACGGCTGGCCCCCCTCGAAAGT",
                        "CTGCAGGGGGACGCTTGAAAGTTGCTGGAGGAGCCGGGGGGAA"]

            sequence_number = int(argument_command(self.path))
            sequence = seq_list[sequence_number]   #para acceder la secuencia deseada

            html = "<h1>Sequence number " + str(sequence_number) + "</h1><p>" + sequence + "</p>"
            contents = html_response("GET", html)

            self.send_response(200)  # -- Status line: OK!

        elif "/gene" in self.path:
            gene = argument_command(self.path)

            s = Seq()
            s.read_fasta("../Session-04/" + gene + ".txt")

            html = "<h1>Gene Sequence: " + gene + '</h1><textarea readonly rows = "20" cols = "80">' + str(
                s) + '</textarea>'
            contents = html_response("GENE", html)

            self.send_response(200)  # -- Status line: OK!

        elif "/info" in self.path:
            seq_info = Seq(argument_command)  # gets the seq chosen
            count_bases_string = ""  # starts the count of bases in a new variable


            for base, count in seq_info.count().items():  # loop to count the base and the times it appears on the chain
                s_base = str(base) + ": " + str(count) + " (" + str(
                    round(count / seq_info.len() * 100,
                          2)) + "%)" + "\n"  # calculates the percentage of the base in chain
                count_bases_string += s_base

            response = ("Sequence: " + str(seq_info) + "\n" +
                        "Total length: " + str(seq_info.len()) + "\n" +
                        count_bases_string)  # prints the result of the seq with its length and bases counted

            html_operation = "<h1>Operation:</h1><p>Info</p>"
            html_result = "<h1>Result:</h1>" + "<p>" + response + "</p>


        elif "/comp" in self.path:
            seq_comp = Seq(argument_command)  # takes the composite function with the method in Seq
            response = seq_comp.complement() + "\n"  # prints the complement

            html_operation = "<h1>Operation:</h1><p>Comp</p>"
            html_result = "<h1>Result:</h1>" + "<p>" + response + "</p>

        elif "/rev" in self.path:
            seq_rev = Seq(argument_command)  # takes the reverse function with the method in Seq
            response = seq_rev.reverse() + "\n"  # prints it

            html_operation = "<h1>Operation:</h1><p>Rev</p>"
            html_result = "<h1>Result:</h1>" + "<p>" + response + "</p>"

            html_sequence = "<h1>Sequence:</h1>" + "<p>" + argument_command + "</p>"
            html = html_sequence + html_operation + html_result

            contents = html_response("OPERATION", html)

            self.send_response(200)  # -- Status line: OK!

        else:
            file = "error.html"
            contents = read_file(FOLDER + file)
            self.send_response(404)  # -- Status line: ERROR NOT FOUND

        # Generating the response message
        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())


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