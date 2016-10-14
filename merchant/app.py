# -*- coding: utf-8 -*-

from flask import Flask, jsonify

from settings import DEBUG
from api import api_bp
from core import NotFoundResourceException


class Merchant(Flask):
    def __init__(self):
        super(Merchant, self).__init__('Merchant')
        self.url_prefix = '/api'
        self.register_blueprints()
        self.register_error_handlers()

    def register_blueprints(self):
        self.register_blueprint(api_bp, url_prefix=self.url_prefix)

    def register_error_handlers(self):
        self.register_error_handler(NotFoundResourceException, self.not_found)

    @staticmethod
    def not_found(err):
        res = jsonify(err.to_dict())
        res.status_code = err.status_code
        return res


def create_app():
    app = Merchant()
    app.config['DEBUG'] = DEBUG

    return app
