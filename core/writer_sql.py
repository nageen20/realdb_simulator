import os

def write_sql_script(dataframes: dict, schema: dict, db_flavor="postgres", output_dir="output/sql"):
    os.makedirs(output_dir, exist_ok=True)
    tables = schema["tables"]
    sql_lines = []

    for table, df in dataframes.items():
        cols = tables[table]["columns"]
        col_names = list(cols.keys())

        # Basic CREATE TABLE placeholder
        sql_lines.append(f"-- Table: {table}")
        col_defs = ", ".join([f"{col} TEXT" for col in col_names])  # Simplified
        sql_lines.append(f"CREATE TABLE {table} ({col_defs});")

        # INSERT statements
        for _, row in df.iterrows():
            values = ", ".join([f"'{str(v)}'" for v in row.tolist()])
            sql_lines.append(f"INSERT INTO {table} ({', '.join(col_names)}) VALUES ({values});")

        sql_lines.append("\n")

    with open(f"{output_dir}/schema_insert_{db_flavor}.sql", "w") as f:
        f.write("\n".join(sql_lines))
