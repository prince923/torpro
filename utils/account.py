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
    if username == DATA['username'] and hashed(password) == DATA['password']:
        return True
    else:
        return False
