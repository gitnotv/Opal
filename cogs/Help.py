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
        embed = discord.Embed(title=f"Help", description=f"Now migrating to a website, you can view all of the bot's commands here! \n [View bot commands.](https://gitnotv.github.io/opal-/)", colour=discord.Colour.magenta())
        await interaction.response.send_message(embed=embed, ephemeral=True)





async def setup(client):
    await client.add_cog(Help(client))
