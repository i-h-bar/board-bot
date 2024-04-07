from pathlib import Path
import random
from types import ModuleType

import discord
from discord import User, Member, SelectOption, Interaction
from discord.ui import View

from bot.lobby.admin_ctrl import RemovePlayersDropdown, StartGameButton, CancelGameButton


class Lobby(discord.Embed):
    def __init__(self, interaction: Interaction, admin: User | Member, name: str, description: str, game: ModuleType):
        self.interaction = interaction
        self.game = game
        self.admin = admin
        self.name = name
        self.emojis: tuple = game.EMOJIS
        self.players = {}
        self.file_name = f"{Path(self.game.__file__).parts[-2]}_logo.png"
        self.file = discord.File(
            f"{'/'.join(Path(self.game.__file__).parts[:-1])}/assets/logo.png", filename=self.file_name
        )

        try:
            url = game.URL
        except AttributeError:
            url = None

        super().__init__(title=name, description=description, url=url)
        self.set_author(name=admin.display_name)
        self.add_to_lobby(self.admin)
        self.set_image(url=f"attachment://{self.file_name}")

    @property
    def admin_controls(self) -> View:
        start_game = StartGameButton(self, self.interaction)
        cancel_game = CancelGameButton(self, self.interaction)
        view = View()
        view.add_item(start_game)
        view.add_item(cancel_game)
        view.add_item(RemovePlayersDropdown(self))

        return view

    def add_to_lobby(self, user: User | Member):
        self.add_field(name=random.choice(self.game.EMOJIS), value=user.display_name)
        self.players[user.display_name] = user

    def remove_from_lobby(self, user: str) -> bool:
        try:
            del self.players[user]
        except KeyError:
            return False
        else:
            for i, field in enumerate(self.fields):
                if field.value == user:
                    self.remove_field(i)
                    return True
            else:
                return False
