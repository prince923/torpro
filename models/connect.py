from sqlalchemy import create_engine

HOSTNAME = '192.168.48.134'   # 主机ip   （看当前py文件运行在哪）
PORT = '3306'    # mysql 端口
DATABASE = 'torpro'    # 数据库名
USERNAME = 'admin'   # 用户名
PASSWORD = 'Root110qwe'   # 密码

db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE
)
#   创建连接
engine = create_engine(db_url)   #  返回一个类似于类的东西

from sqlalchemy.ext.declarative import declarative_base
# 创建一个基类，以后所有的表对应的类都继承自这个基类
Base = declarative_base(engine)

#  增删改查就需要创建会话
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()

#  测试连接
if __name__ == '__main__':
    connection = engine.connect()        # 实例化
