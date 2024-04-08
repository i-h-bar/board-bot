import discord.ui
from discord.ui import View

from bot.const.custom_types import Interaction
from bot.const.emoji import DEFAULT_EMOJI
from bot.lobby import Lobby
from bot.lobby.admin_ctrl import AdmitKickedPlayerButton, BanPlayerButton


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

    async def callback(self, interaction: Interaction):
        not_in_lobby = interaction.user not in self.lobby.players.values()

        if not_in_lobby and interaction.user.display_name in self.lobby.banned_players:
            return await interaction.response.send_message(
                "You are banned from this lobby.", ephemeral=True, delete_after=60
            )
        elif not_in_lobby and interaction.user.display_name in self.lobby.kicked_players:
            admit_button = AdmitKickedPlayerButton(self.lobby, interaction.user)
            ban_player = BanPlayerButton(self.lobby, interaction.user)
            view = View()
            view.add_item(admit_button)
            view.add_item(ban_player)

            await self.lobby.admin.send(f"{interaction.user.display_name} has asked to rejoin the lobby.", view=view)
            await interaction.response.send_message(
                "You have asked the admin if you can rejoin the lobby.", ephemeral=True, delete_after=60
            )

        elif not_in_lobby:
            if len(self.lobby.players) >= self.lobby.game.MAX_PLAYERS:
                return await interaction.response.send_message(
                    "Sorry, the lobby is at it max players for this game. :(", ephemeral=True, delete_after=600
                )
            else:
                self.lobby.add_to_lobby(interaction.user)
                await self.lobby.update()
                await interaction.response.send_message("Welcome to the game!", ephemeral=True, delete_after=600)

        else:
            await interaction.response.send_message("You are in the lobby silly! 😝", ephemeral=True, delete_after=60)


class LeaveLobbyButton(discord.ui.Button):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby
        super().__init__(label=f"Leave Lobby", emoji="💩")

    async def callback(self, interaction: Interaction):
        if interaction.user.display_name in self.lobby.players:
            if self.lobby.remove_from_lobby(interaction.user.display_name):
                await self.lobby.update()

            await interaction.response.send_message(
                "You have successfully left this lobby.", ephemeral=True, delete_after=600
            )

        else:
            await interaction.response.send_message(
                "You are not in this lobby silly! 😝", ephemeral=True, delete_after=600
            )
