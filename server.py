#!/usr/bin/env python3
"""HTTP server that always sends charset=utf-8 for HTML/CSS/JS."""
import http.server
import socketserver

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

with socketserver.TCPServer(("", PORT), UTF8Handler) as httpd:
    httpd.allow_reuse_address = True
    print(f"Serving at http://localhost:{PORT}/report.html")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()
