from core.generators.table_generator import TableDataGenerator
import pandas as pd
import os


def generate_project_data(project_schema, writer, global_data_dir, fk_lookup=None):
    fk_lookup = fk_lookup or {}
    all_dataframes = {}

    for table_name, table_config in project_schema['tables'].items():
        generator = TableDataGenerator(table_name, table_config, global_data_dir, fk_lookup)
        rows = generator.generate_and_update_fk_lookup()
        df = pd.DataFrame(rows)

        # Update FK cache
        fk_lookup[table_name] = {
            col: df[col].tolist() for col in df.columns if col in table_config['columns']
        }
        all_dataframes[table_name] = df

        writer.write(table_name, df)

    return all_dataframes
