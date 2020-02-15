from flask import Blueprint, render_template, jsonify
from apps.extensions import db
# 导入当前用户
from flask_login import current_user

posts = Blueprint('posts',__name__)

@posts.route('/collect/<int:pid>',methods=['GET','POST'])
def collect(pid):
    if current_user.is_favorite(pid):
        current_user.del_favorite(pid)
        db.session.commit()
    else:
        current_user.add_favorite(pid)
        db.session.commit()
    return jsonify({'result':'ok'})
