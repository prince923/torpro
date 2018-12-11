from .main import BaseHandler
import requests
from utils.pictule import SaveUploadPhoto
from tornado.web import authenticated
from utils.account import make_chat
from tornado.httpclient import AsyncHTTPClient
import tornado.gen
from .chat import ChatHandler
import tornado.escape

class SyncHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        save_url = self.get_argument('save_url', None)  # 会阻塞
        response = requests.get(save_url)
        img_content = response.content
        s = SaveUploadPhoto(img_name='x.jpg', static_path=self.settings['static_path'])
        s.upload_pic(img_content=img_content)
        s.make_thumbnail()
        post = self.orm.add_post(image_url=s.get_url, thumb_url=s.get_thumb_url)
        self.redirect('/post/{}'.format(post.id))


class AsyncHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        save_url = self.get_argument('save_url', None)
        form = self.get_argument('form')
        user = self.get_argument('user')
        if form and form == 'room' and user:
            http_client = AsyncHTTPClient()
            response = yield http_client.fetch(save_url)
            img_content = response.body
            s = SaveUploadPhoto(img_name='x.jpg', static_path=self.settings['static_path'])
            s.upload_pic(img_content=img_content)
            s.make_thumbnail()
            post = self.orm.add_post( image_url=s.get_url, thumb_url=s.get_thumb_url)
            chat = make_chat(msg_body='{} 上传成功一张图片,图片地址为 : 192.168.47.134:8080/post/{}'.format(user,post.id),name='系统',
                             image_url=post.thumb_url,post_id=post.id)
            msg = {
                'html': tornado.escape.to_basestring(
                    self.render_string('message.html', message=chat)
                ),
                'id': chat['id']
            }
            ChatHandler.history_message(msg)
            ChatHandler.send_message(msg)

        else:
            self.write('error')
