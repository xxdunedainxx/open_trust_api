class FeatureNameAlreadyExists(Exception):
    def __init__(self, message):

        super().__init__(message)

class FeatureDoesNotExist(Exception):
    def __init__(self, message):

        super().__init__(message)