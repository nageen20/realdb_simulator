import json
from pathlib import Path
import yaml

PROJECT_INDEX_PATH = Path("schemas/project_index.json")

def load_project_index():
    with open(PROJECT_INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_project_by_name(name):
    index = load_project_index()
    return next((proj for proj in index if proj["name"] == name), None)

def load_schema(project):
    schema_path = Path("schemas") / project["path"]
    with open(schema_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_context(project):
    context_path = Path("business_context") / Path(project["context"])
    context_path = context_path.as_posix()
    with open(context_path, "r", encoding="utf-8") as f:
        return f.read()
