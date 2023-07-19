import base64
import binascii
import http.server
import socketserver
import requests
import ssl

PORT = 9998

VPN_API_KEY = "xtaszcvbjklsqnqkxjazvfuagioazdncbjuqfieuzhfuoizaeuvifciupzr"

class VpnHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        receviedApiKey = self.headers.get('Api-Key')
        if receviedApiKey != VPN_API_KEY:
            self.send_response(403)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Forbidden\n")
            return
        try:
            rightUrl = base64.urlsafe_b64decode(self.path[1:]).decode()
            response = requests.get(rightUrl)

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

httpd = socketserver.TCPServer(("", PORT), VpnHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile="cert.pem", keyfile="key.pem", server_side=True)
print("serving at port", PORT)
httpd.serve_forever()