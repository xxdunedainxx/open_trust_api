
#region General Framework imports
from ....ServiceCore import Service
from ...APICore import API
from .....conf.API.apis.APICoreConfig import APICoreConfig
from ...routing.Router import Router
from ......util.api.validators.InternalAPIValidators import InternalAPIValidator
#endregion
#region Decorators
from ......util.api.decorators.http import http_logger
#endregion
#region Flask imorts
# Flask framework imports
from flask_restplus import Namespace, Resource
from flask import request
#endregion
#region DB Imports
from ....helpers.db_client.IDBClient import IDBClient
from ......data.models.service import get_all_services,new_service
#endregion

# Endpoint /api/service
class ServiceRootAPI(API):

    #region Constructor
    def __init__(self,apiConfig: APICoreConfig,services: [IDBClient],inputValidation: InternalAPIValidator=InternalAPIValidator()):
        super().__init__(
            apiConfig=apiConfig,
            services=services,
            inputValidation=inputValidation)
        self.db_client: IDBClient=services[0]
    #endregion

    #region Private Methods


    #endregion

    #region Pubic Methods

    #endregion

    #region API Resource Builder
    # Builds out the Flask API Resource
    def build_api_resource(self)->Namespace:
        APIReference = self
        @APIReference.namespace_object.route(APIReference.api_config().resource_name)
        class API_Resource(Resource):

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["get"])
            @APIReference.route_manager.route_check(method="get")
            @http_logger
            def get(self):
                all_svcs=get_all_services(
                    db=APIReference.db_client
                )
                return {"message" : "test return data! API Works!"}


            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["post"])
            @APIReference.route_manager.route_check(method="post")
            @http_logger
            def post(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["patch"])
            @APIReference.route_manager.route_check(method="patch")
            @http_logger
            def patch(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["delete"])
            @APIReference.route_manager.route_check(method="delete")
            @http_logger
            def delete(self):
                pass

        return APIReference.namespace_object
    #endregion