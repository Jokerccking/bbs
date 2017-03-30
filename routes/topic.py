from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from models.topic import Topic
from models.user import User
from routes import current_user

main = Blueprint('topic', __name__)


@main.route('/')
def index():
    ts = Topic.all()
    return render_template('topic/index.html', ts=ts)


@main.route('/detail/<int:tid>')
def detail(tid):
    t = Topic.get(tid)
    u = User.find(t.uid)
    return render_template('topic/topic.html', topic=t, user=u)


@main.route('/new')
def new():
    return render_template('topic/new_topic.html')


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form.copy()
    form['uid'] = u.id
    t = Topic.new(form)
    return redirect(url_for('.detail', tid=t.id))
