import os

SG_ENV = os.environ.get('SG_ENV', 'dev')
DEBUG = (SG_ENV == "dev")
BASE_URL = "https://a2h4.showoff.io"
