import asyncio
import logging
from datetime import datetime

import discord.ui
from discord import Interaction

from bot.const.emoji import DEFAULT_EMOJI
from bot.lobby import Lobby
from games.interface.game import GameInterface


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
        if len(self.lobby.players) >= self.game.MIN_PLAYERS:
            game: GameInterface = await self.game.Game.setup_game(interaction, self.lobby.players)

            try:
                await interaction.message.delete()
            except (discord.errors.NotFound, discord.errors.Forbidden, discord.errors.HTTPException) as error:
                logging.warning(
                    f"[%s] - Could not delete DM due to - %s",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    str(error)
                )

            try:
                await (await self.lobby_interation.original_response()).delete()
            except (discord.errors.NotFound, discord.errors.Forbidden, discord.errors.HTTPException) as error:
                logging.warning(
                    f"[%s] - Could not delete previous bot message due to - %s",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    str(error)
                )

            await self.lobby_interation.channel.send("Let the games begin!")

            logging.info(
                f"[%s] - A game of %s has started in - %s: %s.",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.lobby.name,
                self.lobby_interation.guild,
                self.lobby_interation.channel
            )

            await asyncio.gather(*(player.send(f"Have fun in your game of {game.name}!") for player in game.players))
            await game.run()

        else:
            await interaction.response.send_message(
                f"Not enough player to start {self.lobby.name}; "
                f"you need {self.lobby.game.MIN_PLAYERS}-{self.lobby.game.MAX_PLAYERS} to start."
            )


class CancelGameButton(discord.ui.Button):
    def __init__(self, lobby: Lobby, lobby_interaction: Interaction):
        self.lobby = lobby
        self.lobby_interation = lobby_interaction
        self.game = self.lobby.game
        super().__init__(
            label=f"Cancel Game!", emoji="💩"
        )

    async def callback(self, interaction: Interaction):
        pass
