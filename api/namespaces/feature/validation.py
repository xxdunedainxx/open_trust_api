from api.api_util.validators import Validators
from marshmallow import Schema, fields, ValidationError

class feature_validators:
    class validateFeature(Schema):
        feature_id=fields.Integer(required=True,validate=Validators.validate_feature)

    class validateServiceInformation(Schema):
        name=fields.String(required=True)

    class validateServiceDescription(Schema):
        name=fields.String(required=True,validate=Validators.validate_desciption)