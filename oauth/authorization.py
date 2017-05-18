from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    render_template,
    make_response,
)
from utils import log
import random, uuid, json
users = {
    'user1': '123',
}

auth_appname = {
    "bbs": "c3baa566-eef2-4dc4-80bb-bc2026147ae1",
}

auth_client_id = {
    "c3baa566-eef2-4dc4-80bb-bc2026147ae1": "http://localhost:2000/authorization",
}
auth_code = {
}
auth_token = {
}

app = Flask(__name__)


def get_auth_code(uri):
    code = str(uuid.uuid4())
    auth_code[code] = uri
    return code


def get_auth_token(uri):
    token = str(uuid.uuid4())
    auth_token[token] = uri
    return token


@app.route('/oauth', methods=['POST', 'GET'])
def oauth():
    if request.args.get('response_type') == 'code':
        client_id = request.args.get('client_id')
        return render_template('login.html', redirect_uri=auth_client_id.get(client_id))
    if request.method == 'POST':
        redirect_uri = request.form.get('redirect_uri')
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        if users.get(user) == pwd:
            code = get_auth_code(redirect_uri)
            data = json.dumps({
                'code': code,
            })
            log(data)
            uri = redirect_uri + '?code={}'.format(code)
            return redirect(uri)

    if request.args.get('grant_type') == 'authorization_code':
        code = request.args.get('code')
        redirect_uri = request.args.get('redirect_uri')
        client_id = request.args.get('client_id')
        if auth_code[code] == redirect_uri and auth_client_id[client_id] == redirect_uri:
            token = get_auth_token(redirect_uri)
            data = json.dumps({
                'access_token': token,
                'token_type': 'example_type',
                'expires_in': 3600,
                'refresh_token': '#',
                'scope': 'abc',
            })
            log(data)
            resp = make_response(data)
            resp.headers['Content-Tye'] = 'application/json'
            resp.headers['Cache-Control'] = 'no-store'
            resp.headers['Pragma'] = 'no-cache'
            return resp


@app.route('/client_register', methods=['POST', 'GET'])
def client_register():
    if request.method == 'GET':
        return render_template('client_register.html')
    else:
        appname = request.form.get('appname')
        redirect_uri = request.form.get('redirect_uri')
        client_id = str(uuid.uuid4())
        auth_appname[appname] = client_id
        auth_client_id[client_id] = redirect_uri
        log(json.dumps(auth_appname), json.dumps(auth_client_id))
        data = {
            'client_id': client_id,
        }
        return json.dumps(data)

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=9001,
    )
    app.run(**config)
