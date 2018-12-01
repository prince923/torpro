import uuid

import tornado.websocket
from .main import BaseHandler
import tornado.escape


class RoomHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('room.html', messages=ChatHandler.history)


class ChatHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    userset = set()  # 存放用户的集合
    history = []  # 存放历史消息的消息列表
    count = 200  # 显示历史消息的条数

    def open(self, *args, **kwargs):
        """
        用户连接成功时调用
        """
        ChatHandler.userset.add(self)
        print('%s已连接' % self.current_user)

    def on_message(self, message):
        """
        处理消息，当客户端有消息发送过来的时候调用
        :param message:
        :return:
        """
        body = tornado.escape.json_decode(message)['body']  # json_decode 将返回的json字符串变成dict
        chat = {
            'id': str(uuid.uuid4()),
            'body': body
        }
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
        if self in ChatHandler.userset:
            ChatHandler.userset.remove(self)
        print('连接关闭')

    @classmethod
    def send_message(cls, msg):
        """
        给所有用户发送消息
        :param msg:
        :return:
        """
        for u in ChatHandler.userset:
            u.write_message(msg)

    @classmethod
    def history_message(cls, msg):
        cls.history.append(msg)
        if len(cls.history) > cls.count:
            cls.history = cls.history[-cls.count]
