# Service routes
SERVICE_ROUTE_BASE="/api/service"
GET_ALL_SERVICES=f"{SERVICE_ROUTE_BASE}/list_services"
GET_SPECIFIC_SERVICE=f"{SERVICE_ROUTE_BASE}/get_service/<int:service_id>"