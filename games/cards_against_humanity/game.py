import random
from pathlib import Path
from typing import Self

from discord import User, Member

from bot.const.custom_types import Interaction
from games.cards_against_humanity.cards import Deck
from games.default_assets.emojis import DEFAULT_EMOJIS
from games.interface import Game, GameInterface


class CAH(GameInterface):
    __slots__ = ("white", "black", "hands", "points", "round", "player_list")

    def __init__(self: Self, players: dict[str, User | Member], interaction: Interaction):
        super().__init__(players, interaction)
        self.white = Deck.white()
        self.black = Deck.black()
        self.round = 0
        self.player_list = list(self.players.values())
        random.shuffle(self.player_list)

        self.hands = {player: self.white.draw() for player in self.players.keys()}
        self.points = {player: 0 for player in self.players.keys()}

    @classmethod
    async def setup_game(cls: type[Self], interaction: Interaction, players: dict[str, User | Member]) -> Self:
        return cls(players, interaction)
    
    @property
    def card_czar(self) -> User | Member:
        return self.player_list[self.round & len(self.player_list)]

    async def run(self: Self) -> None:
        while any(point < 10 for point in self.points.values()):
            pass


cah = Game(
    url="https://www.cardsagainsthumanity.com/",
    name="Cards Against Humanity",
    max_players=12,
    min_players=4,
    game_interface=CAH,
    emojis=DEFAULT_EMOJIS,
    logo=Path("games/cards_against_humanity/assets/logo.png"),
    select_emoji="🙈",
)
