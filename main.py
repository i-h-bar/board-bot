import logging
import os

import discord
from discord.ext.commands import Bot
from discord.ui import View
from dotenv import load_dotenv

from bot.const.custom_types import Interaction
from bot.const.games import current_games
from bot.lobby.select import GameSelect

load_dotenv()
bot = Bot(command_prefix="/", intents=discord.Intents.all())
logging.getLogger().setLevel(logging.DEBUG)


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
    print("Bot ready")


@bot.tree.command(name="play", description="Start playing a board game!")
async def play(interaction: Interaction):
    if interaction.channel not in current_games:
        current_games.add(interaction.channel)
        dropdown = GameSelect()
        view = View()
        view.add_item(dropdown)
        await interaction.response.send_message("Pick a game to play...", view=view, ephemeral=True, delete_after=600.0)
    else:
        await interaction.response.send_message(
            "There is already a game being played or organised in this channel!", ephemeral=True, delete_after=60.0
        )


if __name__ == "__main__":
    bot.run(os.getenv("BOARD_BOT_TOKEN"))
