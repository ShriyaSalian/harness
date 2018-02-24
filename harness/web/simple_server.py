from http import server
# from http.server import SimpleHTTPRequestHandler, HTTPServer as BaseHTTPServer


port = 8018
server_address = ('127.0.0.1', port)


class CORSRequestHandler (server.SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        server.SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    server.test(CORSRequestHandler, server.HTTPServer, port=port)
