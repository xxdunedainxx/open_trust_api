from google_transfer1_0.core.util.errorFactory.api_errors.internal.CoreInternalError import InternalAPIError

class CouldNotFindTransferEvent(InternalAPIError):
    def __init__(self,tid):
        super().__init__(
            message=f"Could find transfer event {tid}",
            returnCode=404)