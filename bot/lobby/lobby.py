from pathlib import Path
import random
from types import ModuleType

import discord
from discord import User, Member


class Lobby(discord.Embed):
    def __init__(self, admin: User | Member, name: str, description: str, game: ModuleType):
        self.game = game
        self.admin = admin
        self.name = name
        self.emojis: tuple = game.EMOJIS
        self.players = set()
        self.file_name = f"{Path(self.game.__file__).parts[-2]}_logo.png"
        self.file = discord.File(
            f"{'/'.join(Path(self.game.__file__).parts[:-1])}/assets/logo.png", filename=self.file_name
        )

        try:
            url = game.URL
        except AttributeError:
            url = None

        super().__init__(title=name, description=description, url=url)
        self.set_author(name=admin.nick)
        self.add_to_lobby(self.admin)
        self.set_image(url=f"attachment://{self.file_name}")

    def add_to_lobby(self, user: User | Member):
        self.add_field(name=random.choice(self.game.EMOJIS), value=user.nick or user.name)
        self.players.add(user)

    def remove_from_lobby(self, user: User | Member) -> bool:
        try:
            self.players.remove(user)
        except KeyError:
            return False
        else:
            for i, field in enumerate(self.fields):
                if field.value == user.nick or field.value == user.name:
                    self.remove_field(i)
                    return True
            else:
                return False

