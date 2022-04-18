import asyncio
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional
from loguru import logger
import yaml
from discord import Client, Guild, VoiceChannel, Member
from sbbot.core import play_audio
from sbbot.core.config import is_local

GUILDLOCK = defaultdict(asyncio.Lock)

@dataclass
class Greeting:
    discord_name: str
    clip: Path
    guilds: List[int]
    debug: bool = False

GREETINGS: Optional[List[Greeting]] = None
GREETING_STATES = defaultdict(lambda: True) # Its assumed everyone is already in a channel so that
                                            # when the bot restarts it wont play audio for people in a channel
                                            # but this will still play audio when someone joins after restart
async def get_config() -> List[Greeting]:
    global GREETINGS

    if GREETINGS is None:
        path = Path("data/config/voice_join_greetings.yaml")
        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        GREETINGS = [Greeting(**greeting) for greeting in data['greetings']]

        for greeting in GREETINGS:
            greeting.clip = Path('data/audio')/greeting.clip

    return GREETINGS

def get_state(username: str, voice_channel: VoiceChannel):
    return GREETING_STATES[(username, voice_channel.id)]

def set_state(username: str, voice_channel: VoiceChannel, value: bool):
    GREETING_STATES[(username, voice_channel.id)] = value

def get_voice_channels_from_guilds(guilds: List[Guild]) -> Iterator[VoiceChannel]:
    for guild in guilds:
        for voice_channel in guild.voice_channels:
            yield voice_channel, guild

def get_full_username(member: Member) -> str:
    return f'{member.name}#{member.discriminator}'

def get_active_voice_channel_for_user(guilds: List[Guild], username: str) -> Optional[VoiceChannel]:
    for voice_channel, guild in get_voice_channels_from_guilds(guilds):
        logger.debug(f"Checking channel `{voice_channel.name}` for `{username}`")
        for member in voice_channel.members:
            logger.debug(f"In voice channel `{voice_channel.name}` member `{get_full_username(member)}`")
            if get_full_username(member) == username:
                return voice_channel, guild
    return None, None

async def single_voice_greeting(client: Client, greeting: Greeting):
    if greeting.debug != is_local():
        return

    guilds = []
    for guild_id in greeting.guilds:
        guild = client.get_guild(guild_id)
        if guild is not None:
            guilds.append(guild)

    logger.info(
        f"Guilds found for user: `{greeting.discord_name}`\n" +
        yaml.safe_dump([guild.name for guild in guilds])
    )

    while True:
        active_voice_channel, active_guild = get_active_voice_channel_for_user(guilds, greeting.discord_name)

        if active_voice_channel is not None:
            if not get_state(greeting.discord_name, active_voice_channel):
                set_state(greeting.discord_name, active_voice_channel, True)

                logger.info(f'Playing clip for {greeting.discord_name}')
                async with GUILDLOCK[active_guild.id]:
                    await play_audio(active_voice_channel ,greeting.clip)

        for voice_channel, _ in get_voice_channels_from_guilds(guilds):
            if active_voice_channel is None or voice_channel.id != active_voice_channel.id:
                set_state(greeting.discord_name, voice_channel, False)

        await asyncio.sleep(0.1)

async def voice_join_greetings(client: Client):
    config = await get_config()

    for greeting in config:
        client.loop.create_task(single_voice_greeting(client, greeting))
