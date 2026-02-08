import json
from pathlib import Path

def write_to_file(file_path: str, content: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def add_to_file(file_path: str, content: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(content)

def load_json(file_path: str) -> dict:
    path = Path(file_path)
    path.read_text(encoding="utf-8")
    return json.loads(path.read_text(encoding="utf-8"))