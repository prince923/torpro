import os
import uuid



class SaveUploadPhoto(object):
    upload_path = 'image/upload'
    thumb_path = 'image/upload/thumbs'
    size = (200,200)

    def __init__(self,img_name,static_path):
        self.img_name = img_name
        self.static_path = static_path
        self.new_name = self.gen_new_name


    @property
    def gen_new_name(self):
        """
        生成唯一的图片名
        :return:
        """
        _,ext = os.path.splitext(self.img_name)
        news_name = uuid.uuid4().hex + ext
        return news_name

    def upload_pic(self, img_content):
        """
        保存上传的图片
        :param img_content:
        :return:
        """
        upload_pic_path = os.path.join(self.static_path,self.upload_path)
        with open(upload_pic_path+'/{}'.format(self.new_name), 'wb') as f:
            f.write(img_content)

    @property
    def get_url (self):
        """
        返回图片地址
        :return:
        """
        return os.path.join(self.upload_path,self.new_name)


    def make_thumbnail(self):
        """
        生成上传图片缩略图
        """
        from PIL import Image
        file, ext = os.path.splitext(self.new_name)  # 分离文件名与扩展名
        upload_dir = os.path.join(self.static_path,self.upload_path,self.new_name)
        im = Image.open(upload_dir)
        im.thumbnail(self.size)
        im.save(self.static_path+'/'+self.thumb_path+'/'+'{}_{}x{}.png'.format(file, self.size[0], self.size[1]), 'PNG')  # 把缩放后的图像用png格式保存



    @property
    def get_thumb_url(self):
        """
        生成缩略图地址
        :return:
        """
        file, ext = os.path.splitext(self.new_name)
        thumb_url = self.thumb_path+'/'+'{}_{}x{}.png'.format(file, self.size[0],self.size[1])
        return thumb_url

