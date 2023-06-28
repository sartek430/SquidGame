import http.server
import socketserver
import http.client
import base64
import ssl

PORT = 9999


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        camouflaged_url = "/" + base64.urlsafe_b64encode(self.path.encode()).decode()

        conn = http.client.HTTPConnection('localhost', 9998)
        conn.request("GET", camouflaged_url)
        response = conn.getresponse()

        self.send_response(response.status)
        self.send_header("Content-type", response.getheader("Content-type"))
        self.end_headers()
        self.wfile.write(response.read())


with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()