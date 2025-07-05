from abc import ABC, abstractmethod
import pandas as pd

class BaseOutputWriter(ABC):
    """
        Abstract base class for all output writers.

        Each output handler subclass must implement the `write(table_name, dataframe)` method.

        This class allows for standardized handling of output logic such as:
        - Writing to file formats (CSV, SQL script)
        - Writing to database tables (PostgreSQL, MySQL, etc.)
        - Adding support for additional targets like BigQuery, Parquet, etc.

        Methods:
            write(table_name: str, dataframe: pd.DataFrame):
            Abstract method to be implemented by all concrete subclasses.

        Usage:
            Subclass this to create a new output handler type.
        """
    @abstractmethod
    def write(self, table_name: str, dataframe: pd.DataFrame):
       
        pass
