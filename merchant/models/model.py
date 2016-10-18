# -*- coding: utf-8 -*-

import datetime
import functools
import logging

from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

logger = logging.getLogger(__name__)
db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/merchant.db"
    db.init_app(app)
    db.app = app
    db.create_all()
    return db


def safe_session(func):
    @functools.wraps(func)
    def deco(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(e)
            raise
        finally:
            db.session.close()
    return deco


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                          onupdate=datetime.datetime.utcnow)


class Shop(Base):

    __tablename__ = 'shop'

    shop_name = db.Column(db.String(50), nullable=False)  # 店铺名字
    shop_logo = db.Column(db.String(100))                 # 店铺logo
    shop_remark = db.Column(db.String(100))               # 店铺备注
    collected_num = db.Column(db.Integer, default=0)      # 被收藏次数
    sales_day = db.Column(db.Integer, default=0)          # 日销量
    sales_month = db.Column(db.Integer, default=0)        # 月销量
    status = db.Column(db.Integer, nullable=False)        # 状态(0/1)
    creator = db.Column(db.String(20), nullable=False)    # 创建者
    reserved = db.Column(db.String(500))                  # 备用

    def to_dict(self):
        return {
            'id': self.id,
            'shop_name': self.shop_name,
            'shop_logo': self.shop_logo,
            'shop_remark': self.shop_remark,
            'collected_num': self.collected_num,
            'sales_day': self.sales_day,
            'sales_month': self.sales_month,
            'status': self.status,
            'creator': self.creator,
            'reserved': self.reserved,
        }

    @classmethod
    @safe_session
    def create(cls, shop_name, shop_status, shop_creator, shop_log=None,
               shop_remark=None):
        shop = cls(shop_name=shop_name, status=shop_status,
                   creator=shop_creator)
        db.session.add(shop)
        db.session.commit()
        return shop.to_dict()

    @classmethod
    @safe_session
    def get(cls, shop_id):
        shop = db.session.query(cls).get(shop_id)
        if shop:
            return shop.to_dict()

    @classmethod
    @safe_session
    def update(cls, shop_id, **kwargs):
        db.session.query(cls).filter(cls.id == shop_id).update(kwargs)
        db.session.commit()

    @classmethod
    @safe_session
    def all(cls):
        shops = db.session.query(cls).order_by(cls.id)
        return [shop.to_dict() for shop in shops]

    @classmethod
    @safe_session
    def limit_all(cls, limit=100):
        current_id = 0
        while True:
            shops = db.session.query(cls).filter(cls.id > current_id).\
                order_by(cls.id).limit(limit).all()  # noqa
            if not shops:
                break
            current_id = shops[-1].id

            for shop in shops:
                res = shop.to_dict()
                yield res


class Goods(Base):
    __tablename__ = 'goods'

    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    goods_code = db.Column(db.String(20), nullable=False)    # 商品编码
    goods_name = db.Column(db.String(100), nullable=False)   # 商品名字
    local_type = db.Column(db.Integer, nullable=False)       # 所属类别 例: 水果
    type_name = db.Column(db.String(30), nullable=False)     # 类别名称
    goods_price = db.Column(db.Float, nullable=False)        # 商品价格
    goods_property = db.Column(db.String(50))                # 商品属性
    to_top = db.Column(db.Integer, default=0)                # 是否置顶
    goods_pic = db.Column(db.String(300))                    # 商品图片
    original_price = db.Column(db.Float)                     # 市场价
    status = db.Column(db.Integer, nullable=False)           # 状态
    reserved = db.Column(db.String(500))                     # 备注

    def to_dict(self):
        return {
            'id': self.id,
            'shop_id': self.shop_id,
            'goods_code': self.goods_code,
            'goods_name': self.goods_name,
            'local_type': self.local_type,
            'type_name': self.type_name,
            'goods_price': self.goods_price,
            'status': self.status
        }

    @classmethod
    @safe_session
    def create(cls, shop_id, goods_code, goods_name, local_type, type_name,
               goods_price, status):
        goods = cls(shop_id=shop_id, goods_code=goods_code, goods_name=goods_name,
                    local_type=local_type, type_name=type_name, goods_price=goods_price,
                    status=status)
        db.session.add(goods)
        db.session.commit()
        return goods.to_dict()

    @classmethod
    @safe_session
    def get(cls, shop_id, goods_id_or_name):
        goods = db.session.query(cls).filter(cls.shop_id == shop_id).\
            filter(or_(cls.id == goods_id_or_name, cls.goods_name == goods_id_or_name))
        if goods:
            return [g.to_dict() for g in goods]

    @classmethod
    @safe_session
    def all(cls, shop_id):
        goods = db.session.query(cls).filter(cls.shop_id == shop_id)
        return [g.to_dict() for g in goods]

    @classmethod
    @safe_session
    def limit_all(cls, shop_id, limit=100):
        current_id = 0
        while True:
            shops = db.session.query(cls).\
                filter(cls.shop_id == shop_id).\
                filter(cls.id > current_id).\
                order_by(cls.id).limit(limit).all()  # noqa
            if not shops:
                break
            current_id = shops[-1].id

            for shop in shops:
                res = shop.to_dict()
                yield res
