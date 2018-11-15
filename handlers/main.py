from tornado import web

class IndexHandler(web.RequestHandler):
    """
    首页，显示用户关注的图片流
    """
    def get(self, *args, **kwargs):
        self.render('index.html')


class ExploreHandler(web.RequestHandler):
    """
    发现页,显示最近上传的图片
    """
    def get(self, *args, **kwargs):
        self.render('explore.html')


class PostHandler(web.RequestHandler):
    """
       详情页，显示图片详情
    """
    def get(self, post_id):
        self.render('post.html',post_id=post_id)