from google_transfer1_0.core.util.errorFactory.api_errors.internal.CoreInternalError import InternalAPIError

class InvalidArgumentProvideed(InternalAPIError):
    def __init__(self,arg, expectedDataType):
        super().__init__(
            message=f"{arg} data type not allowed for this API",
            returnCode=404)

class TransferInactive(InternalAPIError):
    def __init__(self,tid):
        super().__init__(
            message=f"{tid} is inactive",
            returnCode=410 )