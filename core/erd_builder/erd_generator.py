from graphviz import Digraph

def generate_erd_from_schema(schema_dict):
    dot = Digraph(comment=schema_dict.get('name', 'ERD'))
    dot.attr(rankdir='LR', fontsize='12', fontname='Helvetica')

    tables = schema_dict.get("tables", {})

    for table_name, table_data in tables.items():
        columns = table_data.get("columns", {})
        primary_keys = table_data.get("primary_key", [])
        label = f"<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0'>"
        label += f"<TR><TD COLSPAN='2'><B>{table_name}</B></TD></TR>"

        for col_name, col_conf in columns.items():
            col_type = col_conf.get('data_type', '')
            pk_marker = " (PK)" if col_name in primary_keys else ""
            label += f"<TR><TD ALIGN='LEFT'>{col_name}{pk_marker}</TD><TD ALIGN='LEFT'>{col_type}</TD></TR>"

        label += "</TABLE>>"
        dot.node(table_name, label=label, shape='plain')

    for table_name, table_data in tables.items():
        fks = table_data.get("foreign_keys", {})
        for col, ref in fks.items():
            ref_table, ref_col = ref.split(".")
            dot.edge(table_name, ref_table, label=f"{col} → {ref_col}", fontsize='10', fontname='Helvetica', color='blue')

    return dot
