
import discord
from discord.ext import commands
import random
from discord.ui import Button, View
from discord import app_commands
import Embeds
from time_package import time_converter
import asyncio


# Ban function
async def ban_func(interaction: discord.Interaction, member: discord.Member, reason : str, time : str = None):

    if time == None:
        time = "Infinite"
    elif time != None:
        time = time

    await interaction.user.guild.ban(member, reason=reason)
    embed = discord.Embed(description=f"`{member}` has been banned for the following reason: \nReason: **{reason}** \nTime: **{time}**", colour=0x2f3136)
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
            await interaction.response.send_message(embed=await Embeds.Permissions.Ban_Owner(), ephemeral=True)


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
                    await myinter.response.send_message("Seems like the member has already been unbanned.", ephemeral=True)
                
            else:
                    
                # Hasty try/except
                try: 
                    await interaction.response.send_message("You do not have the permissions to run this interaction.", ephemeral=True)
                except discord.errors.InteractionResponded:
                    await interaction.response.send_message("Oops, it seems like this interaction has been responsed to.", ephemeral=True)

                        
        button.callback = button_callback
        view.add_item(button)

        if interaction.guild.me.top_role < member.top_role:
            embed = discord.Embed(title="Error", description="I cannot ban this member since their role is placed higher than mine.", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
 

        else:    


            # Owner bypass
            if interaction.user.id == interaction.guild.owner.id:
                # Time querys
                if time == None:
                    await interaction.response.send_message(embed=await ban_func(interaction=interaction, member=member, reason=reason), view=view)


                # If user input time
                elif time != None:
                    try:
                        time_q = time_converter.time_instance._convert(time)

                    # User fails to input correct time format
                    except:
                        await interaction.response.send_message("Please enter a valid format, s|m|h|d|w|y, e.g. 54d.")

                    # Checks pass
                    else:
                        await interaction.response.send_message(embed=await ban_func(interaction=interaction, member=member, reason=reason, time=time), view=view)
                        await asyncio.sleep(time_q)


                        # Incase failed to unban
                        try:
                            await interaction.guild.unban(discord.Object(id=int(member.id)))
                            embed = discord.Embed(colour=0x2f3136)
                            embed.set_author(name=f"{member} is now unbanned. (Timed ban)", icon_url=member.display_avatar)
                            await interaction.edit_original_message(view=view.disab)
                            await interaction.followup.send(embed=embed)
                        except:
                            return

            else:
                
                # User check for Heirachy
                if user_role <= member_role:

                    # Random LIST
                    title_dict = ['Sorry.', 'Bad choice!', 'oops!']
                    title_dict_txt = random.choice(title_dict)
                    embed = discord.Embed(title=f"{title_dict_txt}", description=f"You can't ban that person! \n**Reasons**: \n- You are trying to ban yourself\n- You are below the role of the person you are trying to ban.", colour = discord.Colour.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
                # If user check passes
                else:

                    # If member is bot 
                    if member == self.client.user:
                        embed = discord.Embed(title='Error.', description='Bot has to be banned manually.', colour = discord.Colour.gold())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        
                    # All checks pass!
                    else:       

                        # Time querys
                        if time == None:
                            await interaction.response.send_message(embed=await ban_func(interaction=interaction, member=member, reason=reason), view=view)

                        # If user input time
                        elif time != None:
                            try:
                                time_q = time_converter.time_instance._convert(time)

                            # User fails to input correct time format
                            except:
                                await interaction.response.send_message("Please enter a valid format, s|m|h|d|w|y, e.g. 54d.")

                            # Checks pass
                            else:

                                await interaction.response.send_message(embed=await ban_func(interaction=interaction, member=member, reason=reason, time=time), view=view)
                                await asyncio.sleep(time_q)

                                # Incase failed to unban
                                try:
                                    await interaction.guild.unban(discord.Object(id=int(member.id)))
                                    embed = discord.Embed(colour=0x2f3136)
                                    embed.set_author(name=f"{member} is now unbanned. (Timed ban)", icon_url=member.display_avatar)
                                    await interaction.followup.send(embed=embed)
                                except:
                                    return

                        







    
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
        except discord.NotFound:
            await interaction.response.send_message("User doesn't exist or is already unbanned.", ephemeral=True)

        # If users are dumb and use letters
        except ValueError:
            await interaction.response.send_message("User_IDs can't contain letters", ephemeral=True)

        except discord.app_commands.errors.TransformerError:
            await interaction.response.send_message("User not in serer", ephemeral=True)




    # Checks if user in server
    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.TransformerError):
            await interaction.response.send_message("The member is not in your server", ephemeral=True)


async def setup(client):
    await client.add_cog(Ban(client))