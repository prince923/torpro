from tornado import web
from tornado import ioloop
from tornado.options import define, options
from handlers import main, auth,chat
from handlers import service
define('port', default=8080, help='run port', type=int)


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/upload', main.UploadHandler),
            (r'/login', auth.LoginHandler),
            (r'/logout', auth.LogoutHandler),
            (r'/register', auth.RegisterHandler),
            (r'/profile',main.ProfileHandler),
            (r'/room',chat.RoomHandler),
            (r'/ws',chat.ChatHandler),
            (r'/sync',service.SyncHandler),
            (r'/async',service.AsyncHandler),

        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    'db_sessions': 5,  # 会话
                    'db_notifications': 11,  # 通知
                    'max_connections': 2 ** 31,  # 最大连接数
                },
                'cookies': {
                    'expires_days': 30,
                }
            },
            login_url='/login',
            cookie_secret='asdasdqweqwe',
        )
        super().__init__(handlers, **settings)


application = Application()

if __name__ == '__main__':
    options.parse_command_line()
    application.listen(options.port)
    print('{}端口正在被监听'.format(str(options.port)))
    ioloop.IOLoop.current().start()
