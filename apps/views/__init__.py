"""
我们需要将蓝本同一注册完成以后 再注册
因为后便可能扩展多个蓝本,因此需要封装一个方法,批量完成蓝本注册

"""
from .main import main
from .user import user
from .posts import posts

DEFAULT_BLUEPRINT = (
    (main,''),
    (user,'/user'),
    (posts,'/posts'),
)

# 单独封装一个方法,批量完成蓝本注册
def config_blueprint(app):
    for blueprint,url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint,url_prefix=url_prefix)