import json
from pathlib import Path


METADATA_DIR = Path(__file__).resolve().parent

def load_json(file_name: str):
    file_path = METADATA_DIR / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_all_metadata():
    return{
        "tables": load_json("tables.json"),
        "columns": load_json("columns.json"),
        "business_rules": load_json("business_rules.json"),
        "relationships": load_json("relationships.json"),
        "fiscal_calendar": load_json("fiscal_calendar.json")

    }



