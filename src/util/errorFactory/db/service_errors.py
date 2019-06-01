class ServiceNameAlreadyExists(Exception):
    def __init__(self, message):

        super().__init__(message)

class ServiceDoesNotExist(Exception):
    def __init__(self, message):

        super().__init__(message)