from flask import Flask

from config.config import secret_key, hp
from routes.user import main as routes_user
from routes.topic import main as routes_topic
from routes.reply import main as routes_reply
from routes.board import main as routes_board

# 使用flask框架并加密session
app = Flask(__name__)
app.secret_key = secret_key

# 注册蓝图
app.register_blueprint(routes_user)
app.register_blueprint(routes_topic, url_prefix='/topic')
app.register_blueprint(routes_reply, url_prefix='/reply')
app.register_blueprint(routes_board, url_prefix='/board')

if __name__ == '__main__':
    app.run(**hp)
