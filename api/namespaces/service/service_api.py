# TODO :: Feature outages?
# TODO :: Feature outage resolution? 

from flask_restplus import Namespace, Resource
from api.api_util.util import http_parse
import api.api_util.ROUTER as ROUTER
from api.namespaces.service.validation import service_validators
from conf.conf import db
from data.models.service import get_all_services, get_service_by_id, new_service, get_service_by_name,reactivate_service,change_service_status, deactivate_service, ServiceDoesNotExist


api = Namespace('service', description='General API for Open Trust Service management.')


@api.route(ROUTER.GET_ALL_SERVICES)
class AllServiceAPI(Resource):
    @api.doc(responses={200: 'Success',400 : 'Invalid payload', 404: 'No records?'})
    def get(self):
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
    @api.doc(responses={200: 'Success',400 : 'Invalid id payload', 404: 'ID does not exist'})
    def get(self,service_id):
        service=get_service_by_id(service_id,db)
        validation_errors = service_validators.validateService().validate({'service_id' : service_id})
        if validation_errors:
            return {'message': validation_errors}, 400
        elif service != None:
            return service.serialize(), 200
        else:
            return {'message': f'{service_id} does not exist'}, 404

    @api.doc(responses={200: 'Success', 400: 'Invalid update flag', 404: 'ID does not exist'})
    def patch(self,service_id,updates):
        try:
            if 'active' in updates.keys() and updates['active'] is True:
                reactivate_service(id,db)
            elif 'active' in updates.keys() and updates['active'] is False:
                deactivate_service(id,db)
            elif 'status' in updates.keys():
                change_service_status(service_id,updates['status'],db)
            else:
                return {'message', 'invalid update flag'},400
        except ServiceDoesNotExist:
            return {'message', f"{service_id} service does not exist"},404
        except Exception as e:
            return {'message', f"internal server error"},500
"""
    @api.doc(responses={200: 'Success', 404: 'ID does not exist'})
    def delete(self,id):
        pass
"""

@api.route(ROUTER.SERVICE_ROUTE_BASE)
class ServiceRouteAPI(Resource):
    @api.doc(responses={200: 'Success', 400: 'Invalid payload', 404: 'ID already exists', 406 : 'name already exists'})
    def post(self, name, description):
        validation_errors = service_validators.validateServiceDescription().validate({'description' : description})
        service=get_service_by_name(name,db)

        if validation_errors:
            return {'message': validation_errors}, 400
        elif service != None:
            return {'message' : 'name already exists!'},406
        else:
            new_service(name, description, db)
            return {'message' : 'service created!'},200



