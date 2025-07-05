import streamlit as st
import yaml
import os
from pathlib import Path
import sys

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from core.schemas_loader import load_all_schemas
from core.generate_erd import generate_erd
from core.erd_builder.erd_generator import generate_erd_from_schema
from core.erd_builder.pretty_erd_generator import generate_pretty_erd
from utils.projects_loader import load_project_index
from utils.projects_loader import load_context
from utils.projects_loader import load_schema
from utils.projects_loader import load_data_dir

import logging

logging.basicConfig(
    level=logging.DEBUG,  # or INFO in production
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# Paths
SCHEMAS_DIR = Path("schemas")
CONTEXT_DIR = Path("business_context")
DATA_DIR = Path("data")

st.set_page_config(page_title="Home", page_icon="🏠",layout="wide")

if "active_project" not in st.session_state:
    st.session_state.active_project = None

if "schema" not in st.session_state:
    st.session_state.schema = None

if "schema_path" not in st.session_state:
    st.session_state.schema_path = None

if "data_path" not in st.session_state:
    st.session_state.data_path = None



st.title("📦 RealDB Playground")
st.markdown("Simulate real-world OLTP databases with rich schema and business context.")


# 1. Load all projects

project_index = load_project_index()
project_display_names = [
    f"{proj['emoji']} {proj['name']} ({proj['difficulty'].capitalize()})"
    for proj in project_index
]

#schema_map = load_all_schemas()
if not project_display_names:
    st.error("No schema files found in /schemas.")
    st.stop()


# --- 2. Project Selector ---

selected_project_display = st.selectbox("📁 Select a schema project:", 
                                        project_display_names, 
                                        width=500, 
                                        placeholder='Select a project...',
                                        index=None)

st.session_state.active_project = selected_project_display
if selected_project_display is not None:
    selected_project = next(
    proj for proj, display in zip(project_index, project_display_names)
    if display == selected_project_display  
    )


    st.session_state.schema_path = selected_project
    

    if st.button("Generate Data 🚀"):
        st.switch_page("pages/1 📈 Data Generator.py")



    st.markdown(f"### {selected_project['emoji']} {selected_project['name']}")
    st.markdown(f"**Difficulty:** {selected_project['difficulty'].capitalize()}")

    
    # --- 4. Show Business Context (Markdown) ---
    with st.expander("📖 Business Context (Expand for full business context)", expanded=False):
        context=load_context(selected_project)
        if context:
            st.markdown(context)
        else:
            st.warning("No business context found.")



    # --- 5. Generate ERD ---

    schema=load_schema(selected_project)
    st.session_state.schema = schema
    st.subheader("🧩 Entity Relationship Diagram (ERD)")
    st.graphviz_chart(generate_pretty_erd(schema), use_container_width=True)

    # --- 6. Load data dir ---
    st.session_state.data_path = load_data_dir(selected_project)

