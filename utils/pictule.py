def upload_pic (img_name,img_content):
    with open('static/image/upload/{}'.format(img_name), 'wb') as f:
        f.write(img_content)


def make_thumbnail(img_name):
    """
    :param img_name:  保存的图片名字

    """
    from PIL import Image
    import os
    file, ext = os.path.splitext(img_name)  # 分离文件名与扩展名
    im = Image.open('static/image/upload/{}'.format(img_name))
    im.thumbnail((80, 80))
    im.save("static/image/upload/thumbs/{}_{}x{}.png".format(file, 80, 80), 'PNG')  # 把缩放后的图像用png格式保存: