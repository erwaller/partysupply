import os

SG_ENV = os.environ.get('SG_ENV', 'dev')
DEBUG = (SG_ENV == "dev")
BASE_URL = "https://2cd3.showoff.io"
