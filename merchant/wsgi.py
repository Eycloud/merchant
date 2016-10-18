# -*- coding: utf-8 -*-

import logging
from gevent.wsgi import WSGIServer

from app import create_app

logger = logging.getLogger(__name__)
app = create_app()
PORT = 5000

logger.info("Start http server on port: %d" % PORT)
http_server = WSGIServer(('', PORT), app)
