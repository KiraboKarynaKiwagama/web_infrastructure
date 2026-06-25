#Tool for running a basic web server (the "shop" and the "clerk")
from http.server import BaseHTTPRequestHandler, HTTPServer
#Tools for breaking a URL like "/add?a=5&b=3" into usable pieces
from urllib.parse import urlparse, parse_qs
#Tool for converting a Python dictionary into JSON text
import json


def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b


class MyHandler(BaseHTTPRequestHandler):

    # Python calls this automatically whenever a GET request arrives.
    def do_GET(self):

        # self.path is just a raw string, e.g. "/add?a=5&b=3"
        # urlparse splits it into a path part and a query part
        parsed_url = urlparse(self.path)

        # parsed_url.path is now just "/add"
        # parsed_url.query is now just "a=5&b=3"

        # parse_qs turns "a=5&b=3" into {'a': ['5'], 'b': ['3']}
        params = parse_qs(parsed_url.query)

        # params['a'] is a LIST containing a STRING, so we grab item [0]
        # and convert it from text to an actual number with int()
        a = int(params['a'][0])
        b = int(params['b'][0])

        # Decide which math function to run, based on the path
        if parsed_url.path == "/add":
            result = add(a, b)
            operation_name = "addition"
        elif parsed_url.path == "/subtract":
            result = subtract(a, b)
            operation_name = "subtraction"
        elif parsed_url.path == "/multiply":
            result = multiply(a, b)
            operation_name = "multiplication"
        else:
            result = None
            operation_name = "unknown"

        # Build the dictionary we want to send back
        response_data = {
            "a": a,
            "b": b,
            "operation": operation_name,
            "result": result
        }

        self.send_response(200)                              # 200 = "OK, success"
        self.send_header('Content-Type', 'application/json')  # tell the browser it's JSON
        self.end_headers()                                    # finished writing headers

        # Convert the dict -> JSON text -> bytes, then send it
        self.wfile.write(json.dumps(response_data).encode())


# This creates the server and tells it to use MyHandler 
server = HTTPServer(('localhost', 5000), MyHandler)

print("Server is running on http://localhost:5000")

server.serve_forever()