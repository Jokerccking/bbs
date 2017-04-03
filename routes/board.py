import uuid

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import abort

from models.board import Board
from routes import current_user, csrf_tokens

main = Blueprint('board', __name__)


@main.route('/')
def index():
    u = current_user()
    if u is None or u.role != 1:
        return redirect(url_for('topic.index'))
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    bs = Board.all()
    return render_template('board/index.html', bs=bs, token=token)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u is None or u.role != 1:
        return redirect(url_for('topic.index'))
    form = request.form.copy()
    Board.new(form)
    return redirect(url_for('topic.index'))


@main.route('/delete/<int:bid>/<token>')
def delete(bid, token):
    u = current_user()
    if u is None or u.role != 1 or csrf_tokens.get(token) != u.id:
        abort(403)
    else:
        csrf_tokens.pop(token)
        board = Board.find(bid)
        board.remove()
        return redirect(url_for('.index'))
