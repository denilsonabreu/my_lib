#!/usr/bin python3

from dotenv import load_dotenv
from os import getenv
from sqlalchemy.engine.url import make_url

load_dotenv()

class PostrgresConfig:
    __db = getenv('DB_NAME')
    __host = getenv('DB_HOST_POSTGRES')
    __user = getenv('DB_USER_POSTGRES')
    __password = getenv('DB_PASSWORD_POSTGRES')
    url = make_url(f"postgresql+psycopg2://{__user}:{__password}@{__host}/{__db}")

class MySqlConfig:
    __db = getenv('DB_NAME')
    __host = getenv('DB_HOST_MYSQL')
    __user = getenv('DB_USER_MYSQL')
    __password = getenv('DB_PASSWORD_MYSQL')
    url = make_url(f"mysql+pymysql://{__user}:{__password}@{__host}/{__db}")

active_config = {
    'postgres': PostrgresConfig(),
    'mysql' : MySqlConfig()
}

# set enviroment variable
active = getenv('DB_ENV')

cfg = active_config[active]