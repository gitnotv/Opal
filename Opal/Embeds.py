import discord
from discord.ext import commands
import random



# Permissions class
class Permissions():

    # No permissions embed
    async def No_permissions():

        # Title switch list
        title_list = ["Sorry.", "Oops.", "Whoops."]
        rnd_title = random.choice(title_list)

        # No perms embed
        embed = discord.Embed(title=f"{rnd_title}", description=f"You don't have the permissions to run this command.", colour = discord.Colour.red())
        return embed

    # Ban owner
    async def Ban_Owner():

        # Title switch list
        title_list = ["Sorry.", "Oops.", "Whoops."]
        rnd_title = random.choice(title_list)

        # Ban error embed
        embed = discord.Embed(title=f"{rnd_title}", description=f"You cannot ban the owner of this guild.", colour = discord.Colour.red())
        return embed

    # Kick owner
    async def Kick_Owner():

        # Title switch list
        title_list = ["Sorry.", "Oops.", "Whoops."]
        rnd_title = random.choice(title_list)

        # Kick error embed
        embed = discord.Embed(title=f"{rnd_title}", description=f"You cannot ban the owner of this guild.", colour = discord.Colour.red())
        return embed





