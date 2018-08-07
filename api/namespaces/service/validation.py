from api.api_util.validators import Validators
from marshmallow import Schema, fields, ValidationError

class service_validators:
    class validateService(Schema):
        service_id=fields.Integer(required=True,validate=Validators.validate_service)

    class validateServiceInformation(Schema):
        name=fields.String(required=True)

    class validateServiceDescription(Schema):
        name=fields.String(required=True,validate=Validators.validate_desciption)