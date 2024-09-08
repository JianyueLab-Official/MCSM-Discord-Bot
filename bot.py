# Imports
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from scripts import *

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


@client.tree.command(name="overview", description="Get overview of your MCSM panel.")
async def overview(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    data = function_getOverview()
    if data["status"] == '200':
        # response
        embed = discord.Embed(
            title="Overview",
            colour=discord.Colour.green(),
            description="The overview of your MCSM panel"
        )
        embed.add_field(name="Panel Version", value=data["panel_version"])
        embed.add_field(name="Login Suc.", value=data["record_login"])
        embed.add_field(name="Login Failed", value=data["record_login_failed"])
        embed.add_field(name="Illegal Access", value=data["record_illegal_access"])
        embed.add_field(name="Banned IPs", value=data["record_banned_ips"])
        embed.add_field(name="Daemons", value=f"{remote_available} / {remote_total}")
        return
    else:
        return data

@client.tree.command(name="info", description="Get information about this bot.")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "## MCSM-Discord-Bot\n",
        "This bot was developed by [JianyueLab](https://awa.ms).\n",
        "**GitHub Repo: ** https://awa.ms/mcsm-discord-bot\n",
        "**Bot Version: **" + BOT_VERSION,
        "**Bot Type: **" + BOT_BUILD_TYPE,
        ephemeral=True,
    )


client.run(DISCORD_TOKEN)
