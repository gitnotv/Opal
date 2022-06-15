
import discord
from discord.ext import commands
import random
from discord.ui import Button, View
from discord import app_commands
from cache.ext import permcache

import asyncio





# Ban function
async def ban_func(interaction: discord.Interaction, member: discord.Member, reason : str):



    await interaction.user.guild.ban(member, reason=reason)
    embed = discord.Embed(description=f"`{member}` has been banned for the following reason: \nReason: **{reason}**", colour=0x2f3136)
    embed.set_author(name=f'Banned.', icon_url=member.display_avatar)
    return embed



class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Ban command
    @app_commands.command(description="Bans specific member(s).")
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.guilds(936084423454113822)
    async def ban(self, interaction: discord.Interaction, member: discord.Member , *, reason: str = "No reason provided", time : str = None): 
   

        # Rare check
        if member == interaction.guild.owner:
            # Title switch list
            title_list = ["Sorry.", "Oops.", "Whoops."]
            rnd_title = random.choice(title_list)

            # Ban error embed
            embed = discord.Embed(title=f"{rnd_title}", description=f"❌ | **You cannot ban the owner of this guild.**", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


        # Defining variables
        view = View()
        member_role = member.top_role
        user = interaction.user
        user_role = user.top_role
        button = Button(style=discord.ButtonStyle.blurple, label="Unban")

        # Button callback
        async def button_callback(myinter : discord.Interaction):

            # Perms Check
            if myinter.user.guild_permissions.administrator:

                # Try check
                try:
                    await myinter.guild.unban(discord.Object(id=int(member.id)))
                    embed = discord.Embed(colour=0x2f3136)
                    embed.set_author(name=f"{member} is now unbanned.", icon_url=member.display_avatar)
                    await interaction.edit_original_message(content="", view=None)
                    await interaction.edit_original_message(embed=embed)

                # Exception
                except discord.NotFound:
                    await myinter.response.send_message("❌ | **Looks like this member doesn't exist**", ephemeral=True)

                    
                
            else:
                    
                # No permissions
                await myinter.response.send_message("❌ | **You do not have the permissions to run this interaction.**", ephemeral=True)


                        
        button.callback = button_callback
        view.add_item(button)

        if interaction.guild.me.top_role < member.top_role:
            embed = discord.Embed(description="❌ | **I cannot ban this member since their role is placed higher than mine.**", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


        else:    


            # Owner bypass
            if interaction.user.id == interaction.guild.owner.id:
                await interaction.response.send_message(embed=await ban_func(interaction=interaction, member=member, reason=reason), view=view)

            else:
                
                # User check for Heirachy
                if user_role <= member_role:

                    # Random LIST
                    title_dict = ['Sorry.', 'Bad choice!', 'oops!']
                    title_dict_txt = random.choice(title_dict)
                    embed = discord.Embed(title=f"{title_dict_txt}", description=f"You can't ban that person! \n**Reasons**: \n- You are trying to ban yourself\n- You are below / same as the role of the person you are trying to ban.", colour = discord.Colour.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
                # If user check passes
                else:

                    # If member is bot 
                    if member == self.client.user:
                        embed = discord.Embed(title='Error.', description='Bot has to be banned manually.', colour = discord.Colour.gold())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        
                    # All checks pass!
                    else:       
                        await interaction.response.send_message(embed=await ban_func(interaction=interaction, member=member, reason=reason), view=view)




                       







    
    # Unban command
    @app_commands.command(description="Unbans specific member(s).")
    @app_commands.guilds(936084423454113822)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member_id : str):

        # Try check
        try:
            # Unbans User
            mem = await self.client.fetch_user(int(member_id)) or self.client.get_user(int(member_id))
            await interaction.guild.unban(discord.Object(id=int(member_id)))
            embed = discord.Embed(description=f"`{mem}` has been unbanned.", colour=discord.Colour.green())
            embed.set_author(name=f'Unbanned.', icon_url=self.client.user.display_avatar)
            await interaction.response.send_message(embed=embed)

        # Exception
        except discord.NotFound as e:
            await interaction.response.send_message("❌ | **Looks like this member doesn't exist**", ephemeral=True)


        # If users are dumb and use letters
        except ValueError as e:
            await interaction.response.send_message("❌ | **Your id cannot contain letters**", ephemeral=True)

        except discord.app_commands.errors.TransformerError as e:
            embed = discord.Embed(description=f"```diff\n- {e}```", colour=discord.Colour.magenta())
            embed.set_author(name="OPAL [ERROR]",icon_url=self.client.user.display_avatar)
            embed.set_footer(text="Contact 0_0#5558 if this issue persists.")
            await interaction.response.send_message(embed=embed, ephemeral=True)




    # Checks if user in server
    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.TransformerError):
            await interaction.response.send_message("The member is not in your server", ephemeral=True)


async def setup(client):
    await client.add_cog(Ban(client))