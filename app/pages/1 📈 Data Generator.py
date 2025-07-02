import streamlit as st
import os
import sys

# This gets the realdb_simulator root, regardless of current file location
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from core.data_generator import FakeDataGenerator
from core.writer_csv import write_csvs
from core.writer_sql import write_sql_script
from core.write_to_db import write_to_db
from utils.projects_loader import load_schema

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

    



    generator = FakeDataGenerator(schema, row_config)
    dataframes = generator.generate()

    # Save outputs
    if db_type=='csv':
        if st.button("Generate data"):
            st.info("Generating data...")
            write_csvs(dataframes)
            st.success("✅ Data generated!")
    else:
        if db_type in ["PostgreSQL", "MySQL"]:
            
            
            sql_generation_type = st.radio(label='Choose how to generate data:',
                                           options=["Generate SQL Insert Scripts","Add to Database Directly"],
                                           index=None,
                                           horizontal=True)
            
            
            if sql_generation_type=="Add to Database Directly":

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
                if st.button("Populate Data"):
                    st.info("Generating data...")
                    insert_status = write_to_db(dataframes, schema, st.session_state.db_credentials, db_flavor=db_flavor)
                    if insert_status=='success':
                        st.success("✅ Data successfully inserted into the database!")
                    else:
                        st.error(f"❌ Database error: {insert_status}")
            
            if sql_generation_type=="Generate SQL Insert Scripts":
                st.info("Generating data...")
                write_sql_script(dataframes, schema, db_flavor=db_flavor)

                st.success("✅ Data generated!")
    #st.rerun()
    
else:
    st.title(f"🛠️ No project selected")