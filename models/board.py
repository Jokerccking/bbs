import time

from models import Model


class Board(Model):
    def __init__(self, form):
        self.id = form.get('id')
        self.name = form.get('name', '')
        self.ct = form.get('ct', int(time.time()))
        self.ut = form.get('ut', self.ct)

    def remove(self):
        from .topic import Topic
        ts = Topic.get_all(self.id)
        for t in ts:
            Topic.pop(t.id)
        self.pop(self.id)
