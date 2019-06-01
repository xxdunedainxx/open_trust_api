from ..HelperCore import  Helper
from ....conf.ServiceConfig import ServiceConfig

class IDBClient(Helper):

    def __init__(self, sqlConfig: ServiceConfig, *args):
        pass

    def connection(self, *args):
        pass

    def kill_connection(self, *args):
        pass

    def executeQuery(self,query, *args):
        pass

    def fetch_client(self):
        return self._client