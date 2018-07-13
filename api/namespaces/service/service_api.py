from flask_restplus import Namespace, Resource
from api.api_util.util import http_parse
import api.api_util.ROUTER as ROUTER
from api.namespaces.service.validation import service_validators
from conf.conf import db
from data.models.service import get_all_services, get_service_by_id


api = Namespace('service', description='General API for Open Trust Service management.')


@api.route(ROUTER.GET_ALL_SERVICES)
class AllServiceAPI(Resource):
    @api.doc(responses={200: 'Success',400 : 'Invalid payload', 404: 'No records?'})
    def get(self):
        """Returns a google drive file by id query"""
        services=get_all_services(db)

        serialized_payload=[]

        for service in services:
            serialized_payload.append(service.serialize())

        if len(serialized_payload) > 0:
            return serialized_payload, 200
        else:
            return {'message': f'No records to return. Something may have gone wrong with the db call'}, 404

@api.route(ROUTER.GET_SPECIFIC_SERVICE)
class ServiceIDAPI(Resource):
    @api.doc(responses={200: 'Success',400 : 'Invalid id payload', 404: 'ID does not exust'})
    def get(self,service_id):
        """Returns a google drive file by id query"""
        service=get_service_by_id(service_id,db)
        validation_errors = service_validators.validateService().validate({'service_id' : service_id})
        if validation_errors:
            return {'message': validation_errors}, 400
        elif service != None:
            return service.serialize(), 200
        else:
            return {'message': f'{service_id} does not exist'}, 404