import json


def load(path):
    """
    use json module get content in the file
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        if s == '':
            s = '[]'
        return json.loads(s)


def save(data, path):
    """
    save data into file by json moudle
    """
    data = json.dumps(data, ensure_ascii=False, indent=2)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(data)


class Model(object):
    """
    base data Class for storing message
    """

    @classmethod
    def data_path(cls):
        """
        get the class file in db
        :return:
        """
        name = cls.__name__
        return 'data/{}.txt'.format(name)

    @classmethod
    def new(cls, form):
        """
        create a new instance of the class and save it into db
        :param form:
        :return:
        """
        m = cls(form)
        return m.save()

    @classmethod
    def all(cls):
        """
        get all the instances of the class in db
        :return:
        """
        path = cls.data_path()
        ms = [cls(m) for m in load(path)]
        return ms

    @classmethod
    def find(cls, i):
        """
        find the instance of the class by id
        :param i:
        :return:
        """
        ms = cls.all()
        mod = None
        for m in ms:
            if m.id == i:
                mod = m
                break
        return mod

    @classmethod
    def pop(cls, d):
        """
        delete the instance by id and return it
        :param d:
        :return:
        """
        ms = cls.all()
        mod = None
        for m in ms:
            if m.id == d:
                mod = m
        if mod is not None:
            ms.remove(mod)
            cls.resave(ms)
        return mod

    @classmethod
    def resave(cls, ms):
        """
        save all the instances in the list into db
        :param ms:
        :return:
        """
        p = [m.__dict__ for m in ms]
        save(p, cls.data_path())

    # def __init__(self, form):
    #     """
    #     initial a instance of the model by form,only has id
    #     :param form:
    #     """
    #     self.id = form.get('id', None)

    def __repr__(self):
        """
        return the string type of the instance
        :return:
        """
        return json.dumps(self.__dict__)

    def to_dict(self):
        """
        get the properties of the instance
        :return:
        """
        return self.__dict__.copy()

    def save(self):
        """
        save the instance and return it
        :return:
        """
        ms = self.all()
        if self.id is None:
            i = 0
            if len(ms) > 0:
                i = ms[-1].id + 1
            self.id = i
            ms.append(self)
        else:
            for index, obj in enumerate(ms):
                if obj.id == self.id:
                    ms[index] = self
        p = [m.__dict__ for m in ms]
        save(p, self.data_path())
        return self
