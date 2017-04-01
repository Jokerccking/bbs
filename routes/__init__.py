# 开发方法

"""
1, 拆分有哪些页面
    1.1
    发博客 link 点进去进入发博客页面
    1.2
    具体的博客，博客标题，可以被点击
    2.1
    博客正文， 作者，title，时间，内容
    2.2
    发表评论的窗口：发表的评论，都是针对该博客的
    2.3
    显示所有评论的地方，这个里面会有评论
    3.1
    创建博客的页面

2， 组织哪些数据，把数据的操作实现
    2.1 Blog数据
        id      ~int
        author  ~string
        content ~string
        ct      ~time

        Blog的方法有哪些
        new（） 创建一个新的博客
        bid（） 通过博客id找到该博客
    2.2 Comment数据
        id      ~int
        bid     ~int
        author
        content
        ct

        Comment操作
        new()
        cid()   通过评论id找到该评论

3，  逻辑      产品经理
    3.1 点创建blog，跳转到blog/new这个页面，去创建blog
    3.2 创建完毕，回到index
    3.3 点击某一个blog，进入blog详情页
    3.4 在详情页，提交一条评论，跳转回来，显示评论

4，  开始实现代码

5，  剩下的部分一点点补全

6，  美化页面，视觉

7，  交互细节，交互

"""
from flask import session

from models.user import User

csrf_token = dict()


def current_user():
    uid = session.get('uid', -1)
    u = User.find(int(uid))
    return u
