from flask import Flask

from config import secret_key, hp

from routes.user import main as routes_user
from routes.static import main as routes_static
from routes.topic import main as routes_topic
from routes.reply import main as routes_reply

# 使用flask框架并加密session
app = Flask(__name__)
app.secret_key = secret_key

# 注册蓝图
app.register_blueprint(routes_user)
app.register_blueprint(routes_static, url_prefix='/static')
app.register_blueprint(routes_topic, url_prefix='/topic')
app.register_blueprint(routes_reply, url_prefix='/reply')

if __name__ == '__main__':
    app.run(**hp)
