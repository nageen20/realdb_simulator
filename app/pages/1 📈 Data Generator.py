import streamlit as st
import os
import sys

# This gets the realdb_simulator root, regardless of current file location
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.build_db_engine import build_db_engine
from core.output_handlers.factory import get_writer
from core.services.data_generation_runner import generate_project_data

st.set_page_config(page_title="Mapping Demo", page_icon="📈")


if "active_project" not in st.session_state:
    st.session_state.active_project = None

if "schema" not in st.session_state:
    st.session_state.schema = None

if "schema_path" not in st.session_state:
    st.session_state.schema_path = None

if "project_meta" not in st.session_state:
    st.session_state.project_meta = None


# --- 3. Load Schema YAML ---
if st.session_state.schema is not None:
    st.title(f"🛠️ {st.session_state.active_project}: Generate Data")
    schema=st.session_state.schema

    selected_project_gd = st.session_state.schema_path
    #project_meta_gd = st.session_state.project_meta 
    tab_label = f"🛠️ Generate: {schema.get('name', selected_project_gd)}"
    tab_key = f"tab_{selected_project_gd}"

    #st.session_state["active_project"] = selected_project_gd
    st.session_state["tab_label"] = tab_label
    st.session_state["schema"] = schema
    #st.session_state["project_meta"] = project_meta_gd

    if not schema:
        st.error("No project selected. Please choose a project from the Overview tab.")
        st.stop()

    st.markdown("### 1️⃣ Choose Output Database")
    db_type = st.selectbox("Select database type", ["PostgreSQL", "MySQL", "csv"], key="db_type")

    st.markdown("### 2️⃣ Set Rows per Table")
    tables = schema.get("tables", {})
    default_rows_config = {
        table: tables[table].get("rows", 10)
        for table in tables
    }

    row_inputs = {}
    col1, col2, col3 = st.columns(3) 
    for table, default_rows in default_rows_config.items():
        with col1:
            row_inputs[table] = st.number_input(
            f"Rows for table: `{table}`", min_value=1, max_value=10000,
            value=default_rows, step=1, key=f"rows_{table}"
        )

    st.session_state["row_inputs"] = row_inputs


    #if st.button("🎉 Generate Fake Data"):
        

    # Get user settings
    row_config = st.session_state["row_inputs"]
    #schema = st.session_state.schema
    db_flavor = st.session_state["db_type"]

    



    if db_type in ["PostgreSQL", "MySQL"]:
        sql_generation_type = st.radio(label='Choose how to generate data:',
                                           options=["Generate SQL Insert Scripts","Add to Database Directly"],
                                           index=None,
                                           horizontal=True)
            
            
        if sql_generation_type=="Add to Database Directly":
            output_mode = 'db'
            st.markdown("### 🔐 Enter Database Credentials")
            db_host = st.text_input("Host", value="localhost")
            db_port = st.text_input("Port", value="5432" if db_type == "PostgreSQL" else "3306")
            db_user = st.text_input("Username")
            db_password = st.text_input("Password", type="password")
            db_name = st.text_input("Database name")

            st.session_state.db_credentials = {
                    "type": db_type.lower(),
                    "host": db_host,
                    "port": db_port,
                    "user": db_user,
                    "password": db_password,
                    "database": db_name,
                }
            
            if st.button("🚀 Generate Data"):
                engine = build_db_engine(st.session_state.db_credentials)
                writer = get_writer(output_mode, db_engine=engine)

                 # Generate & write data
                st.write("⏳ Generating...")
                generate_project_data(schema, writer, st.session_state.data_path)
                st.success("✅ Data generation complete!")
        elif sql_generation_type == 'Generate SQL Insert Scripts':
            # Optional output path for csv or sql
            output_path = st.text_input("Output Path", "output")
            
            if st.button("🚀 Generate Data"):
                output_mode = 'sql'
                 # Get the writer
                writer = get_writer(output_mode, output_path=output_path)

                # Generate & write data
                st.write("⏳ Generating...")
                generate_project_data(schema, writer, st.session_state.data_path)
                st.success("✅ Data generation complete!")

    elif db_type == 'csv':
        # Optional output path for csv or sql
        output_path = st.text_input("Output Path", "output")

        if st.button("🚀 Generate Data"):
            output_mode = 'csv'
                # Get the writer
            writer = get_writer(output_mode, output_path=output_path)

            # Generate & write data
            st.write("⏳ Generating...")
            generate_project_data(schema, writer, st.session_state.data_path)
            st.success("✅ Data generation complete!")


    
else:
    st.title(f"🛠️ No project selected")