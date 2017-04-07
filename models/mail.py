import time

from models import Model


class Mail(Model):
    def __init__(self, form):
        self.id = form.get('id')
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self. ct = int(form.get('ct', time.time()))
        self.read = form.get('read', False)
        self.sender_id = int(form.get('sender_id', -1))
        self.receiver_id = int(form.get('receiver_id', -1))

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.update({'set': {'sender_id': sender_id}})

    def mark_read(self):
        self.read = True
        self.update({'$set': {'read': True}})

    def sender(self):
        from .user import User
        return User.find(self.sender_id)

    def receiver(self):
        from .user import User
        return User.find(self.receiver_id)
