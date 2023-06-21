from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client
import urllib.parse

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request("GET")

    def proxy_request(self, method):
  
        parsed_url = urllib.parse.urlparse(self.path)

        conn = http.client.HTTPSConnection(parsed_url.netloc)
        conn.request(method, parsed_url.path, headers=self.headers)

        response = conn.getresponse()

        self.send_response(response.status, response.reason)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()

        body = response.read()
        self.wfile.write(body)

def run_proxy():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, ProxyHandler)
    httpd.serve_forever()

run_proxy()