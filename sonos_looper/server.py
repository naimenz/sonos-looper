import random
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread
from typing import Optional


class HttpServer(Thread):
    """A simple HTTP Server in its own thread"""

    def __init__(self, ip: str, port: int):
        super().__init__()
        self.daemon = True
        handler = SimpleHTTPRequestHandler
        self.ip = ip
        self.port = port
        self.httpd = TCPServer(("", port), handler)
    
    @property
    def base_url(self) -> str:
        return f"http://{self.ip}:{self.port}"

    def run(self):
        """Start the server"""
        print("Start HTTP server")
        self.httpd.serve_forever()

    def stop(self):
        """Stop the server"""
        print("Stop HTTP server")
        self.httpd.socket.close()

def make_server(ip: Optional[str] = None, port: Optional[int] = None) -> HttpServer:
    if ip is None:
        ip = detect_ip_address()
    if port is None:
        port = random.randint(8000, 9000)
    return HttpServer(ip, port)

def detect_ip_address() -> str:
    """Return the local ip-address"""
    # Rather hackish way to get the local ip-address, recipe from
    # https://stackoverflow.com/a/166589
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return str(ip_address)