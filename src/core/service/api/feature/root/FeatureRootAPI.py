#region General Framework imports
from ....ServiceCore import Service
from ...APICore import API,APIArg
from .....conf.API.apis.APICoreConfig import APICoreConfig
from ......util.errorFactory.db.general import ModelAttributeDoesNotExist
from ......util.errorFactory.api.internal.CoreInternalError import InternalAPIError, DEFAULT_INTERNAL_SERVER_ERROR, PayloadMustExist
from ......util.errorFactory.gen.general import errorStackTrace
from ......util.errorFactory.db.service_errors import ServiceNameAlreadyExists
from ...routing.Router import Router
from ......util.api.validators.InternalAPIValidators import InternalAPIValidator
#endregion
#region Decorators
from ......util.api.decorators.http import http_logger, override_http_log_dir
#endregion
#region Flask imorts
# Flask framework imports
from werkzeug.exceptions import BadRequest
from flask_restplus import Namespace, Resource
from flask import request, copy_current_request_context
#endregion
#region DB Imports
from ....helpers.db_client.IDBClient import IDBClient
from ......data.models.feature import get_all_features, get_feature_by_id, get_feature_by_name, new_feature, FeatureNameAlreadyExists, Feature, generic_feature_update, deactivate_feature, FeatureDoesNotExist
#endregion

# Endpoint /api/service
class FeatureRootAPI(API):

    #region Constructor
    def __init__(self,apiConfig: APICoreConfig,services: [IDBClient],inputValidation: InternalAPIValidator=InternalAPIValidator()):
        override_http_log_dir(".\\dump\\feature.http.log")
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
        APIReference: FeatureRootAPI = self

        @APIReference.namespace_object.route(APIReference.api_config().resource_name)
        class API_Resource(Resource):

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["get"])
            @APIReference.route_manager.route_check(method="get")
            @http_logger
            def get(self):

                # Grab specific service case
                if request.json is not None and "fid" in request.json.keys():
                    rFeature=get_feature_by_id(
                        id=request.json["fid"],
                        db=APIReference.db_client.fetch_client()
                    )
                    return rFeature.serialize(), 200
                elif request.json is not None and "name" in request.json.keys() and "sid" in request.json.keys():
                    rFeature=get_feature_by_name(
                        service_id=request.json["sid"],
                        name=request.json["name"],
                        db=APIReference.db_client.fetch_client()
                    )
                    return rFeature.serialize(),200

                all_fts=get_all_features(
                    db=APIReference.db_client.fetch_client()
                )
                if len(all_fts) == 0:
                    return {'message' : 'no features yet...', "features": []}, 200

                rFeatures=[]
                for ft in all_fts:
                    rFeatures.append(
                        ft.serialize()
                    )
                return {"features" : rFeatures},200


            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["post"])
            @APIReference.route_manager.route_check(method="post")
            @http_logger
            def post(self):
                try:
                    payload = request.json

                    APIReference.validate_required_args(
                        req=[
                            APIArg(
                                arg="name",
                                dataType=str
                            ),
                            APIArg(
                                arg="description",
                                dataType=str
                            ),
                            APIArg(
                                arg="parent",
                                dataType=int
                            )
                        ],
                        passed_args=payload
                    )

                    new_feature(
                        name=payload["name"],
                        description=payload["description"],
                        parent=payload["parent"],
                        db=APIReference.db_client.fetch_client()
                    )
                    return {'message': 'feature created!'}, 200
                except InternalAPIError as e:
                    return e.raise_error()
                except FeatureNameAlreadyExists as e:
                    return {'message': f"Feature name {payload['name']} already exists!"}, 409
                except BadRequest as e:
                    return {'message': f"Bad request: {str(e)}"}, 400
                except Exception as e:
                    return DEFAULT_INTERNAL_SERVER_ERROR

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["patch"])
            @APIReference.route_manager.route_check(method="patch")
            @http_logger
            def patch(self):
                payload = request.json

                if ((payload is None) or ("id" not in payload.keys() or "parent" not in payload.keys())) \
                        or len(payload.keys()) <= 2:
                    return PayloadMustExist(fields=str(Feature.supported_update_fields()))
                else:
                    fid = payload.pop("id", None)
                    parent = payload.pop("parent", None)

                    # validate model has attribute to update
                    for key in payload.keys():
                        if key in Feature.supported_update_fields() is False:
                            raise ModelAttributeDoesNotExist()

                    generic_feature_update(
                        values_to_update=list(payload.keys()),
                        params=(APIReference.payload_to_tuple_helper(payload) + (fid, parent,)),
                        db=APIReference.db_client.fetch_client()
                    )

                    return {'message': 'feature updated!'}, 200

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["delete"])
            @APIReference.route_manager.route_check(method="delete")
            @http_logger
            def delete(self):
                payload = request.json

                if ((payload is None) or ("id" not in payload.keys() or "parent" not in payload.keys())) \
                        or len(payload.keys()) <= 2:
                    return PayloadMustExist(fields=str(Feature.supported_update_fields()))

                else:
                    fid = payload.pop("id", None)
                    parent = payload.pop("parent", None)

                try:
                    deactivate_feature(
                        service_id=parent,
                        id=fid,
                        db=APIReference.db_client.fetch_client()
                    )
                except FeatureDoesNotExist as e:
                    return {'message': f"Feature not found {fid}, for service. {parent}"}, 404
                except Exception as e:
                    return DEFAULT_INTERNAL_SERVER_ERROR

        return APIReference.namespace_object
    #endregion