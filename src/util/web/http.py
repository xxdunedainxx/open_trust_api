from flask_restplus import reqparse
from flask import request

def http_parse(args):
    parse_args = reqparse.RequestParser()
    for arg in args.keys():
        parse_args.add_argument(arg, type=type(args[arg]))
    structure = parse_args.parse_args()
    return structure


def http_parse_simple(args,arg):

    if arg in args.keys():
        return args[arg]
    else:
        return None

def get_page_number(req_args):
    page = http_parse_simple(req_args, 'page')
    if page is not None:
        page = int(page)

    return page

def get_loged_in_user(dev=False):
    auth_user = request.headers.get('X-Remote-User')
    if dev is True:
        return "opentrustuser"
    elif auth_user is None:
        return "null"
    else:
        return auth_user