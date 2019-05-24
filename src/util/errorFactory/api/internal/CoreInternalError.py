class InternalAPIError():

    def __init__(self, message, returnCode):
        self.msg=message
        self.rCode=returnCode

    def raise_error(self):
        return {"message" : self.msg, "ok" : False},self.rCode