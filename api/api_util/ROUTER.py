# Service routes
SERVICE_ROUTE_BASE="/api/service"
GET_ALL_SERVICES=f"{SERVICE_ROUTE_BASE}/list_services"
GET_SPECIFIC_SERVICE=f"{SERVICE_ROUTE_BASE}/<int:service_id>"

# Feature Routes
FEATURE_ROUTE_BASE=f"/<int:service_id>/feature"
GET_SPECIFIC_FEATURE=f"/<int:service_id>/<int:feature_id>"
GET_ALL_FEATURES_BY_SERVICE=f"/<int:service_id>/list_features"

# Event Routes Service
EVENT_ROUTE_BASE_SERVICE=f"{SERVICE_ROUTE_BASE}/event"
GET_SPECIFIC_EVENT_SERVICE=f"{EVENT_ROUTE_BASE_SERVICE}/<int:event_id>"
GET_ALL_EVENTS_BY_SERVICE=f"{EVENT_ROUTE_BASE_SERVICE}/list_events"

# Event Routes Feature