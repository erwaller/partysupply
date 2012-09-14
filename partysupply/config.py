import os

SG_ENV = os.environ.get("SG_ENV", "dev")
DEBUG = (SG_ENV == "dev")
BASE_URL = os.environ.get("BASE_URL")
TAGS = os.environ.get("TAGS", "starbucks").split(",")

INSTAGRAM_CLIENT_ID = os.environ["INSTAGRAM_CLIENT_ID"]
INSTAGRAM_CLIENT_SECRET = os.environ["INSTAGRAM_CLIENT_SECRET"]
