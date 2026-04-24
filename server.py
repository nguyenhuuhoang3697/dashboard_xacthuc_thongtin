#!/usr/bin/env python3
"""HTTP server that always sends charset=utf-8 for HTML/CSS/JS."""
import http.server
import socketserver
import sys

PORT = 8000

class UTF8Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        '':      'application/octet-stream',
        '.html': 'text/html; charset=utf-8',
        '.htm':  'text/html; charset=utf-8',
        '.css':  'text/css; charset=utf-8',
        '.js':   'application/javascript; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.png':  'image/png',
        '.jpg':  'image/jpeg',
        '.svg':  'image/svg+xml',
        '.ico':  'image/x-icon',
        '.woff2':'font/woff2',
        '.woff': 'font/woff',
    }

    def log_message(self, format, *args):
        print(f"  {self.address_string()} - {format % args}")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def start_server(port):
    with ReusableTCPServer(("", port), UTF8Handler) as httpd:
        print(f"Serving at http://localhost:{port}/report.html")
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()


if __name__ == "__main__":
    try:
        start_server(PORT)
    except OSError as err:
        fallback = PORT + 1
        print(f"Port {PORT} is unavailable ({err}). Trying {fallback}...", file=sys.stderr)
        start_server(fallback)
