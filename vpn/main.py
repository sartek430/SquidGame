import base64
import binascii
import http.server
import socketserver
import requests

PORT = 9998


class DecamouflageHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            decamouflaged_url = base64.urlsafe_b64decode(self.path[1:]).decode()

            print(f"URL décamouflée : {decamouflaged_url}")
            response = requests.get(decamouflaged_url)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            print("Envoi de la réponse au client ok")
            self.wfile.write(response.content)

        except binascii.Error:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bad Request: Invalid base64 encoding\n")


with socketserver.TCPServer(("", PORT), DecamouflageHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()