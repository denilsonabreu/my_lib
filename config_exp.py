# export ml_lgbm_ENV=production

from dotenv import load_dotenv
from os import environ

# environ['DB_ENV'] = 'development'

load_dotenv()


class DevelopmentConfig():
    __db = environ['DB_NAME']
    __host = environ['DB_HOST_DEV']
    __user = environ['DB_USER_DEV']
    __password = environ['DB_PASSWORD_DEV']
    uri = f"postgresql://{__user}:{__password}@{__host}/{__db}"

class TestingConfig():
    __db = environ['DB_NAME']
    __host = environ['DB_HOST_TEST']
    __user = environ['DB_USER_TEST']
    __password = environ['DB_PASSWORD_TEST']
    uri = f"postgresql://{__user}:{__password}@{__host}/{__db}"

class ProductionConfig():
    __db = environ['DB_NAME']
    __host = environ['DB_HOST_PROD']
    __user = environ['DB_USER_PROD']
    __password = environ['DB_PASSWORD_PROD']
    uri = f"postgresql://{__user}:{__password}@{__host}/{__db}"

active_config = {
    'development': DevelopmentConfig,
    'testing' : TestingConfig,
    'production': ProductionConfig
}

active = environ['DB_ENV']
CONFIG = active_config[active]