#所有的表单输入格式验证类都继承自FlaskForm这个类
from flask_wtf import FlaskForm  # 导入
#导入表单输入的字段类型,
#StringField,represents an `<input type='text'>`
#PasswordField,except renders an `<input type='text'>`, also, whatever value is accepted, never rendered back to the \
#browser
#SubmitField represents an `<input type='submit'>`. This allows checking if a given submit button has been pressed.
#BooleanField represents an `<input type='checkbox'>`
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
)
#DataRequired表示字段不能为空,Length(min,max)长度要求,message='返回不符合要求的提示'
from wtforms.validators import DataRequired,Length,EqualTo,Email
from wtforms.validators import ValidationError
from apps.models import User
from flask_wtf.file import FileRequired,FileAllowed,FileField
from apps.extensions import photos

# 用户注册表单输入格式验证
class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,30,message="请输入6到30位的用户名")])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,30,message="请输入6到30位的密码")])
    confirm = PasswordField('确认密码',validators=[EqualTo('password',message="两次密码输入不一致")])
    email = StringField('邮箱',validators=[Email(message="邮箱格式不正确")])
    submit = SubmitField('立即注册')

    # 与数据库中已有的数据进行对比,检查是否重复
    # validate_字段名 作为方法名 对字段进一步验证
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            #抛出异常
            raise ValidationError("该用户名已存在!")

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱已注册!")

# 登录表单:登录名 密码 是否记住我 立即登录
class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,30,message="请输入6到30位的用户名")])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,30,message="请输入6到30位的密码")])
    remember  = BooleanField('记住我')
    submit = SubmitField('立即登录')

# 头像上传表单
class UploadForm(FlaskForm):
    icon = FileField('头像',validators=[FileRequired(),FileAllowed(photos,message='只能上传图片')])
    submit = SubmitField('立即上传')