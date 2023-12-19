from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from twisted.internet import reactor
from twisted.web import http

class MyRequestHandler(http.Request):
    def process(self):
        self.setHeader('Content-type', 'text/html')
        self.write(b'<html><head><title>test</title></head>')
        self.write(b'<body>')
        self.write(self.path)
        print(self)
        if self.path == b'/uptime': self.uptime()
        else: self.menu()
        self.write(b'</body></html>')
        self.finish()
        
    def uptime(self): pass
    
class MyHTTP(http.HTTPChannel):
    requestFactory = MyRequestHandler
    
class HTTPServerFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return MyHTTP()
    
reactor.listenTCP(8001, HTTPServerFactory())
reactor.run()