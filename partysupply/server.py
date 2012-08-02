import os
import sys
import logging
import time
import ujson as json

import tornado
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.curl_httpclient import CurlAsyncHTTPClient

from instagram import client, subscriptions

from models import process_update
from insta import INSTAGRAM_CLIENT_SECRET

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):

    def get(self):
        self.write("hello!")


class SubscriptionsHandler(BaseHandler):

    def get(self, obj, object_id):
        mode = self.get_argument("hub.mode")
        self.write(self.get_argument("hub.challenge"))
        logger.debug("Received acknowledgement for subscription: %s/%s", obj, object_id)

    def post(self, obj, object_id):
        self.object = obj
        self.object_id = object_id
        x_hub_signature = self.request.headers.get('X-Hub-Signature')
        raw_body = self.request.body
        try:
            logger.debug("Received updates for subscription: %s/%s", obj, object_id)
            self.application.reactor.process(INSTAGRAM_CLIENT_SECRET,
                                             raw_body,
                                             x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            logger.debug("Signature mismatch for subscription: %s/%s", obj, object_id)
        # I don't know why this is necessary...
        self.write("Thanks Instagram!")


class Application(tornado.web.Application):

    def __init__(self, routes, **settings):
        tornado.web.Application.__init__(self, routes, **settings)
        self.reactor = subscriptions.SubscriptionsReactor()
        self.reactor.register_callback(subscriptions.SubscriptionType.TAG,
                                       process_update)


def get_application(**kwargs):
    routes = [
        (r"^/$", IndexHandler),
        # (r"^/instagram/subscriptions", SubscriptionsHandler),
        (r"^/instagram/subscriptions/([a-z0-9_-]+)/([a-z0-9_-]+)", SubscriptionsHandler),
    ]
    return Application(routes, **kwargs)


def run_server(port=8080):
    env = os.environ.get('SG_ENV', 'dev')
    application = get_application(debug=(env == "dev"))

    application.listen(port, xheaders=True)

    logger.info("api started 0.0.0.0:%d [%s] %d", int(port), env, os.getpid())

    tornado.ioloop.IOLoop.instance().start()
