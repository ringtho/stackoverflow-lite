import os

class Config():
    TESTING = False
    DATABASE_URI = 'postgres://sringtho:.Adgjmp1@localhost/stackoverflow'

class ProductionConfig(Config):
    DATABASE_URI = os.environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True