import json
from pathlib import Path
from datetime import datetime

REGISTRY_PATH = Path("data/knowledge_bases.json")


def load_registry():
    if not REGISTRY_PATH.exists():
        return {"knowledge_bases": []}

    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8-sig") as f:
            content = f.read().strip()

            if not content:
                return {"knowledge_bases": []}

            return json.loads(content)

    except json.JSONDecodeError as e:
        print("⚠️ JSON decode error in knowledge_bases.json:", e)
        return {"knowledge_bases": []}


def save_registry(data):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)


def add_kb(collection_id: str, filename: str):
    data = load_registry()

    data["knowledge_bases"].append(
        {
            "collection_id": collection_id,
            "filename": filename,
            "created_at": datetime.utcnow().isoformat(),
        }
    )

    save_registry(data)


def delete_kb(collection_id: str):
    data = load_registry()

    data["knowledge_bases"] = [
        kb for kb in data["knowledge_bases"] if kb["collection_id"] != collection_id
    ]

    save_registry(data)
