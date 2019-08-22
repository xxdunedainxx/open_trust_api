#region General Framework imports
from ...APICore import API,APIArg
from .....conf.API.apis.APICoreConfig import APICoreConfig
from ......util.errorFactory.db.general import ModelAttributeDoesNotExist
from ......util.errorFactory.gen.general import errorStackTrace
from ......util.errorFactory.api.internal.CoreInternalError import InternalAPIError, DEFAULT_INTERNAL_SERVER_ERROR, PayloadMustExist
from ......util.errorFactory.db.service_errors import ServiceNameAlreadyExists
from ......util.api.validators.InternalAPIValidators import InternalAPIValidator
#endregion
#region Decorators
from ......util.api.decorators.http import http_logger, override_http_log_dir
#endregion
#region Flask imorts
# Flask framework imports
from werkzeug.exceptions import BadRequest
from flask_restplus import Namespace, Resource
from flask import request
#endregion
#region DB Imports
from ....helpers.db_client.IDBClient import IDBClient
from src.data.models.app.service import ServiceDoesNotExist, Service as ServiceModel
#endregion
# Endpoint /api/service
#region ServiceRootAPI
class ServiceRootAPI(API):

    #region Constructor
    def __init__(self,apiConfig: APICoreConfig,services: [IDBClient],inputValidation: InternalAPIValidator=InternalAPIValidator()):
        override_http_log_dir(".\\dump\\service.http.log")
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
        APIReference: ServiceRootAPI = self

        @APIReference.namespace_object.route(APIReference.api_config().resource_name)
        class API_Resource(Resource):

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["get"])
            @APIReference.route_manager.route_check(method="get")
            @http_logger
            def get(self):
                try:
                    # Grab specific service case
                    if request.json is not None and "sid" in request.json.keys():
                        rService=ServiceModel.get_service_by_id(
                            id=request.json["sid"],
                            db=APIReference.db_client.fetch_client()
                        )

                        if rService is None:
                            return {"message": "record not found"},404

                        return rService.serialize(), 200
                    elif request.json is not None and "name" in request.json.keys():
                        rService=ServiceModel.get_service_by_name(
                            name=request.json["name"],
                            db=APIReference.db_client.fetch_client()
                        )

                        if rService is None:
                            return {"message": "record not found"},404

                        return rService.serialize(),200

                    all_svcs=ServiceModel.get_all_services(
                        db=APIReference.db_client.fetch_client()
                    )
                    if len(all_svcs) == 0:
                        return {'message' : 'no services yet...', "services" : []},200

                    rServices=[]
                    for svc in all_svcs:
                        rServices.append(
                            svc.serialize()
                        )
                    return {"services" : rServices},200
                except Exception as e:
                    APIReference.log.write_log(
                        data=f"FeatureRootAPI error: {errorStackTrace(e)}"
                    )
                    return DEFAULT_INTERNAL_SERVER_ERROR

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
                    ServiceModel.new_service(
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
                    APIReference.log.write_log(
                        data=f"FeatureRootAPI error: {errorStackTrace(e)}"
                    )
                    return DEFAULT_INTERNAL_SERVER_ERROR

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["patch"])
            @APIReference.route_manager.route_check(method="patch")
            @http_logger
            def patch(self):
                try:
                    payload=request.json

                    if payload is None or "id" not in payload.keys() or len(payload.keys()) <= 1:
                        return PayloadMustExist(fields=str(ServiceModel.supported_update_fields()))
                    else:
                        sid = payload.pop("id",None)

                        # validate model has attribute to update
                        for key in payload.keys():
                            if key in ServiceModel.supported_update_fields() is False:
                                raise ModelAttributeDoesNotExist()

                        ServiceModel.generic_service_update(
                            values_to_update=list(payload.keys()),
                            params=(APIReference.payload_to_tuple_helper(payload) + (sid,)),
                            db=APIReference.db_client.fetch_client()
                        )

                        return {'message' : 'service updated!'},200
                except Exception as e:
                    APIReference.log.write_log(
                        data=f"FeatureRootAPI error: {errorStackTrace(e)}"
                    )
                    return DEFAULT_INTERNAL_SERVER_ERROR

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["delete"])
            @APIReference.route_manager.route_check(method="delete")
            @http_logger
            def delete(self):
                try:
                    payload = request.json
                    if payload is None or "id" not in payload.keys() or len(payload.keys()) <= 1:
                        return PayloadMustExist(fields=str(ServiceModel.supported_update_fields()))

                    sid = payload.pop("id", None)
                    ServiceModel.deactivate_service(
                        id=sid,
                        db=APIReference.db_client.fetch_client()
                    )
                except ServiceDoesNotExist as e:
                    return {'message': f"Service not found {sid}"}, 404
                except Exception as e:
                    APIReference.log.write_log(
                        data=f"FeatureRootAPI error: {errorStackTrace(e)}"
                    )
                    return DEFAULT_INTERNAL_SERVER_ERROR

        return APIReference.namespace_object
    #endregion
#endregion