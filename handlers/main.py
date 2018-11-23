from tornado import web
from tornado.web import authenticated
import glob
from utils import pictule
from pycket.session import SessionMixin
from utils.account import add_post,get_post,id_get_post


class BaseHandler(web.RequestHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user_info')
        if current_user:
            return current_user
        else:
            return None


class IndexHandler(BaseHandler):
    """
    首页，显示用户关注的图片流
    """
    @authenticated
    def get(self, *args, **kwargs):
        posts = get_post(username=self.current_user)
        self.render('index.html', posts=posts)


class ExploreHandler(BaseHandler):
    """
    发现页,显示最近上传的图片
    """
    @authenticated
    def get(self, *args, **kwargs):
        posts = get_post(username=self.current_user)
        self.render('explore.html', posts=posts)


class PostHandler(BaseHandler):
    """
       详情页，显示图片详情
    """

    @authenticated
    def get(self, post_id):
        post = id_get_post(post_id=post_id)
        if post:
            self.render('post.html', post = post)
        else:
            self.write('post不存在')


class UploadHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render('upload_img.html')

    @authenticated
    def post(self, *args, **kwargs):
        files = self.request.files  # dict
        imgs = files.get('img', None)  # list
        for img in imgs:
            img_name = img['filename']
            img_content = img['body']
            print(img_name)
            image_url = pictule.upload_pic(img_name=img_name, img_content=img_content)
            thumb_url = pictule.make_thumbnail(img_name, (80, 80))
            print(self.current_user)
            add_post(username=self.current_user, image_url=image_url,thumb_url=thumb_url)
        self.write('upload success')

