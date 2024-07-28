import asyncio
import random
from pathlib import Path
from typing import Self

from discord import User, Member, HTTPException
from discord.ui import View

from bot.const.custom_types import Interaction
from games.cards_against_humanity.cards import Deck, BlackCard
from games.cards_against_humanity.pick import Pick
from games.default_assets.emojis import DEFAULT_EMOJIS
from games.interface import Game, GameInterface


class CAH(GameInterface):
    __slots__ = ("white", "black", "hands", "points", "round", "player_list", "picks", "current_black_card")

    def __init__(self: Self, players: dict[str, Interaction], interaction: Interaction):
        super().__init__(players, interaction)
        self.white = Deck.white()
        self.black = Deck.black()
        self.round = 0
        self.player_list = list(self.players.values())
        random.shuffle(self.player_list)

        self.hands = {player: [self.white.draw() for _ in range(10)] for player in self.players.keys()}
        self.points = {player: 0 for player in self.players.keys()}
        self.picks = {}
        self.current_black_card: BlackCard = None

    @classmethod
    async def setup_game(cls: type[Self], interaction: Interaction, players: dict[str, User | Member]) -> Self:
        return cls(players, interaction)

    @property
    def card_czar(self: Self) -> Interaction:
        return self.player_list[self.round % len(self.player_list)]

    async def run(self: Self) -> None:
        self.round += 1

        while any(point < 10 for point in self.points.values()):
            self.current_black_card = self.black.draw()

            black_card_text = self.current_black_card.text.format(
                *("\u001b[4;32m     \u001b[0m\u001b[1;32m" for _ in range(self.current_black_card.slots))
            )
            black_card_message = await self.card_czar.followup.send(
                f"Round {self.round} - Card Czar is **__{self.card_czar.user.display_name}__**\n"
                f"```ansi\n"
                f"\u001b[1;32m"
                f"{black_card_text}"
                f"\u001b[0m```"
            )
            await self.white_card_phase()
            await self.card_czar_pick()

            self.refresh_hands()
            await black_card_message.delete()
            self.black.discard(self.current_black_card)
            self.round += 1

    def refresh_hands(self):
        for hand in self.hands.values():
            for _ in range(10 - len(hand)):
                hand.append(self.white.draw())

    async def card_czar_pick(self):
        for answer in self.picks.values():
            await self.card_czar.followup.send(answer)

    async def white_card_phase(self):
        self.picks = {interaction.user.display_name: [] for interaction in self.players.values()}
        for player, interaction in self.players.items():
            pick = Pick(self.current_black_card.slots, self.hands[player], self.picks[player])
            view = View()
            view.add_item(pick)
            try:
                await interaction.followup.send(f"Pick {self.current_black_card.slots} cards...", view=view,
                                                ephemeral=True)
            except HTTPException:
                for choice in pick.options:
                    print("Potential Invalid Emoji: ")
                    print(choice.emoji)

                raise

        picking_message = await self.card_czar.followup.send("Calculating who is still picking...")
        while still_picking := [player for player, pick in self.picks.items() if
                                len(pick) != self.current_black_card.slots]:
            await picking_message.edit(content=f"Still picking...\n{"\n".join(still_picking)}")
            await asyncio.sleep(1)

        await picking_message.delete()


cah = Game(
    url="https://www.cardsagainsthumanity.com/",
    name="Cards Against Humanity",
    max_players=12,
    min_players=1,
    game_interface=CAH,
    emojis=DEFAULT_EMOJIS,
    logo=Path("games/cards_against_humanity/assets/logo.png"),
    select_emoji="🙈",
)
