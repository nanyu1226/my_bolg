import os
from flask import (
    Blueprint,
    render_template,
    views,
    request,
    flash,
    redirect,
    url_for,
    current_app,
    send_from_directory
)
from apps.models import User
from apps.forms import RegisterForm,LoginForm,UploadForm
from apps.extensions import db
from apps.email import send_mail
from flask_login import login_user,logout_user,login_required,current_user
from PIL import Image

user = Blueprint('user',__name__)

class RegisterView(views.MethodView):
    def get(self,message=None):
        form = RegisterForm()
        return render_template('user/register.html',form=form,message=message)

    def post(self):
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            u = User(username=username,password=password,email=email)
            db.session.add(u)
            db.session.commit()
            #如果注册成功,生成token,token会发送验证给邮箱,在model中写
            token = u.gernerate_active_token()

            #发送邮件
            send_mail(u.email,'账户激活','mail/activate',username=u.username,token=token)

            #在前端页面弹出消息,提示用户 flash,全局的模板,都可以直接遍历它
            flash("恭喜注册成功,请点击链接完成激活")
            return redirect(url_for('main.index'))
        else:
            return self.get(message="您的输入不符合要求")

user.add_url_rule('/register/',view_func=RegisterView.as_view('register'))

# 激活用户
#http://127.0.0.1:5000/activate/你的token
@user.route('/activate/<token>')
def activate(token):
    if User.check_active_token(token):
        flash('账户已经激活')
        return redirect(url_for('user.login'))
    else:
        return redirect(url_for('main.index'))

#登录的类视图
class LoginView(views.MethodView):
    def get(self,message=None):
        form = LoginForm()
        return render_template('user/login.html',form=form,message=message)

    def post(self):
        # 实例化表单对象
        form = LoginForm(request.form)
        if form.validate_on_submit():
            # 根据用户输入的用户名,去数据库中查询
            u = User.query.filter_by(username=form.username.data).first()
            if not u:
                flash('该用户不存在')
                return redirect(url_for('user.login'))
            #激活验证
            elif not u.confirmed:
                flash('请先移步邮箱,激活该用户')
                return redirect(url_for('main.index'))
            #密码验证
            elif u.verify_password(form.password.data):
                #1.将用户id或者用户名写入session
                #2.如果点击了记住我,那么让过期时间延长
                #duration = timedelta(seconds=100),设置过期时间
                #login_user(u,remember=form.remember.data,duration=duration)
                login_user(u,remember=form.remember.data)
                flash('登录成功')
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                return self.get(message='您的输入不符合要求')


user.add_url_rule('/login/',view_func=LoginView.as_view('login'))

@user.route('/logout/')
def logout():
    logout_user()
    flash('注销登陆成功')
    return redirect(url_for('main.index'))

#路由保护
@user.route('/profile/')
@login_required #必须先登录才可以查看个人中心,这就是路保护
def profile():
    return '个人中心'

@user.route('/change_icon/',methods=['GET','POST'])
@login_required
def change_icon():
    img_url = None
    form = UploadForm()
    # 以下按照原生的文件上传,来写
    if request.method == "POST":
        file = request.files.get("icon")# 可行,拿到文件对象
        if file and allowed_file(file.filename):
            # 获取文件的后缀
            suffix = os.path.splitext(file.filename)[1]
            # 将生成的文件名与原来的后缀拼接起来,做成新的文件名filename
            filename = random_string()+suffix
            file.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename))

            # 重新设置图片尺寸
            # 1.打开图片;2.图片处理;3.保存图片
            # 指定待处理图片的路径
            pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
            # 打开图片
            img = Image.open(pathname)
            #重设尺寸
            img.thumbnail((128,128))
            #保存修改
            img.save(pathname)

            # 文件上传成功以后,把static.uploads中非默认的原有图片给删除掉
            if current_user.icon != 'default.jpg':
                os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
            # 更新数据库
            current_user.icon = filename
            db.session.add(current_user)
            db.session.commit()
            flash('头像已经保存')

            return redirect(url_for('user.change_icon'))
    #图片位置根据图片名生成url
    img_url = url_for('user.uploaded',filename=current_user.icon)
    return render_template('user/change_icon.html',form=form,img_url=img_url)

# 判断上传文件的后缀名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in current_app.config['ALLOWED_EXTENSIONS']

#生成随机字符串,命名上传的文件,防止上传之后覆盖同名但是内容不一样的文件
def random_string(lenth=16):
    import random
    base_dir = 'abcdefghijklmnopqrstubwxyz0123456789'
    return ''.join(random.choice(base_dir) for i in range(lenth))



# 获取上传文件(将文件暴露给一个url,让浏览器可以直接加载)
@user.route('/uploaded/<filename>')
def uploaded(filename):
    #send_from_directory:安全地发送文件
    return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'],filename)



