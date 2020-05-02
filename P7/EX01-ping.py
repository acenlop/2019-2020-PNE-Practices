import http.client
import json

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
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
# .getresponse() method that returns the reSponse information from the server

#Print the status line -- OK
tc.cprint(f"Response received!: {response.status} {response.reason}\n", 'blue')

data = response.read().decode("utf-8")  # It is necessary to decode the information
# read JSON
info_api = json.loads(data)  # loads(). is a method from JSON library  (read JSON response)

# PING
ping = info_api['ping']  # OK!

if ping == 1:  # if the response is == 1 the server is OK!
    print("PING OK! The database is running!")