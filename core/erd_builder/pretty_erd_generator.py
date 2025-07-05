import streamlit as st
from graphviz import Digraph

def generate_pretty_erd(schema_dict):
    graph = Digraph("ERD", format="png")
    graph.attr(rankdir="LR", nodesep="1", ranksep="1", fontsize="10")

    # Define styles
    node_style = {
        'shape': 'plaintext',
        'fontname': 'Helvetica',
    }
    
    # Step 1: Create table nodes
    for table_name, table in schema_dict["tables"].items():
        columns = table.get("columns", {})
        primary_keys = table.get("primary_key", [])
        foreign_keys = table.get("foreign_keys", {})

        rows = []
        rows.append(f'<tr><td bgcolor="black" align="center" colspan="2"><font color="white"><b>{table_name}</b></font></td></tr>')
        
        for col_name, col_def in columns.items():
            col_type = col_def.get("data_type", "")
            style = ""
            if col_name in primary_keys:
                style = f'<b>{col_name}</b>'
            elif col_name in foreign_keys:
                style = f'<i>{col_name}</i>'
            else:
                style = col_name
            rows.append(f'<tr><td align="left">{style}</td><td align="left">{col_type}</td></tr>')

        table_html = f'''<
            <table border="0" cellborder="1" cellspacing="0">
                {''.join(rows)}
            </table>
        >'''

        graph.node(table_name, label=table_html, **node_style)

    # Step 2: Draw foreign key edges
    for table_name, table in schema_dict["tables"].items():
        foreign_keys = table.get("foreign_keys", {})
        for col, ref in foreign_keys.items():
            ref_table, _ = ref.split('.')
            graph.edge(table_name, ref_table, label=col, color="gray", fontsize="10", arrowsize="0.7")

    return graph
