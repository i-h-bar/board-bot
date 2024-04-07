from __future__ import annotations
import asyncio
import logging
from datetime import datetime
from typing import TYPE_CHECKING

import discord.errors
import discord.ui
from discord import Interaction, SelectOption

from bot.const.emoji import DEFAULT_EMOJI
from bot.const.games import current_games
from games.interface.game import GameInterface

if TYPE_CHECKING:
    from bot.lobby import Lobby


class CancelGameButton(discord.ui.Button):
    def __init__(self, lobby: Lobby, lobby_interaction: Interaction):
        self.lobby = lobby
        self.lobby_interation = lobby_interaction
        self.game = self.lobby.game
        super().__init__(
            label=f"Cancel Game!", emoji="💩"
        )

    async def callback(self, interaction: Interaction):
        try:
            current_games.remove(self.lobby_interation.channel)
        except KeyError:
            pass

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

        await self.lobby_interation.channel.send(f"Game cancelled!")


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


class RemovePlayersDropdown(discord.ui.Select):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby

        options = [
            SelectOption(label=user.display_name, emoji=user.display_icon) for user in self.lobby.players.values()
        ]

        if not options:
            options = [
                SelectOption(label="Empty Lobby :(", emoji=DEFAULT_EMOJI)
            ]

        super().__init__(placeholder="Kick a player from lobby...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: Interaction):
        try:
            choice = self.values[0]
        except IndexError:
            return await interaction.response.send_message(
                "I didn't successfully get the option", ephemeral=True, delete_after=600.0
            )

        self.lobby.remove_from_lobby(choice)
        await interaction.response.edit_message(view=self.lobby.admin_controls)
