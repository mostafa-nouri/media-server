#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import unquote
from subprocess import Popen
import os

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path[1:]
        if path.startswith("file") and path.find("\\") == -1 and path.find("/") == -1:
            appdir = os.path.dirname(os.path.realpath(__file__))
            f = open(appdir + "/img/" + parsed.path[5:], 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.send_header('Cache-control', 'max-age=31536000')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        self._set_headers()
        if parsed.path == "/play":
            movieId = parsed.query
            print(movieId)
            p = Popen("play.bat " + movieId + " 720", cwd=r".")
            stdout, stderr = p.communicate()
        elif parsed.path == "/play1080":
            movieId = parsed.query
            print(movieId)
            p = Popen("play.bat " + movieId + " 1080", cwd=r".")
            stdout, stderr = p.communicate()
        elif parsed.path == "/exec":
            command = parsed.query
            command = unquote(command)
            print(command)
            p = Popen("mpv-remote.bat " + command, cwd=r".")
            stdout, stderr = p.communicate()
        elif parsed.path == "/shutdown":
            p = Popen("shutdown.bat", cwd=r".")
            stdout, stderr = p.communicate()

        appdir = os.path.dirname(os.path.realpath(__file__))
        f = open(appdir + "/img/page.html", 'rb')
        self.wfile.write(f.read())
        f.close()
        
    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>".encode("utf-8"))
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
