from core.output_handlers.base import BaseOutputWriter
import os

class CSVOutputWriter(BaseOutputWriter):
    def __init__(self, output_path):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)

    def write(self, table_name, dataframe):
        dataframe.to_csv(f"{self.output_path}/{table_name}.csv", index=False)
