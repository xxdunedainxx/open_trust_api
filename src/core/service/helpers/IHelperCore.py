from ..IServiceCore import IService
from ...conf.ServiceConfig import ServiceConfig
class IHelper(IService):

    def __init__(self,helperConfig: ServiceConfig):
        super().__init__(serviceConfig=helperConfig)

