from models.account import User,Post
from models.connect import session
import uuid



def hashed (text):
    """
    hash加密用户密码
    :param text:
    :return: 加密后的字符串
    """
    import hashlib
    return hashlib.md5(text.encode('utf8')).hexdigest()



def authenticate(username, password):
    """
    用户名和密码验证
    :param username: 用户名
    :param password:  密码
    :return: True 或者 False  True代表验证通过，False代表验证没过
    """
    hash_password = hashed(password)
    if hash_password == User.get_password(username=username):
        return True
    else:
        return False


def register (username,password):
    """
    用户注册
    :param username:
    :param password:
    :return:
    """
    if not User.user_is_exists(username=username):
        User.add_user(username=username, password=hashed(password))
        return {'msg':'ok'}
    else:
        return {'msg':'此用户已经存在'}


def add_post(username,image_url,thumb_url):
    """
    往数据库里加入图片信息
    :param username:
    :param image_url:
    :param thumb_url:
    :return:
    """
    return Post.add_post(username=username,image_url=image_url,thumb_url=thumb_url)


def get_post (username):
    """
    获取用户对应的图片
    :param username:
    :return:
    """
    return Post.get_post(username=username)

def id_get_post(post_id):
    """
    根据post_id 获取对应的post
    :param post_id:
    :return:
    """
    return Post.id_get_post(post_id=post_id)


def get_all_post():
    """
    按降序获取所有的post
    :return:
    """
    return Post.get_post_all()


def get_user(username):
    """
    根据用户名返回用户对象
    :param username:
    :return: 如果有返回单个用户对象,否则返回None
    """
    return User.get_user(username=username)


def get_like_posts(username):
    """
    获取用户喜欢的图片
    :param username:
    :return:
    """
    user = get_user(username=username)
    return  user. like_posts


def get_count(post_id):
    """
    获取单个图片被多少人标记为喜欢
    :param post_id:
    :return:
    """
    post = id_get_post(post_id=post_id)
    user_like = post.user_like
    count = len(user_like)
    return count


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

