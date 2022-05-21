import discord
from discord.ext import commands
import random
from discord import app_commands
import random
import Embeds

# Kick function
async def kick_func(interaction: discord.Interaction, member: discord.Member, reason : str):
    await interaction.user.guild.kick(member, reason=reason)
    embed = discord.Embed(description=f"`{member}` has been kicked for the following reason: \nReason: **{reason}**", colour=0x2f3136)
    embed.set_author(name=f'Kicked.', icon_url=member.display_avatar)
    return embed


class Kick(commands.Cog):
    def __init__(self, client):
        self.client=client



    @app_commands.command(description="Kicks specific member(s).")
    @app_commands.guilds(936084423454113822)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason : str = "No reason provided"):

        # Rare check
        if member == interaction.guild.owner:
            await interaction.response.send_message(embed=await Embeds.Permissions.Kick_Owner(), ephemeral=True)

        # Owner bypass
        if interaction.user.id == interaction.guild.owner.id:
            try:
                await interaction.response.send_message(embed=await kick_func(interaction=interaction, member=member, reason=reason))

            # Try except
            except:
                embed = discord.Embed(title="Error", description="I cannot ban this member since his role is placed higher than mine.", colour = discord.Colour.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)

        # Defining Variables
        member_role = member.top_role       
        user = interaction.user        
        user_role = user.top_role
        
        # Checking role heirachy
        if user_role <= member_role:
            # Random LIST
            title_dict = ['Sorry.', 'Bad choice!', 'Oops!']
            title_dict_txt = random.choice(title_dict)
            embed = discord.Embed(title=f"{title_dict_txt}", description=f"You can't kick that person! \n**Reasons**: \n- You are trying to kick yourself\n- You are below the role of the person you are trying to kick.", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


        # If heirachy check passes
        else:

            # If user is bot
            if member == self.client.user:
                embed = discord.Embed(title=f"Error.", description=f"Bot has to be kicked manually.", colour=discord.Colour.gold())
                await interaction.response.send_message(embed=embed, ephemeral=True)

            # All checks pass!
            else:
                await interaction.response.send_message(embed=await kick_func(interaction=interaction, member=member, reason=reason))


            

    # Checks if user in server
    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.TransformerError):
            await interaction.response.send_message("The member is not in your server", ephemeral=True)




async def setup(client):
    await client.add_cog(Kick(client))