class InternalAPIError(Exception):

    def __init__(self, message, returnCode):
        self.msg=message
        self.rCode=returnCode

        self.raise_error()

    def raise_error(self):
        return {"message" : self.msg, "ok" : False},self.rCode

DEFAULT_INTERNAL_SERVER_ERROR={"message" : "Internal Server issues..", "ok" : False},501

def PayloadMustExist(fields: str):
    api_error=InternalAPIError(
        message=f"Payload and field \"id\" cannot be null. Or further fields must be provided: {fields} !",
        returnCode=400
    )

    return api_error.raise_error()