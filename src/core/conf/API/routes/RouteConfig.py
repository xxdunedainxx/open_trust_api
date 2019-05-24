from ...ServiceConfig import ServiceConfig

class RouteConfig(ServiceConfig):

    def __init__(self,
                 file: str,
                 requiredAttributes: []=None,
                 defaultAttributes: {}=None):

        self.core_route=None
        self.api_specific_resource=None
        self.supported_methods=None
        self.method_docs = None
        self.api_specific_routes = None

        self.route_required_attributes=[
            "core_route",
            "api_specific_resource"
        ]

        if requiredAttributes is not None:
            self.route_required_attributes.extend(requiredAttributes)

        super().__init__(file,self.route_required_attributes,defaultAttributes)
        self._check_defaults()

    def _check_defaults(self):
        if getattr(self, "supported_methods") is None:
            self.supported_methods=[
                "get",
                "post",
                "delete",
                "patch"
            ]

        if getattr(self, "api_specific_routes") is None:
            self.api_specific_routes={
                "get" : "get",
                "post" : "create",
                "delete" : "remove",
                "patch" : "update"
            }
