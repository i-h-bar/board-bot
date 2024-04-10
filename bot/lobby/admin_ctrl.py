from __future__ import annotations
import asyncio
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

import discord.errors
import discord.ui
from discord import SelectOption, User
from discord._types import ClientT

from bot.const.custom_types import Interaction
from bot.const.emoji import DEFAULT_EMOJI
from bot.const.games import current_games
from games.interface.game import GameInterface

if TYPE_CHECKING:
    from bot.lobby import Lobby


class CancelGameButton(discord.ui.Button):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby
        self.game = self.lobby.game
        super().__init__(
            label=f"Cancel Game!", emoji="💩"
        )

    async def callback(self, interaction: Interaction):
        try:
            current_games.remove(self.lobby.interaction.channel)
        except KeyError:
            pass

        await delete_message(interaction)
        await self.lobby.interaction.channel.send(f"Game cancelled!")
        await self.lobby.delete()


class StartGameButton(discord.ui.Button):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby
        self.game = self.lobby.game
        super().__init__(
            label=f"Start Game!", emoji="👍"
        )

    async def callback(self, interaction: Interaction):
        if len(self.lobby.players) >= self.game.MIN_PLAYERS:
            game: GameInterface = await self.game.Game.setup_game(interaction, self.lobby.players)
            name = self.lobby.name
            guild = self.lobby.interaction.guild
            channel = self.lobby.interaction.channel

            await delete_message(interaction)
            await self.lobby.interaction.channel.send("Let the games begin!")
            await self.lobby.delete()

            logging.info(
                f"[%s] - A game of %s has started in - %s: %s.",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                name,
                guild,
                channel
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
        # Add a kicked persons list that gets checked on person attempting to rejoin with an except / decline / ban
        # if len(self.lobby.players) <= 1:
        #     await delete_message(interaction)
        #     await self.lobby.delete()
        #     return await self.lobby.interaction.channel.send(f"Game cancelled!")

        try:
            choice = self.values[0]
        except IndexError:
            return await interaction.response.send_message(
                "I didn't successfully get the option", ephemeral=True, delete_after=600
            )

        self.lobby.kicked_players[choice] = self.lobby.players[choice]
        self.lobby.remove_from_lobby(choice)
        await self.lobby.update()

        await self.lobby.kicked_players[choice].send("You have been kicked from the lobby!")
        await interaction.response.send_message(f"Removed {choice} from lobby.", delete_after=10)


class AdmitKickedPlayerButton(discord.ui.Button):
    def __init__(self, lobby: Lobby, user: User):
        self.user = user
        self.lobby = lobby
        super().__init__(
            label=f"Admit to the Lobby", emoji="👍"
        )

    async def callback(self, interaction: Interaction):
        if self.user.display_name not in self.lobby.players:
            if len(self.lobby.players) >= self.lobby.game.MAX_PLAYERS:
                return await interaction.response.send_message(
                    "Sorry, the lobby is at it max players for this game. :(", delete_after=10
                )
            else:
                self.lobby.add_to_lobby(self.user)
                await self.lobby.update()

                await self.user.send("You have been allowed back into the lobby! 🙃")
                await interaction.response.send_message(
                    f"{self.user.display_name} allowed back into the lobby", delete_after=10
                )


class BanPlayerButton(discord.ui.Button):
    def __init__(self, lobby: Lobby, user: User):
        self.user = user
        self.lobby = lobby
        super().__init__(label=f"Ban Player", emoji="💩", style=discord.ButtonStyle.red)

    async def callback(self, interaction: Interaction):
        self.lobby.banned_players[self.user.display_name] = self.user
        await self.user.send("You have been banned from the lobby! 🫢")
        await interaction.response.send_message(
            f"{self.user.display_name} has been banned from the lobby", delete_after=10
        )


async def delete_message(interaction: Interaction):
    try:
        await interaction.message.delete()
    except (discord.errors.NotFound, discord.errors.Forbidden, discord.errors.HTTPException) as error:
        logging.warning(
            f"[%s] - Could not delete message due to - %s",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(error)
        )