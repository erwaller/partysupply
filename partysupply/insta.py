import instagram.client

INSTAGRAM_CLIENT_ID = "f3d7765e22254561bb9d784666a7c772"
INSTAGRAM_CLIENT_SECRET = "4774228b55044b268e6143b93ddb4d31"

api = instagram.client.InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                                    client_secret=INSTAGRAM_CLIENT_SECRET)
