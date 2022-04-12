#Joshua Peter Roux
#Discord bot
import json
import os
import asyncio
import random
import time
import traceback
from typing import List
import discord
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ANDRE = os.getenv('DISCORD_ANDRE')

ANDRE_IN_CHANNEL = False
SOUNDPAD = 0

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    client.loop.create_task(andre_loop())
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.send(
        f'Hi {member.name},\n Andre is a doos.'
    )

async def andre_loop():
    global ANDRE_IN_CHANNEL
    global SOUNDPAD
    print('Loops')
    while True:
        try:
            voiceChannels = await get_v_channels()
            andreChannel = await check_andre(voiceChannels)

            if andreChannel is not None and not ANDRE_IN_CHANNEL:
                ANDRE_IN_CHANNEL = True
            elif andreChannel is None and ANDRE_IN_CHANNEL:
                ANDRE_IN_CHANNEL = False

            if andreChannel is not None:
                SOUNDPAD = input("Choose sound: ")
                await play_recording(andreChannel)
        except:
            print(traceback.format_exc())
        await asyncio.sleep(5)

async def get_v_channels()->List[discord.VoiceChannel]:
    guild = client.get_guild(int(GUILD))
    channels = guild.voice_channels
    return  channels

async def check_andre(channels:List[discord.VoiceChannel])->discord.VoiceChannel:
    for voiceChannel in channels:
        for member in voiceChannel.members:
            if member.name == ANDRE:
                return voiceChannel
    return None

async def play_recording(chanel:discord.VoiceChannel):
    await chanel.connect()
    guild = client.get_guild(int(GUILD))
    voiceCLient = discord.utils.get(client.voice_clients, guild=guild)

    if SOUNDPAD == "1":
        audioPath = Path('phill.mp3').absolute()
    else:
        audioPath = Path('doos.mp3').absolute()

    exePath = Path('E:\Coding\Downloads\\ffmpeg-N-105621-g59c647bcf3-win64-gpl-shared\\bin\\ffmpeg.exe')
    audio_source = discord.FFmpegPCMAudio(audioPath, executable=exePath)

    if not voiceCLient.is_playing():
        voiceCLient.play(audio_source)

    while voiceCLient.is_playing():
        time.sleep(0.1)
    await voiceCLient.disconnect()

client.run(TOKEN)