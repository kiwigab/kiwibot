import discord, humanfriendly
from discord.ext import commands
from discord.utils import find
from discord import option, SlashCommandGroup

class Moderation(commands.Cog):
    role = SlashCommandGroup("role", "Commands related to roles")

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cmds.moderation")

    #MULTIPLE ROLE
    @role.command(name="multiple", description="Add or remove a role from multiple members.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @option("filter", choices=["All", "Members", "Bots"], default="All", description="Filter members by type.")
    @option("type", choices=["Give", "Remove"], default="Give", description="Specify the action to perform.")
    @commands.has_permissions(manage_roles=True)
    async def multiplerole(self, ctx, role: discord.Role, filter: str, type: str):
        embed = discord.Embed(title="Multiple Role", color=discord.Color.blue())

        try:
            if filter == "All":
                members = ctx.guild.members

            elif filter == "Members":
                members = [m for m in ctx.guild.members if not m.bot]

            else:
                members = [m for m in ctx.guild.members if m.bot]

            if type == "Give":
                await role.add_members(*members, reason="Multiple Role command")

            else:
                await role.remove_members(*members, reason="Multiple Role command")

            embed.add_field(name="Role", value=role.name)
            embed.add_field(name="Type", value=f"{type}")
            embed.add_field(name="Filter", value=filter)
            embed.add_field(name="Members affected", value=len(members))

        except discord.Forbidden:
            embed.title = "Error"
            embed.description = "I don't have the necessary permissions to modify roles."

        except:
            embed.title = "Error"
            embed.description = "An error occurred while modifying roles. Please try again later."

        await ctx.respond(embed=embed, ephemeral=True)

    #REMOVE ROLE   
    @role.command(name="remove", description=f"Remove a role from a member.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)

    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
                       
      embed = discord.Embed(title="Remove Role", color=discord.Colour.blue(), description=f"❌Changed roles for {member.name}. Removed '{role.name}'!")  

      try:
          if ctx.author.top_role > member.top_role:
              await member.remove_roles(role)
          else:
              embed.title = "Insufficient Permissions"
              embed.description = f"Sorry, you don't have the necessary permissions to remove the role from {member.display_name}. They have a higher role in the hierarchy."

      except:
          embed.title = "Error"
          embed.description = f"Oops! Something went wrong while removing the role from {member.display_name}. They have a higher role in the hierarchy than me."

      await ctx.respond(embed=embed, ephemeral=True)
      
    #GIVE ROLE   
    @role.command(name="give", description="Assign a role to a member.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, member: discord.Member, role: discord.Role):
        embed = discord.Embed(title="Role Assignment", color=discord.Colour.red(), description=f"The role '{role.name}' has been successfully assigned to {member.name}!")

        try:
            if ctx.author.top_role > role:
                await member.add_roles(role)
            else:
                embed.title = "Insufficient Permissions"
                embed.description = f"Sorry, you can't assign the role to {member.display_name}. They have a higher role in the hierarchy."

        except:
            embed.title = "Error"
            embed.description = "Oops! An error occurred while assigning the role."

        await ctx.respond(embed=embed, ephemeral=True)
    #SLOWMODE
    @commands.slash_command(name="slowmode", description="Adjust the slowmode delay for the current channel.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)

    async def slowmode(self, ctx, seconds: int):
        embed = discord.Embed(title="Slowmode", color=discord.Colour.red(), description=f"The slowmode delay in this channel has been updated to {seconds} seconds!")

        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            
        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. Unable to modify the slowmode delay for this channel."

        await ctx.respond(embed=embed, ephemeral=True)

    #SOFTBAN
    @commands.slash_command(name="softban", description="Softban a certain user from the server, removing their recent messages.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(title="Softban", color=discord.Colour.blue())

        try:
            await member.ban(reason=reason)
            await member.unban(reason=reason)
            embed.description = f"{member.mention} has been softbanned! 🥾👋"

        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. Unable to perform the softban on this member."

        await ctx.respond(embed=embed, ephemeral=True)

    #CLEAR
    @commands.slash_command(name="clear", description="Clear a targeted number of messages from the current channel.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, limit: int):
        embed = discord.Embed(title="Clear", color=discord.Colour.blue())

        try:
            messages = await ctx.channel.purge(limit=limit)
            deleted_count = len(messages)
            embed.description = f"{deleted_count} messages have been deleted! 🗑️"

        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong during the message deletion."

        await ctx.respond(embed=embed, ephemeral=True)

    #REMOVE TIMEOUT
    @commands.slash_command(name="removetimeout", description=f"Remove the timeout restriction for a specific user.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(moderate_members=True)
    async def removetimeout(self, ctx, member: discord.Member):
        embed = discord.Embed(title="Timeout", color=discord.Colour.red(), description=f"Timeout removed for {member.display_name}")

        try:
            if ctx.author.top_role > member.top_role:
                await member.remove_timeout()
            else:
                embed.title = "Error"
                embed.description = f"You cannot remove the timeout for {member.display_name} as they have a higher role than you in the hierarchy."
        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. Unable to remove the timeout for this member."

        await ctx.respond(embed=embed, ephemeral=True)

      
    #TIMEOUT
    @commands.slash_command(name="timeout", description=f"Temporarily restrict a specific user's access or actions.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, time, reason=None):
        embed = discord.Embed(title="Timeout", color=discord.Colour.red(), description=f"{member.display_name} has been timed out.")

        try:
            if ctx.author.top_role > member.top_role:
                timeout_duration = humanfriendly.parse_timespan(time)
                timeout_end = discord.utils.utcnow() + datetime.timedelta(seconds=timeout_duration)
                await member.timeout(until=timeout_end, reason=reason)

            else:
                embed.title = "Error"
                embed.description = f"You cannot timeout {member.display_name} as they have a higher role than you in the hierarchy."
        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. Unable to timeout this member."

        await ctx.respond(embed=embed, ephemeral=True)

    #UNMUTE
    @commands.slash_command(name="unmute", description="Restore the ability to send messages for a certain user.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        embed = discord.Embed(title="Unmute", color=discord.Colour.blue())

        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not role:
            embed.title = "Error"
            embed.description = "No 'Muted' role found!"

        elif role not in member.roles:
            embed.title = "Error"
            embed.description = f"{member.mention} is not muted!"

        else:
            try:
                await member.remove_roles(role)
                embed.description = f"{member.mention} has been unmuted! 🔊"

            except:
                embed.title = "Error"
                embed.description = "Oops! Something went wrong. Unable to unmute this member."

        await ctx.respond(embed=embed, ephemeral=True)

    #MUTE
    @commands.slash_command(name="mute", description=f"Mute a certain user.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, reason=None):
        embed = discord.Embed(title="Mute", color=discord.Colour.blue())

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            try:
                perms = discord.Permissions(send_messages=False)
                role = await ctx.guild.create_role(name="Muted", permissions=perms)
                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages=False)

            except:
                embed.title = "Error"
                embed.description = "Oops! Something went wrong. Unable to create the 'Muted' role."

        try:
            await member.add_roles(role, reason=reason)
            embed.description = f"{member.mention} has been muted! 🔇"

        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. Unable to mute this member."

        await ctx.respond(embed=embed, ephemeral=True)

    #KICK
    @commands.slash_command(name="kick", description=f"Remove a specific user from the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)

    async def kick(self, ctx, member: discord.Member, reason=None):
        embed = discord.Embed(title="Kick", color=discord.Colour.red(), description=f"{member.display_name}#{member.discriminator} has been removed from the server.\nID: {member.id} \nReason: {reason}")

        try:
            if ctx.author.top_role > member.top_role:
                await member.kick(reason=reason)

            else:
                embed.title = "Error"
                embed.description = f"You cannot kick {member.display_name} as they have a higher role than you in the hierarchy."
        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. Unable to kick this member."

        await ctx.respond(embed=embed, ephemeral=True)
      
    #BAN
    @commands.slash_command(name="ban", description=f"Permanently ban a specific user from the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        embed = discord.Embed(title="Ban", color=discord.Colour.red(), description=f"{member.display_name}#{member.discriminator} has been permanently banned.\nID: {member.id} \nReason: {reason}")

        try:
            if ctx.author.top_role > member.top_role:
                await member.ban(reason=reason)
            else:
                embed.title = "Error"
                embed.description = f"You cannot ban {member.display_name} as they have a higher role than you in the hierarchy."
        except:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. Unable to ban this member."

        await ctx.respond(embed=embed, ephemeral=True)

    #UNBAN
    @commands.slash_command(name="unban", description=f"Revoke a ban on a specific user.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        embed = discord.Embed(title="Unban", color=discord.Colour.blue())

        try:
            banned = await ctx.guild.fetch_ban(user)
            embed.description = f"The ban on {banned.user.name} has been lifted!"
            await ctx.guild.unban(banned.user)

        except discord.NotFound:
            embed.title = "Error"
            embed.description = "Oops! Something went wrong. The specified user was not found."

        await ctx.respond(embed=embed, ephemeral=True)

    #unlock
    @commands.slash_command(name="unlock", description="Restore access to a specific channel by enabling message sending.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
      embed = discord.Embed(title="Channel Unlocked", color=discord.Colour.blue(), description=f"{ctx.channel.mention} has been successfully unlocked. ✅")

      try:
          await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
      except:
          embed.title = "Error"
          embed.description = "Oops! Something went wrong. Unable to unlock this channel!"

      await ctx.respond(embed=embed, ephemeral=True)

    #lock
    @commands.slash_command(name="lock", description="Restrict access to a specific channel by disabling message sending.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
      embed = discord.Embed(title="Channel Locked", color=discord.Colour.red(), description=f"{ctx.channel.mention} has been successfully locked. ❌")

      try:
          await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

      except:
          embed.title = "Error"
          embed.description = "Oops! Something went wrong. Unable to lock this channel!"

      await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))