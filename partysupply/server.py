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

logger = logging.getLogger(__name__)

INSTAGRAM_CLIENT_ID = "f3d7765e22254561bb9d784666a7c772"
INSTAGRAM_CLIENT_SECRET = "4774228b55044b268e6143b93ddb4d31"


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):

    def get(self):
        self.write("hello!")


class SubscriptionsHandler(BaseHandler):

    def get(self, ident=None):
        mode = self.get_argument("hub.mode")
        self.write(self.get_argument("hub.challenge"))
        logger.debug("Received acknowledgement for subscription: %s", ident)

    def process_tag_update(self, update):
        logger.debug("Update for %s %s", self.ident, update)

    def post(self, ident=None):
        self.ident = ident
        x_hub_signature = self.request.headers.get('X-Hub-Signature')
        raw_body = self.request.body
        reactor = subscriptions.SubscriptionsReactor()
        reactor.register_callback(subscriptions.SubscriptionType.TAG, self.process_tag_update)
        try:
            logger.debug("Received updates for subscription: %s", ident)
            reactor.process(INSTAGRAM_CLIENT_SECRET, raw_body, x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            logger.debug("Signature mismatch for subscription: %s", ident)
        self.write("Thanks Instagram!")


class Application(tornado.web.Application):

    def __init__(self, routes, **settings):
        tornado.web.Application.__init__(self, routes, **settings)


def get_application(**kwargs):
    routes = [
        (r"^/$", IndexHandler),
        # (r"^/instagram/subscriptions", SubscriptionsHandler),
        (r"^/instagram/subscriptions/([^\/]+)", SubscriptionsHandler),
    ]
    return Application(routes, **kwargs)


def run_server(port=8080):
    env = os.environ.get('SG_ENV', 'dev')
    application = get_application(debug=(env == "dev"))

    application.listen(port, xheaders=True)

    logger.info("api started 0.0.0.0:%d [%s] %d", int(port), env, os.getpid())

    tornado.ioloop.IOLoop.instance().start()
