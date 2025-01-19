import abc
from dataclasses import dataclass
from pathlib import Path

from discord import Interaction


class GameInterface(abc.ABC):
    __slots__ = ("_players", "interaction")

    def __init__(self, players: dict[str, Interaction], interaction: Interaction):
        """Initialise the game interface"""
        self._players: dict[str, Interaction] = players
        self.interaction = interaction

    @property
    def players(self) -> dict[str, Interaction]:
        """Get the players of the game"""
        return self._players

    @classmethod
    async def setup_game(cls, interaction: Interaction, players: dict[str, Interaction]):
        """Sets up game and returns a game object"""
        raise NotImplementedError

    @abc.abstractmethod
    async def run(self):
        """Starts the game loop"""
        raise NotImplementedError


@dataclass(slots=True, frozen=True)
class Game:
    url: str
    name: str
    max_players: int
    min_players: int
    emojis: tuple[str, ...]
    select_emoji: str
    logo: Path
    game_interface: type[GameInterface]
