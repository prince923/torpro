from utils.account import authenticate,register
from handlers.main import BaseHandler
from models.account import User
from utils import res


class LoginHandler(BaseHandler):
    """
    用户登录接口
    """

    def get(self, *args, **kwargs):
        next = self.get_argument('next','/')
        print(next)
        self.render('login.html', next=next)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next = self.get_argument('next', '/')
        print(username, password)
        if authenticate(username=username, password=password):
            self.session.set('user_info', username)
            self.redirect(next)
        else:
            self.write('login fail')


class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.session.delete('user_info')
        self.write('logout success')


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('register.html',msg='')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        repassword = self.get_argument('repassword', None)
        print(username,password,repassword)
        if username and password and repassword:
            if password == repassword:
              ret = register(username=username,password=password)
              if ret['msg'] == 'ok':
                 self.session.set('user_info',username)
                 self.redirect('/')
              else:
                  msg = ''
                  msg = ret['msg']
            else:
                msg='两次密码输入不一致'
        else:
           msg = '用户名或密不能为空'
        self.render('register.html',msg=msg)
