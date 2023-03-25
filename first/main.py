"""Main file which runs server."""
from http.server import HTTPServer
from config import PORT, HOST
from http_hendler import CustomHTTP

if __name__ == "__main__":
    with HTTPServer((HOST, PORT), CustomHTTP) as server:
        server.serve_forever()
