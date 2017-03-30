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
        us = cls.all()
        ul.password = cls.salted_password(ul.password)
        for u in us:
            if u.username == ul.username and u.password == ul.password:
                b = u
                break
        return b

    @classmethod
    def validate_register(cls, form):
        ur = cls(form)
        us = cls.all()
        ur.password = cls.salted_password(ur.password)
        if len(ur.username) > 2:
            for u in us:
                if u.username == ur.username:
                    return None
        new_user = ur.save()
        return new_user

    def __init__(self, form):
        # super(Model, self).__init__()
        self.id = form.get('id')
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', 10)
