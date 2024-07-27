import random

import discord

from bot.const.custom_types import Interaction
from games.cards_against_humanity.cards import WhiteCard
from games.default_assets.emojis import DEFAULT_EMOJIS


class Pick(discord.ui.Select):
    def __init__(self, num_of_choices: int, hand: list[WhiteCard], picks: list[str]):
        options = [
            discord.SelectOption(label=card.text, emoji=random.choice(DEFAULT_EMOJIS)) for card in hand
        ]
        self.hand = hand
        self.picks = picks
        super().__init__(
            placeholder=f"Select {num_of_choices} cards...",
            max_values=num_of_choices,
            min_values=num_of_choices,
            options=options
        )

    async def callback(self, interaction: Interaction):
        for pick in self.values:
            self.picks.append(pick)
            self.hand.remove(WhiteCard(pick))

        await interaction.response.defer()
