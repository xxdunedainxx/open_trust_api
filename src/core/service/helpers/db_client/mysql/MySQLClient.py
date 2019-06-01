from ......data.sql.sql import sql
from ..IDBClient import IDBClient
from .....conf.ServiceConfig import ServiceConfig

class MySQLClient(IDBClient):

    def __init__(self, conf: ServiceConfig, autoCommit=False):
        if getattr(ServiceConfig, "conf") is None:
            raise Exception("MySQL Client required a \'conf\' section in the service config")
        else:
            self._conf=ServiceConfig.conf
        self._client: sql = self.connection(conf, autoCommit)

    def connection(self, conf: {}, autoCommit: bool)->sql:
        return sql(
            config=conf,
            autoCommit=autoCommit
        )

    def kill_connection(self, *args)->None:
        if self._client is None:
            return
        else:
            self._client.killConnection()

    def executeQuery(self,query: str, fetchAll: bool=True, paramitized: tuple=None)->None:
        self._client.executeQuery(query, fetchAll, paramitized)

    def fetch_client(self)->sql:
        return self._client