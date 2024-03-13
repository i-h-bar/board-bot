import abc
from discord import Interaction, User, Member


class GameInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, players: set[User | Member], *args, **kwargs):
        """Initialise the game interface"""
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
