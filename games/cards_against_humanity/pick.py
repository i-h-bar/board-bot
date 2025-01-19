import random

import discord

from bot.const.custom_types import Interaction
from games.cards_against_humanity.cards import WhiteCard
from games.default_assets.emojis import DEFAULT_EMOJIS


class PlayerPick(discord.ui.Select):
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


class CzarPick(discord.ui.Select):
    def __init__(self, picks: dict[str, list[str]]):
        options = [
            discord.SelectOption(label=" & ".join(answers), emoji=random.choice(DEFAULT_EMOJIS)) for answers in picks.values()
        ]
        self.picks = {" & ".join(v): k for k, v in picks.items()}
        self.is_picking = True
        self.winner = None
        super().__init__(
            placeholder="Select the best answer",
            max_values=1,
            min_values=1,
            options=options
        )

    async def callback(self, interaction: Interaction):
        self.winner = self.picks[" & ".join(self.values)]
        await interaction.response.send_message(f"{self.winner} has won this round!")
        self.is_picking = False

