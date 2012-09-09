import os
import urlparse
import logging
import json

import redis

from config import BASE_URL
from insta import api, my_tag_recent_media


REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
_url = urlparse.urlparse(REDIS_URL, scheme="redis")
_, _, _db = _url.path.rpartition("/")
REDIS = redis.StrictRedis(_url.hostname, _url.port, int(_db))

logger = logging.getLogger(__name__)


def process_update(update):
    # TODO: debounce this
    logger.debug("Update for %s/%s %s", update["object"], update["object_id"], update)


class Subscription(object):

    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_

    def update_media(self, limit=10, max_id=None):
        if self.type_ == "tag":
            logger.info("Updating media for %s/%s", self.type_, self.id_)
            resp = my_tag_recent_media(limit, max_id, self.id_)
            with REDIS.pipeline() as pipe:
                sorted_set_key = "partysupply:tag:%s:media_ids" % (self.id_,)
                for media in resp["data"]:
                    created_time = int(media["created_time"])
                    pipe.zadd(sorted_set_key, created_time, media["id"])
                    pipe.hset("partysupply:media", media["id"], json.dumps(media))
                pipe.execute()

    @classmethod
    def ensure_exists(cls, type_, id_):
        key = "partysupply:subscriptions:%s" % (type_,)
        if REDIS.hget(key, id_) is None:
            cls.add_subscription(type_, id_)

    @classmethod
    def add_subscription(cls, type_, id_):
        logger.info("Adding subscription for %s/%s", type_, id_)
        callback_url = "%s/instagram/subscriptions/%s/%s" % (BASE_URL, type_, id_)
        resp = api.create_subscription(object=type_,
                                       object_id=id_,
                                       aspect='media',
                                       # TODO: parameterize url
                                       callback_url=callback_url)

    @classmethod
    def cache_subscriptions(cls, type_):
        logger.info("Caching %s subscriptions", type_)
        resp = api.list_subscriptions()
        with REDIS.pipeline() as pipe:
            key = "partysupply:subscriptions:%s" % (type_,)
            try:
                pipe.watch(key)
                pipe.multi()
                pipe.delete(key)
                for sub in resp["data"]:
                    if sub["object"] == type_:
                        pipe.hset(key, sub["object_id"], json.dumps(sub))
                pipe.execute()
            except redis.WatchError:
                pass


class Media(object):

    @classmethod
    def find_by_tag_and_created_time(cls, id_, min_created_time):
        key = "partysupply:tag:%s:media_ids" % (id_,)
        ids = REDIS.zrangebyscore(key, min_created_time, float("inf"))
        data = REDIS.hmget("partysupply:media", ids)
        return [json.loads(d) for d in data]

    @classmethod
    def find_by_tag(cls, id_, limit):
        key = "partysupply:tag:%s:media_ids" % (id_,)
        ids = REDIS.zrange(key, limit * -1, -1)
        data = REDIS.hmget("partysupply:media", ids)
        return [json.loads(d) for d in data]

