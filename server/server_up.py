import http.server

server_address = ("127.0.0.1", 8000)

#handler_simple = http.server.SimpleHTTPRequestHandler #ハンドラを設定
#simple_server = http.server.HTTPServer(server_address, handler_simple)
#simple_server.serve_forever()

handler_cgi = http.server.CGIHTTPRequestHandler #ハンドラを設定
cgi_server = http.server.HTTPServer(server_address, handler_cgi)
cgi_server.serve_forever()