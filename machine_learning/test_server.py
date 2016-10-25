import http.server

server_address = ("130.158.80.39", 8080)
handler_class = http.server.CGIHTTPRequestHandler #ハンドラを設宁E
simple_server = http.server.HTTPServer(server_address, handler_class)
simple_server.serve_forever()
