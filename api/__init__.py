from flask_restplus import Api

from flask import Flask,send_from_directory
from flask_cors import CORS

# API Imports
from api.namespaces.service.service_api import api as ServiceAPI
from api.namespaces.feature.feature_api import api as FeatureAPI

import api.api_util.ROUTER as ROUTER

api = Api(
    title='Open Trust Application Interface',
    version='1.0',
    description='Backend logic for open trust application'
)

# Add Namespaces
api.add_namespace(ServiceAPI,ROUTER.SERVICE_ROUTE_BASE)
api.add_namespace(FeatureAPI, ROUTER.SERVICE_ROUTE_BASE)