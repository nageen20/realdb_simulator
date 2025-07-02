import streamlit as st
import yaml
import os
from pathlib import Path
import sys

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from core.schemas_loader import load_all_schemas
from core.generate_erd import generate_erd

# Paths
SCHEMAS_DIR = Path("schemas")
CONTEXT_DIR = Path("business_context")

st.set_page_config(page_title="Home", page_icon="🏠",layout="wide")

if "active_project" not in st.session_state:
    st.session_state.active_project = None

if "schema" not in st.session_state:
    st.session_state.schema = None

if "schema_path" not in st.session_state:
    st.session_state.schema_path = None

if "project_meta" not in st.session_state:
    st.session_state.project_meta = None


st.title("📦 RealDB Playground")
st.markdown("Simulate real-world OLTP databases with rich schema and business context.")


# 1. Load all schemas
schema_map = load_all_schemas()
if not schema_map:
    st.error("No schema files found in /schemas.")
    st.stop()

# --- 2. Project Selector ---

selected_project = st.selectbox("📁 Select a schema project:", list(schema_map.keys()), width=500, placeholder='Select a project...',index=None)

if selected_project is not None:
    st.session_state.schema_path = schema_map[selected_project]
    st.session_state.active_project = selected_project
    schema_path = schema_map[selected_project].get('path')
    head, tail = os.path.split(schema_path)
    context_path = CONTEXT_DIR / head.replace("schemas\\","") / tail.replace(".yaml", ".md")
    st.session_state.schema_path = schema_path


    if st.button("Generate Data 🚀"):
        st.switch_page("pages/1 📈 Data Generator.py")

    # --- 3. Load Schema YAML ---
    with open(schema_path, "r") as f:
        schema = yaml.safe_load(f)

    st.subheader(f"🧠 Project: {schema.get('name', 'Unnamed')}")
    st.markdown(f"**Domain:** `{schema.get('tag')}` &nbsp;&nbsp;&nbsp;&nbsp; **Difficulty:** `{schema.get('difficulty')}`")




    # --- 4. Show Business Context (Markdown) ---
    with st.expander("📖 Business Context (Expand for full business context)", expanded=False):
        if context_path.exists():
            with open(context_path, "r", encoding="utf-8") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        else:
            st.warning("No business context found.")






    # --- 5. Generate ERD ---



    st.subheader("🧩 Entity Relationship Diagram (ERD)")
    st.graphviz_chart(generate_erd(schema), use_container_width=True)

