# Imports
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from scripts import *

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
MESSAGE: bool = os.getenv("EPHEMERAL_MESSAGE", "False").lower() in ("true", "1")

# Create shortcut
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# Version information
BOT_VERSION = '0.1.1'
BOT_BUILD_TYPE = 'Release'


# Start Bot
@client.event
async def on_ready():
    # Try to sync commands
    try:
        synced = await client.tree.sync()
        function_fetchAllData()
        print(f"Synced {len(synced)} command(s)")
        print('Bot is ready for use!')
    except Exception as e:
        print(e)


# Manual Update Information
# /update
@client.tree.command(name="update", description="Update the data dict for your web panel.")
async def update(interaction: discord.Interaction):
    # send defer message, and hide the message only for the person who send the message.
    await interaction.response.defer(ephemeral=MESSAGE)

    try:
        function_fetchAllData()
        await interaction.followup.send("Data Dict Update Successfully")

    except Exception as e:
        print(e)
        await interaction.followup.send(f"Data Dict Update Failed | {e}")

    return


# /overview
@client.tree.command(name="overview", description="Get overview of your MCSM panel.")
async def overview(interaction: discord.Interaction):
    # Send a wait message ("Bot is thinking"), only the sender can see this message.
    await interaction.response.defer(ephemeral=MESSAGE)
    # Get data from script$
    data = function_getOverview()
    # Check status
    if data["status"] == 200:
        # response - create am embed message
        embed = discord.Embed(
            # title of embed message
            title="Overview",
            # Description under the title
            description="The overview of your MCSM panel",
            # Colour of sidebar
            colour=discord.Colour.green(),
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
    # if the status is not 200 then just send the error message
    else:
        # Send the error message
        await interaction.followup.send(f"Request failed | {data["message"]}")
    return


# instance (action) [instance_name]
@client.tree.command(name="instance", description="List all your instance")
# create choice and value
@app_commands.choices(
    action=[
        app_commands.Choice(name="Detail", value=0),
        # app_commands.Choice(name="List", value=1),
        app_commands.Choice(name="Start", value=2),
        app_commands.Choice(name="Stop", value=3),
        app_commands.Choice(name="Restart", value=4),
        app_commands.Choice(name="Kill", value=5)
    ]
)
# function
async def instance(interaction: discord.Interaction, action: app_commands.Choice[int], instance_name: str):
    await interaction.response.defer(ephemeral=MESSAGE)

    # check if uuid, daemon_id is not none
    try:
        # exchange instance_name to uuid, and daemon_id
        uuid, daemon_id = function_nameIdTransfer(instance_name)

        # check action value
        match action.value:
            # if value is 0 - Detail
            case 0:
                # get data from instance detail
                data = function_instanceDetail(uuid, daemon_id)

                # create Embed Message
                embed = discord.Embed(
                    title="Instance Detail",
                    description=f"Instance Detail - {instance_name}",
                    color=discord.Color.purple(),
                )
                # add items to Embed Message
                embed.add_field(name="Status", value=data["instance_status"])
                embed.add_field(name="Auto Start", value=data["autoStart"])
                embed.add_field(name="Auto Restart", value=data["autoRestart"])
                embed.add_field(name="UUID", value=uuid),

                # return Message
                await interaction.followup.send(embed=embed)

            # if value is 2 - Start
            case 2:
                # send request
                data = function_startInstance(uuid, daemon_id)

                # check the status for the request
                if data["status"] == 200:
                    # if instance started, send message
                    await interaction.followup.send(f"Started {instance_name} | {data["time"]}")
                else:
                    # if instance request failed, send error message
                    await interaction.followup.send(f"Start failed {instance_name} | {data["message"]}")

            # if value is 3 - Stop
            case 3:
                # send request
                data = function_stopInstance(uuid, daemon_id)

                # check the status for the request
                if data["status"] == 200:
                    # instance stopped
                    await interaction.followup.send(f"Stopped {instance_name} | {data["time"]}")
                else:
                    # request failed
                    await interaction.followup.send(f"Stop failed {instance_name} | {data["message"]}")

            # if value is 4 - Restart
            case 4:
                # send request
                data = function_restartInstance(uuid, daemon_id)

                # check request status
                if data["status"] == 200:
                    # instance restarted
                    await interaction.followup.send(f"Restarted {instance_name} | {data["time"]}")
                else:
                    # request failed
                    await interaction.followup.send(f"Restart failed {instance_name} | {data["message"]}")

            # if value is 5 - Kill
            case 5:
                # send request
                data = function_killInstance(uuid, daemon_id)

                # check request status
                if data["status"] == 200:
                    # instance killed
                    await interaction.followup.send(f"Killed {instance_name} | {data["time"]}")
                else:
                    await interaction.followup.send(f"Kill failed {instance_name} | {data["message"]}")

            # if value is none of above
            case _:
                await interaction.followup.send("Value Error")

    except Exception as e:
        error_message = f"Error {e}"
        await interaction.followup.send(error_message)
        print(e)

    return


# command & console
# command [instance name] [command]
@client.tree.command(name="command", description="Send a command to your instance")
async def command(interaction: discord.Interaction, instance_name: str, command: str):
    await interaction.response.defer(ephemeral=MESSAGE)

    # try
    try:
        uuid, daemon_id = function_nameIdTransfer(instance_name)

        # send command
        function_sendCommand(uuid, daemon_id, command)

        # get output
        data = function_getOutput(uuid, daemon_id)

        # send the output
        await interaction.followup.send(
            f"""
            ```bash
            {data["data"]}
            ```
            """
        )

    except Exception as e:
        error_message = f"Error {e}"
        await interaction.followup.send(error_message)
        print(e)

    return


# Get output
@client.tree.command(name="output", description="Get output of your instance")
async def output(interaction: discord.Interaction, instance_name: str):
    await interaction.response.defer(ephemeral=MESSAGE)

    try:
        uuid, daemon_id = function_nameIdTransfer(instance_name)

        data = function_getOutput(uuid, daemon_id)

        await interaction.followup.send(
            f"""
            ```bash
            {data["data"]}
            ```
            """
        )

    except Exception as e:
        error_message = f"Error {e}"
        await interaction.followup.send(error_message)
        print(e)

    return


"""
# add node
@client.tree.command(name="node_add", description="Add a node to your panel")
async def node_add(interaction: discord.Interaction, ip: str, port: int, remarks: str, daemon_apikey: str):
    # sending defer message
    await interaction.response.defer(ephemeral=MESSAGE)

    try:
        data = function_addNode(ip, port, remarks, daemon_apikey)

        # update dictionary for discord bot
        function_fetchAllData()

        await interaction.followup.send(f"Daemon successfully added to MCSM Panel | DaemonId {data}")

    except Exception as e:
        print(e)
        await interaction.followup.send(f"Error {e}")

    return


# user control
"""


# info
@client.tree.command(name="info", description="Some information about this bot")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="INFO",
        description="SOME INFORMATION",
        colour=discord.Colour.green(),
    )

    embed.add_field(name="Developer", value="JianyueHugo")
    embed.add_field(name="Homepage", value="awa.ms")
    embed.add_field(name="LICENSE", value="MIT")
    embed.add_field(name="GitHub Repo", value="https://github.com/JianyueLab-Official/MCSM-Discord-Bot", inline=False)
    embed.add_field(name="Version", value=BOT_VERSION)
    embed.add_field(name="Build Type", value=BOT_BUILD_TYPE)

    embed.set_footer(text="Powered by JianyueLab",
                     icon_url="https://pic.awa.ms/f/1/65ed96d9842a5/65ed96d9842a5.png")

    await interaction.response.send_message(embed=embed, ephemeral=MESSAGE)
    return

client.run(DISCORD_TOKEN)
