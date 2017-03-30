from flask import Blueprint

main = Blueprint('static', __name__)


@main.route('/img/<file>')
def img(file):
    path = 'static/img/' + file
    body = b''
    with open(path, 'rb') as f:
        body += f.read()
    return body


@main.route('/css/<file>')
def css(file):
    path = 'static/css/' + file
    body = b''
    with open(path, 'rb') as f:
        body += f.read()
    return body


@main.route('/js/<file>')
def js(file):
    path = 'static/js/' + file
    body = b''
    with open(path, 'rb') as f:
        body += f.read()
    return body
