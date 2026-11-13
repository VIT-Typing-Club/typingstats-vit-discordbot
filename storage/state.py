import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"


def load_state():
    if not STATE_FILE.exists():
        return {"last_quote_id": None, "last_leaderboard_id": None}

    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(state):
    temp_file = STATE_FILE.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)

    temp_file.replace(STATE_FILE)
