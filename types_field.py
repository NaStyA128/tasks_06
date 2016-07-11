class DbField:
    pass


class CharField(DbField):
    query = 'VARCHAR'

    def __init__(self, max_length=255):
        if max_length > 255:
            print('Incorrect length.')
        else:
            self.max_length = max_length
            a = '(' + str(max_length) + ')'
            self.query += a


class IntegerField(DbField):
    query = 'INT'

    def __init__(self, length=10):
        self.length = length
        a = '(' + str(length) + ')'
        self.query += a


class FloatField(DbField):
    query = 'FLOAT'


class BooleanField(DbField):
    query = 'BOOLEAN'
