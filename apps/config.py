"""
数据库配置等
"""
import os


# 获取项目的主目录apps目录的绝对路径
# __file__当前文件所在的位置
# os.path.dirname
# 返回规范绝对路径
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    #先从环境变量中找,如果有取出来,没有使用后面的秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ASFKJA123456'

    # 允许上传文件的大小
    MAX_CONTENT_LENGTH = 8*1024*1024 #最大为8M
    # 上传文件的位置
    UPLOADED_PHOTOS_DEST= os.path.join(base_dir,'static/uploads')
    # 上传文件限制只能是图片格式(通过后缀进行)
    ALLOWED_EXTENSIONS =set(['jpg','jpeg','png','gif'])

    # 邮件配置,smtp是邮件发送服务器,pop3是邮件接收服务器
    #借助qq,163等进行邮件发送
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USERNAME = '122671487@qq.com'
    # 这里不是邮箱的密码,而是授权码
    MAIL_PASSWORD = 'khgbanyrvjubbjgf'

    #bootstrap使用本地的库
    BOOTSTRAP_SERVE_LOCAL = True

    #静态方法,完成特定环境的初始化
    @staticmethod
    def init_app(app):
        pass

#开发环境
class DevelopmentConfig(Config):
    DB_USERNAME = 'root'
    DB_PASSWORD = '123'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME='1904project'
    DB_URI='mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'%(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 使用sqlite,是一种文件的形式,进行数据库配置

#测试环境
class TestingConfig(Config):
    # 数据库配置 sqlite是一个文件,设置存储位置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'project-test.sqlite')


#生产环境
class ProductionConfig(Config):
    # 数据库配置 sqlite是一个文件,设置存储位置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'project-product.sqlite')


#配置字典 方便设置
config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'projection':ProductionConfig,
    'default':DevelopmentConfig
}