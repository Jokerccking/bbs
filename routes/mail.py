from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from models.mail import Mail
from routes import current_user

main = Blueprint('mail', __name__)


@main.route('/')
def index():
    u = current_user()
    return render_template('mail/index.html', user=u)


@main.route('/send/<int:receiver_id>')
def send(receiver_id):
    return render_template('mail/send.html', receiver_id=receiver_id)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form.copy()
    form['sender_id'] = u.id
    Mail.new(form)
    return redirect(url_for('.index'))
