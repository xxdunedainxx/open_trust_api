from api import api # ,logger


# Error handling

@api.errorhandler
def default_error_handler(error):
    """Default error handler"""
    #logger.error(error)
    return {'message': 'Internal Server Error'}, 500