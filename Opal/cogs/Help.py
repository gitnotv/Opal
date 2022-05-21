import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite as db



# Gets prefix using guild_id
async def get_prefix(client, interaction : discord.Interaction):
    conn = await db.connect("opal.db")
    cur = await conn.cursor()
    guild_id = interaction.user.guild.id

    # Fetches prefix
    await cur.execute(f"SELECT Prefix FROM Prefixes where guild_id = {guild_id}")
    req = await cur.fetchone()

    # Check to see if prefix is None
    if req is None:
        req = '-'
    elif req != None:
        req = req[0]

    # Returns request
    return req


class Help(commands.Cog):
    def __init__(self, client):
        self.client=client

    @app_commands.command(description="View all my commands!")
    @app_commands.guilds(936084423454113822)
    async def help(self, interaction: discord.Interaction):

        #Base embed
        embed = discord.Embed(title=f"Help", description=f"Displaying all the slash commands available to your guild.", colour=discord.Colour.magenta())
        embed.add_field(name="Commands:",value=f"**Prefix:** \n>   `Usage:` /prefix <prefix> \n>   `Description:` Changes your bot prefix for your server!\n**Kick:** \n>   `Usage:` /kick <member> [reason] \n>   `Description:` Kicks specific member(s)\n **Ban:** \n>   `Usage:` /ban <member> [reason] \n>   `Description:` Bans specific member(s) \n**Purge** \n>    `Usage:` {await get_prefix(self.client, interaction)}purge [messages] \n>   `Description:` Purges a certain amount of channel messages")
        await interaction.response.send_message(embed=embed, ephemeral=True)





async def setup(client):
    await client.add_cog(Help(client))
