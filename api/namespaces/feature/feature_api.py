from flask_restplus import Namespace, Resource
from api.api_util.util import http_parse
import api.api_util.ROUTER as ROUTER
from api.namespaces.feature.validation import feature_validators
from conf.conf import db
from data.models.feature import Feature, get_all_features,get_all_features_by_service_id,get_feature_by_id_and_service
from src.util.errorFactory.service_errors import ServiceDoesNotExist


api = Namespace('feature', description='General API for Open Trust Feature management.')

@api.route(ROUTER.GET_ALL_FEATURES_BY_SERVICE)
class AllFeatureAPI(Resource):
    @api.doc(responses={200: 'Success',400 : 'Invalid payload', 404: 'Service ID does not exist'})
    def get(self,service_id):
        features=get_all_features_by_service_id(service_id, db)

        serialized_payload=[]

        for feature in features:
            serialized_payload.append(feature.serialize())

        if len(serialized_payload) > 0:
            return serialized_payload, 200
        else:
            return {'message': f'Service ID {service_id} does not exist'}, 404

@api.route(ROUTER.GET_SPECIFIC_FEATURE)
class FeatureSpecificAPI(Resource):
    @api.doc(responses={200: 'Success',400 : 'Invalid payload', 404: 'Feature ID does not exist'})
    def get(self,service_id,feature_id):
        feature=get_feature_by_id_and_service(service_id,feature_id, db)


        if feature != None:
            return feature.serialize(), 200
        else:
            return {'message': f'Feature ID {feature_id} does not exist for service ID {service_id}'}, 404

