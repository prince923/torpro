def upload_pic (img_name,img_content):
    with open('static/image/upload/{}'.format(img_name), 'wb') as f:
        f.write(img_content)
    image_url = 'image/upload/{}'.format(img_name)
    return image_url


def make_thumbnail(img_name,size):
    """
    :param img_name:  保存的图片名字
    :param size: 图片大小 tuple
    """
    from PIL import Image
    import os
    file, ext = os.path.splitext(img_name)  # 分离文件名与扩展名
    im = Image.open('static/image/upload/{}'.format(img_name))
    im.thumbnail(size)
    im.save("static/image/upload/thumbs/{}_{}x{}.png".format(file, size[0], size[1]), 'PNG')  # 把缩放后的图像用png格式保存:
    thumb_url = "image/upload/thumbs/{}_{}x{}.png".format(file,size[0],size[1])
    return thumb_url