import abc
from dataclasses import dataclass
from pathlib import Path

from discord import Interaction, User, Member


class GameInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, players: dict[str, User | Member], interaction: Interaction, *args, **kwargs):
        """Initialise the game interface"""
        self._players: dict[str, User | Member] = players
        self.interaction = interaction

    @property
    @abc.abstractmethod
    def players(self) -> dict[str, User | Member]:
        """Get the players of the game"""
        raise NotImplemented

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Get the name of the game"""
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    async def setup_game(cls, interaction: Interaction, players: dict[User | Member]):
        """Sets up game and returns a game object"""
        raise NotImplemented

    @abc.abstractmethod
    async def run(self):
        """Starts the game loop"""
        raise NotImplemented


@dataclass(slots=True, frozen=True)
class Game:
    url: str
    max_players: int
    min_players: int
    emojis: tuple[str, ...]
    select_emoji: str
    logo: Path
    game_interface: type[GameInterface]
