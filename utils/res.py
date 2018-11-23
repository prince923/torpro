import json


class HttpCode:
    ok = 200
    params_error = 400
    un_auth_error = 403
    method_error = 405
    server_error = 500


def result(code=HttpCode.ok, message='', data=None, kwargs=None):
    json_dict = {'code': code, 'message': message, 'data': data}

    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return json.dumps(json_dict)


def ok():
    return result()


def params_error(message='', data=None):
    """
        参数错误
    """
    return result(HttpCode.params_error, message=message, data=data)


def un_auth_error(message='', data=None):
    """
        权限错误
    """
    return result(code=HttpCode.un_auth_error, message=message, data=data)


def method_error(message='', data=None):
    """
        方法错误
    """
    return result(code=HttpCode.method_error, message=message, data=data)


def server_error(message='', data=None):
    """
        服务器内部错误
    """
    return result(code=HttpCode.server_error, message=message, data=data)