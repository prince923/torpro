from utils.account import authenticate
from handlers.main import BaseHandler


class LoginHandler(BaseHandler):
    """
    用户登录接口
    """
    def get(self, *args, **kwargs):
        next = self.get_argument('next', None)
        print(next)
        self.render('login.html', next=next)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next = self.get_argument('next', None)
        print(username, password)
        if authenticate(username=username, password=password):
            self.session.set('user_info', username)
            if next:
                self.redirect(next)
            else:
                self.write('login success')
        else:
            self.write('login fail')


class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.session.delete('user_info')
        self.write('logout success')
