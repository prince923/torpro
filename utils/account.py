from models.account import User,Post
import uuid



def hashed (text):
    """
    hash加密用户密码
    :param text:
    :return: 加密后的字符串
    """
    import hashlib
    return hashlib.md5(text.encode('utf8')).hexdigest()





def make_chat(msg_body,name,image_url = None,post_id = None):
    """
    用于 websocket 构造消息
    :param msg_body:  接受到的消息
    :param name:  名字
    :param image_url : 图片地址默认为None
    :param post_id: 图片id
    :return:  chat     type:dict
    """
    chat = {
        'id': str(uuid.uuid4()),
        'body': msg_body,
        'user': name,
        'image_url':image_url,
        'post_id':post_id
    }
    return chat


class HandlerOrm(object):
    """
    db_session : Session 实例化的对象
    username :   获取到的用户姓名
    """
    def __init__(self,db_session,username):
        self.db = db_session
        self.username = username


    def get_post(self):
        """
        获取用户对应的图片

        :return:
        """
        return Post.get_post(username=self.username,session=self.db)


    def add_post(self, image_url, thumb_url):
        """
        往数据库里加入图片信息
        :param image_url:
        :param thumb_url:
        :return: post 实例对象
        """
        return Post.add_post(username=self.username, image_url=image_url, thumb_url=thumb_url,session=self.db)


    def id_get_post(self,post_id):
        """
        根据post_id 获取对应的post
        :param post_id:
        :return:
        """
        return Post.id_get_post(post_id=post_id,session=self.db)


    def get_all_post(self):
        """
        按降序获取所有的post
        :return:
        """
        return Post.get_post_all(session=self.db)


    def get_user(self):
        """
        根据用户名返回用户对象
        :return: 如果有返回单个用户对象,否则返回None
        """
        return User.get_user(username=self.username,session=self.db)


    def get_like_posts(self):
        """
        获取用户喜欢的图片
        :return:
        """
        user = self.get_user()
        return user.like_posts


    def get_count(self,post_id):
        """
        获取单个图片被多少人标记为喜欢
        :param post_id:
        :return:
        """
        post = self.id_get_post(post_id=post_id)
        user_like = post.user_like
        count = len(user_like)
        return count

    def authenticate(self,password):
        """
        用户名和密码验证
        :param password:  密码
        :return: True 或者 False  True代表验证通过，False代表验证没过
        """
        hash_password = hashed(password)
        if hash_password == User.get_password(username=self.username,session=self.db):
            return True
        else:
            return False


    def register(self, password):
        """
        用户注册
        :param password:
        :return:
        """
        if not User.user_is_exists(username=self.username,session=self.db):
            User.add_user(username=self.username, password=hashed(password),session=self.db)
            return {'msg': 'ok'}
        else:
            return {'msg': '此用户已经存在'}


