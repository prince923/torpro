from .main import BaseHandler
import requests
from utils.pictule import SaveUploadPhoto
from tornado.web import authenticated
from utils.account import add_post
from tornado.httpclient import AsyncHTTPClient
import tornado.gen

class SyncHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        save_url = self.get_argument('save_url', None)  # 会阻塞
        response = requests.get(save_url)
        img_content = response.content
        s = SaveUploadPhoto(img_name='x.jpg', static_path=self.settings['static_path'])
        s.upload_pic(img_content=img_content)
        s.make_thumbnail()
        post = add_post(username=self.current_user, image_url=s.get_url, thumb_url=s.get_thumb_url)
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
            post = add_post(username=user, image_url=s.get_url, thumb_url=s.get_thumb_url)
            self.write(str(post.id))
        else:
            self.write('error')
