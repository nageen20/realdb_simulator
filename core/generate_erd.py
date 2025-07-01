from graphviz import Digraph


def generate_erd(schema: dict) -> str:
    """
    Generates a Graphviz DOT representation of the schema with proper FK edges.
    """
    dot = ["digraph ERD {", "  rankdir=LR;", "  node [shape=record];"]

    tables = schema["tables"]

    for table_name, table in tables.items():
        #st.write(table_name,table)
        col_defs = []
        for col_name, col_meta in table["columns"].items():
            col_type = col_meta.get("type", "unknown")
            annotation = ""
            if col_meta.get("column_type") == "pk":
                annotation = " (PK)"
            elif col_meta.get("column_type") == "fk":
                annotation = " (FK)"
            col_defs.append(f"{col_name}: {col_type}{annotation}")
        
        label = r"\l".join(col_defs) + r"\l"
        dot.append(f'  {table_name} [label="{{{table_name}|{label}}}"];')

    # Foreign key edges
    for table_name, table in tables.items():
        for col_name, col_meta in table["columns"].items():
            if col_meta.get("column_type") == "fk":
                ref = col_meta.get("references")
                if ref:
                    ref_table = ref.split(".")[0]
                    dot.append(f"  {table_name} -> {ref_table};")

    dot.append("}")
    return "\n".join(dot)