
import pandas as pd
from pandas import DataFrame
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import schema, MetaData, create_engine

class SQLData:
    """_summary_
    """    
    def __init__(self, url, schema:str=None) -> None:
        """_summary_

        Args:
            url (_type_): _description_
            schema (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """        
        self.url = url
        if schema:
            self.schema = schema
        else:
            self.schema='db'
        self.engine = create_engine(self.url, isolation_level="AUTOCOMMIT")
        self.meta = MetaData(bind=self.engine, schema=self.schema)
        self.create_database()
        return None     
    
    def create_database(self) -> None:
        """_summary_
        """        
        if not database_exists(self.url):
            create_database(self.url)

        if not self.engine.dialect.has_schema(self.engine, self.schema):
            self.engine.execute(schema.CreateSchema(self.schema))
    
    def drop_all_tables(self) -> None:
        """_summary_
        """        
        self.meta.reflect()
        self.meta.drop_all(checkfirst=True)
    
    def drop_database(self) -> None:
        """_summary_
        """        
        drop_database(self.url)
    
    def create_table(self, dataframe: DataFrame , name: str) -> None:
        """_summary_

        Args:
            dataframe (DataFrame): _description_
            name (str): _description_
        """
        dataframe.to_sql(name, con=self.engine, schema=self.schema, index=False, if_exists='append')
    
    def drop_table(self, name:str) -> None:

        self.engine.execute(f"DROP TABLE {self.schema}.{name};")

    def get_all_tables(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """        
        tables = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema='db'",
            self.engine)
        return tables.table_name.tolist()
               
    def get_table(self, name: str) -> None:
        """_summary_

        Args:
            name (str): _description_

        Returns:
            _type_: _description_
        """        
        return pd.read_sql(f'SELECT * FROM db.{name}', self.engine)
