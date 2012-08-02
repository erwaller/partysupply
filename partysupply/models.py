import os
import urlparse
import logging

import redis


REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
_url = urlparse.urlparse(REDIS_URL, scheme="redis")
_, _, _db = _url.path.rpartition("/")
REDIS = redis.StrictRedis(_url.hostname, _url.port, int(_db))

logger = logging.getLogger(__name__)


def process_update(update):
    # TODO: debounce this
    logger.debug("Update for %s/%s %s", update["object"], update["object_id"], update)
    