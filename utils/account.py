from models.account import User



def hashed (text):
    """
    hash加密用户密码
    :param text:
    :return: 加密后的字符串
    """
    import hashlib
    return hashlib.md5(text.encode('utf8')).hexdigest()



DATA = {
    'username': 'wyf',
    'password': hashed('qwe123')
}


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


