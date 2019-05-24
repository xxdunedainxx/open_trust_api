from ...ServiceConfig import ServiceConfig
from ....conf.API.routes.RouteConfig import RouteConfig

class APICoreConfig(ServiceConfig):

    def __init__(self,
                 file: str,
                 routerConfig: RouteConfig,
                 requiredAttributes: []=None,
                 defaultAttributes: {}=None,
                 ):

        # Dependency Injection from RouterConfiguration
        self._router_config=routerConfig



        # Namespace descriptors
        self.resource_name=None
        self.api_namespace_name=None
        self.api_namespace_description=None
        self._supported_api_responses = None
        self.method_docs = None



        # Required
        required_api_attributes=[
            "api_namespace_name","api_namespace_description"
        ]

        if requiredAttributes is not None:
            required_api_attributes.extend(requiredAttributes)

        super().__init__(file,required_api_attributes,defaultAttributes)
        self._check_defaults()

    def router_config(self)->RouteConfig:
        return self._router_config

    def _check_defaults(self):
        if getattr(self, "_supported_api_responses") is None:
            self._supported_api_responses=[
                200,
                401,
                500]

        if getattr(self, "method_docs") is None:
            self.method_docs={
                "get" : {
                    200: 'Success',401 : 'Unauthorized', 500 : 'Internal Server Error'
                },
                "post": {
                    200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'
                },
                "patch": {
                    200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'
                },
                "delete": {
                    200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'
                }

            }