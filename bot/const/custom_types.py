import discord
from discord import InteractionResponse
from discord._types import ClientT


class Interaction(discord.Interaction):
    response: InteractionResponse[ClientT]
