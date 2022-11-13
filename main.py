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

    def get_databases_list(self, filter: list = None):
        cur = self.__get_db_cursor()
        cur.execute('show databases')
        res = cur.fetchall()
        db_list = []
        if filter is None:
            for item in res:
                db_list.append(item[0])
        else:
            assert isinstance(filter, list), print('parma illegal')
            for item in res:
                if item[0] not in filter:
                    db_list.append(item[0])
        return db_list


    def GetDBconnection(self):
        pass








if __name__ == '__main__':

    db = DBUtil(host='127.0.0.1', user='root', password='password', port=3306)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
 