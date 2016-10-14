# -*- coding: utf-8 -*-

from gevent.wsgi import WSGIServer

from app import create_app

app = create_app()

http_server = WSGIServer(('', 5000), app)
