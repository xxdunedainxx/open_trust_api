from ...HelperCore import Helper
from .....conf.ServiceConfig import ServiceConfig

class INetworkChecker(Helper):

    def __init__(self,helperConfig: ServiceConfig, protocol: str, default_timeout_seconds: int):
        super().__init__(helperConfig=helperConfig)

    def execute_check(self, endpoint, ntests)->{}:
        pass

    def test_endpoint(self, endpoint)->bool:
        pass



