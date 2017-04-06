import json
from pymongo import MongoClient
db = MongoClient().bbs


def new_id(name):
    query = {'name': name, }
    update = {
        '$inc': {'seq': 1},
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    id_coll = db['model_id']
    return id_coll.find_and_modify(**kwargs).get('seq')


class Model(object):
    """
    base data Class for storing message
    """

    @classmethod
    def new(cls, form):
        """
        create a new instance of the class and save it into db
        :param form:
        :return:
        """
        coll = cls.__name__
        m = cls(form)
        m.id = new_id(coll)
        db[coll].save(m.__dict__)
        return m

    @classmethod
    def all(cls):
        """
        get all the instances of the class in db
        :return:
        """
        field = {'_id': 0, }
        result = db[cls.__name__].find({}, field)
        return [cls(form) for form in result]

    @classmethod
    def find(cls, i):
        result = db[cls.__name__].find_one({'id': i})
        if result is None:
            return result
        else:
            return cls(result)

    @classmethod
    def find_all(cls, query):
        ms = []
        result = db[cls.__name__].find(query, {'_id': 0})
        for form in result:
            ms.append(cls(form))
        return ms

    @classmethod
    def delete(cls, query):
        """
        delete the instance by id and return it
        :param query: the instance id of one model
        """
        db[cls.__name__].delete_many(query)

    def __repr__(self):
        """
        return the string type of the instance
        :return:
        """
        return json.dumps(self.__dict__)

    def update(self, modify):
        query = {'id': getattr(self, 'id')}
        db[self.__class__.__name__].update_many(query, modify)

    def to_dict(self):
        """
        get the properties of the instance
        :return:
        """
        return self.__dict__.copy()
