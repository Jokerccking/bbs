from flask import Blueprint
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from models.topic import Reply
from routes import current_user

main = Blueprint('reply', __name__)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form.copy()
    form['uid'] = u.id
    r = Reply.new(form)
    return redirect(url_for('topic.detail', tid=r.tid))
