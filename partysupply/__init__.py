import os
import logging
import logging.config

import instagram.client

current_path = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
logging.config.fileConfig(os.path.join(current_path, '..', 'logging.conf'))
logger = logging.getLogger(__name__)

from partysupply.server import (run_server,
                                INSTAGRAM_CLIENT_ID,
                                INSTAGRAM_CLIENT_SECRET)


def cli(args, options):
    if args[0] == "server":
        run_server(options.port)
    if args[0] == "subscription":
        api = instagram.client.InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                                            client_secret=INSTAGRAM_CLIENT_SECRET)
        if args[1] == "add":
            tyype, object_id = args[2:4]
            ident = "%s::%s" % (tyype, object_id)
            callback_url = "https://n1p.showoff.io/instagram/subscriptions/%s" % (ident,)
            logger.info("Adding subscription for %s %s", tyype, object_id)
            resp = api.create_subscription(object='tag',
                                           object_id=object_id,
                                           aspect='media',
                                           # TODO: parameterize url
                                           callback_url=callback_url)
            print resp
        elif args[1] == "list":
            print api.list_subscriptions()
    else:
        from IPython.Shell import IPythonShellEmbed
        ipshell = IPythonShellEmbed([])
        ipshell()
