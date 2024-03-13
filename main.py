import os
import logging
import discord
from discord.interactions import Interaction
from discord.ext.commands import Bot
from discord.ui import View

from bot.lobby.select import GameSelect

bot = Bot(command_prefix="/", intents=discord.Intents.all())
logging.getLogger().setLevel(logging.DEBUG)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
    print("Bot ready")


@bot.tree.command(name="play")
async def play(interaction: Interaction):
    dropdown = GameSelect()
    view = View()
    view.add_item(dropdown)
    await interaction.response.send_message("Pick a game to play...", view=view, ephemeral=True, delete_after=600.0)


if __name__ == "__main__":
    bot.run(os.getenv("GAME_BOT_TOKEN"))
