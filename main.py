import pymysql

class DBUtil:
    __host = None
    __user = None
    __password = None
    __port = None

    def __init__(self, host: str, user: str, password: str, port: int):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port

    def __get_db_cursor(self):
        try:
            connection = pymysql.connect(host=self.__host, user=self.__user, passwd=self.__password, port=self.__port)
            cursor = connection.cursor()
            return cursor
        except Exception as e:
            print('connected failed')

    def get_databases_list(self, leach: list = None):
        cur = self.__get_db_cursor()
        cur.execute('show databases')
        res = cur.fetchall()
        return self.__get_list_from_tuple(res, leach)

    def get_table_list(self, database_name: str, leach: list = None, only_table: bool = True):
        cur = self.__get_db_cursor()
        cur.execute('use `{}`;'.format(database_name))
        cur.execute('show tables')
        res = cur.fetchall()
        if only_table:
            return self.__get_list_from_tuple(res, leach)
        else:
            return ['{}.'.format(database_name)+item for item in self.__get_list_from_tuple(res, leach)]

    def __get_list_from_tuple(self, tup, leach: list = None):
        temp = []
        assert isinstance(tup,tuple), print('param is not tuple')
        if leach is None:
            for item in tup:
                assert isinstance(item,tuple),print('param[0] is not tuple')
                temp.append(item[0])
        else:
            assert isinstance(leach, list), print('leach type is not list')
            for item in tup:
                assert isinstance(item, tuple), print('param[0] is not tuple')
                if item[0] not in leach:
                    temp.append(item[0])
        return temp

if __name__ == '__main__':

    db = DBUtil(host='127.0.0.1', user='root', password='password', port=3306)
    databases=db.get_databases_list()
    print(db.get_table_list(database_name=databases[0], leach=['regions']))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
 