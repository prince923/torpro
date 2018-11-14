from tornado import web
from tornado import ioloop
from tornado.options import define,options
from handlers import main

define('port', default=8080, help='run port', type=int)

class Application (web.Application):
  def __init__(self):
      handlers = [
          (r'/',main.IndexHandler),
          (r'/explore',main.ExploreHandler),
          (r'/post/(?P<post_id>[0-9]+)',main.PostHandler),
      ]
      settings = dict(
          debug= True,
          template_path ='templates',
          static_path = 'static'
      )
      super().__init__(handlers,**settings)

application = Application()

if __name__ == '__main__':
    options.parse_command_line()
    application.listen(options.port)
    print('{}端口正在被监听'.format(str(options.port)))
    ioloop.IOLoop.current().start()