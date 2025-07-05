import pandas as pd
from sqlalchemy.engine import Engine
from core.output_handlers.base import BaseOutputWriter

class DatabaseWriter(BaseOutputWriter):
    def __init__(self, engine: Engine, if_exists: str = "replace"):
        """
        Parameters:
            engine (sqlalchemy.Engine): SQLAlchemy engine connected to the target DB
            if_exists (str): 'replace', 'append', or 'fail'
        """
        self.engine = engine
        self.if_exists = if_exists

    def write(self, table_name: str, dataframe: pd.DataFrame):
        try:
            dataframe.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=self.if_exists,
                index=False,
                method="multi"
            )
            print(f"✅ Inserted {len(dataframe)} rows into '{table_name}'")
        except Exception as e:
            print(f"❌ Error inserting into '{table_name}': {e}")
