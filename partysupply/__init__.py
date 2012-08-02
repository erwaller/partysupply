import os
import logging
import logging.config

current_path = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
logging.config.fileConfig(os.path.join(current_path, '..', 'logging.conf'))
logger = logging.getLogger(__name__)

from partysupply.server import run_server
from partysupply.insta import api


def cli(args, options):
    if args[0] == "server":
        run_server(options.port)
    if args[0] == "subscription":
        if args[1] == "add":
            obj, object_id = args[2:4]
            callback_url = "https://7s7w.showoff.io/instagram/subscriptions/%s/%s" % (obj, object_id)
            logger.info("Adding subscription for %s/%s", obj, object_id)
            resp = api.create_subscription(object='tag',
                                           object_id=object_id,
                                           aspect='media',
                                           # TODO: parameterize url
                                           callback_url=callback_url)
            print resp
        elif args[1] == "list":
            resp = api.list_subscriptions()
            print "%10s\t%10s\t%10s\t%10s" % ("id", "object", "object_id", "callback_url")
            for sub in resp["data"]:
                print "%10s\t%10s\t%10s\t%10s" % (sub["id"], sub["object"], sub["object_id"], sub["callback_url"])
        elif args[1] == "delete":
            resp = api.delete_subscriptions(id=args[2])
            print resp
    else:
        from IPython.Shell import IPythonShellEmbed
        ipshell = IPythonShellEmbed([])
        ipshell()
