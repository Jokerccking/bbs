from models import Model


class User(Model):
    @staticmethod
    def salted_password(password, salt='$/i3& f*~^k'):
        import hashlib
        hash1 = hashlib.sha256(password.encode('ascii')).hexdigest()
        hash2 = hashlib.sha256((hash1 + salt).encode('ascii')).hexdigest()
        return hash2

    @classmethod
    def validate_login(cls, form):
        b = None
        ul = cls(form)
        ul.password = cls.salted_password(ul.password)
        us = cls.find_all({})
        for u in us:
            if u.username == ul.username and u.password == ul.password:
                b = u
                break
        return b

    @classmethod
    def validate_register(cls, form):
        form['password'] = cls.salted_password(form.get('password'))
        ur = cls(form)
        us = cls.find_all({})
        if len(ur.username) > 2:
            for u in us:
                if u.username == ur.username:
                    return None
        new_user = cls.new(form)
        return new_user

    def __init__(self, form):
        self.id = form.get('id')
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', 10)
        self.image = form.get('image', 'default.gif')

    def topics(self):
        from .topic import Topic
        return Topic.find_all({'uid': self.id})

    def received_mails(self):
        from .mail import Mail
        return Mail.find_all({'receiver_id': self.id})

    def send_mails(self):
        from .mail import Mail
        return Mail.find_all({'sender_id': self.id})
