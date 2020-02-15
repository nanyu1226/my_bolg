from apps.extensions import db
from datetime import datetime

# id  rid
# 1    0
# 2    0
# 3    0
# 4    1
# 5    3 第五篇帖子是对第3篇帖子的回复(评论)
# rid = 0表示新发表的,没有任何评论
class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer,index=True,default=0)
    content = db.Column(db.Text)
    #datetime.utcnow,格林尼治时间
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    #外建,表名.字段名
    uid = db.Column(db.Integer,db.ForeignKey('users.id'))