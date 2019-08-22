# TODO EVENT MODEL / EVENT COMMENT MODEL
#region Custom Lib Imports
from ....util.errorFactory.db.event_errors import EventDoesNotExist,EventInactive, EventExists
from ....util.errorFactory.db.status_errors import InvalidStatus
from .status import Status
from ....core.service.helpers.db_client.IDBClient import IDBClient
#endregion
#region Python Imports
from datetime import datetime
#endregion
#region Event

class Event:
    active=1
    inactive=0

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
    def create_event(db: IDBClient, id: int, description: str, event_status: int, feature_id: int, service_id: int):
        create_event_sql=f"INSERT INTO event " \
            f"(event_id, description, when_created, active,event_status, feature_id, service_id)" \
            f"VALUES (%s, %s, now(), {str(Event.active)}, %s, %s, %s)"

        # if no event exists for service / feature && no all out outage exists
        if (Status.reserved_status_values["Complete Outage"] == event_status and Event.get_service_events(service_id=service_id) is None) or \
                (Event.get_open_feature_events(service_id=service_id,feature_id=feature_id) is None):
            # insert event into DB
            db.executeQuery(
                create_event_sql,
                (id, description, event_status, feature_id,service_id)
            )
        else:
            raise EventExists()
    @staticmethod
    def get_event(db: IDBClient, id: int) -> object:
        pass

    @staticmethod
    def get_service_events(db: IDBClient,service_id: int):
        pass

    @staticmethod
    def get_open_service_events(db: IDBClient, service_id: int):
        pass

    @staticmethod
    def get_open_feature_events(db: IDBClient, service_id: int, feature_id: int):
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
            # TODO maybe have a on /off switch for event close, if online may require manual intervention 
            # event close
            pass
        else:
            pass
#endregion