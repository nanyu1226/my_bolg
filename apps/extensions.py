"""
1.导入扩展
2.实例化扩展对象
3.完成扩展对象与app的绑定,调用对象的init_app方法
"""
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# 导入Mail类
from flask_mail import Mail
# 导入登录类
from flask_login import LoginManager
# 上传文件的类 及相关设置
from flask_uploads import UploadSet,IMAGES
# 保证上传的文件与app绑定
from flask_uploads import configure_uploads,patch_request_class
# 导入时间管理插件,封装的是moment.js
from flask_moment import Moment


#创建Bootstrap,SQLALchemy,Migrate扩展对象
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
#实例化一个登录管理对象
login_manager = LoginManager()
#设置只能上传图片
photos = UploadSet('photos',IMAGES)
# 实例化一个时间管理对象
moment = Moment()

#封装一个方法,让其跟app完成绑定
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)

    mail.init_app(app)
    # 时间管理对象绑定app
    moment.init_app(app)

    # 登录管理的初始化,与app绑定
    login_manager.init_app(app)
    #指定登录的url地址是哪个
    login_manager.login_view = 'user.login'#这是一个蓝本
    #登录的提示信息,如果用户没有登录如何去提示他
    login_manager.login_message='请先登录才可以访问'
    #设置session的保护级别:
    #None,没有任何的保护;basic,最基本的;strong,最严格的
    login_manager.session_protection = 'strong'
    ##然后到model写个方法,登录认证后的回调方法

    #上传文件的初始化
    configure_uploads(app,photos)
    #设置size为None,则采用Config中自定义的文件大小,不设置的话默认文件大小64M
    patch_request_class(app,size=None)