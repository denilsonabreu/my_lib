
import pandas as pd
from pandas import DataFrame
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import schema, MetaData

from config_exp import CONFIG

"""
https://towardsdatascience.com/how-to-create-a-sql-practice-database-with-python-d320908e1faf
"""

class SQLData:
    def __init__(self) -> None:
        return None
    
    def connect(self) -> None:
        self.__engine = sqlalchemy.create_engine(CONFIG.uri, isolation_level="AUTOCOMMIT")
        self.__meta = MetaData(bind=self.__engine, schema='dbo')
        self.create_database()
    
    def create_database(self) -> None: 
        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)

        schema_name = 'dbo'
        if not self.__engine.dialect.has_schema(self.__engine, schema_name):
            self.__engine.execute(schema.CreateSchema(schema_name))
    
    def drop_all_tables(self) -> None:
        self.__meta.reflect()
        self.__meta.drop_all(checkfirst=True)
    
    def drop_database(self) -> None:
        drop_database(self.__engine.url)
    
    def create_table(self, dataframe: DataFrame , name: str) -> None:
        dataframe.to_sql(name, con=self.__engine, schema='dbo', if_exists='append')

    def get_all_tables(self) -> list:
        tables = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema='dbo'",
            self.__engine)
        return tables.table_name.tolist()
               
    def get_table(self, name: str) -> None:
        return pd.read_sql(f'SELECT * FROM dbo.{name}', self.__engine, parse_dates='Date', index_col='Date')

if __name__ == '__main__':
    sql = SQLData()
    sql.connect()
    tables = sql.get_all_tables()
    print(tables)