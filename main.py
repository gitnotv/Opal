from ast import pattern
import discord
from discord.ext import commands
import sqlite3 as db
import aiosqlite as db2
import re
from discord import app_commands
import Embeds


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


# Defining Client
client = commands.Bot(command_prefix=get_prefix, intents=intents)


# Command Not foun error
@client.listen("on_command_error")
async def command_not_found(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'That command does not exist. Use **/help** to view commands.')


# Loads cog
@client.command()
@commands.has_permissions(kick_members=True)
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    embed = discord.Embed(title='Loaded ✅', description='Cog has been loaded.', colour=0x00FF00)
    await ctx.send(embed=embed, delete_after=1)
    await ctx.message.delete()


# On message event to find guild prefix
@client.listen("on_message")
async def prefix_listener(message):

    # Check for message content
    pattern = re.compile(r"prefix")
    matches = pattern.finditer(str(message.content))
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


# Removes help command
client.remove_command("help")
        


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
    if isinstance(error, app_commands.BotMissingPermissions):
        embed = discord.Embed(description=f"{error}", color=discord.Colour.magenta())
        embed.set_author(name="OPAL ERROR",icon_url=client.user.display_avatar)
        await interaction.response.send_message(embed=embed)

    # User missing perms
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(description=f"{error}", color=discord.Colour.magenta())
        embed.set_author(name="OPAL ERROR",icon_url=client.user.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)


# On command error
@client.listen("on_command_error")
async def command_error(ctx, error):

    # Bot missing permissions
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description=f"{error}", color=discord.Colour.magenta())
        embed.set_author(name="OPAL ERROR",icon_url=client.user.display_avatar)
        await ctx.send(embed=embed)

    # User missing perms
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description=f"{error}", color=discord.Colour.magenta())
        embed.set_author(name="OPAL ERROR",icon_url=client.user.display_avatar)
        await ctx.send(embed=embed)


        
# On ready
@client.event
async def on_ready():
    print(f"{client.user} has loaded.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
    await client.load_extension("cogs.Ban_Util")
    await client.load_extension("cogs.Kick_Util")
    await client.load_extension("cogs.Prefix")
    await client.load_extension("cogs.Help")
    await client.load_extension("cogs.Mute")





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
async def reload(ctx, extension):
    if ctx.author.id == 735757517765869589 or 745801072869900352 or 745801072869900352:
        await client.reload_extension(f'cogs.{extension}')
        embed = discord.Embed(title='Reloaded ✅', description='Cog has been reloaded.', colour=discord.Colour.green())
        await ctx.send(embed=embed, delete_after=1)
        await ctx.message.delete()
    else:
        pass



# Runs token [ESSENTIAL]
client.run(token)