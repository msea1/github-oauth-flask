import os


class Config:
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "default")


class DevConfig(Config):
    DEVELOPMENT = True


class ProdConfig(Config):
    pass
