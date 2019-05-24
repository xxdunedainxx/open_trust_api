class OverideServiceNumber (Exception):
    def __init__(self ):
        super().__init__("You are required to override services.")
class InvalidNumberOfServicesProvided (Exception):
    def __init__(self,expected: int, provided: int):
        super().__init__(f"Invalid number of services provided for this job."
                         f"\nExpected: {str(expected)}. "
                         f"\nProvided: {str(provided)}"
                         )
