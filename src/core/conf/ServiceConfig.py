from ..conf.Configuration import Configuration

class ServiceConfig(Configuration):

    required_attributes = [""]
    default_attributes = {}

    def __init__(self,file,requiredAttributes: [] = None, defaultAttributes: {} = None):
        self.svc_name:  str="Default Service Config"
        self.svc_description: str="Some service description"
        self.svc_version: str="0"
        self.svc_namespace: str="blank"
        self.authors: [str]=["zach.mcfadden"]
        self.last_update: str="N/A"

        super().__init__(
                file,
                requiredAttributes=requiredAttributes if requiredAttributes is not None else ServiceConfig.required_attributes,
                defaultAttributes=defaultAttributes if defaultAttributes is not None else ServiceConfig.default_attributes
        )
