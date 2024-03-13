from types import ModuleType

from games import secret_hitler

GAMES: dict[str, ModuleType] = {
    "Secret Hitler": secret_hitler
}
