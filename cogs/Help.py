from discord import app_commands
from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, client):
        self.client=client


    @app_commands.command(description="View all my commands!")
    @app_commands.guilds(936084423454113822)
    async def help(self, interaction: discord.Interaction):

        #Base embed
        embed = discord.Embed(title=f"Help", description=f"Displaying all the slash commands available to your guild.", colour=discord.Colour.magenta())
        embed.add_field(name="Commands:",value=f"**Prefix:** \n>   `Usage:` /prefix <prefix> \n>   `Description:` Changes your bot prefix for your server!\n**Kick:** \n>   `Usage:` /kick <member> [reason] \n>   `Description:` Kicks specific member(s)\n **Ban:** \n>   `Usage:` /ban <member> [reason] \n>   `Description:` Bans specific member(s)\n **Unban:** \n>   `Usage:` /unban <member> [reason] \n>   `Description:` Unbans specific member(s)")
        await interaction.response.send_message(embed=embed, ephemeral=True)





async def setup(client):
    await client.add_cog(Help(client))
