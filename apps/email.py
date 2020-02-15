"""
与邮件相关的的东西为何单独
因为有很多地方,邮件需要单独使用

邮件,可以通过网页打开,也可以通过客户端打开
"""
#导入mail对象
from apps.extensions import mail
from flask_mail import Message
#导入当前实例
from flask import current_app,render_template
#导入创建多线程的类
from threading import Thread
#异步发送
def async_send_mail(app,msg):
    #发送邮件需要上下文,新的线程没有上下文,需要手动创建乡下文
    #新的线程没有上下文,
    with app.app_context():#手动创建上下文,将当前app的上下文赋值给新的线程
        #发送邮件
        mail.send(message=msg)

#封装函数用来发送邮件
def send_mail(to,subject,template,**kwargs):
    """

    :param to:
    :param subject:
    :param template:
    :param kwargs:
    :return:
    """
    app = current_app._get_current_object()  #这里current_app 必须调用_get_current_object方法
    #创建邮件发送对象
    msg = Message(subject=subject,recipients=[to],sender=app.config['MAIL_USERNAME'])

    #客户端看到的内容
    msg.body = render_template(template + '.txt',**kwargs)
    #网页看到的内容
    msg.html = render_template(template + '.html',**kwargs)

    #创建线程发送邮件
    thr = Thread(target=async_send_mail,args=[app,msg])
    #启动线程
    thr.start()

    return thr