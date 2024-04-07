from types import ModuleType

import discord
from discord import SelectOption, Interaction
from discord.ui import View

from bot.const.games import GAMES
from bot.lobby import Lobby
from bot.lobby.buttons import JoinLobbyButton, LeaveLobbyButton
from bot.lobby.admin_ctrl import CancelGameButton, StartGameButton


class GameSelect(discord.ui.Select):
    def __init__(self):
        options = [
            SelectOption(label=game, emoji=module.SELECT_EMOJI) for game, module in GAMES.items()
        ]
        super().__init__(placeholder="Select a game...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: Interaction):
        try:
            choice = self.values[0]
        except IndexError:
            return await interaction.response.send_message("I didn't successfully get the option", ephemeral=True, delete_after=600.0)

        game: ModuleType = GAMES.get(choice)
        if not game:
            return await interaction.response.send_message(f"I couldn't find the game called: {choice}", ephemeral=True, delete_after=600.0)

        lobby = Lobby(
            admin=interaction.user,
            name=choice,
            description=f"Come play {choice} with me!",
            game=game
        )
        join = JoinLobbyButton(lobby)
        leave = LeaveLobbyButton(lobby)
        view = View()
        view.add_item(join)
        view.add_item(leave)

        await interaction.response.send_message(file=lobby.file, embed=lobby, view=view)

        start_game = StartGameButton(lobby, interaction)
        cancel_game = CancelGameButton(lobby, interaction)
        view = View()
        view.add_item(start_game)
        view.add_item(cancel_game)
        await interaction.user.send("Admin controls:", view=view)