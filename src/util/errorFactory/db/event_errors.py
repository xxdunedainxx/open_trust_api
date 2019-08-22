class EventInactive(Exception):
    def __init__(self, event):

        super().__init__(f"Event ID {event} is inactive")

class EventDoesNotExist(Exception):
    def __init__(self, message):

        super().__init__(message)

class EventExists(Exception):
    def __init__(self, event):

        super().__init__(f"Event already exists!")
