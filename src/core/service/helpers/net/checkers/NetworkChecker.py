from .INetworkChecker import INetworkChecker
from .....conf.ServiceConfig import ServiceConfig

class NetworkChecker(INetworkChecker):

    def __init__(self,helperConfig: ServiceConfig,protocol: str, default_timeout_seconds: int):
        super().__init__(helperConfig=helperConfig)

        self.protocol: str = protocol
        self.default_timeout_seconds: int = default_timeout_seconds

    def execute_check(self, endpoint, ntests)->{}:
        i=0
        while i < ntests:
            self.test_endpoint(
                endpoint=endpoint,
            )
            i+=1

    def test_endpoint(self, endpoint)->bool:
        pass
