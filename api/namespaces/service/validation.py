from api.api_util.validators import Validators
from marshmallow import Schema, fields, ValidationError

class service_validators:
    class validateService(Schema):
        service_id=fields.Integer(required=True,validate=Validators.validate_service)