#!/usr/bin/env python3

from openssl import OpenSSL

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class OpenSSLHandler(tornado.web.RequestHandler):
    def get(self):
        openssl = OpenSSL()
        version = openssl.version()
        self.write(version)


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', MainHandler),
        (r'/openssl', OpenSSLHandler)
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
