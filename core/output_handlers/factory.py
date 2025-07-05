from core.output_handlers.csv_writer import CSVOutputWriter
from core.output_handlers.sql_script_writer import SQLScriptWriter
from core.output_handlers.db_writer import DatabaseWriter

def get_writer(output_mode, output_path=None, db_engine=None):
    """
    Factory method to return the appropriate writer class based on output_mode.

    Parameters:
        output_mode (str): One of 'csv', 'sql', 'db'
        output_path (str): Path to save files (for csv/sql)
        db_engine (sqlalchemy.Engine): Database engine (for db)

    Returns:
        BaseOutputWriter: An instance of the appropriate writer class
    """
    output_mode = output_mode.lower()

    if output_mode == 'csv':
        return CSVOutputWriter(output_path)
    elif output_mode == 'sql':
        return SQLScriptWriter(output_path)
    elif output_mode == 'db':
        return DatabaseWriter(db_engine)
    else:
        raise ValueError(f"Unsupported output mode: {output_mode}")
