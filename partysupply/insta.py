import instagram.client
import instagram.bind

INSTAGRAM_CLIENT_ID = "f3d7765e22254561bb9d784666a7c772"
INSTAGRAM_CLIENT_SECRET = "4774228b55044b268e6143b93ddb4d31"

api = instagram.client.InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                                    client_secret=INSTAGRAM_CLIENT_SECRET)

# HACK: force tag_recent_media to return the raw json structure
def my_tag_recent_media(*args):
    fn = instagram.bind.bind_method(
        path="/tags/{tag_name}/media/recent",
        accepts_parameters=instagram.client.MEDIA_ACCEPT_PARAMETERS + ['tag_name'],
        objectify_response=False)
    return fn(api, *args)
