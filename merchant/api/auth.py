# -*- coding: utf-8 -*-

from merchant.core import (
    MerchantResource,
    ParserMixin,
    NotFoundResourceException,
)

user_lists = ['admin', 'kiven']


class MerchantAuthResource(MerchantResource, ParserMixin):

    def get(self, username=None):
        if username != 'kiven':
            raise NotFoundResourceException('Username %s not found' % username)
        else:
            return user_lists
