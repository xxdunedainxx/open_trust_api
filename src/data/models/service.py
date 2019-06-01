from ...util.errorFactory.db.service_errors import ServiceNameAlreadyExists,ServiceDoesNotExist
from src.data.models.feature import Feature, get_all_features_by_service_id,deactivate_feature,reactivate_feature

class Service:

    def __init__(self,id,name,when_created,description,active,status, features=[]):
        self.id=id
        self.name=name
        self.description=description
        self.when_created=when_created
        self.active=active
        self.status=status
        self.features=features

    def serialize(self):
        serialize_features=[]

        for f in self.features:
            serialize_features.append(f.serialize())

        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'when_created' : str(self.when_created),
            'active' : self.active,
            'status' : self.status,
            'features' : serialize_features,
        }

def get_all_services(db):
    GET_ALL_SERVICES="SELECT * FROM service"


    get_services=db.executeQuery(GET_ALL_SERVICES)

    if get_services == None:
        return []

    serviceObjs=[]

    for service in get_services:
        serviceObjs.append(Service(service[0],service[1],service[2],service[3],service[4],service[5], get_all_features_by_service_id(service[0],db)))

    return serviceObjs

def get_service_by_id(id, db):
    get_service=db.executeQuery("SELECT * FROM service WHERE service_id=%s", paramatized=(id))

    if get_service!= None:
        return Service(get_service[0][0], get_service[0][1], get_service[0][2], get_service[0][3], get_service[0][4], get_service[0][5], get_all_features_by_service_id(get_service[0][0],db))
    else:
        return get_service

def get_service_by_name(name, db):
    get_service=db.executeQuery("SELECT * FROM service WHERE name=%s", paramatized=(name))
    if get_service!= None:
        return Service(get_service[0][0], get_service[0][1], get_service[0][2], get_service[0][3], get_service[0][4], get_service[0][5], get_all_features_by_service_id(get_service[0][0],db))
    else:
        return get_service

def new_service(name, description, db):

    if get_service_by_name(name,db) == None:
        CREATE_FEATURE="INSERT INTO service (name, when_created,description) VALUES (%s ,now(),%s)"
        exec=db.executeQuery(CREATE_FEATURE, paramatized=(name,description))
    else:
        raise ServiceNameAlreadyExists(f"{name} service already exists")

    return exec
# TODO :: update child features
def deactivate_service(id, db):

    if get_service_by_id(id, db) != None:
        features=get_all_features_by_service_id(id,db)

        for f in features:
            deactivate_feature(id,f.id,db)

        db.executeQuery("UPDATE service SET active=0 WHERE service_id=%s", paramatized=(id))
    else:
        raise ServiceDoesNotExist(f"{id} does not exist")
# TODO :: handle re-activate non active service
def reactivate_service(id, db):

    if get_service_by_id(id, db) != None:
        features=get_all_features_by_service_id(id,db)

        for f in features:
            reactivate_feature(id,f.id,db)

        db.executeQuery("UPDATE service SET active=1 WHERE service_id=%s", paramatized=(id))
    else:
        raise ServiceDoesNotExist(f"{id} does not exist")
# TODO :: error handling for service update on de-activated service
def change_service_status(id, status,db):
    if get_service_by_id(id, db) != None:
        db.executeQuery("UPDATE service SET status=%s WHERE service_id=%s", paramatized=(status, id))
    else:
        raise ServiceDoesNotExist(f"{id} does not exist")

