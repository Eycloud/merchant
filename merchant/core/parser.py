# -*- coding: utf-8 -*-

from flask_restful import reqparse


class ParserMixin(object):

    @staticmethod
    def get_key(key, required=False):
        parser = reqparse.RequestParser()
        parser.add_argument(key, type=unicode, help="", required=required)
        return parser.parse_args().get(key)
