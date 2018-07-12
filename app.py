#TODO :: install and set up structure for flask apis
#TODO :: begin to integrate sql db schemas with flask apis


from conf.conf import db
from data.models.service import Service, new_service, get_service_by_name,get_service_by_id, deactivate_service,reactivate_service, change_service_status
from data.models.feature import *
from data.models.status import serve_sprite_path
#test_get=get_service_by_name("testerrr",db)
#t=new_service("test", "testing db routines", db)
t=get_service_by_id(1,db)
#change_service_status(1, "BROKEN",db)

deactivate_service(1,db)
p=serve_sprite_path(1,db)

#features=get_all_features_by_service_id(1,db)
exit(0)