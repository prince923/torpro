from tornado import web
from tornado.web import authenticated
from utils.pictule import SaveUploadPhoto
from pycket.session import SessionMixin
from utils.account import HandlerOrm
from models.connect import Session


class BaseHandler(web.RequestHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user_info')
        if current_user:
            return current_user
        else:
            return None

    def prepare(self):
        self.db_session = Session()
        self.orm = HandlerOrm(self.db_session,self.current_user)

    def on_finish(self):
        self.db_session.close()




class IndexHandler(BaseHandler):
    """
    首页，显示用户关注的图片流
    """
    @authenticated
    def get(self, *args, **kwargs):
        posts = self.orm.get_post()
        self.render('index.html', posts=posts)


class ExploreHandler(BaseHandler):
    """
    发现页,显示最近上传的图片
    """
    @authenticated
    def get(self, *args, **kwargs):
        posts = self.orm.get_all_post()
        self.render('explore.html', posts=posts)


class PostHandler(BaseHandler):
    """
       详情页，显示图片详情
    """

    @authenticated
    def get(self, post_id):
        post = self.orm.id_get_post(post_id=post_id)
        count=self.orm.get_count(post_id=post_id)
        if post:
            self.render('post.html', post = post,count=count)
        else:
            self.write('post不存在')


class UploadHandler(BaseHandler):
    """
    用户上传图片得接口
    """
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
            s = SaveUploadPhoto(img_name=img_name,static_path=self.settings['static_path'])
            s.upload_pic(img_content=img_content)
            s.make_thumbnail()
            post = self.orm.add_post(image_url=s.get_url,thumb_url=s.get_thumb_url)
        self.redirect('/post/{}'.format(post.id))


class ProfileHandler(BaseHandler):
    """
    展示用户上传和喜欢的图片
    """

    @authenticated
    def get(self, *args, **kwargs):
        username = self.get_argument('username','')
        if username:
            self.orm.username = username   # 临时修改username 属性为获取到的username
            posts =self.orm.get_post()
            like_posts = self.orm.get_like_posts()
        else:
            posts =self.orm.get_post()
            like_posts =self.orm. get_like_posts()
        self.render('profile.html',posts=posts,like_posts=like_posts,username=username)







