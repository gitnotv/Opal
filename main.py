from ast import pattern
from click import command
import discord
from discord.ext import commands
import sqlite3 as db
import aiosqlite as db2

import re
from discord import app_commands

# Terminal text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Gets prefix using guild_id
async def get_prefix(client, message):
    conn = await db2.connect("opal.db")
    cur = await conn.cursor()
    guild_id = message.author.guild.id

    # Fetches prefix [SANITISED SQL]
    fetch_query = (f"SELECT Prefix FROM Prefixes where guild_id = (?)")
    values = (guild_id,)
    await cur.execute(fetch_query, values)
    req = await cur.fetchone()

    # Check to see if prefix is None
    if req is None:
        req = '-'
    elif req != None:
        req = req[0]

    # Returns request
    return req
 

# Token
token = 'OTUyMTI0ODY3MTg3MTk1OTU1.YixdYQ.2D7_vkwU8Q3wPzHrHL50rzIej2Q'


# Intents
intents = discord.Intents.all()

# List vars
extensions = ("cogs.Ban_Util", "cogs.Kick_Util", "cogs.Prefix", "cogs.Help")
owner_ids = (745801072869900352,725355495229227048,735757517765869589)

# Setup hook
class Mybot(commands.Bot):
    # init function to pass in parameters
    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=intents)

    # Setup hook (loading cogs)    
    async def setup_hook(self) -> None:


        #Cogs
        for extension in extensions:
            print(f"{bcolors.OKGREEN}{extension} has been loaded{bcolors.ENDC}")
            await client.load_extension(extension)

        # Opal load
        print(f"{bcolors.OKCYAN}{super().user} has loaded.{bcolors.ENDC}")


# Defining Client
client = Mybot()



# Setting client help command
client.help_command = None






# Loads cog
@client.command()
@commands.has_permissions(kick_members=True)
async def load(ctx, extension : str):


    # Multi load
    if ctx.author.id in owner_ids:
        if str(extension) == "~":
            for extensiond in extensions:
                await client.load_extension(f'{extensiond}')

            embed = discord.Embed(title='Loaded ✅', description=f'Extensions have been loaded.', colour=discord.Colour.green())
            await ctx.send(embed=embed, delete_after=1)
            await ctx.message.delete()

    # If extension isn't all
        elif str(extension) != "~":
            await client.load_extension(f'cogs.{extension}')
            embed = discord.Embed(title='Loaded ✅', description=f'{extension} has been loaded.', colour=discord.Colour.green())
            await ctx.send(embed=embed, delete_after=1)
            await ctx.message.delete()
            
    else:
        pass


# On message event to find guild prefix
@client.listen("on_message")
async def prefix_listener(message : discord.Message):

    # Check for message content
    pattern = re.compile(r"952124867187195955")
    for mention in message.mentions:
        matches = pattern.finditer(str(mention.id))
        for match in matches:
            if match != None:
                conn = await db2.connect("opal.db")
                cur = await conn.cursor()
                guild_id = message.guild.id

                # Gets prefix from DB
                sql = (f"SELECT Prefix FROM Prefixes WHERE guild_id = (?)")
                vals = (guild_id,)
                await cur.execute(sql, vals)
                prefix = await cur.fetchone()
                if prefix == None:
                    prefix = '-'
                elif prefix != None:
                    prefix = prefix[0]
                embed = discord.Embed(title=f"Current prefix is: {prefix}", colour = discord.Colour.magenta())
                await message.channel.send(embed=embed)
                return

            else:

                pass




# On guild join
@client.listen("on_guild_join")
async def on_join(guild):
    channel = client.get_channel(974851424989114438)
    embed = discord.Embed(description=f"**Total guilds:** `{len(client.guilds) - 1}` -> `{len(client.guilds)}` \n**Guild id:** `{guild.id}`", color = discord.Colour.magenta())
    embed.set_author(name=f"Joined {guild.name}")
    await channel.send(embed=embed)


# On command error
@client.tree.error
async def app_command_error(interaction : discord.Interaction, error):

    # Bot missing permissions
    if isinstance(error, app_commands.errors.CommandNotFound):
        return


    # Broad handler
    else:
        embed = discord.Embed(description=f"```diff\n- {error}```", color=discord.Colour.magenta())
        embed.set_footer(text=f"User ID | {interaction.user.id}")
        embed.set_author(name="Opal [ERROR]",icon_url=client.user.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)


# On ready
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))


# On command error
@client.listen("on_command_error")
async def command_error(ctx, error):


    # Bot missing permissions
    if isinstance(error, commands.errors.CommandNotFound):
        return

    # Broad handler
    else:
        embed = discord.Embed(description=f"```diff\n- {error}```", color=discord.Colour.magenta())
        embed.set_footer(text=f"User ID | {ctx.author.id}")
        embed.set_author(name="Opal [ERROR]",icon_url=client.user.display_avatar)
        await ctx.send(embed=embed, ephemeral=True)




# Syncs / commands
@client.command() 
async def sync(ctx):
    await client.tree.sync(guild=discord.Object(id=936084423454113822))



# Unloads cog
@client.command()
@commands.has_permissions(kick_members=True)
async def unload(ctx, extension):
    if ctx.author.id == 735757517765869589: 
        await client.unload_extension(f'cogs.{extension}')
        embed = discord.Embed(title='Unloaded ✅', description='Cog has been unloaded.', colour=discord.Colour.red())
        await ctx.send(embed=embed, delete_after=1)
        await ctx.message.delete()
    else:
        pass


# Reloads cog
@client.command()
@commands.has_permissions(kick_members=True)
async def reload(ctx, extension : str):


    # Multi reload
    if ctx.author.id in owner_ids:
        if str(extension) == "~":
            for extensiond in extensions:
                await client.reload_extension(f'{extensiond}')

            embed = discord.Embed(title='Reloaded ✅', description=f'Extensions have been reloaded.', colour=discord.Colour.green())
            await ctx.send(embed=embed, delete_after=1)
            await ctx.message.delete()

    # If extension isn't all
        elif str(extension) != "~":
            await client.reload_extension(f'cogs.{extension}')
            embed = discord.Embed(title='Reloaded ✅', description=f'{extension} has been reloaded.', colour=discord.Colour.green())
            await ctx.send(embed=embed, delete_after=1)
            await ctx.message.delete()
            
    else:
        pass




# Runs token [ESSENTIAL]
client.run(token)