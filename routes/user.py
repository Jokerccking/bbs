# 1，拆分页面
# 1.1 index页面：
#       欢迎，
#       登录，link，点击进入login页面，
#       注册，link，点击进入register页面，
#       退出，link，点击后退出登录，
#       app入口：link-todo，blog
# 1.2 login页面：
#       欢迎登录
#       form，post，
#       用户名，密码，提交按钮
# 1.3 register页面：
#       欢迎注册
#       form， post
#       用户名，密码，提交按钮
# 1.4 todo页面：
#       欢迎你xxx
#       todolist

# 2，组织数据
#   user：
#   id，username，password，todos(),
#   topic:
#   id,uid,content,ct,
#

# 3, 逻辑详情：
#       访问index页面，登录跳转到登录，
#       登录：成功返回index，失败返回login
#       注册：成功返回index，失败返回register
#       topic：成功进入topic，失败跳转login

# 4, 实现代码，一点点补全

# 5，美化页面

# 6，交互细节
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
)

from models.user import User

main = Blueprint('index', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        u = User.validate_login(request.form)
        if u is None:
            flash('用户名或密码不正确，请重新登录！')
            return render_template('login.html')
        else:
            session['uid'] = u.id
            flash('登录成功！')
            flash('欢迎你，{}!'.format(u.username))
            return redirect(url_for('.index'))
    return render_template('login.html')


@main.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        u = User.validate_register(request.form.copy())
        if u is None:
            return redirect(url_for('.index'))
        return redirect(url_for('.login'))
    return render_template('register.html')


@main.route('/logout')
def logout():
    session.pop('uid', None)
    flash('注销成功！')
    return redirect(url_for('.index'))
