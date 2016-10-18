# -*- coding: utf-8 -*-

import logging

from flask import jsonify

from merchant.core import (
    MerchantResource,
    ParserMixin,
    NotFoundResourceException
)
from merchant.models.model import Shop

logger = logging.getLogger(__name__)


class ShopResource(MerchantResource, ParserMixin):

    def get(self, shop_id=None):
        logger.info("Get shop_id %s" % shop_id)
        if shop_id is not None:
            res = Shop.get(shop_id)
        else:
            res = Shop.all()
        if not res:
            raise NotFoundResourceException("Shop id %s not found" % shop_id)
        return jsonify(res)

    def post(self):
        shop_name = self.get_key('shop_name', required=True)
        shop_status = self.get_key('shop_status', required=True)
        shop_creator = self.get_key('shop_creator', required=True)
        res = Shop.create(shop_name, shop_status, shop_creator)
        return jsonify(res)
