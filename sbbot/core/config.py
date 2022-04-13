import os

def is_local():
    return os.environ.get('LOCAL', 'yes') == 'yes'

if is_local():
    from dotenv import load_dotenv
    load_dotenv()

class Config:
    DiscordToken: str = os.environ['DISCORD_TOKEN']
