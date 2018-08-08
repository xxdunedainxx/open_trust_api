from marshmallow import Schema, fields, ValidationError

MAX_ALLOWED_DESCRIPTION=100


# TODO :: SECURITY CHECKS FOR EACH
class Validators:


    @staticmethod
    def validate_service(servce_id):
        pass


    @staticmethod
    def validate_feature(feature_id):
        pass

    @staticmethod
    def validate_desciption(description):
        if len(description) > MAX_ALLOWED_DESCRIPTION:
            raise ValidationError("description longer than allowed length!")