import os

S3_BUCKET = "dakobed-transcriptions-service"
S3_KEY = os.environ.get("AWS_ACCESS_KEY")
S3_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000

import os


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SECRET_KEY = "my_precious"


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    pass


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    pass


class ProductionConfig(BaseConfig):
    """Production configuration"""

    pass

