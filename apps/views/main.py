from flask import Blueprint,render_template,request,flash,redirect,url_for
from apps.forms import PostsForm
from flask_login import current_user
from apps.models import Posts
from apps.extensions import db


# 实例化蓝本对象main是蓝本对象,'main'是蓝本的名字,二者有区别
main = Blueprint('main',__name__)

@main.route('/',methods=['GET','POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        #判断用户是否登录
        if current_user.is_authenticated:
            #获取当前登录用户
            u = current_user._get_current_object()
            p = Posts(content=form.content.data,user=u)
            db.session.add(p)
            db.session.commit()
            return redirect((url_for('main.index')))
        else:
            flash('请先登录')
            return redirect(url_for('user.login'))

    # 取出所有的博客,类视图,get方法
    # rid = 0,表示是发表的,而不是评论
    # posts = Posts.query.filter_by(rid=0).all()

    # 接收前端用户提交的页码
    page = request.args.get('page',1,type=int)
    # 查询:按照格林尼治时间,desc倒序,pagenate,page:传递过来的请求页的页码,per_page每页展示多少条,
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page,per_page=5,error_out=False)
    # pagination.items:当前页的所有对象
    posts = pagination.items
    return render_template('main/index.html',form=form,posts=posts,pagination=pagination)