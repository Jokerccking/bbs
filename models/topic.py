import time

from models import Model


class Topic(Model):
    @classmethod
    def get(cls, i):
        t = cls.find(i)
        t.view_times += 1
        t.save()
        return t

    def __init__(self, form):
        self.id = form.get('id')
        self.uid = int(form.get('uid'))
        self.view_times = int(form.get('view_times', 0))
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = form.get('ct', int(time.time()))

    def replies(self):
        return Reply.all_rep(self.id)


class Reply(Model):
    @classmethod
    def all_rep(cls, tid):
        rs = []
        ms = cls.all()
        for m in ms:
            if m.tid == tid:
                rs.append(m)
        return rs

    def __init__(self, form):
        self.id = form.get('id')
        self.uid = int(form.get('uid'))
        self.tid = int(form.get('tid'))
        self.content = form.get('content', '')
        self.ct = form.get('ct', int(time.time()))
