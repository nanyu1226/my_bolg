"""
1.导入扩展
2.实例化一个对象
3.因为是一个扩展,必须要跟app绑定

"""
from flask_script import Manager #命令行启动app服务器,这是一个类库
from apps import create_app
from flask_migrate import MigrateCommand
from apps.models import User,Posts
from apps.extensions import db

app = create_app('default') #指定此刻我们是什么环境
manager = Manager(app) #实例化对象,并跟app完成绑定

manager.add_command('db',MigrateCommand)

@manager.command
def create_test_posts():
    for x in range(2,201):
        content = '内容:%s' % x
        author = User.query.first()
        post = Posts(content=content,user=author)
        db.session.add(post)
        db.session.commit()
    print('帖子添加成功')


#python manage.py db init 生成迁移目录
#python manage.py db migrate 生成迁移脚本
#python manage.py db upgrade 更新数据库

if __name__ == '__main__':
    manager.run()