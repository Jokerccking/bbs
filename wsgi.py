#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import app
# 设置当前目录为工作目录
sys.path.insert(0, abspath(dirname(__file__)))


# 必须有一个叫做 application 的变量
# gunicorn 就要这个变量
# 这个变量的值必须是 Flask 实例
# 这是规定的套路(协议)
application = app.app

# 这是把代码部署到 apache gunicorn nginx 后面的套路
"""
建立一个软连接
sudo ln -s ~/myproject/bbs/config/supervisor.conf /etc/supervisor/conf.d/bbs.conf

sudo ln -s ~/myproject/bbs/config/nginx.conf /etc/nginx/sites-enabled/bbs.conf



➜  ~ cat myproject/bbs/config/gunicorn.config

bind = '0.0.0.0:2001'
pid = '/tmp/bbs.pid'


➜  ~ cat /etc/supervisor/conf.d/bbs.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c config/gunicorn.config
directory=~/myproject/bbs
autostart=true
autorestart=true

➜  ~ cat /etc/nginx/sites-enabled/bbs.conf

server {
    listen 80;
    location / {
        proxy_pass http://localhost:2001;
    }
}

"""
