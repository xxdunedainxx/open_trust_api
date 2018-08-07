# TODO :: finish service APIs/  feature APIs / status APIs
# TODO :: Once these apis are complete, MVP for client can begin
# TODO :: EVENT MODEL / EVENT COMMENT MODEL
from flask import Flask,send_from_directory
from flask_cors import CORS
from api import api

from conf.conf import db
from data.models.service import Service, new_service, get_service_by_name,get_service_by_id, deactivate_service,reactivate_service, change_service_status
from data.models.feature import *
from data.models.status import serve_sprite_path

app = Flask(__name__)
CORS(app)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)

#features=get_all_features_by_service_id(1,db)
exit(0)