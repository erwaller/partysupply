import instagram.client
import instagram.bind

import config

api = instagram.client.InstagramAPI(client_id=config.INSTAGRAM_CLIENT_ID,
                                    client_secret=config.INSTAGRAM_CLIENT_SECRET)

# HACK: force tag_recent_media to return the raw json structure
def my_tag_recent_media(*args):
    fn = instagram.bind.bind_method(
        path="/tags/{tag_name}/media/recent",
        accepts_parameters=instagram.client.MEDIA_ACCEPT_PARAMETERS + ['tag_name'],
        objectify_response=False)
    return fn(api, *args)
