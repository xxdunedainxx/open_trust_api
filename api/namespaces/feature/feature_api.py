from flask_restplus import Namespace, Resource
import api.api_util.ROUTER as ROUTER
from api.namespaces.feature.validation import feature_validators
from conf.conf import db
from src.data.models.app.feature import get_all_features_by_service_id,get_feature_by_id_and_service, reactivate_feature,deactivate_feature,change_feature_status, get_feature_by_name, new_feature

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


    @api.doc(responses={200: 'Success', 400: 'Invalid payload', 404: 'Feature ID does not exist'})
    def patch(self, service_id, feature_id, updates):
        feature = get_feature_by_id_and_service(service_id, feature_id, db)
        if feature != None:
            # TODO Stick in validation
            if 'active' in updates.keys() and updates['active'] is True:
                reactivate_feature(service_id,feature_id,db)
            elif 'active' in updates.keys() and updates['active'] is False:
                deactivate_feature(service_id,feature_id,db)
            elif 'status' in updates.keys():
                change_feature_status(service_id,feature_id,updates['status'],db)
            else:
                return {'message', 'invalid update flag'},400
        else:
            return {'message', f"{feature_id} feature does not exist"},404

@api.route(ROUTER.FEATURE_ROUTE_BASE)
class FeatureRouteAPI(Resource):
    @api.doc(responses={200: 'Success', 400: 'Invalid payload', 404: 'ID already exists', 406 : 'name already exists'})
    def post(self,service_id, name, description):
        validation_errors = feature_validators.validateServiceDescription().validate({'description' : description})
        service=get_feature_by_name(service_id,name,db)

        if validation_errors:
            return {'message': validation_errors}, 400
        elif service != None:
            return {'message' : 'name already exists!'},406
        else:
            new_feature(name, description, service_id, db)
            return {'message' : 'service created!'},200
