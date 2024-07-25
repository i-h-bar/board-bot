import json
from pathlib import Path

DEFAULT_EMOJIS = json.loads(Path("games/default_assets/emojis.json").read_text()).splitlines()