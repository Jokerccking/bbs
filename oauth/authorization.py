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

# 所有的用户
users = {
    'user1': '123',
}
# 所有的注册的app
# todo 用户注册之后自动添加到数据库，用户可以查询app对应的id
auth_appname = {
    "bbs": "c3baa566-eef2-4dc4-80bb-bc2026147ae1",
}
# app id对应的URI
# 在client注册的时候添加
auth_client_id = {
    "c3baa566-eef2-4dc4-80bb-bc2026147ae1": "http://localhost:2000/authorization",
}
# 临时生成的授权码，短期有效，使用一次有效
auth_code = {
}
# todo 令牌，有效时限？重新生成令牌？
auth_token = {
}

app = Flask(__name__)


def get_auth_code(uri):
    """
    生成随机授权码code
    :param uri:
    :return:
    """
    code = str(uuid.uuid4())
    auth_code[code] = uri
    return code


def get_auth_token(uri):
    """
    生成随机令牌token
    :param uri:
    :return:
    """
    token = str(uuid.uuid4())
    auth_token[token] = uri
    return token


@app.route('/oauth', methods=['POST', 'GET'])
def oauth():
    """
    授权认证服务端路由
    :return:
    """
    # client申请授权码，将用户导向登录页面
    if request.args.get('response_type') == 'code':
        client_id = request.args.get('client_id')
        return render_template('login.html', redirect_uri=auth_client_id.get(client_id))

    # 用户同意授权，生成随机授权码，在Location中返回，todo 安全？
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

    # client携code和重定向URI申请令牌，验证code，URI和client_id后，以json形式发放令牌
    if request.args.get('grant_type') == 'authorization_code':
        code = request.args.get('code')
        redirect_uri = request.args.get('redirect_uri')
        client_id = request.args.get('client_id')
        if auth_code[code] == redirect_uri and auth_client_id[client_id] == redirect_uri:
            token = get_auth_token(redirect_uri)
            auth_code.pop(code)
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
    """
    client在oauth认证之前，携appname向认和重定向URI证服务器申请client_id进行备案
    返回 client_id
    :return:
    """
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
