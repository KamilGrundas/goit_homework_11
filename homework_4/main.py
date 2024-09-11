from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
from threading import Thread
import socket
import json
from datetime import datetime

IP = socket.gethostname()

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (IP, 5000))
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def save_to_file(data):
    with open("storage/data.json", "r+") as file:
        loaded_data = json.load(file)
        loaded_data[f"{datetime.now()}"] = data
        json.dump(loaded_data, file)


def run_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = (IP, 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, 5000))
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f"Reveived data: {data.decode()} from : {address}")
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {
                key: value
                for key, value in [el.split("=") for el in data_parse.split("&")]
            }
            save_to_file(data_dict)
    except KeyboardInterrupt:
        print(f"Destroy server")
    finally:
        sock.close()


if __name__ == "__main__":
    http_server = Thread(target=run_http_server, args=())
    socket_server = Thread(target=run_socket_server, args=())

    socket_server.start()
    http_server.start()

    http_server.join()
    socket_server.join()
    print("Done!")
