import http.server
import socketserver
import http.client
import base64
import ssl

PORT = 9999

VPN_API_KEY = "xtaszcvbjklsqnqkxjazvfuagioazdncbjuqfieuzhfuoizaeuvifciupzr"

VPN = '51.103.110.178'
VPN_PORT = 443

LOCAL_VPN = '127.0.0.1'
LOCAL_VPN_PORT = 9998

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        camouflaged_url = "/" + base64.urlsafe_b64encode(self.path.encode()).decode()

        conn = http.client.HTTPSConnection(LOCAL_VPN, LOCAL_VPN_PORT, context=ssl._create_unverified_context())
        conn.request("GET", camouflaged_url, headers={"Api-Key": VPN_API_KEY})
        response = conn.getresponse()

        self.send_response(response.status)
        self.send_header("Content-type", response.getheader("Content-type"))
        self.end_headers()
        self.wfile.write(response.read())

    def do_CONNECT(self):
        host, port = self.path.split(':')
        port = int(port)

        try:
            conn = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
            self.send_response(200, 'Connection established')
            self.send_header('Proxy-Agent', 'Python-Proxy')
            self.end_headers()
        except:
            self.send_response(502, 'Bad Gateway')
            self.end_headers()
            return

        self.close_connection = False

        self.connection = conn
        self.handle_one_request()

httpd = socketserver.TCPServer(("", PORT), ProxyHandler)
print("serving at port", PORT)
httpd.serve_forever()