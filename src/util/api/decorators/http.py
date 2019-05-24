
# General library imports
from functools import wraps
import os

# Flask imports
from flask import request

# log in user import
from ...web.http import get_loged_in_user

# Logging
from ...logging.LogFactory import LogFactory



def http_logger(api):
    @wraps(api)
    def logger_wrapper(*args, **kwargs):
            if 'http_log_override' in kwargs.keys():
                Logger = args['http_log_override']
            else:
                Logger = LogFactory(f"{os.getcwd()}http_info.log")
            Logger.write_log(data=f"Method - {request.method} // Endpoint - {request.base_url} // User {get_loged_in_user()}")
            Logger.commit_data()
            return api(*args,**kwargs)
    return logger_wrapper