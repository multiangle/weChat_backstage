__author__ = 'multiangle'
import tornado

import tornado.web
import tornado.ioloop
import tornado.options

from tornado.options import define,options
define('port',default=80,help='run on the given port',type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',AuthHandler)
        ]
        settings=dict(
            debug=True
        )
        tornado.web.Application.__init__(self,handlers,**settings)

class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        data=dict(
            signature=self.get_argument('signature'),
            timestamp=self.get_argument('timestamp'),
            nonce=self.get_argument('nonce'),
            echostr=self.get_argument('echostr')
        )
        self.write(data['echostr'])
        print(data)
        self.finish()
    def post(self):
        data=self.get()
        print(data)


if __name__=='__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()