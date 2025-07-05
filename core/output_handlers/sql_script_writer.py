import os
import numpy as np
from core.output_handlers.base import BaseOutputWriter
import pandas as pd

class SQLScriptWriter(BaseOutputWriter):
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
