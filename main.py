from http.server import HTTPServer
from http_handler import CastomHandler
from config import HOST, PORT


if __name__ == '__main__':
    with HTTPServer((HOST, PORT), CastomHandler) as server:
        server.serve_forever()
