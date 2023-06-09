import discord, asyncio, requests, humanfriendly, datetime
from discord.ext import commands
from discord import SlashCommandGroup, option
from main import Bot

class Miscellaneous(commands.Cog):
    def __init__(self, bot : Bot):
        self.bot = bot
        self.database = bot.database
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("cmds.miscellaneous")

    #guild
    @commands.slash_command(name="guild", description="Display information about the current guild.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guild(self, ctx):
        embed = discord.Embed(color=discord.Color.blue())
        guild = ctx.author.guild

        try:
            embed.title = f"Guild Information"

            embed.add_field(name="🏰 Guild Name", value=f"```{guild.name}```", inline=True)
            embed.add_field(name="👑 Guild Owner", value=f"```@{guild.owner.name}```", inline=True)
            embed.add_field(name="🆔 Guild ID", value=f"```{guild.id}```", inline=True)

            bots = sum(member.bot for member in guild.members)
            embed.add_field(name="👥 Members", value=f"```Total Members: {guild.member_count} | Humans: {guild.member_count - bots} | Bots: {bots}```", inline=False)
            embed.add_field(name="📺 Channels", value=f"```Text: {len(guild.text_channels)} | Voice: {len(guild.voice_channels)} | Stage: {len(guild.stage_channels)} | Forum: {len(guild.forum_channels)} | Categories: {len(guild.categories)}```", inline=False)
            embed.add_field(name="🐸 Emojis & Stickers", value=f"```Emojis: {len(guild.emojis)} | Stickers: {len(guild.stickers)}```", inline=False)

            guild_roles = ", ".join(role.name for role in guild.roles if role.name != "@everyone")
            embed.add_field(name="👮 Roles", value=f"```{guild_roles}```", inline=False)

            formatted_created_at = guild.created_at.strftime("%m/%d/%Y, %H:%M")
            created_time = humanfriendly.format_timespan(datetime.datetime.now(datetime.timezone.utc) - guild.created_at, detailed=False, max_units=1)
            embed.add_field(name="⏰ Created the Guild", value=f"```{formatted_created_at} ({created_time} ago)```", inline=False)

            await ctx.respond(embed=embed)

        except:
            embed.title = "Error"
            embed.description = "There was an error while trying to execute this command!"
            await ctx.respond(embed=embed, ephemeral=True)

    #avatar
    @commands.slash_command(name="avatar", description="Get your avatar or the avatar of a user from the guild.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        embed = discord.Embed(color=discord.Color.blue(), title="Avatar")
        member = member or ctx.author

        try:
            if member.display_avatar.is_animated():
                embed.title = f"{member.name}'s Animated Avatar"
                embed.description = f"Here is the animated avatar for {member.mention}:"
            else:
                embed.title = f"{member.name}'s Avatar"
                embed.description = f"Here is the avatar for {member.mention}:"

            embed.set_image(url=member.display_avatar.url)

            await ctx.respond(embed=embed)

        except:
            embed.title = "Error"
            embed.description = "There was an error while trying to execute this command!"
            await ctx.respond(embed=embed, ephemeral=True)
            return


    @commands.slash_command(name="whois", description="Find information about you or a member from this guild.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whois(self, ctx, member: discord.Member = None):

        try:
            embed = discord.Embed(color=discord.Color.blue(), title = "Member Information")

            member = member or ctx.author

            embed.add_field(name="👤 Username", value=f"```@{member.name}```", inline=True)
            embed.add_field(name="👑 Nickname", value=f"```{member.display_name}```", inline=True)
            embed.add_field(name="🔖 User ID", value=f"```{member.id}```", inline=True)
            embed.add_field(name="🤖 Bot", value=f"```{str(member.bot)}```", inline=True)

            member_roles = ", ".join(role.name for role in member.roles if role.name != "@everyone")
            embed.add_field(name="👮 Roles", value=f"```{member_roles}```", inline=False)

            joined_time = humanfriendly.format_timespan(datetime.datetime.now(datetime.timezone.utc) - member.joined_at)
            embed.add_field(name="🎉 Joined on server", value=f"```{member.joined_at.strftime('%m/%d/%Y, %H:%M')} ({joined_time} ago)```", inline=False)

            created_time = humanfriendly.format_timespan(datetime.datetime.now(datetime.timezone.utc) - member.created_at)
            embed.add_field(name="⏰ Created the accouent", value=f"```{member.created_at.strftime('%m/%d/%Y, %H:%M')} ({created_time} ago)```", inline=False)

            if member.activity:
                embed.add_field(
                    name="🎮 Activity",
                    value=f"```{str(member.activity.type.name).title()} {member.activity.name}```",
                    inline=False
                )

            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

            await ctx.respond(embed=embed)

        except:
            embed = discord.Embed(color=discord.Color.blue(), title = "Error", description = "There was an error trying to execute this command!")
            await ctx.respond(embed=embed, ephemeral=True)

    ### SETUP COMMANDS
    setup = SlashCommandGroup("setup")

    #W&G MESSAGES SETUP
    @setup.command(name="messages", description="Set up welcome and goodbye messages when a user joins or leaves a server.")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @option("type", choices=["Welcome", "Goodbye"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def messages(self, ctx, type : str, channel : discord.TextChannel, text : str, welcome_card : bool = False):
        embed = discord.Embed(title="Message", color=discord.Color.blue())
        
        if type == "Welcome":
            welcome = {
                "message" : text,
                "channel_id" : channel.id,
                "welcome_card" : welcome_card
            }

            await self.database.set_welcome(ctx.guild.id, welcome)

            embed.title = "Welcome Message"
            embed.add_field(name="Message", value=text, inline=False)
            embed.add_field(name="Channel", value=f"`{channel.name}`", inline=False)
            embed.add_field(name="Card", value=f"`{welcome_card}`", inline=False)

        if type == "Goodbye":
            goodbye = {
                "message" : text,
                "channel_id" : channel.id,
            }

            await self.database.set_goodbye(ctx.guild.id, goodbye)

            embed.title = "Goodbye Message"
            embed.add_field(name="Message", value=text, inline=False)
            embed.add_field(name="Channel", value=f"`{channel.name}`", inline=False)


        await ctx.respond(embed=embed, ephemeral=True)

    #AUTOMATIC ROLE SETUP
    @setup.command(name="automaticrole", description="Setup automatic role assignment upon joining for both human users and bots.")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @option(
        "type",
        choices=["Bots", "Humans"]
    )
    @commands.has_permissions(administrator=True)
    @commands.guild_only()

    async def automaticrole(self, ctx, type : str, role : discord.Role):
        embed = discord.Embed(title="Automatic Role Setup", color=discord.Color.blue())

        try:
            if type == "Bots":
                await self.database.set_automatic_bot_role_id(ctx.guild.id, role.id)

            if type == "Humans":
                await self.database.set_automatic_human_role_id(ctx.guild.id, role.id)        

            embed.description = f"The role for {type.lower()} has been successfully updated to: \n{role.name}"
            await ctx.respond(embed=embed, ephemeral=True)

        except:
            embed.color=discord.Color.red()
            embed.description = "There was an error trying to execute this command. Please try again later."
            await ctx.respond(embed=embed, ephemeral=True)

    #TEMPORARY CHANNEL SETUP
    @setup.command(name="temporarychannel", description="Setup a 'Join To Create' channel for temporary voice channels!")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()

    async def temporarychannel(self, ctx):
        embed = discord.Embed(title="Temporary Channel Setup", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        try: 
            category = await ctx.guild.create_category(name="🔊VOICE")
            await asyncio.sleep(1)
            channel = await ctx.guild.create_voice_channel(name="[🎤] Join To Create", category=category)

            await self.database.set_temporary_channel_id(ctx.guild.id, channel.id)
            temporarychannelevent.temporary_channel_cache[ctx.guild.id] = channel.id

            embed.description = "The setup has been completed successfully! 🎉"
            await ctx.respond(embed=embed, ephemeral=True)

        except:
            embed.color=discord.Color.red()
            embed.description = "There was an error trying to execute this command. Please try again later."
            await ctx.respond(embed=embed, ephemeral=True)


    ### VOICE COMMANDS
    voice = SlashCommandGroup("voice")

    #VOICE BITRATE
    @voice.command(name="bitrate", description="Modify the bitrate of the channel.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @option(
        "value",
        description="Please specify a bitrate value within the range of 8 to 256.",
        min_value=8,
        max_value=256,
    )
    @commands.guild_only()

    async def bitrate(self, ctx, value : int):
        embed = discord.Embed(title="Voice Bitrate", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.edit(bitrate=value*1000)
        
        embed.description = f"The bitrate value has been updated to {value}."
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE LIMIT
    @voice.command(name="limit", description="Limit how many users can join the voice channel.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @option(
        "value",
        description="Please specify a value within the range of 0 to 99. (0 for unlimited)",
        min_value=0,
        max_value=99,
    )
    @commands.guild_only()

    async def limit(self, ctx, value : int):
        embed = discord.Embed(title="Voice User Limit", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.edit(user_limit=value)
        
        embed.description = f"The user limit has been updated to {value}."
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE LOCK
    @voice.command(name="lock", description="Locks the voice channel.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def lock(self, ctx):
        embed = discord.Embed(title="Voice Lock", color=discord.Color.red())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=False)
        
        embed.description = f"The voice channel is locked. ❌"
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE UNLOCK
    @voice.command(name="unlock", description="Unlocks the voice channel.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def unlock(self, ctx):
        embed = discord.Embed(title="Voice Unlock", color=discord.Color.green())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=True)
        
        embed.description = f"The voice channel is unlocked. ✅"
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE GHOST
    @voice.command(name="ghost", description="Makes the voice channel invisible to everyone.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def ghost(self, ctx):
        embed = discord.Embed(title="Voice Ghost", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        
        embed.description = "This voice channel is now hidden from everyone's view. 👻"
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE UNGHOST
    @voice.command(name="unghost", description="Makes the voice channel visible to everyone.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def unghost(self, ctx):
        embed = discord.Embed(title="Voice Unghost", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        
        embed.description = "This voice channel is now visible to everyone. 👀"
        await ctx.respond(embed=embed, ephemeral=True)


    #VOICE NAME
    @voice.command(name="name", description="Change the name of the voice channel.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def name(self, ctx, name : str):
        embed = discord.Embed(title="Voice Name", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.edit(name=name)
        
        embed.description = f"The voice channel has been renamed to:\n**{name}**"
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE NSFW
    @voice.command(name="nsfw", description="Modify the channel NSFW status.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def nsfw(self, ctx, toggle : bool):
        embed = discord.Embed(title="Voice Nsfw Status", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        channel = ctx.author.voice.channel
        await channel.edit(nsfw=toggle)
        
        embed.description = f"The NSFW status of this voice channel has been updated to: \n**{toggle}**"
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE REJECT
    @voice.command(name="reject", description="Kick and disallow the member to connect to the voice channel.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def reject(self, ctx, user : discord.Member):
        embed = discord.Embed(title="Voice Reject", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        voice_channel = ctx.author.voice

        if user.voice and voice_channel.channel == user.voice.channel:
            await user.move_to(None)

        await voice_channel.channel.set_permissions(user, connect=False)

        embed.description = f"Attention! {user.name} will no longer be able to connect to the voice channel."
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE PERMIT
    @voice.command(name="permit", description="Grants users permission to connect to the channel and view it.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()

    async def permit(self, ctx, user : discord.Member):
        embed = discord.Embed(title="Voice Permit", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color=discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return   

        if not ctx.author.guild_permissions.manage_channels or not ctx.author.guild_permissions.administrator:
            if ctx.author.id not in temporarychannelevent.voice_channels or ctx.author.voice.channel.id != temporarychannelevent.voice_channels[ctx.author.id]:
                embed.color=discord.Color.red()
                embed.description = "In order to utilize this command, you need to be in your own temporary channel."
                await ctx.respond(embed=embed, ephemeral=True)
                return      

        voice_channel = ctx.author.voice
        await voice_channel.channel.set_permissions(user, connect=True, view_channel=True)

        embed.description = f"Great news! {user.name} now has access to this channel and can connect with ease."
        await ctx.respond(embed=embed, ephemeral=True)

    #VOICE CLAIM
    @voice.command(name="claim", description="Claim a temporary voice channel if the channel owner is not present.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    async def claim(self, ctx):
        embed = discord.Embed(title="Voice Claim", color=discord.Color.blue())
        temporarychannelevent = self.bot.get_cog("Temporarychannel")

        if not ctx.author.voice:
            embed.color = discord.Color.red()
            embed.description = "To utilize this command, please ensure that you are currently in a voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return

        voice_channel = ctx.author.voice.channel

        if ctx.author.id in temporarychannelevent.voice_channels:
            embed.color = discord.Color.red()
            embed.description = "Oops! It seems like you already have a temporary voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return

        if voice_channel.id not in temporarychannelevent.voice_channels.values():
            embed.color = discord.Color.red()
            embed.description = "Oops! This command can only be used with temporary voice channels."
            await ctx.respond(embed=embed, ephemeral=True)
            return

        last_owner_id = list(temporarychannelevent.voice_channels.keys())[list(temporarychannelevent.voice_channels.values()).index(voice_channel.id)]
        last_owner = ctx.guild.get_member(last_owner_id)

        if last_owner and last_owner.voice and last_owner.voice.channel == voice_channel:
            embed.color = discord.Color.red()
            embed.description = "Oops! The owner is currently in the temporary voice channel."
            await ctx.respond(embed=embed, ephemeral=True)
            return

        temporarychannelevent.voice_channels[last_owner_id] = None
        temporarychannelevent.voice_channels[ctx.author.id] = voice_channel.id

        embed.description = "Congratulations! You are now the owner of this temporary voice channel."
        await ctx.respond(embed=embed, ephemeral=True)

    #PING
    @commands.slash_command(ping="ping", description="Latency of the bot.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓Pong", description=f"{round(self.bot.latency * 1000)}ms", color=discord.Color.blue())
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot : Bot):
    bot.add_cog(Miscellaneous(bot))