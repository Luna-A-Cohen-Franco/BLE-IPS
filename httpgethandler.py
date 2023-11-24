from http.server import SimpleHTTPRequestHandler, HTTPServer

# Set up a basic HTTP server
class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get_coordinates':
            # Specify the path to the file you want to send
            file_path = 'coordinates.json'

            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
                self.end_headers()
                self.wfile.write(file.read())

# Start the server
def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
