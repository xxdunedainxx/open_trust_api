# TODO :: finish service APIs/  feature APIs / status APIs
# TODO :: Once these apis are complete, MVP for client can begin
# TODO :: EVENT MODEL / EVENT COMMENT MODEL

"""
from ...basicTestAPI.conf.api.conf import conf as APIConfig
from ..basicAPI import BasicAPI
from ...root.BuildAPI import BuildAPI
from ...root.conf.conf import conf as APIConfiguration

def testClassImplementation():
    Tester=BasicAPI(apiConfig=APIConfig,services=[])
    return Tester

ClassTester=testClassImplementation()

def testAddToFlask(api: BasicAPI):
    app=BuildAPI(
        apiConfig=APIConfiguration,
        apis=[api])

    app.build()
"""
from src.core.conf.API.apis.APICoreConfig import APICoreConfig
from src.core.conf.API.routes.RouteConfig import RouteConfig
from src.core.service.api.root.BuildAPI import BuildAPI
from src.core.service.api.root.conf.conf import conf as APIConfig
from src.core.service.helpers.db_client.mysql.MySQLClient import  MySQLClient
from src.core.conf.ServiceConfig import  ServiceConfig
from src.core.service.api.service.root.ServiceRootAPI import ServiceRootAPI
db_config=ServiceConfig(file="./sql_client_config.json")
db_config.initialize_config()
mysql_db=MySQLClient(
    conf=db_config,
    autoCommit=True
)

RouterConfiguration=RouteConfig(file=".\\service_core_route.json")
RouterConfiguration.initialize_config()
conf=APICoreConfig(
    file=".\\service_api_root.json",
    routerConfig=RouterConfiguration)
conf.initialize_config()
api=ServiceRootAPI(
    apiConfig=conf,
    services=[mysql_db]
)
app = BuildAPI(
    apiConfig=APIConfig,
    apis=[api])

app.build()
#features=get_all_features_by_service_id(1,db)
exit(0)