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

from models import Subscription, Media
import config

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):

    @property
    def tags(self):
        return self.application.tags


class IndexHandler(BaseHandler):

    def get(self):
        bootstrap_data = dict(posts=Media.find_by_tag(self.tags[0], 15))
        self.render("index.html", bootstrap_data_json=json.dumps(bootstrap_data),
                                  tags=self.tags)


class PostsHandler(BaseHandler):

    def get(self):
        min_created_time = self.get_argument("since", 0)
        ids = Media.find_by_tag_and_created_time(self.tags[0], min_created_time)
        ret = dict(posts=ids, meta=dict(tags=self.tags))
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(ret))


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
            logger.info("Received updates for subscription: %s/%s", obj, object_id)
            self.application.reactor.process(config.INSTAGRAM_CLIENT_SECRET,
                                             raw_body,
                                             x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            logger.error("Signature mismatch for subscription: %s/%s", obj, object_id)
        # I don't know why this is necessary...
        self.write("Thanks Instagram!")


class Application(tornado.web.Application):

    def __init__(self, tags, **settings):
        routes = [
            (r"^/$", IndexHandler),
            # (r"^/instagram/subscriptions", SubscriptionsHandler),
            (r"^/posts", PostsHandler),
            (r"^/instagram/subscriptions/([a-z0-9_-]+)/([a-z0-9_-]+)", SubscriptionsHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=config.DEBUG,
        )
        tornado.web.Application.__init__(self, routes, **settings)
        self.reactor = subscriptions.SubscriptionsReactor()
        self.reactor.register_callback(subscriptions.SubscriptionType.TAG,
                                       self.process_update)
        self.tags = tags

    def process_update(self, update):
        # TODO: debounce this
        logger.debug("Received update for %s/%s %s", update["object"], update["object_id"], update)
        def defer():
            Subscription(update["object"], update["object_id"]).update_media(limit=5)
        tornado.ioloop.IOLoop.instance().add_callback(defer)


def run_server(port, tags):
    tornado.options.parse_command_line()

    application = Application(tags)
    application.listen(port, xheaders=True)
    logger.info("api started 0.0.0.0:%d [%s] %d", int(port), config.SG_ENV, os.getpid())
    tornado.ioloop.IOLoop.instance().start()
