#!/usr/bin/env python3
"""HTTP server for Godot 4 Web exports with required COOP/COEP headers."""
import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class GodotWebRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self) -> None:
        # Required headers for Godot 4 Web (SharedArrayBuffer / AudioWorklet)
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        # Cache control for large wasm/pck files
        self.send_header("Cache-Control", "public, max-age=3600")
        super().end_headers()

    def log_message(self, format: str, *args) -> None:
        # Quiet down verbose logging
        pass


with socketserver.TCPServer(("0.0.0.0", PORT), GodotWebRequestHandler) as httpd:
    print(f"Godot Web Server running at http://localhost:{PORT}")
    print(f"Serving files from: {DIRECTORY}")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()
