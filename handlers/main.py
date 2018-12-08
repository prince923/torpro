from tornado import web
from tornado.web import authenticated
from utils.pictule import SaveUploadPhoto
from pycket.session import SessionMixin
from utils.account import add_post,get_post,id_get_post,get_all_post,get_like_posts,get_count


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
        posts = get_all_post()
        self.render('explore.html', posts=posts)


class PostHandler(BaseHandler):
    """
       详情页，显示图片详情
    """

    @authenticated
    def get(self, post_id):
        post = id_get_post(post_id=post_id)
        count=get_count(post_id=post_id)
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
            post = add_post(username=self.current_user, image_url=s.get_url,thumb_url=s.get_thumb_url)
        self.redirect('/post/{}'.format(post.id))


class ProfileHandler(BaseHandler):
    """
    展示用户上传和喜欢的图片
    """

    @authenticated
    def get(self, *args, **kwargs):
        username = self.get_argument('username','')
        if username:
            posts = get_post(username=username)
            like_posts = get_like_posts(username=username)
        else:
            username=self.current_user
            posts = get_post(username=username)
            like_posts = get_like_posts(username=username)
        self.render('profile.html',posts=posts,like_posts=like_posts,username=username)

    def post(self, *args, **kwargs):
        pass





