from tornado import web
from tornado.web import authenticated
import glob
from utils import pictule
from pycket.session import SessionMixin

class BaseHandler(web.RequestHandler,SessionMixin):
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
        img_urls = glob.glob(r'static/image/upload/*.png')
        self.render('index.html', img_urls=img_urls)


class ExploreHandler(BaseHandler):
    """
    发现页,显示最近上传的图片
    """
    @authenticated
    def get(self, *args, **kwargs):
        thumbnails_url = glob.glob(r'static/image/upload/thumbs/*')
        self.render('explore.html', thumbnails_url=thumbnails_url)


class PostHandler(BaseHandler):
    """
       详情页，显示图片详情
    """
    @authenticated
    def get(self, post_id):
        self.render('post.html', post_id=post_id)


class UploadHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render('upload_img.html')

    def post(self, *args, **kwargs):
        files = self.request.files  # dict
        imgs = files.get('img', None)  # list
        for img in imgs:
            img_name = img['filename']
            img_content = img['body']
            print(img_name)
            pictule.upload_pic(img_name=img_name,img_content=img_content)
            pictule.make_thumbnail(img_name)
        self.write('upload success')
