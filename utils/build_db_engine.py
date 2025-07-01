from sqlalchemy import create_engine

def build_db_engine(creds: dict):
    if creds["type"] == "postgresql":
        url = f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
    elif creds["type"] == "mysql":
        url = f"mysql+pymysql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
    else:
        raise ValueError("Unsupported DB type")
    
    return create_engine(url)
