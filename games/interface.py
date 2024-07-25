import abc
from dataclasses import dataclass
from pathlib import Path

from discord import Interaction, User, Member


class GameInterface(abc.ABC):
    __slots__ = ("_players", "interaction")

    def __init__(self, players: dict[str, User | Member], interaction: Interaction):
        """Initialise the game interface"""
        self._players: dict[str, User | Member] = players
        self.interaction = interaction

    @property
    def players(self) -> dict[str, User | Member]:
        """Get the players of the game"""
        return self._players

    @classmethod
    async def setup_game(cls, interaction: Interaction, players: dict[str, User | Member]):
        """Sets up game and returns a game object"""
        raise NotImplemented

    @abc.abstractmethod
    async def run(self):
        """Starts the game loop"""
        raise NotImplemented


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
