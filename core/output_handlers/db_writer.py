import pandas as pd
from sqlalchemy.engine import Engine
from core.output_handlers.base import BaseOutputWriter

class DatabaseWriter(BaseOutputWriter):
    """
    Writes data directly into a live SQL database (PostgreSQL, MySQL, SQLite, etc.).

    Parameters:
        db_url (str): SQLAlchemy-compatible database URI.
        if_exists (str): What to do if the table already exists.
                         Options: 'fail', 'replace', 'append'. Default is 'replace'.

    Methods:
        write(table_name: str, dataframe: pd.DataFrame):
            Uses pandas `.to_sql()` to insert data into the specified table.

    Example:
        writer = DatabaseWriter("postgresql://user:pass@localhost/db")
        writer.write("customers", df)

    Notes:
        - Make sure the database is running and accessible.
        - SQLAlchemy and pandas handle datatype inference.
        - Performance can be tuned with `chunksize`, `method='multi'`, etc.
    """

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
