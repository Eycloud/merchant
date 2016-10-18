# -*- coding: utf-8 -*-

import logging

from flask import jsonify

from merchant.core import (
    MerchantResource,
    ParserMixin,
    NotFoundResourceException,
)
from merchant.models.model import Goods

logger = logging.getLogger(__name__)


class GoodsResource(MerchantResource, ParserMixin):

    def get(self, shop_id, goods_id_or_name=None):
        logger.info('Get shop_id: %s, goods_id_or_name: %s ' % (shop_id, goods_id_or_name))
        if goods_id_or_name is not None:
            res = Goods.get(shop_id, goods_id_or_name)
        else:
            res = Goods.all(shop_id)
        if not res:
            raise NotFoundResourceException(
                "Goods %s not found" % goods_id_or_name)
        return jsonify(res)

    def post(self, shop_id):
        goods_code = self.get_key('goods_code', required=True)
        goods_name = self.get_key('goods_name', required=True)
        local_type = self.get_key('local_type', required=True)
        type_name = self.get_key('type_name', required=True)
        goods_price = self.get_key('goods_price', required=True)
        status = self.get_key('status', required=True)
        res = Goods.create(shop_id, goods_code, goods_name, local_type,
                           type_name, goods_price, status)
        return jsonify(res)
