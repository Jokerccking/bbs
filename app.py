import markdown2
from flask import Flask

from config.config import secret_key, hp
from routes.user import main as routes_user
from routes.topic import main as routes_topic
from routes.reply import main as routes_reply
from routes.board import main as routes_board
from routes.mail import main as routes_mail

# 使用flask框架并加密session
app = Flask(__name__)
app.secret_key = secret_key

# 注册蓝图
app.register_blueprint(routes_user)
app.register_blueprint(routes_topic, url_prefix='/topic')
app.register_blueprint(routes_reply, url_prefix='/reply')
app.register_blueprint(routes_board, url_prefix='/board')
app.register_blueprint(routes_mail, url_prefix='/mail')


@app.context_processor
def include_markdown():
    return {'markdown2': markdown2}


@app.template_filter('delta')
def time_delta(utime):
    import datetime
    now = datetime.datetime.now()
    ct = datetime.datetime.fromtimestamp(utime)
    delta = now - ct
    if delta.days != 0:
        return str(delta.days) + 'days ago'
    else:
        sec = delta.seconds
        if sec < 60:
            return str(sec) + 'seconds ago'
        elif sec < 3600:
            return str(sec//60) + 'minuts ago'
        else:
            return str(sec//3600) + 'hours ago'


@app.template_filter('local_time')
def time_convert(ct):
    import time
    return time.strftime('%Y/%m/%d', time.localtime(int(ct)))

if __name__ == '__main__':
    app.run(**hp)
