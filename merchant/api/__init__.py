# -*- coding: utf-8 -*-

from flask_restful import Api
from flask import Blueprint

from auth import MerchantAuthResource
from shop import ShopResource
from goods import GoodsResource

api_bp = Blueprint('merchant_api', __name__)
api = Api(api_bp)

api.add_resource(MerchantAuthResource, '/auth/<username>', '/auth',
                 endpoint='merchant_auth')
api.add_resource(ShopResource, '/shop/<shop_id>', '/shops',
                 endpoint='merchant_shop')
api.add_resource(GoodsResource, '/shop/<shop_id>/goods/<goods_id_or_name>', '/shop/<shop_id>/goods',
                 endpoint='merchant_goods')
