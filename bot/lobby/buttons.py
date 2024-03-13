import logging
from datetime import datetime

import discord.ui
from discord import Interaction

from bot.const.emoji import DEFAULT_EMOJI
from bot.lobby import Lobby


class JoinLobbyButton(discord.ui.Button):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby
        try:
            self.button_emoji = self.lobby.emojis[0]
        except IndexError:
            self.button_emoji = DEFAULT_EMOJI

        super().__init__(
            label=f"Play {self.lobby.name}!", emoji=self.button_emoji, style=discord.ButtonStyle.green
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user not in self.lobby.players:
            if len(self.lobby.players) >= self.lobby.game.MAX_PLAYERS:
                return await interaction.response.send_message(
                    "Sorry, the lobby is at it max players for this game. :(", ephemeral=True
                )
            else:
                self.lobby.add_to_lobby(interaction.user)
                await interaction.message.edit(embed=self.lobby)

        await interaction.response.defer()


class LeaveLobbyButton(discord.ui.Button):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby
        self.button_emoji = "💩"
        super().__init__(
            label=f"Leave Lobby", emoji=self.button_emoji
        )

    async def callback(self, interaction: Interaction):
        if interaction.user in self.lobby.players:
            if self.lobby.remove_from_lobby(interaction.user):
                await interaction.message.edit(embed=self.lobby)

            await interaction.response.defer()


class StartGameButton(discord.ui.Button):
    def __init__(self, lobby: Lobby, lobby_interaction: Interaction):
        self.lobby = lobby
        self.lobby_interation = lobby_interaction
        self.game = self.lobby.game
        super().__init__(
            label=f"Start Game!", emoji="👍"
        )

    async def callback(self, interaction: Interaction):
        await self.game.Game.setup_game(interaction, self.lobby.players)

        await interaction.response.send_message("Game started!")
        await self.lobby_interation.channel.send("Let the games begin!")

        await (await interaction.original_response()).delete()
        await (await self.lobby_interation.original_response()).delete()

        logging.info(
            f"[%s] - A game of %s has started in - %s: %s.",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.lobby.name,
            self.lobby_interation.guild,
            self.lobby_interation.channel
        )

        players = self.lobby.players
        del self.lobby

        await self.game.Game(players).run()
