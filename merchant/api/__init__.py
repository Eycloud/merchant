# -*- coding: utf-8 -*-

from flask_restful import Api
from flask import Blueprint

from auth import MerchantAuthResource

api_bp = Blueprint('merchant_api', __name__)
api = Api(api_bp)

api.add_resource(MerchantAuthResource, '/auth/<username>', '/auth',
                 endpoint='merchant_auth')
