# TODO EVENT MODEL / EVENT COMMENT MODEL
#region Custom Lib Imports
from ....util.errorFactory.db.event_errors import EventDoesNotExist,EventInactive
from ....util.errorFactory.db.status_errors import InvalidStatus
from .status import Status
from ....core.service.helpers.db_client.IDBClient import IDBClient
#endregion
#region Python Imports
from datetime import datetime
#endregion
#region Event

class Event:

    def __init__(self, id: int, description: str, when_created: datetime , active: int , event_status: int, feature_id: int, service_id: int, when_closed: datetime):
        # validate event ID is valid
        if event_status not in Event.valid_support_fields():
            raise InvalidStatus(event_status)

        self.id=id
        self.description=description
        self.when_created = when_created
        self.active=active
        self.event_status = event_status
        self.feature_id = feature_id
        self.service_id = service_id
        self.when_closed = when_closed

    def serialize(self):
        return {

        }

    @staticmethod
    def valid_support_fields() -> []:
        return [
            0,
            1,
            2,
            3
        ]

    @staticmethod
    def create_event(db: IDBClient,id: int, description: str, active: int , event_status: int, feature_id: int, service_id: int):
        pass

    @staticmethod
    def get_event(db: IDBClient,id: int):
        pass

    @staticmethod
    def get_service_events(db: IDBClient,service_id: int):
        pass

    @staticmethod
    def get_feature_events(db: IDBClient, service_id: int, feature_id: int):
        pass

    @staticmethod
    def close_event(db: IDBClient, id: int):
        pass

    @staticmethod
    def update_event_status(db: IDBClient, status: int):
        if Status.reserved_status_values["Online"] == status:
            # event close
            pass
        else:
            pass
#endregion