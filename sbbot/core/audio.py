import asyncio
from pathlib import Path
from discord import VoiceChannel, FFmpegPCMAudio, VoiceClient

async def wait_stop_playing(voice_client: VoiceClient):
    while voice_client.is_playing():
        await asyncio.sleep(0.1)

async def play_audio(voice_channel: VoiceChannel, path: Path):
    voice_client = await voice_channel.connect()

    audio_source = FFmpegPCMAudio(path)

    await wait_stop_playing(voice_client)
    
    voice_client.play(audio_source)    
    
    await wait_stop_playing(voice_client)
    
    await voice_client.disconnect()
