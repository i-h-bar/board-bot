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
        if interaction.user not in self.lobby.players.values():
            if len(self.lobby.players) >= self.lobby.game.MAX_PLAYERS:
                return await interaction.response.send_message(
                    "Sorry, the lobby is at it max players for this game. :(", ephemeral=True
                )
            else:
                self.lobby.add_to_lobby(interaction.user)
                await interaction.response.edit_message(embed=self.lobby)


class LeaveLobbyButton(discord.ui.Button):
    def __init__(self, lobby: Lobby):
        self.lobby = lobby
        self.button_emoji = "💩"
        super().__init__(
            label=f"Leave Lobby", emoji=self.button_emoji
        )

    async def callback(self, interaction: Interaction):
        if interaction.user in self.lobby.players:
            if self.lobby.remove_from_lobby(interaction.user.display_name):
                await interaction.response.edit_message(embed=self.lobby)
