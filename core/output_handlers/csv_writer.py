from core.output_handlers.base import BaseOutputWriter
import os

class CSVOutputWriter(BaseOutputWriter):
    """
    Handles writing synthetic data to CSV files, one file per table.

    Parameters:
        output_path (str or Path): Directory path where CSV files will be saved.

    Methods:
        write(table_name: str, dataframe: pd.DataFrame):
            Writes the given DataFrame to `output_path/table_name.csv`.

    Example:
        writer = CSVWriter("output/")
        writer.write("orders", orders_df)
    """
    def __init__(self, output_path):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)

    def write(self, table_name, dataframe):
        dataframe.to_csv(f"{self.output_path}/{table_name}.csv", index=False)
