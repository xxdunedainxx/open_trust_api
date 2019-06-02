
#region General Framework imports
from ....ServiceCore import Service
from ...APICore import API,APIArg
from .....conf.API.apis.APICoreConfig import APICoreConfig
from ......util.errorFactory.api.internal.CoreInternalError import InternalAPIError, DEFAULT_INTERNAL_SERVER_ERROR
from ......util.errorFactory.gen.general import errorStackTrace
from ......util.errorFactory.db.service_errors import ServiceNameAlreadyExists
from ...routing.Router import Router
from ......util.api.validators.InternalAPIValidators import InternalAPIValidator
#endregion
#region Decorators
from ......util.api.decorators.http import http_logger
#endregion
#region Flask imorts
# Flask framework imports
from werkzeug.exceptions import BadRequest
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
                    db=APIReference.db_client.fetch_client()
                )
                if len(all_svcs) == 0:
                    return {'message' : 'no services yet...'},204

                rServices=[]
                for svc in all_svcs:
                    rServices.append(
                        svc.serialize()
                    )
                return {"service" : rServices},200


            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["post"])
            @APIReference.route_manager.route_check(method="post")
            @http_logger
            def post(self):
                try:
                    payload=request.json

                    APIReference.validate_required_args(
                        req=[
                            APIArg(
                                arg="name",
                                dataType=str
                            ),
                            APIArg(
                                arg="description",
                                dataType=str
                            )
                        ],
                        passed_args=payload
                    )
                    new_service(
                        name=payload["name"],
                        description=payload["description"],
                        db=APIReference.db_client.fetch_client()
                    )
                    return {'message' : 'service created!'},200
                except InternalAPIError as e:
                    return e.raise_error()
                except ServiceNameAlreadyExists as e:
                    return {'message' : f"Servicenae {payload['name']} already exists!"}, 409
                except BadRequest as e:
                    return {'message' : f"Bad request: {str(e)}"},400
                except Exception as e:
                    return DEFAULT_INTERNAL_SERVER_ERROR

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