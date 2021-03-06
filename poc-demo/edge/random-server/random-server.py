import secrets
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from cpu_load_generator import load_all_cores


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        parts = str.split(self.path, '/')

        n = int(parts[2])
        if parts[1] == "random":
            content = ""
            for i in range(n):
                generated = secrets.randbelow(sys.maxsize)
                content += str(generated)
                content += "\n"

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()

            self.wfile.write(content.encode("ascii"))
        elif parts[1] == "load":
            load_all_cores(n, 0.25)
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            self.send_error(404)


server_address = ('0.0.0.0', 8080)
httpd = HTTPServer(server_address, RequestHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.socket.close()
