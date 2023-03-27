"""There you can start flask server."""

from flask_server import app
from config import HOST, PORT, SECRET_KEY


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run(host=HOST, port=PORT, debug=True)
