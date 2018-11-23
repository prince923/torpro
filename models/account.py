from .connect import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .connect import session
from sqlalchemy.sql import exists


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return 'id:{},username:{},password:{},create_time:{}'.format(
            self.id,
            self.username,
            self.password,
            self.create_time,

        )

    @classmethod
    def add_user(cls, username, password):
        user = User(username=username, password=password)
        session.add(user)
        session.commit()

    @classmethod
    def user_is_exists(cls, username):
         return session.query(exists().where(User.username == username)).scalar()    # return True or False  存在为True不存在为False

    @classmethod
    def get_password (cls,username):
        user = session.query(User).filter_by(username=username).first()
        if user:
            password = user.password
            return password
        else:
            return None
