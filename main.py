import http.server
import socketserver
import http.client
import base64
import ssl

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_CONNECT(self):
        camouflaged_url = "/" + base64.urlsafe_b64encode(self.path.encode()).decode()

        conn = http.client.HTTPConnection('51.103.110.178', 443)
        # conn = http.client.HTTPConnection('127.0.0.1', 9998)
        conn.request("CONNECT", camouflaged_url)
        response = conn.getresponse()

        self.send_response(response.status)
        self.send_header("Content-type", response.getheader("Content-type"))
        self.end_headers()
        self.wfile.write(response.read())


    def do_GET(self):
        camouflaged_url = "/" + base64.urlsafe_b64encode(self.path.encode()).decode()

        # conn = http.client.HTTPConnection('51.103.110.178', 443)
        conn = http.client.HTTPConnection('127.0.0.1', 9998)
        conn.request("GET", camouflaged_url)
        response = conn.getresponse()

        self.send_response(response.status)
        self.send_header("Content-type", response.getheader("Content-type"))
        self.end_headers()
        self.wfile.write(response.read())

PORT = 9999

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()