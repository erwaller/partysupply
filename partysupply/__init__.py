import os
import logging
import logging.config

current_path = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
logging.config.fileConfig(os.path.join(current_path, '..', 'logging.conf'))
logger = logging.getLogger(__name__)

from partysupply.server import run_server
from partysupply.insta import api
from partysupply.models import Subscription


def cli(args, options):
    if args[0] == "server":
        run_server(options.port)
    if args[0] == "subscription":
        if args[1] == "add":
            obj, object_id = args[2:4]
            Subscription.ensure_exists(obj, object_id)
            Subscription(obj, object_id).update_media(limit=50)
        elif args[1] == "list":
            resp = api.list_subscriptions()
            print "%10s\t%10s\t%10s\t%10s" % ("id", "object", "object_id", "callback_url")
            for sub in resp["data"]:
                print "%10s\t%10s\t%10s\t%10s" % (sub["id"], sub["object"], sub["object_id"], sub["callback_url"])
        elif args[1] == "delete":
            resp = api.delete_subscriptions(id=args[2])
            # TODO: don't assume "tag" here
            Subscription.cache_subscriptions("tag")
            print resp
    else:
        from IPython.Shell import IPythonShellEmbed
        ipshell = IPythonShellEmbed([])
        ipshell()
