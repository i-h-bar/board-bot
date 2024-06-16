from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import TYPE_CHECKING

import discord
from discord import SelectOption, User

from bot.const.custom_types import Interaction
from bot.const.emoji import DEFAULT_EMOJI
from bot.const.games import current_games

if TYPE_CHECKING:
    from bot.lobby import Lobby


EMPTY_LOBBY_TEXT = "Empty Lobby :("


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
        if len(self.lobby.players) >= self.game.min_players:
            game_interface = await self.game.game_interface.setup_game(interaction, self.lobby.players)
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

            await asyncio.gather(
                *(player.send(f"Have fun in your game of {self.game.name}!") for player in
                  game_interface.players.values())
            )
            await game_interface.run()

        else:
            await interaction.response.send_message(
                f"Not enough player to start {self.lobby.name}; "
                f"you need {self.lobby.game.min_players}-{self.lobby.game.max_players} to start."
            )


class RemovePlayersDropdown(discord.ui.Select):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby

        options = [
            SelectOption(label=user.display_name) for user in self.lobby.players.values() if user != self.lobby.admin
        ]

        if not options:
            options = [
                SelectOption(label=EMPTY_LOBBY_TEXT, emoji=DEFAULT_EMOJI)
            ]

        super().__init__(placeholder="Kick a player from lobby...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if len(self.lobby.players) < 1:
            await delete_message(interaction)
            await self.lobby.interaction.channel.send(f"Game cancelled!")
            return await self.lobby.delete()

        try:
            choice = self.values[0]
        except IndexError:
            return await interaction.response.send_message(
                "I didn't successfully get the option", delete_after=10
            )

        if choice == EMPTY_LOBBY_TEXT:
            await interaction.response.send_message(
                f"The empty lobby choice is not meant to be clicked you silly goose!", delete_after=10
            )
            await self.lobby.update()
        else:
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
            if len(self.lobby.players) >= self.lobby.game.max_players:
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
