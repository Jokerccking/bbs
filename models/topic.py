import time

from models import Model


class Topic(Model):
    @classmethod
    def get(cls, i):
        t = cls.find(i)
        if t is not None:
            inc = {'$inc': {'view_times': 1}}
            t.update(inc)
        return t

    @classmethod
    def all_of_user(cls, uid):
        query = {'uid': uid}
        return cls.find_all(query)

    def __init__(self, form):
        self.id = form.get('id')
        self.uid = int(form.get('uid'))
        self.bid = int(form.get('bid'))
        self.view_times = int(form.get('view_times', 0))
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = form.get('ct', int(time.time()))

    def remove(self):
        self.delete({'id': self.id})

    def user(self):
        from .user import User
        return User.find(self.uid)

    def replies(self):
        return Reply.all_of_topic(self.id)


class Reply(Model):
    @classmethod
    def all_of_topic(cls, tid):
        query = {'tid': tid}
        return cls.find_all(query)

    @classmethod
    def all_of_user(cls, uid):
        query = {'uid': uid}
        return cls.find_all(query)

    def __init__(self, form):
        self.id = form.get('id')
        self.uid = int(form.get('uid'))
        self.tid = int(form.get('tid'))
        self.content = form.get('content', '')
        self.ct = form.get('ct', int(time.time()))

    def user(self):
        from .user import User
        return User.find(self.uid)

    def topic(self):
        return Topic.find(self.tid)
