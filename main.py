import MySQLdb
import MySQLdb.cursors
from abc import ABCMeta
import types_field


def start_connection():
    connection = MySQLdb.connect(user='root',
                                 passwd='456756',
                                 db='animals_shop',
                                 cursorclass=MySQLdb.cursors.DictCursor)
    return connection


class AbstractModel:
    __metaclass__ = ABCMeta


class Animals(AbstractModel):
    type_animal = types_field.CharField(max_length=50)
    name = types_field.BooleanField()
    weight = types_field.IntegerField()
    price = types_field.FloatField()


def migrate(model_class):
    connection = start_connection()
    cursor = connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS ' + model_class.__name__.lower() +\
            ' (id INT(10) AUTO_INCREMENT PRIMARY KEY'
    for i in model_class.__dict__:
        if i != '__module__' and i != '__doc__':
            short_query = ', ' + i + ' ' + model_class.__dict__[i].query
            query += short_query
    query += ');'
    cursor.execute(query)
    connection.commit()


def insert(obj):
    connection = start_connection()
    cursor = connection.cursor()
    query = 'INSERT INTO ' + obj.__class__.__name__.lower() + ' ('
    j = 1
    for i in obj.__dict__:
        if j > 1:
            query += ', '
        query += i
        j += 1
    query += ') values ('
    j = 1
    for i in obj.__dict__:
        if j > 1:
            query += ', '
        if isinstance(obj.__dict__[i], str):
            short_query = '"' + obj.__dict__[i] + '"'
        else:
            short_query = str(obj.__dict__[i])
        query += short_query
        j += 1
    query += ');'
    cursor.execute(query)
    connection.commit()


def select(model_class, **kwargs):
    connection = start_connection()
    cursor = connection.cursor()
    comparsion = {'lt': ' < ',
                  'gt': ' > ',
                  'lte': ' <= ',
                  'gte': ' >= ',
                  'contains': ' LIKE '}
    query = 'SELECT * FROM '+ model_class.__name__.lower()
    if kwargs:
        query += ' WHERE '
        j = 1
        for i in kwargs:
            if j > 1:
                query += ' AND '
            key = i.split('__')
            query += key[0]
            if len(key) > 1:
                for comp in comparsion:
                    if comp == key[1]:
                        query += comparsion[comp]
            else:
                query += ' = '
            if type(kwargs[i]) == str or type(kwargs[i]) == bool:
                short_query = '"' + str(kwargs[i]) + '"'
                query += short_query
            else:
                query += str(kwargs[i])
            j += 1
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == '__main__':
    a = Animals()
    a.type_animal = 'cat'
    a.name = True
    a.weight = 4
    a.price = 300.0
    # migrate(Animals)
    # insert(a)
    print(select(Animals, price__lt=400.0))
