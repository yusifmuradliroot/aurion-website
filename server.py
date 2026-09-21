import http.server, socketserver, os

ROOT = '/root/aurion-website'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def serve_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(os.path.join(ROOT, 'en', '404.html'), 'rb') as f:
            self.wfile.write(f.read())
    def do_GET(self):
        path = self.path.split('?')[0].strip('/')
        if path == '':
            self.send_response(302)
            self.send_header('Location', '/en/')
            self.end_headers()
            return
        if path == 'en':
            self.path = '/en/index.html'
            return super().do_GET()
        if path.startswith('en/') and '.' not in path.split('/')[-1]:
            candidate = os.path.join(ROOT, path + '.html')
            if os.path.isfile(candidate):
                self.path = '/' + path + '.html'
                return super().do_GET()
            return self.serve_404()
        if os.path.isfile(os.path.join(ROOT, path)):
            return super().do_GET()
        return self.serve_404()

class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    server = ReuseTCPServer(('0.0.0.0', 3000), Handler)
    server.serve_forever()
