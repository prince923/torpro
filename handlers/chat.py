import uuid
import tornado.websocket
from .main import BaseHandler
import tornado.escape
from tornado.web import authenticated

from tornado.httpclient import AsyncHTTPClient
import tornado.gen
from tornado.ioloop import IOLoop
from utils.account import make_chat


class RoomHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render('room.html', messages=ChatHandler.history)


class ChatHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    user_set = set()  # 存放用户的集合
    history = []  # 存放历史消息的消息列表
    count = 5  # 显示历史消息的条数

    def open(self, *args, **kwargs):
        """
        用户连接成功时调用
        """
        ChatHandler.user_set.add(self)
        print('%s已连接' % self.current_user)

    def on_message(self, message):
        """
        处理消息，当客户端有消息发送过来的时候调用
        :param message:
        :return:
        """
        # print(message)  # {"body":"ppp"}
        body = tornado.escape.json_decode(message)['body']  # json_decode 将返回的json字符串变成dict
        if body.startswith('http://'):
                http_client = AsyncHTTPClient()
                save_api = 'http://192.168.48.134:8080/async?save_url={}&form=room&user={}'.format(body, self.current_user)
                IOLoop.current().spawn_callback(http_client.fetch, save_api)
                body = 'url 正在处理中，请等待...'
                chat = make_chat(msg_body=body,name='系统')
                msg = {
                    'html': tornado.escape.to_basestring(
                        self.render_string('message.html', message=chat)
                    ),
                    'id': chat['id']
                }
                self.write_message(msg)

        else:
                chat = make_chat(msg_body=body,name=self.current_user)
                msg = {
                    'html': tornado.escape.to_basestring(
                        self.render_string('message.html', message=chat)
                    ),
                    'id': chat['id']
                }
                # print(msg)   # {'html': '<div class="message" id="mef1947ac-7f68-4381-b6c9-93b484c4ee85">ppp</div>', 'id': 'ef1947ac-7f68-4381-b6c9-93b484c4ee85'}
                ChatHandler.history_message(msg)
                ChatHandler.send_message(msg)


    def on_close(self):
        """
         断开连接的时候
        :return:
        """
        if self in ChatHandler.user_set:
            ChatHandler.user_set.remove(self)
        print('连接关闭')


    @classmethod
    def send_message(cls, msg):
        """
        给所有用户发送消息
        :param msg:
        :return:
        """
        for u in ChatHandler.user_set:
            u.write_message(msg)


    @classmethod
    def history_message(cls, msg):
        cls.history.append(msg)
        if len(cls.history) > cls.count:
            cls.history = cls.history[-cls.count:]
