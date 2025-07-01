import pandas as pd
import random
from utils.faker_utils import generate_fake_value
from utils.dependency_sorter import get_table_generation_order
import streamlit as st

class FakeDataGenerator:
    def __init__(self, schema: dict, row_config: dict):
        self.schema = schema
        self.row_config = row_config
        self.generated_data = {}
        self.pk_index = {}  # {table: [id1, id2, ...]}

    def generate(self):
        tables = self.schema["tables"]
        generation_order = get_table_generation_order(tables)

        for table_name in generation_order:
            table_schema = tables[table_name]
            n_rows = self.row_config.get(table_name, table_schema.get("rows", 10))
            df = self._generate_table(table_name, table_schema, n_rows)
            self.generated_data[table_name] = df

        return self.generated_data

    def _generate_table(self, table_name, table_schema, n_rows):
        cols = table_schema["columns"]
        data = {col: [] for col in cols}
        #st.write(cols)
        # Step 1: Generate PKs first
        pk_col = None
        for col, meta in cols.items():
            if meta.get("column_type") == "pk":
                pk_col = col
                break

        if pk_col:
            pk_values = list(range(1, n_rows + 1))
            data[pk_col] = pk_values
            self.pk_index[table_name] = pk_values
        else:
            pk_values = list(range(1, n_rows + 1))
            self.pk_index[table_name] = pk_values  # fallback

        # Step 2: Fill other columns
        for row_idx in range(n_rows):
            for col, meta in cols.items():
                if col == pk_col:
                    continue

                col_type = meta.get("column_type")
                base_type = meta["type"]
                #st.write(base_type)
                if col_type == "fk":
                    ref_table = meta["references"].split(".")[0]
                    ref_values = self.pk_index.get(ref_table, [1])
                    data[col].append(random.choice(ref_values))
                else:
                    data[col].append(generate_fake_value(base_type))

        return pd.DataFrame(data)
