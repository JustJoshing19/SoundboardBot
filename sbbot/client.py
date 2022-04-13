import discord
from loguru import logger
from sbbot.core import voice_join_greetings

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')
    client.loop.create_task(voice_join_greetings(client))
