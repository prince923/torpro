from .connect import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Table
from datetime import datetime
from .connect import session
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)

    like_posts = relationship('Post',backref='user_like',secondary='like_posts')


    def __repr__(self):
        return 'id:{},username:{},password:{},create_time:{}'.format(
            self.id,
            self.username,
            self.password,
            self.create_time,

        )

    @classmethod
    def add_user(cls, username, password,session):
        user = User(username=username, password=password)
        session.add(user)
        session.commit()

    @classmethod
    def user_is_exists(cls, username,session):
        return session.query(
            exists().where(User.username == username)).scalar()  # return True or False存在为True不存在为False

    @classmethod
    def get_password(cls, username,session):
        user = session.query(User).filter_by(username=username).first()
        if user:
            password = user.password
            return password
        else:
            return None

    @classmethod
    def get_user(cls,username,session):
        user = session.query(User).filter_by(username=username).first()
        if user:
            return user
        else:
            return None


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(100))
    thumb_url = Column(String(100))
    user_id = Column(Integer, ForeignKey('user.id'))
    create_time = Column(DateTime, default=datetime.now)

    user = relationship('User', backref='posts', uselist=True, cascade='all')

    def __repr__(self):
        return "post id {}".format(self.id)

    @classmethod
    def add_post(cls, username, image_url, thumb_url,session):
        user = session.query(User).filter_by(username=username).first()
        if user:
            post = Post(image_url=image_url, thumb_url=thumb_url, user_id=user.id)
            session.add(post)
            session.commit()
            return post
        else:
            return None

    @classmethod
    def get_post(cls, username,session):
        user = session.query(User).filter_by(username=username).first()
        if user:
            posts = user.posts
            return posts
        else:
            return None

    @classmethod
    def id_get_post(cls,post_id,session):
        post  = session.query(Post).filter_by(id=post_id).first()
        return post

    @classmethod
    def get_post_all (cls,session):
        posts = session.query(Post).order_by(Post.id.desc()).all()
        return posts

# 记录用户喜欢那张图片
like_posts = Table('like_posts',Base.metadata,
                   Column('user_id',ForeignKey('user.id'),primary_key=True),
                   Column('post_id',ForeignKey('posts.id'),primary_key=True)
                   )