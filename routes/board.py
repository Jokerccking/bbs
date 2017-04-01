from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from models.board import Board

main = Blueprint('board', __name__)


@main.route('/')
def index():
    bs = Board.all()
    return render_template('board/index.html', bs=bs)


@main.route('/add', methods=['POST'])
def add():
    form = request.form.copy()
    Board.new(form)
    return redirect(url_for('topic.index'))
