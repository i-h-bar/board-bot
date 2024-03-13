from discord import Interaction, User, Member

from games.interface.game import GameInterface


class Game(GameInterface):
    def __init__(self, players: set[User | Member]):
        self.players = players

    @classmethod
    async def setup_game(cls, interaction: Interaction, players: set[User | Member]):
        return cls(players)

    async def run(self):
        pass
