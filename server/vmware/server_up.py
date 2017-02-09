import http.server
server_address = ("130.158.80.39", 8080)

#handler_simple = http.server.SimpleHTTPRequestHandler #ハンドラを設宁E
#simple_server = http.server.HTTPServer(server_address, handler_simple)
#simple_server.serve_forever()

handler_cgi = http.server.CGIHTTPRequestHandler #ハンドラを設宁E
cgi_server = http.server.HTTPServer(server_address, handler_cgi)

try:
    cgi_server.serve_forever()
except KeyboardInterrupt:
    cgi_server.serve_close()
