from discord import Interaction, User, Member

from games.interface.game import GameInterface


class Game(GameInterface):
    def __init__(self, players: set[User | Member], interaction: Interaction):
        self._players = players
        self._name = "Secret Hitler"
        self.interaction = interaction

    @property
    def players(self) -> set[User | Member]:
        return self._players

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    async def setup_game(cls, interaction: Interaction, players: set[User | Member]):
        return cls(players, interaction)

    async def run(self):
        pass
