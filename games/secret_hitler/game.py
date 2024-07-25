from pathlib import Path

from games.interface import Game, GameInterface
from games.secret_hitler.assets.emoji import EMOJIS, SELECT_EMOJI


class SecretHitler(GameInterface):
    async def run(self):
        pass


secret_hitler = Game(
    url="https://www.secrethitler.com/",
    name="Secret Hitler",
    max_players=10,
    min_players=5,
    game_interface=SecretHitler,
    emojis=EMOJIS,
    logo=Path("games/secret_hitler/assets/logo.png"),
    select_emoji=SELECT_EMOJI,
)
