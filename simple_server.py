# File: simple_server.py
# Description: Static server to serve a single HTML document from a folder
# Date: 2024-11-19

import http.server
import socketserver

# Configuration
PORT = 5551
DIRECTORY = "static"


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler to serve files from a specific directory
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


if __name__ == "__main__":
    # Start the server
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving HTML files from {DIRECTORY} on http://0.0.0.0:{PORT}")
        httpd.serve_forever()
