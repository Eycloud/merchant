# -*- coding: utf-8 -*-

import datetime
import functools
import logging

from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

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
            'reserved': self.reserved
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
