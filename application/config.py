import os
from os.path import dirname


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    PROJECT_NAME = "rd_cms"
    BASE_DIRECTORY = dirname(dirname(os.path.abspath(__file__)))

    # Should point to content repo top level directory
    CONTENT_REPO = os.environ['RD_CONTENT_REPO']
    CONTENT_DIRECTORY = '/'.join((CONTENT_REPO, "content"))
    WTF_CSRF_ENABLED = False


class DevConfig(Config):
    DEBUG = True


class TestConfig(DevConfig):
    TESTING = True
