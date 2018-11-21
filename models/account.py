from .connect import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


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
