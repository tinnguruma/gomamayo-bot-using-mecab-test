import os
import re
import time
import discord
import MeCab

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    emoji ="👍"
    await message.add_reaction(emoji)

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
