from ...conf.Configuration import Configuration
from ....util.errorFactory.core.ConfigErrors import ConfigAttributeDoesNotExist
import json

class FlaskConfiguration(Configuration):

    def __init__(self,file,requiredAttributes=None,defaultValues=None):
        self.debug=None
        self.ENV=None
        self.title=None
        self.version=None
        self.description=None
        self.cors_enabled=None
        self.cors_resource_setting=None
        self.cors_with_creds=None
        self.angular_client=None
        self.angular_client_directory=None


        super().__init__(file,requiredAttributes,defaultValues)
        self._read_config(file)

    def update_config(self,file,key,value):
        pass

    def _read_config(self,file):
        self._initialize_object(json.load(open(file)))
        self._check_defaults()

    def _initialize_object(self,json):

        for config_item in json.keys():
            if self._attribute_exists(json,config_item):
                 setattr(self,config_item,json[config_item])

            elif self._is_default(config_item):
                setattr(self,config_item,self._grab_default(config_item))

            elif self._is_attribute_required(config_item):
                raise ConfigAttributeDoesNotExist(config_item)

    def _check_defaults(self):
        if self._defaults is None:
            return
        for default in self._defaults.keys():
            if hasattr(self,default) and getattr(self,default) is not None:
                continue
            else:
                setattr(self,default,self._defaults[default])


