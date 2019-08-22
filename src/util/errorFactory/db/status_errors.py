class InvalidStatus(Exception):
    def __init__(self, status):

        super().__init__(f"Status {str(status)}, does not exist!")