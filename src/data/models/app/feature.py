# TODO Detect feature colision

from ....util.errorFactory.db.feature_errors import FeatureDoesNotExist, FeatureNameAlreadyExists
from ....core.service.helpers.db_client.IDBClient import IDBClient

class Feature:

    def __init__(self, id, name, when_created, description, parent_service, active, status):
        self.id = id
        self.name = name
        self.description = description
        self.when_created = when_created
        self.parent_service = parent_service
        self.active = active
        self.status = status

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'when_created': str(self.when_created),
            'parent_service': self.parent_service,
            'active': self.active,
            'status': self.status
        }

    @staticmethod
    def supported_update_fields() -> []:
        return [
            "name",
            "description",
            "active",
            "status",
            "parent_service"
        ]

    @staticmethod
    def generic_feature_update(values_to_update: [str], params: tuple, db: IDBClient):
        db.executeQuery(
            f"UPDATE feature SET {db.update_set_helper(values_to_update)} WHERE feature_id=%s AND parent_service=%s",
            paramatized=params
        )

    @staticmethod
    def get_all_features(db: IDBClient):
        GET_ALL_FEATURES = "SELECT * FROM feature"

        get_features = db.executeQuery(GET_ALL_FEATURES)
        featureObjs = []

        if get_features is None:
            return featureObjs

        for feature in get_features:
            featureObjs.append(Feature(feature[0], feature[1], feature[2], feature[3], feature[4], feature[5], feature[6]))

        return featureObjs

    @staticmethod
    def new_feature(name, description, parent, db: IDBClient):
        CREATE_FEATURE = "INSERT INTO feature (name, when_created,parent_service,description) VALUES (%s ,now(), %s,%s)"

        if Feature.get_feature_by_name(parent, name, db) is None:
            exec = db.executeQuery(CREATE_FEATURE, paramatized=(name, parent, description,))
        else:
            raise FeatureNameAlreadyExists(f"{name} feature already exists for service {parent}")

    @staticmethod
    def get_feature_by_id(id, db: IDBClient):
        get_feature = db.executeQuery("SELECT * FROM feature WHERE feature_id=%s", paramatized=(id))

        if get_feature is not None:
            return Feature(get_feature[0][0], get_feature[0][1], get_feature[0][2], get_feature[0][3],
                           get_feature[0][4], get_feature[0][5], get_feature[0][6])
        else:
            return None

    @staticmethod
    def get_feature_by_id_and_service(service_id, id, db: IDBClient):
        get_feature = db.executeQuery("SELECT * FROM feature WHERE feature_id=%s AND parent_service=%s",
                                      paramatized=(id, service_id))

        if get_feature is not None:
            return Feature(get_feature[0][0], get_feature[0][1], get_feature[0][2], get_feature[0][3],
                           get_feature[0][4], get_feature[0][5], get_feature[0][6])
        else:
            return None

    @staticmethod
    def get_feature_by_name(service_id, name, db:IDBClient):
        get_feature = db.executeQuery("SELECT * FROM feature WHERE name=%s AND parent_service=%s",
                                      paramatized=(name, service_id))

        if get_feature is not None:
            return Feature(get_feature[0][0], get_feature[0][1], get_feature[0][2], get_feature[0][3],
                           get_feature[0][4], get_feature[0][5], get_feature[0][6])
        else:
            return None

    @staticmethod
    def get_all_features_by_service_id(service_id, db: IDBClient):
        get_features = db.executeQuery("SELECT * FROM feature where parent_service=%s", paramatized=(service_id))

        if get_features is None:
            return []

        featureObjs = []

        for feature in get_features:
            featureObjs.append(Feature(feature[0], feature[1], feature[2], feature[3], feature[4], feature[5], feature[6]))

        return featureObjs

    @staticmethod
    def deactivate_feature(service_id, id, db: IDBClient):
        if Feature.get_feature_by_id(id, db) is not None:
            db.executeQuery("UPDATE feature SET active=0 WHERE feature_id=%s and parent_service=%s",
                            paramatized=(id, service_id))
        else:
            raise FeatureDoesNotExist(f"{id} for {service_id} does not exist")

    @staticmethod
    def reactivate_feature(service_id, id, db: IDBClient):
        if Feature.get_feature_by_id(id, db) is not None:
            db.executeQuery("UPDATE feature SET active=1 WHERE feature_id=%s and parent_service=%s",
                            paramatized=(id, service_id))
        else:
            raise FeatureDoesNotExist(f"{id} for {service_id} does not exist")

    @staticmethod
    def change_feature_status(id, service_id, status, db: IDBClient):
        if Feature.get_feature_by_id(id, db) is not None:
            db.executeQuery("UPDATE feature SET status=%s WHERE feature_id=%s and parent_service=%s",
                            paramatized=(status, id, service_id))
        else:
            raise FeatureDoesNotExist(f"{id} does not exist")
