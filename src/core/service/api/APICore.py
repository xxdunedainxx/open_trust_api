from ..ServiceCore import Service
from .IAPICore import IAPI
from .routing.Router import Router
from ...conf.API.apis.APICoreConfig import APICoreConfig
from ....util.api.validators.InternalAPIValidators import InternalAPIValidator


# Flask framework imports
from flask_restplus import Namespace, Resource
from flask import request


class API(IAPI):

    #region Constructor
    def __init__(self,apiConfig: APICoreConfig,services: [Service],inputValidation: InternalAPIValidator):
        self._supported_api_responses=[]
        self.namespace_object:Namespace=None
        self._service_config=apiConfig
        super().__init__(
            apiConfig=apiConfig,
            services=services,
            inputValidation=inputValidation)

        self.api_validation=inputValidation
    #endregion

    #region Private Methods

    # Constructs a Flask Namespace object
    def _build_namespace(self)->None:
        self.namespace_object=Namespace(
            name=self.build_resource_route(),
            description=self.api_config().api_namespace_description)

    def _build_router(self)->None:
        self.route_manager=Router(routerConfig=self
                                  .api_config()
                                  .router_config())


    #endregion

    #region Pubic Methods
    def api_config(self)->APICoreConfig:
        return self._service_config

    def build_resource_route(self)->str:
        return(f"{self.route_manager.core_route}/"
               f"{self.route_manager.api_specific_resource}")
               #f"{self.route_manager.api_specific_routes}")

    #endregion

    #region API Resource Builder
    # Builds out the Flask API Resource
    def build_api_resource(self)->Namespace:
        APIReference = self
        @APIReference.namespace_object.route(APIReference.build_resource_route())
        class API_Resource(Resource):

            #@APIReference.namespace_object.route(f"{APIReference.build_resource_route()}/{APIReference.route_manager.api_specific_routes['get']}")
            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["get"])
            def get(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["post"])
            def post(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["patch"])
            def patch(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["delete"])
            def delete(self):
                pass

        return APIReference.namespace_object
    #endregion