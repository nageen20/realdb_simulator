from pathlib import Path
import yaml

SCHEMA_DIR = Path("schemas")

def load_all_schemas():
    schema_map = {}  # {display_name: {"path": ..., "data": ...}}

    for file_path in SCHEMA_DIR.rglob("*.yaml"):
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        name = data.get("name", file_path.stem)
        tag = data.get("tag", file_path.parent.name)
        difficulty = data.get("difficulty", "")
        
        emoji = {
            "supply_chain": "🧺",
            "ecommerce": "🛒",
            "retail": "🏬",
        }.get(tag.lower(), "📦")

        display_name = f"{emoji} {name} ({tag.replace('_', ' ').title()})"

        schema_map[display_name] = {
            "path": file_path,
            "data": data
        }

    return schema_map


