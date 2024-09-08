# Imports
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create shortcut
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# Version information
BOT_VERSION = '0.0.1'
BOT_BUILD_TYPE = 'DEV'


# Start Bot
@client.event
async def on_ready():
    print('Bot is ready for use!')
    # Try to sync commands
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


client.run(DISCORD_TOKEN)
