import os
import numpy as np
from core.output_handlers.base import BaseOutputWriter
import pandas as pd

class SQLScriptWriter(BaseOutputWriter):
    """
    Generates `.sql` scripts containing INSERT statements for each table.

    Useful when learners want to inspect or run SQL manually in a client.

    Parameters:
        output_path (str or Path): Directory to save the `.sql` files.

    Methods:
        write(table_name: str, dataframe: pd.DataFrame):
            Generates and writes SQL INSERT statements to `table_name.sql`.

    Notes:
        - Strings are escaped to prevent syntax errors.
        - Dates and NULLs are formatted properly.
        - Multiline INSERTs are batched for better readability.

    Example:
        writer = SQLScriptWriter("scripts/")
        writer.write("products", df)
    """
    def __init__(self, output_path):
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def _format_value(self, value):
        if pd.isna(value) or value is None:
            return "NULL"
        elif isinstance(value, str):
            return f"'{value.replace("'", "''")}'"
        elif isinstance(value, (int, float, bool)):
            return str(value)
        elif isinstance(value, pd.Timestamp):
            return f"'{value.isoformat()}'"
        else:
            return f"'{str(value)}'"  # fallback

    def write(self, table_name, dataframe):
        sql_lines = [f"INSERT INTO {table_name} ({', '.join(dataframe.columns)}) VALUES\n"]
        
        for _, row in dataframe.iterrows():
            values = [self._format_value(v) for v in row]
            sql_lines.append(f"({', '.join(values)}),\n")

        if sql_lines:
            # Replace the last comma with a semicolon
            sql_lines[-1] = sql_lines[-1].rstrip(',\n') + ';\n'

            with open(f"{self.output_path}/{table_name}.sql", 'w', encoding='utf-8') as f:
                f.writelines(sql_lines)
