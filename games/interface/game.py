import abc

from discord import Interaction, User, Member


class GameInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, players: set[User | Member], interaction: Interaction, *args, **kwargs):
        """Initialise the game interface"""
        raise NotImplemented

    @property
    @abc.abstractmethod
    def players(self) -> set[User | Member]:
        """Get the players of the game"""
        raise NotImplemented

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Get the name of the game"""
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    async def setup_game(cls, interaction: Interaction, players: set[User | Member]):
        """Sets up game and returns a game object"""
        raise NotImplemented

    @abc.abstractmethod
    async def run(self):
        """Starts the game loop"""
        raise NotImplemented
