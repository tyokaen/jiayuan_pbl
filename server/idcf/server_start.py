from http.server import HTTPServer, CGIHTTPRequestHandler

class MyHandler(CGIHTTPRequestHandler):
        cgi_directories = ['/cgi-bin']

host = '10.11.0.241'
port = 8080
#port = 443
httpd = HTTPServer((host, port), MyHandler)
print('serving at port', port)
try:
    print("server up")
    httpd.serve_forever()
except:
    print("server down")
    httpd.server_close()
