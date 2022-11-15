import pymysql

class DBUtil:
    __host = None
    __user = None
    __password = None
    __port = None
    __connection = None

    def __init__(self, host: str, user: str, password: str, port: int):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port

    def __get_db_cursor(self):
        try:
            self.__connection = pymysql.connect(host=self.__host, user=self.__user, passwd=self.__password, port=self.__port)
            cursor = self.__connection.cursor()
            return cursor
        except Exception as e:
            print('connected failed')

    def get_databases_list(self, leach: list = None):
        cur = self.__get_db_cursor()
        assert cur is not None, print('get cursor failed')
        cur.execute('show databases;')
        res = cur.fetchall()
        self.__connection.close()
        return self.__get_list_from_tuple(res, leach)

    def get_table_list(self, database_name: str, leach: list = None, only_table: bool = True):
        cur = self.__get_db_cursor()
        cur.execute('use `{}`;'.format(database_name))
        cur.execute('show tables;')
        res = cur.fetchall()
        self.__connection.close()
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

    def execute_sql(self, all_sql: list = None):
        result = []
        if all_sql is None:
            return None
        else:
            cur = self.__get_db_cursor()
            for sql in all_sql:
                assert isinstance(sql, str), print('type of sql should be str')
                try:
                    cur.execute(sql)
                    res = cur.fetchall()
                    # if len(res) == 0:
                    #     res=["{} success".format(sql.split(' ')[0])]
                    #     result.append(tuple(res))
                    # else:
                    #     result.append(res)
                    result.append(res)
                    self.__connection.commit()
                except Exception as e:
                    self.__connection.rollback()
                    print('executed \'{}\' failed, Exception:{}'.format(sql,e))
                    # result.append(('{} failed'.format(sql.split(' ')[0])))
                    result.append(())
            print(result)
            self.__connection.close()


if __name__ == '__main__':

    db = DBUtil(host='127.0.0.1', user='root', password='password', port=3306)
    databases = db.get_databases_list()
    db.execute_sql(["insert into atguigudb.countries values({},{},{})".format("'UK'", "'Johnny2'", 1), "select * from atguigudb.countries order by region_id desc ",
                    "delete from atguigudb.countries where country_name={}".format("'Johnny2'"),"select * from atguigudb.countries ","  SELECT TABLE_SCHEMA,TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'atguigudb'  and table_name like '%j%'"])
    #print(db.get_table_list(database_name=databases[0], leach=['regions'],only_table=False))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
 