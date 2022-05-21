import discord
from discord.ext import commands
import aiosqlite as db
from discord import Embed, app_commands
import Embeds



class Prefix(commands.Cog):
    def __init__(self, client):
        self.client=client

    @app_commands.command(description="Changes the bot prefix for your server!")
    @app_commands.guilds(936084423454113822)
    @app_commands.checks.has_permissions(administrator=True)
    async def prefix(self, interaction: discord.Interaction, prefix: str):


        # Prefix length check
        if len(prefix) > 4:
            embed = discord.Embed(title=f"Sorry.", description=f"Prefix can't be more than `4 letters` long.", colour=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        # If check passes
        else:
            # DB initialisation
            conn = await db.connect("opal.db")
            cur = await conn.cursor()
            guild_id = interaction.user.guild.id

            # Sanitised SQL
            sqlite = (f"DELETE FROM Prefixes WHERE guild_id = (?)")
            vals = (guild_id,)
            await cur.execute(sqlite, vals)

            # Sanitised SQL
            sql = (f"INSERT INTO Prefixes(Prefix, guild_id) VALUES (?,?)")
            val = (prefix, guild_id)
            await cur.execute(sql, val)

            # Confirmation
            prefix_embed = discord.Embed(title=f"Success", description=f"You have succesfully changed your guild prefix to `{prefix}`.", colour=0x2f3136)
            await interaction.response.send_message(embed=prefix_embed)
            await conn.commit()
            await conn.close()
        



async def setup(client):
    await client.add_cog(Prefix(client))