from abc import ABC, abstractmethod
import pandas as pd

class BaseOutputWriter(ABC):
    @abstractmethod
    def write(self, table_name: str, dataframe: pd.DataFrame):
        """
        Write the given table's DataFrame to the desired output destination.
        
        Parameters:
            table_name (str): The name of the table being written.
            dataframe (pd.DataFrame): The table data.
        """
        pass
