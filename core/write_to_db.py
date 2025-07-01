from utils.build_db_engine import build_db_engine
import pandas as pd

def write_to_db(dataframes: dict, schema: dict, creds: dict, db_flavor="postgres"):
    engine = build_db_engine(creds)
    try:
        engine = build_db_engine(creds)
        with engine.connect() as conn:
            for table_name, df in dataframes.items():
                df.to_sql(table_name, conn, if_exists="replace", index=False)
        return 'success'
    except Exception as e:
        return e



