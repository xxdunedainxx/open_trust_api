from flask_restplus import reqparse


def http_parse(args):
    parse_args = reqparse.RequestParser()
    for arg in args.keys():
        parse_args.add_argument(arg, type=type(args[arg]))
    structure = parse_args.parse_args()
    return structure