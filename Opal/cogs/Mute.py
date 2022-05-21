
import discord
from discord.ext import commands
import random
from discord import app_commands









class Mute(commands.Cog):
    def __init__(self, client):
        self.client=client

    @app_commands.command(description="Mutes specified member(s).")
    @app_commands.guilds(936084423454113822)
    @app_commands.default_permissions(kick_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason:str="No reason provided"):
        # Check for administrator
        if interaction.user.guild_permissions.kick_members:

            # Variables
            member_role = member.top_role
            user = interaction.user
            user_role = user.top_role
            
            # User check for heirachy
            if user_role <= member_role:

                title_dict = ['Sorry.', 'Bad choice!', 'Oops!']
                title_dict_txt = random.choice(title_dict)
                embed = discord.Embed(title=f"{title_dict_txt}", description=f"You can't mute that person! \n**Reasons**: \n- You are trying to mute yourself \n- You are below the role of the person you are trying to mute", colour = discord.Colour.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)

            # If member is not self
            elif member != interaction.user:
                await member.timeout(until=None, reason=reason)


                    
        
            elif member == interaction.user:
                error_embed = discord.Embed(title=f"You can't mute yourself!", colour = discord.Colour.red())
                await interaction.user.send(embed=error_embed, ephemeral=True)
            






    @app_commands.command(description="Unmutes specific member(s).")
    @app_commands.guilds(936084423454113822)
    @commands.has_permissions(kick_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            unmute_embed = discord.Embed(description=f"`{member}` has now been unmuted.", colour=discord.Colour.green())
            unmute_embed.set_author(name=f'Unmuted.', icon_url=self.client.user.display_avatar)
            await interaction.response.send_message(embed=unmute_embed)

        # Check
        elif role not in member.roles:
            embed = discord.Embed(title='User not muted.',description="The user you tried to unmute wasn't even muted in the first place.", colour=discord.Colour.red())
            await interaction.response.send_message(embed=embed)





async def setup(client):
    await client.add_cog(Mute(client))