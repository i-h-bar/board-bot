from pathlib import Path

from discord import Interaction, User, Member

from games.interface import Game, GameInterface
from games.secret_hitler.assets.emoji import EMOJIS, SELECT_EMOJI


class SecretHitler(GameInterface):
    __slots__ = ("_players", "_name", "interaction")

    def __init__(self, players: dict[str, User | Member], interaction: Interaction):
        self._players = players
        self._name = "Secret Hitler"
        self.interaction = interaction

    @property
    def players(self) -> dict[str, User | Member]:
        return self._players

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    async def setup_game(cls, interaction: Interaction, players: dict[str, User | Member]):
        return cls(players, interaction)

    async def run(self):
        pass


secret_hitler = Game(
    url="https://www.secrethitler.com/",
    max_players=10,
    min_players=5,
    game_interface=SecretHitler,
    emojis=EMOJIS,
    logo=Path("games/secret_hitler/assets/logo.png"),
    select_emoji=SELECT_EMOJI,
)
