"""
所有的实例放在这里

"""
from flask import Flask, render_template
from apps.views import config_blueprint # config_blueprint是一个蓝本注册函数
from apps.extensions import config_extensions
from apps.config import config
#工厂设计模式

def create_app(config_name):
    """
    Create an app, configure database environment.
    Bind app to database,config_blueprint,config_extensions and
    :param config_name:
    :return:
    """
    # 创建实例
    app = Flask(__name__) # 实参app
    # 初始化配置文件
    app.config.from_object(config[config_name])#告诉我找那个配置文件

    #调用初始化方法 让配置文件生效
    config[config_name].init_app(app)
    config_blueprint(app) # 形参app
    config_extensions(app)
    config_errorhandler(app) #错误页面配置视图函数与app绑定
    return app

# 配置错误页面
def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

