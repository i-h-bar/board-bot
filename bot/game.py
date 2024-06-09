from dataclasses import dataclass
from pathlib import Path
from typing import Type

from games.interface.game import GameInterface


@dataclass(slots=True, frozen=True)
class Game:
    url: str
    max_players: int
    min_players: int
    emojis: tuple[str, ...]
    select_emoji: str
    logo: Path
    game_interface: Type[GameInterface]
