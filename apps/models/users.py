"""
将模型映射到数据库,3步骤
1.init, 生成迁移目录 ,这个步骤只执行一次,只要生成了迁移目录就不再执行了
2.migrate,生成迁移脚本,只要模型改变,就执行,生成新的脚本
3.upgrade,更新,1 or 2执行,3,就执行
"""

from apps.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import flash, current_app  # current_app代表当前实例项目
from flask_login import UserMixin
from apps.models.posts import Posts


# 继承自UserMixin,能够检测到底有没有登录.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)  # 是否激活
    icon = db.Column(db.String(64), default='default.jpg')
    # 创建表关系:posts是本模型的属性;'Posts'是另一个需要建立关系的模型;
    # 'user'是给Posts模型增加一个属性Posts.user,可直接调用与之相关联的本模型中的对象
    posts = db.relationship('Posts', backref='user', lazy='dynamic')
    # 添加收藏操作,跟中间表建立关联
    favorites = db.relationship('Posts',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')

    # 保护密码属性
    @property
    def password(self):  # 对外字段password对内password_hash
        raise AttributeError("密码不可读属性")

    # 对外password,对内,password_hash
    # 设置密码 保存加密后的hash值
    @password.setter
    def password(self, password):  # password是用户提交过来的密码
        self.password_hash = generate_password_hash(password)

    # 用户登录,获取用户输入的密码,先加密
    # 然后跟数据库中的数据进行比较
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成token的方法
    def gernerate_active_token(self, expires_in=3600):
        """
        生成token,发送给用户
        :param expires_in: 过期时间
        :return:
        """
        # current_app.config['SECRET_KEY'],加密用的
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})  # 藏一个id

    # 解密token
    @staticmethod
    def check_active_token(token):
        # token使用户带过来的
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 解密token
        except:
            return False
        u = User.query.get(data.get('id'))
        if not u:
            flash('用户不存在')
            return False
        if not u.confirmed:
            u.confirmed = True
            db.session.add(u)
            db.session.commit()
        return True

    #判断用户是否收藏了指定的博客
    def is_favorite(self,pid):
        # 获取用户收藏的所有帖子
        # 判断指定的博客是否在列表中
        favorites = self.favorites.all()  # 这是所有的收藏的帖子对象
        # 从favorites中过滤出指定的帖子,如果存在则表示收藏了
        posts = list(filter(lambda p:p.id==pid,favorites))
        if len(posts) > 0:
            return True
        else:
            return False

    # 收藏指定的博客,向users.favorites字段添加帖子对象
    def add_favorite(self,pid):
        #模型中favorites代表用户的收藏
        p = Posts.query.get(pid)
        self.favorites.append(p)

    # 取消收藏博客,从users.favorites字段删除帖子对象
    def del_favorite(self,pid):
        p = Posts.query.get(pid)
        self.favorites.append(p)

# 登陆成功以后的回调函数
# 你登录成功了,拿到你的详细信息,然后在页面上显示,eg:你好玉玉,
@login_manager.user_loader
def load_user(uid):  # 传递用户的id
    return User.query.get(int(uid))
