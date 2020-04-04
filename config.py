import os
from dotenv import load_dotenv
from os.path import dirname, join, abspath

basedir = abspath(dirname(dirname(__file__)))

env_path = join(dirname(dirname(__file__)),'.flaskenv')
load_dotenv(env_path)

db_name =  os.environ.get('DATABASE_NAME')
localhost = os.environ.get('HOSTNAME')
password = os.environ.get('DB_PASSORD')
username = os.environ.get('DB_USER')
type_db = os.environ.get('DB_TYPE')

uri_database_server = f'{type_db}+pymysql://{username}:{password}@{localhost}/{db_name}' or 'sqlite:///' + join(basedir, 'app.db')

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.environ.get('SECRET')
    SQLALCHEMY_DATABASE_URI = uri_database_server

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/adjame_market'
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}