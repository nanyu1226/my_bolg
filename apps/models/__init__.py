from .users import User
from .posts import Posts

# 添加中间表collections,左 多对多 关系
from apps.extensions import db
collections = db.Table('collections',
   db.Column('users_id',db.Integer,db.ForeignKey('users.id')),
   db.Column('posts_id',db.Integer,db.ForeignKey('posts.id'))
)