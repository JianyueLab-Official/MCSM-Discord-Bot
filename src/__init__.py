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
BOT_VERSION = '0.1.0'
BOT_BUILD_TYPE = 'DEV'


# Start Bot
@client.event
async def on_ready():
    # Try to sync commands
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        print('Bot is ready for use!')
    except Exception as e:
        print(e)


# /overview
@client.tree.command(name="overview", description="Get overview of your MCSM panel.")
async def overview(interaction: discord.Interaction):
    # Send a wait message ("Bot is thinking"), only the sender can see this message.
    await interaction.response.defer(ephemeral=True)
    # Get data from script
    data = function_getOverview()
    # Check status
    if data["status"] == 200:
        # response - create am embed message
        embed = discord.Embed(
            # title of embed message
            title="Overview",
            # Colour of sidebar
            colour=discord.Colour.green(),
            # Description under the title
            description="The overview of your MCSM panel"
        )
        # Add fields to the embed message
        embed.add_field(name="Panel Version", value=data["panel_version"])
        embed.add_field(name="Login Suc.", value=data["record_login"])
        embed.add_field(name="Login Failed", value=data["record_login_failed"])
        embed.add_field(name="Illegal Access", value=data["record_illegal_access"])
        embed.add_field(name="Banned IPs", value=data["record_banned_ips"])
        embed.add_field(name="Daemons", value=f"{data["remote_available"]} / {data["remote_total"]}")
        # response the embed message
        await interaction.followup.send(embed=embed)
        return
    # if the status is not 200 then just send the error message
    else:
        # Send the error message
        await interaction.followup.send(f"{data["message"]}")
        return


# /search_user (unfinished)
@client.tree.command(name="search_user", description="Search up a user")
async def search_user(interaction: discord.Interaction):
    # ephemeral = private
    await interaction.response.defer(ephemeral=True)
    data = function_searchUser()
    if data["status"] == 200:
        # response process
    else:
        await interaction.followup.send(f"{data['message']}")
    return


# /create_user [username] [password] [role selection]
@client.tree.command(name="create_user", description="Add a user to your panel")
# create choice for role
@app_commands.choices(
    role=[
        # name of the choice and value
        app_commands.Choice(name='Admin', value=10),
        app_commands.Choice(name='User', value=1),
        app_commands.Choice(name='Banned User', value=-1),
    ]
)
async def create_user(interaction: discord.Interaction, username: str, password: str, role: app_commands.Choice[int]):
    await interaction.response.defer(ephemeral=True)
    data = function_createUser(username, password, role.value)
    if data["status"] == 200:
        await interaction.followup.send(f"**User Created Successfully | UUID:** {data["user_uuid"]}")
    else:
        await interaction.followup.send(f"{data["message"]}")
    return


# /delete_user [user_uuid] (unfinished)
@client.tree.command(name="delete_user", description="Delete exist user on your panel")
async def delete_user(interaction: discord.Interaction, user_uuid: str):
    await interaction.response.defer(ephemeral=True)
    data = function_deleteUser(user_uuid)
    if data["status"] == 200:
        await interaction.followup.send(data["message"])
        return
    else:
        await interaction.followup.send(f"{data["message"]}")
        return


# /instance_list (unfinished)
@client.tree.command(name="instance_list", description="List all your instances")
async def instance_list(interaction: discord.Interaction):
    data = function_instanceList()
    if data["status"] == 200:
        # data process
    else:
        await interaction.followup.send(f"{data['message']}")

    return


# /create_instance [daemon_id] (unfinished)
@client.tree.command(name="create_instance", description="Create a instance")
async def create_instance(interaction: discord.Interaction, daemon_id: str):
    data = function_createInstance(daemon_id)
    if  data["status"] == 200:
        # data process
    else:
        await interaction.followup.send(f"{data['message']}")
    return


# /update_config [uuid] [daemon_id] (unfinished)
async def update_config(interaction: discord.Interaction, uuid: str, daemon_id: str):
    data = function_updateConfig(uuid, daemon_id)
    if data["status"] == 200:
        # data proces
    else:
        await interaction.followup.send(f"{data['message']}")
    return


# /delete_instance [daemon_id] [uuid] [delete_file]
@client.tree.command(name="delete_instance", description="Delete an instance")
@app_commands.choices(
    delete_file = [
        app_commands.Choice(name='true', value=True),
        app_commands.Choice(name='false', value=False),
    ]
)
async def delete_config(interaction: discord.Interaction, uuid: str, daemon_id: str, delete_file: app_commands.Choice[str]):
    await interaction.response.defer(ephemeral=True)
    data = function_deleteInstance(uuid, daemon_id, delete_file.value)
    if data["status"] == 200:
        await interaction.followup.send(f"{data['message']}, UUID: {uuid}")
    else:
        await interaction.followup.send(f"{data['message']}")
    return


# /instance [start / stop / restart] [uuid] [daemon_id]
@client.tree.command(name="instance", description="Instance control")
@app_commands.choices(
    action = [
        app_commands.Choice(name='Start', value="start"),
        app_commands.Choice(name='Stop', value="stop"),
        app_commands.Choice(name='Restart', value="restart"),
        app_commands.Choice(name='Kill', value='kill')
    ]
)
async def instance(interaction: discord.Interaction, action: app_commands[str], uuid: str, daemon_id: str):
    await interaction.response.defer(ephemeral=True)

    if action.value == 'start':
        data = function_startInstance(uuid, daemon_id)
        if data["status"] == 200:
            await interaction.followup.send(f"{data['message']}, UUID: {uuid}")
        else:
            await interaction.followup.send(f"{data['message']}")
    elif action.value == 'stop':
        data = function_stopInstance(uuid, daemon_id)
        if data["status"] == 200:
            await interaction.followup.send(f"{data['message']}, UUID: {uuid}")
        else:
            await interaction.followup.send(f"{data['message']}")
    elif action.value == 'restart':
        data = function_restartInstance(uuid, daemon_id)
        if data["status"] == 200:
            await interaction.followup.send(f"{data['message']}, UUID: {uuid}")
        else:
            await interaction.followup.send(f"{data['message']}")
    elif action.value == 'kill':
        data = function_killInstance(uuid, daemon_id)
        if data["status"] == 200:
            await interaction.followup.send(f"{data['message']}, UUID: {uuid}")
        else:
            await interaction.followup.send(f"{data['message']}")
    else:
        await interaction.followup.send("Invalid Input.")
    return


# /command [uuid] [daemon_id] [command]
@client.tree.command(name="command", description="Send a command of instance")
async def command(interaction: discord.Interaction, uuid, daemon_id, command: str):
    await interaction.response.defer(emphemeral=True)
    command_data = function_sendCommand(uuid, daemon_id, command)
    if command_data["status"] == 200:
        output_data = function_getOutput(uuid, daemon_id)
        if output_data["status"] == 200:
            await interaction.followup.send(f"```bash \n {output_data['message']} \n```")
        else:
            await interaction.followup.send(f"{output_data['message']}")
        return
    else:
        await interaction.followup.send(f"{command_data['message']}")
    return


# /add_node [ip] [port] [remarks] [daemon_apikey]
@client.tree.command(name="add_node", description="Add a new Node.")
async def add_node(interaction: discord.Interaction, ip: str, port: int, remarks: str, daemon_apikey: str):
    data = function_addNode(ip, port, remarks, daemon_apikey)
    if data["status"] == 200:
        await interaction.followup.send(f"{data["message"]} | Daemon Id: {data["data"]}")
    else:
        await interaction.followup.send(f"{data['message']}")
    return


# /delete_node [daemon_id]
@client.tree.command(name="remove_node", description="Remove a Node.")
async def remove_node(interaction: discord.Interaction, daemon_id: str):
    await interaction.response.defer(emphemeral=True)

    data = function_deleteNode(daemon_id)

    if data["status"] == 200:
        await interaction.follow.send(f"{data['message']} | Daemon Id: {data['data']}")
    else:
        await interaction.followup.send(f"{data['message']}")
    return


# /try_node [daemon_id]
@client.tree.command(name="try_instance", description="Try to connect Node")
async def try_instance(interaction: discord.Interaction, daemon_id: str):
    await interaction.response.defer(ephemeral=True)

    data = function_tryNode(daemon_id)

    if data["status"] == 200:
        await interaction.followup.send(f"{data['message']} | {data["data"]}")
    else:
        await interaction.followup.send(f"{data['message']}")
    return


# /info
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
