import uuid

from flask import abort
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from models.board import Board
from models.topic import Topic
from routes import current_user, csrf_tokens

main = Blueprint('topic', __name__)


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.login'))
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    bs = Board.all()
    ts = Topic.all()
    return render_template('topic/index.html', ts=ts, bs=bs, token=token)


@main.route('/ball/<int:bid>')
def ball(bid):
    u = current_user()
    if u is None:
        return redirect(url_for('index.login'))
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    bs = Board.all()
    ts = Topic.find_all({'bid': bid})
    return render_template('topic/index.html', ts=ts, bs=bs, token=token)


@main.route('/detail/<int:tid>')
def detail(tid):
    t = Topic.get(tid)
    b = Board.find(t.bid)
    return render_template('topic/topic.html', topic=t, board=b)


@main.route('/new')
def new():
    bs = Board.all()
    return render_template('topic/new_topic.html', bs=bs)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form.copy()
    form['uid'] = u.id
    t = Topic.new(form)
    return redirect(url_for('.detail', tid=t.id))


@main.route('/delete/<int:tid>/<token>')
# TODO: CSRF攻击，加入csrf - token验证
def delete(tid, token):
    u = current_user()
    if u is not None and csrf_tokens.get(token) == u.id:
        csrf_tokens.pop(token)
        topic = Topic.find(tid)
        if u.id == topic.uid or u.role == 1:
            topic.remove()
            return redirect(url_for('.index'))
        else:
            abort(403)
    else:
        abort(403)
