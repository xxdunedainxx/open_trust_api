import pymysql as mysql

class sql:

    def __init__(self, config, autoCommit=False):
        self.mysqlConfig = None
        self._connection = None
        self._cursor = None
        self.newConnection(config, autoCommit)

    def setMySQLConnection(self, config, autoCommit=False):
        self.mysqlConfig = config
        self._connection = mysql.connect(host=config['host'], user=config['user'], password=config['password'],
                                         db=config['database'], autocommit=autoCommit)

    def newConnection(self, config, autoCommit=False):
        if (self._connection is not None) and (self._connection.open is True):
            self.killConnection()
        self.setMySQLConnection(config, autoCommit)

        self._cursor = self._connection.cursor()


    def killConnection(self):
        self._cursor.close()
        if self._connection.open is True:
            self._connection.close()

    def executeQuery(self, query, fetchAll=True, paramatized=None):
        if paramatized is None:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, (paramatized))
        if (self._cursor.rowcount is 0) or (self._cursor.description is None):
            return None
        elif fetchAll is True:
            return self._cursor.fetchall()

    def fetchItem(self):
        return self._cursor.fetchone()

    def param_value_helper(self, params: tuple)->str:
        rValues=""
        i = 0
        while i < len(params):
            rValues+="%s"
            if i != len(params) + 1:
                rValues+=","
            i+=1
        return rValues

    def update_set_helper(self,keys: [str]):
        rValues=""
        i = 0
        while i < len(keys):
            rValues+=f"{keys[i]}=%s"

            i += 1

            if i < len(keys):
                rValues+=","
            else:
                rValues+=" "

        return rValues