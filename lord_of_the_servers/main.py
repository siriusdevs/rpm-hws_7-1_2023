"""Runs the server."""
from http.server import ThreadingHTTPServer
from http_handler import CustomHandler
from config import HOST, PORT

if __name__ == '__main__':
    with ThreadingHTTPServer((HOST, PORT), CustomHandler) as server:
        server.serve_forever()
