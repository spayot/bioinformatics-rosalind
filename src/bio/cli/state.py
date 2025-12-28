import json
from pathlib import Path

STATE_FILE = Path(".bio_state.json")


def set_current(name: str):
    with open(STATE_FILE, "w") as f:
        json.dump({"current": name}, f)


def get_current() -> str | None:
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("current")
    return None
