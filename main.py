import http.server
import socketserver
import http.client
import base64

PORT = 9999

VPN_API_KEY="xtaszcvbjklsqnqkxjazvfuagioazdncbjuqfieuzhfuoizaeuvifciupzr"

VPN = '51.103.110.178'
VPN_PORT = 443

LOCAL_VPN = '127.0.0.1'
LOCAL_VPN_PORT = 9998

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        camouflaged_url = "/" + base64.urlsafe_b64encode(self.path.encode()).decode()

        # conn = http.client.HTTPConnection(VPN, VPN_PORT)
        conn = http.client.HTTPConnection(LOCAL_VPN, LOCAL_VPN_PORT)
        conn.request("GET", camouflaged_url, headers={"Api-Key": VPN_API_KEY})
        response = conn.getresponse()

        self.send_response(response.status)
        self.send_header("Content-type", response.getheader("Content-type"))
        self.end_headers()
        self.wfile.write(response.read())

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()